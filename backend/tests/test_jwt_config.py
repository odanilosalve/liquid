import pytest
import os
import importlib
import jwt_config
from unittest.mock import patch
from jwt_config import generate_token, validate_token, get_token_from_header, UnauthorizedError
from exceptions import ConfigurationError
import jwt
from datetime import datetime, timedelta


class TestGenerateToken:
    @patch.dict(os.environ, {'JWT_SECRET_KEY': 'test-secret-key-with-minimum-32-chars', 'JWT_ALGORITHM': 'HS256', 'JWT_EXPIRATION_HOURS': '24', 'STAGE': 'dev'})
    def test_generate_token_success(self):
        importlib.reload(jwt_config)
        
        token = jwt_config.generate_token('user123', 'testuser')
        
        assert token is not None
        assert isinstance(token, str)
        
        payload = jwt.decode(token, 'test-secret-key-with-minimum-32-chars', algorithms=['HS256'])
        assert payload['user_id'] == 'user123'
        assert payload['username'] == 'testuser'
        assert 'exp' in payload
        assert 'iat' in payload

    @patch.dict(os.environ, {'JWT_SECRET_KEY': 'test-secret-key-with-minimum-32-chars', 'JWT_ALGORITHM': 'HS256', 'JWT_EXPIRATION_HOURS': '1', 'STAGE': 'dev'})
    def test_token_has_expiration(self):
        importlib.reload(jwt_config)
        
        token = jwt_config.generate_token('user123', 'testuser')
        payload = jwt.decode(token, 'test-secret-key-with-minimum-32-chars', algorithms=['HS256'])
        
        exp_time = datetime.fromtimestamp(payload['exp'])
        iat_time = datetime.fromtimestamp(payload['iat'])
        diff = exp_time - iat_time
        
        assert diff.total_seconds() >= 3600


class TestValidateToken:
    @patch.dict(os.environ, {'JWT_SECRET_KEY': 'test-secret-key-with-minimum-32-chars', 'JWT_ALGORITHM': 'HS256', 'JWT_EXPIRATION_HOURS': '24', 'STAGE': 'dev'})
    def test_validate_token_success(self):
        importlib.reload(jwt_config)
        
        token = jwt_config.generate_token('user123', 'testuser')
        payload = jwt_config.validate_token(token)
        
        assert payload['user_id'] == 'user123'
        assert payload['username'] == 'testuser'

    @patch.dict(os.environ, {'JWT_SECRET_KEY': 'test-secret-key-with-minimum-32-chars', 'JWT_ALGORITHM': 'HS256', 'JWT_EXPIRATION_HOURS': '24', 'STAGE': 'dev'})
    def test_validate_token_invalid(self):
        importlib.reload(jwt_config)
        
        invalid_token = 'invalid.token.here'
        
        with pytest.raises(UnauthorizedError):
            jwt_config.validate_token(invalid_token)

    @patch.dict(os.environ, {'JWT_SECRET_KEY': 'test-secret-key-with-minimum-32-chars', 'JWT_ALGORITHM': 'HS256', 'JWT_EXPIRATION_HOURS': '24', 'STAGE': 'dev'})
    def test_validate_token_expired(self):
        importlib.reload(jwt_config)
        
        payload = {
            'user_id': 'user123',
            'username': 'testuser',
            'exp': datetime.utcnow() - timedelta(hours=1),
            'iat': datetime.utcnow() - timedelta(hours=2)
        }
        expired_token = jwt.encode(payload, jwt_config.JWT_SECRET_KEY, algorithm='HS256')
        
        with pytest.raises(UnauthorizedError) as exc_info:
            jwt_config.validate_token(expired_token)
        
        assert 'expired' in str(exc_info.value).lower()


class TestGetTokenFromHeader:
    def test_get_token_from_header_success(self):
        event = {
            'headers': {
                'Authorization': 'Bearer test-token-123'
            }
        }
        
        token = get_token_from_header(event)
        assert token == 'test-token-123'

    def test_get_token_from_header_case_insensitive(self):
        event = {
            'headers': {
                'authorization': 'Bearer test-token-123'
            }
        }
        
        token = get_token_from_header(event)
        assert token == 'test-token-123'

    def test_get_token_from_header_missing(self):
        event = {
            'headers': {}
        }
        
        token = get_token_from_header(event)
        assert token is None

    def test_get_token_from_header_invalid_format(self):
        event = {
            'headers': {
                'Authorization': 'InvalidFormat test-token-123'
            }
        }
        
        token = get_token_from_header(event)
        assert token is None


class TestJWTSecretKeyValidation:
    @patch.dict(os.environ, {'STAGE': 'prod', 'JWT_ALGORITHM': 'HS256', 'JWT_EXPIRATION_HOURS': '24'}, clear=True)
    def test_missing_jwt_secret_in_production(self):
        with pytest.raises(ConfigurationError) as exc_info:
            importlib.reload(jwt_config)
        assert 'JWT_SECRET_KEY environment variable is required in production' in str(exc_info.value)
    
    @patch.dict(os.environ, {'STAGE': 'prod', 'JWT_SECRET_KEY': 'dev-secret-key-change-in-production', 'JWT_ALGORITHM': 'HS256', 'JWT_EXPIRATION_HOURS': '24'}, clear=True)
    def test_default_jwt_secret_in_production(self):
        with pytest.raises(ConfigurationError) as exc_info:
            importlib.reload(jwt_config)
        assert 'cannot use the default development key' in str(exc_info.value)
    
    @patch.dict(os.environ, {'STAGE': 'prod', 'JWT_SECRET_KEY': 'short', 'JWT_ALGORITHM': 'HS256', 'JWT_EXPIRATION_HOURS': '24'}, clear=True)
    def test_short_jwt_secret_in_production(self):
        with pytest.raises(ConfigurationError) as exc_info:
            importlib.reload(jwt_config)
        assert 'must be at least 32 characters long' in str(exc_info.value)
    
    @patch.dict(os.environ, {'STAGE': 'dev', 'JWT_ALGORITHM': 'HS256', 'JWT_EXPIRATION_HOURS': '24'}, clear=True)
    def test_missing_jwt_secret_in_dev_allowed(self):
        importlib.reload(jwt_config)
        assert jwt_config.JWT_SECRET_KEY == 'dev-secret-key-change-in-production'


import pytest
from unittest.mock import Mock, patch
from middleware import require_auth, UnauthorizedError
from jwt_config import UnauthorizedError as JWTUnauthorizedError


class TestRequireAuth:
    @patch('middleware.get_token_from_header')
    @patch('middleware.validate_token')
    def test_require_auth_success(self, mock_validate, mock_get_token):
        mock_get_token.return_value = 'valid-token'
        mock_validate.return_value = {'user_id': 'user123', 'username': 'testuser'}
        
        event = {'path': '/convert', 'httpMethod': 'POST'}
        context = Mock()
        context.aws_request_id = 'req-123'
        
        payload = require_auth(event, context)
        
        assert payload['user_id'] == 'user123'
        assert payload['username'] == 'testuser'
        mock_get_token.assert_called_once_with(event)
        mock_validate.assert_called_once_with('valid-token')

    @patch('middleware.get_token_from_header')
    def test_require_auth_no_token(self, mock_get_token):
        mock_get_token.return_value = None
        
        event = {'path': '/convert', 'httpMethod': 'POST'}
        context = Mock()
        context.aws_request_id = 'req-123'
        
        with pytest.raises(UnauthorizedError) as exc_info:
            require_auth(event, context)
        
        assert 'required' in str(exc_info.value).lower()

    @patch('middleware.get_token_from_header')
    @patch('middleware.validate_token')
    def test_require_auth_invalid_token(self, mock_validate, mock_get_token):
        mock_get_token.return_value = 'invalid-token'
        mock_validate.side_effect = JWTUnauthorizedError('Invalid token')
        
        event = {'path': '/convert', 'httpMethod': 'POST'}
        context = Mock()
        context.aws_request_id = 'req-123'
        
        with pytest.raises(UnauthorizedError):
            require_auth(event, context)


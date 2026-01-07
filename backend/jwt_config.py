import os
import jwt
import logging
from datetime import datetime, timedelta
from exceptions import ConfigurationError, AuthenticationError
from utils.logging_helpers import create_log_extra
from utils.config_validator import get_jwt_secret_key, is_production

logger = logging.getLogger()

JWT_SECRET_KEY = get_jwt_secret_key()

def get_jwt_algorithm():
    algorithm = os.environ.get('JWT_ALGORITHM')
    if not algorithm:
        if is_production():
            raise ConfigurationError('JWT_ALGORITHM environment variable is required in production')
        return 'HS256'
    return algorithm

def get_jwt_expiration_hours():
    hours_str = os.environ.get('JWT_EXPIRATION_HOURS')
    if not hours_str:
        if is_production():
            raise ConfigurationError('JWT_EXPIRATION_HOURS environment variable is required in production')
        return 24
    try:
        return int(hours_str)
    except (ValueError, TypeError):
        raise ConfigurationError('JWT_EXPIRATION_HOURS must be a valid integer')

JWT_ALGORITHM = get_jwt_algorithm()
JWT_EXPIRATION_HOURS = get_jwt_expiration_hours()


class UnauthorizedError(AuthenticationError):
    pass


def generate_token(user_id, username):
    if not user_id or not username:
        raise ValueError('user_id and username are required')
    
    try:
        expiration = datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
        
        payload = {
            'user_id': user_id,
            'username': username,
            'exp': expiration,
            'iat': datetime.utcnow()
        }
        
        token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        
        if isinstance(token, bytes):
            token = token.decode('utf-8')
        
        logger.info('JWT token generated', extra=create_log_extra(
            None,
            user_id=user_id,
            username=username,
            expiration_hours=JWT_EXPIRATION_HOURS
        ))
        
        return token
    except (TypeError, ValueError) as e:
        logger.error('Error generating JWT token', extra=create_log_extra(
            None,
            user_id=user_id,
            error_type=type(e).__name__,
            error=str(e)
        ), exc_info=True)
        raise ConfigurationError(f'Failed to generate token: {str(e)}')


def validate_token(token):
    if not token or not isinstance(token, str):
        raise UnauthorizedError('Token must be a non-empty string')
    
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        
        if 'user_id' not in payload or 'username' not in payload:
            logger.warning('JWT token missing required fields', extra=create_log_extra(None, payload_keys=list(payload.keys())))
            raise UnauthorizedError('Token missing required fields')
        
        logger.debug('JWT token validated', extra=create_log_extra(
            None,
            user_id=payload.get('user_id'),
            username=payload.get('username')
        ))
        
        return payload
        
    except jwt.ExpiredSignatureError:
        logger.warning('JWT token expired')
        raise UnauthorizedError('Token has expired')
    except (jwt.InvalidTokenError, jwt.DecodeError) as e:
        logger.warning('Invalid JWT token', extra=create_log_extra(None, error=str(e)))
        raise UnauthorizedError('Invalid token')
    except (ValueError, TypeError) as config_error:
        logger.error('Configuration error validating JWT token', extra=create_log_extra(
            None,
            error_type=type(config_error).__name__,
            error=str(config_error)
        ), exc_info=True)
        raise ConfigurationError(f'Token validation configuration error: {str(config_error)}')
    except jwt.PyJWTError as e:
        logger.error('JWT library error validating token', extra=create_log_extra(
            None,
            error_type=type(e).__name__,
            error=str(e)
        ), exc_info=True)
        raise UnauthorizedError('Token validation failed')
    except Exception as e:
        logger.error('Unexpected error validating JWT token', extra=create_log_extra(
            None,
            error_type=type(e).__name__,
            error=str(e)
        ), exc_info=True)
        raise UnauthorizedError('Token validation failed')


def get_token_from_header(event):
    if not event or not isinstance(event, dict):
        return None
    
    headers = event.get('headers', {}) or {}
    
    if not isinstance(headers, dict):
        return None
    
    auth_header = headers.get('Authorization') or headers.get('authorization')
    
    if not auth_header or not isinstance(auth_header, str):
        return None
    
    if not auth_header.startswith('Bearer '):
        return None
    
    token = auth_header.replace('Bearer ', '').strip()
    
    return token if token else None


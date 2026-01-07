import os
import logging
from exceptions import ConfigurationError

logger = logging.getLogger()


def is_production():
    stage = os.environ.get('STAGE')
    if not stage:
        return False
    return stage.lower() in ('prod', 'production')


def validate_jwt_secret_key(secret_key):
    if not secret_key:
        raise ConfigurationError('JWT_SECRET_KEY is required and cannot be empty')
    
    if secret_key == 'dev-secret-key-change-in-production':
        raise ConfigurationError(
            'JWT_SECRET_KEY cannot use the default development key. '
            'Please set a secure secret key in production environment.'
        )
    
    min_length_str = os.environ.get('JWT_SECRET_MIN_LENGTH', '32')
    try:
        min_length = int(min_length_str)
    except (ValueError, TypeError):
        min_length = 32
    
    if len(secret_key) < min_length:
        raise ConfigurationError(
            f'JWT_SECRET_KEY must be at least {min_length} characters long. '
            f'Current length: {len(secret_key)}'
        )
    
    return True


def get_jwt_secret_key():
    secret_key = os.environ.get('JWT_SECRET_KEY')
    is_prod = is_production()
    
    if not secret_key:
        if is_prod:
            raise ConfigurationError(
                'JWT_SECRET_KEY environment variable is required in production. '
                'Please set a secure secret key.'
            )
        else:
            logger.warning(
                'JWT_SECRET_KEY not set. Using default development key. '
                'This should NEVER be used in production!'
            )
            return 'dev-secret-key-change-in-production'
    
    if is_prod:
        validate_jwt_secret_key(secret_key)
    
    return secret_key


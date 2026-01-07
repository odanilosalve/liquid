import logging
from jwt_config import get_token_from_header, validate_token, UnauthorizedError
from exceptions import ConfigurationError
from utils.logging_helpers import create_log_extra

logger = logging.getLogger()


def require_auth(event, context):
    request_id = context.aws_request_id if context else None
    
    try:
        token = get_token_from_header(event)
    except (AttributeError, TypeError) as e:
        logger.error('Error extracting token from header', extra=create_log_extra(
            request_id,
            path=event.get('path'),
            method=event.get('httpMethod'),
            error_type=type(e).__name__
        ), exc_info=True)
        raise ConfigurationError('Failed to extract authorization token')
    
    if not token:
        logger.warning('No token provided in request', extra=create_log_extra(
            request_id,
            path=event.get('path'),
            method=event.get('httpMethod')
        ))
        raise UnauthorizedError('Authorization token required')
    
    try:
        payload = validate_token(token)
        
        logger.info('Authentication successful', extra=create_log_extra(
            request_id,
            user_id=payload.get('user_id'),
            username=payload.get('username'),
            path=event.get('path'),
            method=event.get('httpMethod')
        ))
        
        return payload
        
    except UnauthorizedError:
        raise
    except (ValueError, TypeError, KeyError) as config_error:
        logger.error('Configuration error during token validation', extra=create_log_extra(
            request_id,
            error_type=type(config_error).__name__,
            path=event.get('path'),
            method=event.get('httpMethod')
        ), exc_info=True)
        raise ConfigurationError('Token validation configuration error')
    except (AttributeError, KeyError, TypeError) as e:
        logger.error('Error accessing event or context during authentication', extra=create_log_extra(
            request_id,
            error_type=type(e).__name__,
            error=str(e),
            path=event.get('path') if isinstance(event, dict) else None,
            method=event.get('httpMethod') if isinstance(event, dict) else None
        ), exc_info=True)
        raise UnauthorizedError('Authentication failed')
    except Exception as e:
        logger.error('Unexpected error during authentication', extra=create_log_extra(
            request_id,
            error_type=type(e).__name__,
            path=event.get('path') if isinstance(event, dict) else None,
            method=event.get('httpMethod') if isinstance(event, dict) else None
        ), exc_info=True)
        raise UnauthorizedError('Authentication failed')


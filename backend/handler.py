import logging
from datetime import datetime
from request_parser import parse_request_body, extract_request_data, RequestParsingError
from validators import validate_conversion_request, ValidationError
from database import get_conversion_rate, ExternalAPIUnavailableError, DatabaseError
from converters import calculate_conversion
from responses import create_response
from auth import verify_credentials
from jwt_config import generate_token, UnauthorizedError
from middleware import require_auth
from exceptions import ConfigurationError, AuthenticationError
from utils.request_helpers import extract_request_context, handle_cors_preflight
from utils.error_handlers import (
    handle_unexpected_error,
    handle_configuration_error,
    handle_unauthorized_error
)
from utils.logging_helpers import create_log_extra
from utils.user_helpers import get_user_info

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_service_name():
    import os
    from utils.config_validator import is_production
    from exceptions import ConfigurationError
    
    name = os.environ.get('SERVICE_NAME')
    if not name:
        if is_production():
            raise ConfigurationError('SERVICE_NAME environment variable is required in production')
        return 'liquid-api'
    return name


def login(event, context):
    ctx = extract_request_context(event, context)
    request_id = ctx['request_id']
    request_origin = ctx['origin']
    
    cors_response = handle_cors_preflight(event, request_id, 'login')
    if cors_response:
        return cors_response
    
    try:
        body = parse_request_body(event)
        username = body.get('username')
        password = body.get('password')
        
        if not username or not password:
            logger.warning('Missing username or password in login request', extra=create_log_extra(request_id))
            return create_response(400, {'error': 'Username and password are required'}, request_origin)
        
        try:
            user = verify_credentials(username, password, request_id)
        except AuthenticationError as auth_error:
            logger.warning('Authentication failed', extra=create_log_extra(request_id, username=username, error=str(auth_error)))
            return create_response(401, {'error': str(auth_error)}, request_origin)
        except DatabaseError as db_error:
            logger.error('Database error during login', extra=create_log_extra(request_id, username=username, error=str(db_error)), exc_info=True)
            return create_response(500, {'error': 'Database error occurred'}, request_origin)
        
        try:
            token = generate_token(user.get('user_id'), user.get('username'))
        except (ValueError, TypeError) as config_error:
            return handle_configuration_error(config_error, request_id, request_origin)
        
        user_info = get_user_info(user)
        logger.info('Login successful', extra=create_log_extra(request_id, username=username, user_id=user_info['user_id']))
        
        return create_response(200, {
            'token': token,
            'user': user_info
        }, request_origin)
        
    except RequestParsingError as parse_error:
        logger.warning('Request parsing error in login', extra=create_log_extra(request_id, error=str(parse_error)))
        return create_response(400, {'error': str(parse_error)}, request_origin)
    except (KeyError, AttributeError, TypeError) as e:
        logger.error('Error accessing request data in login', extra=create_log_extra(
            request_id,
            error_type=type(e).__name__,
            error=str(e)
        ), exc_info=True)
        return handle_unexpected_error(e, request_id, 'during login', request_origin)
    except Exception as e:
        return handle_unexpected_error(e, request_id, 'during login', request_origin)


def health(event, context):
    ctx = extract_request_context(event, context)
    request_id = ctx['request_id']
    request_origin = ctx['origin']
    
    cors_response = handle_cors_preflight(event, request_id, 'health')
    if cors_response:
        return cors_response
    
    try:
        user_payload = require_auth(event, context)
        user_info = get_user_info(user_payload)
        
        logger.info('Health check requested', extra=create_log_extra(
            request_id,
            function_name=context.function_name if context else None,
            **user_info
        ))
        
        return create_response(200, {
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'service': get_service_name()
        }, request_origin)
        
    except UnauthorizedError as auth_error:
        return handle_unauthorized_error(auth_error, request_id, request_origin)
    except (ValueError, TypeError, KeyError) as config_error:
        return handle_configuration_error(config_error, request_id, request_origin)
    except (AttributeError, NameError) as e:
        logger.error('Error accessing context or service name in health check', extra=create_log_extra(
            request_id,
            error_type=type(e).__name__,
            error=str(e)
        ), exc_info=True)
        return handle_unexpected_error(e, request_id, 'during health check', request_origin)
    except Exception as e:
        return handle_unexpected_error(e, request_id, 'during health check', request_origin)


def convert(event, context):
    ctx = extract_request_context(event, context)
    request_id = ctx['request_id']
    request_origin = ctx['origin']
    
    cors_response = handle_cors_preflight(event, request_id, 'convert')
    if cors_response:
        return cors_response
    
    try:
        user_payload = require_auth(event, context)
        user_info = get_user_info(user_payload)
        
        logger.info('Conversion request received', extra=create_log_extra(request_id, **user_info))
        
    except UnauthorizedError as auth_error:
        return handle_unauthorized_error(auth_error, request_id, request_origin)
    except (ValueError, TypeError, KeyError) as config_error:
        return handle_configuration_error(config_error, request_id, request_origin)
    except (AttributeError, NameError) as e:
        logger.error('Error accessing context during authentication in convert', extra=create_log_extra(
            request_id,
            error_type=type(e).__name__,
            error=str(e)
        ), exc_info=True)
        return handle_unexpected_error(e, request_id, 'during authentication', request_origin)
    except Exception as e:
        return handle_unexpected_error(e, request_id, 'during authentication', request_origin)
    
    try:
        body = parse_request_body(event)
        amount, from_currency, to_currency = extract_request_data(body)
        
        try:
            amount_float = validate_conversion_request(
                amount, from_currency, to_currency, request_id
            )
        except ValidationError as validation_error:
            logger.warning('Validation error in conversion request', extra=create_log_extra(request_id, error=str(validation_error)))
            return create_response(400, {'error': str(validation_error)}, request_origin)
        
        try:
            rate = get_conversion_rate(from_currency, to_currency, request_id)
            converted_amount = calculate_conversion(amount_float, rate)
            
            logger.info('Conversion successful', extra=create_log_extra(
                request_id,
                **user_info,
                amount=amount_float,
                from_currency=from_currency,
                to_currency=to_currency,
                rate=rate,
                converted_amount=converted_amount
            ))
            
            return create_response(200, {
                'amount': amount_float,
                'from': from_currency,
                'to': to_currency,
                'rate': rate,
                'converted_amount': converted_amount
            }, request_origin)
            
        except ExternalAPIUnavailableError as api_error:
            logger.error('External API unavailable', extra=create_log_extra(
                request_id,
                from_currency=from_currency,
                to_currency=to_currency,
                error=str(api_error)
            ))
            return create_response(503, {'error': 'External currency API is currently unavailable'}, request_origin)
        except ValueError as e:
            logger.warning('Currency not found', extra=create_log_extra(
                request_id,
                from_currency=from_currency,
                to_currency=to_currency,
                error=str(e)
            ))
            return create_response(404, {'error': str(e)}, request_origin)
        except DatabaseError as db_error:
            logger.error('Database error during conversion', extra=create_log_extra(
                request_id,
                from_currency=from_currency,
                to_currency=to_currency,
                error=str(db_error)
            ), exc_info=True)
            return create_response(500, {'error': 'Database error occurred'}, request_origin)
    
    except RequestParsingError as parse_error:
        logger.warning('Request parsing error in conversion', extra=create_log_extra(request_id, error=str(parse_error)))
        return create_response(400, {'error': str(parse_error)}, request_origin)
    except (KeyError, AttributeError, TypeError) as e:
        logger.error('Error accessing request data in conversion', extra=create_log_extra(
            request_id,
            error_type=type(e).__name__,
            error=str(e)
        ), exc_info=True)
        return handle_unexpected_error(e, request_id, 'during conversion', request_origin)
    except Exception as e:
        return handle_unexpected_error(e, request_id, 'during conversion', request_origin)

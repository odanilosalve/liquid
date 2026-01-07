import json
import logging
from datetime import datetime
from request_parser import parse_request_body, extract_request_data
from validators import validate_conversion_request
from database import get_conversion_rate
from converters import calculate_conversion
from responses import create_response

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def health(event, context):
    logger.info('Health check requested', extra={
        'request_id': context.aws_request_id if context else None,
        'function_name': context.function_name if context else None
    })
    return create_response(200, {
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'liquid-api'
    })


def convert(event, context):
    request_id = context.aws_request_id if context else None
    
    if event.get('httpMethod') == 'OPTIONS':
        logger.info('CORS preflight request', extra={
            'request_id': request_id
        })
        return create_response(200, {})
    
    try:
        body = parse_request_body(event)
        amount, from_currency, to_currency = extract_request_data(body)
        
        is_valid, error, amount_float = validate_conversion_request(
            amount, from_currency, to_currency, request_id
        )
        
        if not is_valid:
            return create_response(400, {'error': error})
        
        try:
            rate = get_conversion_rate(from_currency, to_currency, request_id)
            converted_amount = calculate_conversion(amount_float, rate)
            
            logger.info('Conversion successful', extra={
                'request_id': request_id,
                'amount': amount_float,
                'from_currency': from_currency,
                'to_currency': to_currency,
                'rate': rate,
                'converted_amount': converted_amount
            })
            
            return create_response(200, {
                'amount': amount_float,
                'from': from_currency,
                'to': to_currency,
                'rate': rate,
                'converted_amount': converted_amount
            })
            
        except ValueError as e:
            return create_response(404, {'error': str(e)})
        except Exception as db_error:
            error_type = type(db_error).__name__
            logger.error('Database error during conversion', extra={
                'request_id': request_id,
                'error_type': error_type,
                'from_currency': from_currency,
                'to_currency': to_currency
            }, exc_info=True)
            return create_response(500, {
                'error': 'Database error occurred'
            })
    
    except json.JSONDecodeError as json_error:
        logger.warning('Invalid JSON in request body', extra={
            'request_id': request_id,
            'error': str(json_error)
        })
        return create_response(400, {
            'error': 'Invalid JSON in request body'
        })
    except Exception as e:
        error_type = type(e).__name__
        logger.error('Unexpected error during conversion', extra={
            'request_id': request_id,
            'error_type': error_type
        }, exc_info=True)
        return create_response(500, {
            'error': 'Internal server error'
        })

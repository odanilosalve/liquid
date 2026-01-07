import json
import logging
from exceptions import RequestParsingError
from utils.logging_helpers import create_log_extra

logger = logging.getLogger()


def parse_request_body(event):
    try:
        body = event.get('body', {})
        
        if isinstance(body, str):
            if not body.strip():
                return {}
            try:
                return json.loads(body)
            except json.JSONDecodeError as e:
                logger.warning('Invalid JSON format in request body', extra=create_log_extra(None, error=str(e)))
                raise RequestParsingError('Invalid JSON format in request body')
        elif isinstance(body, dict):
            return body
        else:
            raise RequestParsingError('Request body must be a JSON object or string')
    except RequestParsingError:
        raise
    except (json.JSONDecodeError, TypeError, AttributeError, KeyError) as e:
        logger.error('Error parsing request body', extra=create_log_extra(
            None,
            error_type=type(e).__name__,
            error=str(e)
        ), exc_info=True)
        raise RequestParsingError(f'Failed to parse request body: {str(e)}')
    except Exception as e:
        logger.error('Unexpected error parsing request body', extra=create_log_extra(
            None,
            error_type=type(e).__name__,
            error=str(e)
        ), exc_info=True)
        raise RequestParsingError(f'Failed to parse request body: {str(e)}')


def extract_request_data(body):
    amount = body.get('amount')
    from_currency = body.get('from', '').upper()
    to_currency = body.get('to', '').upper()
    return amount, from_currency, to_currency



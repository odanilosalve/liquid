import logging
from responses import create_response

logger = logging.getLogger()


def extract_origin(event):
    return event.get('headers', {}).get('Origin') or event.get('headers', {}).get('origin')


def extract_request_context(event, context):
    return {
        'request_id': context.aws_request_id if context else None,
        'origin': extract_origin(event)
    }


def handle_cors_preflight(event, request_id, endpoint_name):
    if event.get('httpMethod') == 'OPTIONS':
        logger.info(f'CORS preflight request for {endpoint_name}', extra={
            'request_id': request_id
        })
        return create_response(200, {}, extract_origin(event))
    return None


import os
import logging
from responses import create_response
from utils.request_helpers import extract_request_context, handle_cors_preflight
from utils.logging_helpers import create_log_extra

logger = logging.getLogger()


def swagger_yaml(event, context):
    """Serve Swagger/OpenAPI YAML file."""
    ctx = extract_request_context(event, context)
    request_id = ctx['request_id']
    request_origin = ctx['origin']
    
    cors_response = handle_cors_preflight(event, request_id, 'swagger')
    if cors_response:
        return cors_response
    
    try:
        swagger_path = os.path.join(os.path.dirname(__file__), 'swagger.yaml')
        
        with open(swagger_path, 'r', encoding='utf-8') as f:
            swagger_content = f.read()
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/yaml; charset=utf-8',
                'Access-Control-Allow-Origin': request_origin,
                'Access-Control-Allow-Methods': 'GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
            },
            'body': swagger_content
        }
    except FileNotFoundError:
        logger.error('Swagger file not found', extra=create_log_extra(request_id))
        return create_response(404, {'error': 'Swagger documentation not found'}, request_origin)
    except Exception as e:
        logger.error('Error serving swagger documentation', extra=create_log_extra(
            request_id,
            error_type=type(e).__name__,
            error=str(e)
        ), exc_info=True)
        return create_response(500, {'error': 'Error serving documentation'}, request_origin)


def swagger_ui(event, context):
    """Serve Swagger UI HTML page."""
    ctx = extract_request_context(event, context)
    request_id = ctx['request_id']
    request_origin = ctx['origin']
    
    cors_response = handle_cors_preflight(event, request_id, 'swagger')
    if cors_response:
        return cors_response
    
    try:
        html_path = os.path.join(os.path.dirname(__file__), 'swagger_ui.html')
        
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/html; charset=utf-8',
                'Access-Control-Allow-Origin': request_origin,
                'Access-Control-Allow-Methods': 'GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
            },
            'body': html_content
        }
    except FileNotFoundError:
        logger.error('Swagger UI file not found', extra=create_log_extra(request_id))
        return create_response(404, {'error': 'Swagger UI not found'}, request_origin)
    except Exception as e:
        logger.error('Error serving swagger UI', extra=create_log_extra(
            request_id,
            error_type=type(e).__name__,
            error=str(e)
        ), exc_info=True)
        return create_response(500, {'error': 'Error serving documentation'}, request_origin)


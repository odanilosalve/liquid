import json
import os
from exceptions import ConfigurationError
from utils.config_validator import is_production


def get_allowed_origin(request_origin=None):
    allowed = os.environ.get('ALLOWED_ORIGIN')
    if not allowed:
        if is_production():
            raise ConfigurationError('ALLOWED_ORIGIN environment variable is required in production')
        allowed = '*'
    
    stage = os.environ.get('STAGE')
    if not stage:
        if is_production():
            raise ConfigurationError('STAGE environment variable is required in production')
        stage = 'dev'
    
    if allowed == '*' or stage == 'dev':
        return '*'
    
    if request_origin and request_origin == allowed:
        return request_origin
    
    return allowed


def get_cors_headers():
    headers_str = os.environ.get('CORS_ALLOW_HEADERS', 'Content-Type')
    methods_str = os.environ.get('CORS_ALLOW_METHODS', 'POST, GET, OPTIONS')
    
    return {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Headers': headers_str,
        'Access-Control-Allow-Methods': methods_str
    }


def create_response(status_code, body, request_origin=None):
    allowed_origin = get_allowed_origin(request_origin)
    cors_headers = get_cors_headers()
    
    headers = {
        'Access-Control-Allow-Origin': allowed_origin,
        **cors_headers
    }
    
    return {
        'statusCode': status_code,
        'headers': headers,
        'body': json.dumps(body, default=str)
    }



import pytest
import json
import os
from unittest.mock import patch
from responses import create_response, get_allowed_origin


class TestGetAllowedOrigin:
    @patch.dict(os.environ, {'ALLOWED_ORIGIN': '*', 'STAGE': 'dev'})
    def test_dev_stage_returns_wildcard(self):
        assert get_allowed_origin() == '*'
        assert get_allowed_origin('https://example.com') == '*'

    @patch.dict(os.environ, {'ALLOWED_ORIGIN': 'https://example.com', 'STAGE': 'prod'})
    def test_prod_stage_returns_allowed_origin(self):
        assert get_allowed_origin() == 'https://example.com'
        assert get_allowed_origin('https://example.com') == 'https://example.com'

    @patch.dict(os.environ, {'ALLOWED_ORIGIN': 'https://example.com', 'STAGE': 'prod'})
    def test_prod_stage_rejects_other_origins(self):
        assert get_allowed_origin('https://other.com') == 'https://example.com'

    @patch.dict(os.environ, {}, clear=True)
    def test_default_returns_wildcard(self):
        assert get_allowed_origin() == '*'


class TestCreateResponse:
    def test_status_code(self):
        response = create_response(200, {'status': 'ok'})
        assert response['statusCode'] == 200

    @patch.dict(os.environ, {'STAGE': 'dev'})
    def test_cors_headers_dev(self):
        response = create_response(200, {'status': 'ok'})
        headers = response['headers']
        
        assert headers['Content-Type'] == 'application/json'
        assert headers['Access-Control-Allow-Origin'] == '*'
        assert headers['Access-Control-Allow-Headers'] == 'Content-Type'
        assert headers['Access-Control-Allow-Methods'] == 'POST, GET, OPTIONS'

    @patch.dict(os.environ, {'ALLOWED_ORIGIN': 'https://example.com', 'STAGE': 'prod'})
    def test_cors_headers_prod(self):
        response = create_response(200, {'status': 'ok'}, 'https://example.com')
        headers = response['headers']
        
        assert headers['Access-Control-Allow-Origin'] == 'https://example.com'

    def test_body_as_dict(self):
        body = {'status': 'ok', 'data': {'key': 'value'}}
        response = create_response(200, body)
        
        parsed_body = json.loads(response['body'])
        assert parsed_body == body

    def test_body_as_list(self):
        body = [1, 2, 3, {'key': 'value'}]
        response = create_response(200, body)
        
        parsed_body = json.loads(response['body'])
        assert parsed_body == body

    def test_body_primitive_string(self):
        body = 'simple string'
        response = create_response(200, body)
        
        parsed_body = json.loads(response['body'])
        assert parsed_body == body

    def test_body_primitive_number(self):
        body = 42
        response = create_response(400, body)
        
        parsed_body = json.loads(response['body'])
        assert parsed_body == body

    def test_body_primitive_boolean(self):
        body = True
        response = create_response(200, body)
        
        parsed_body = json.loads(response['body'])
        assert parsed_body == body

    def test_body_none(self):
        body = None
        response = create_response(200, body)
        
        parsed_body = json.loads(response['body'])
        assert parsed_body is None

    def test_different_status_codes(self):
        for status in [200, 400, 404, 500, 503]:
            response = create_response(status, {'error': 'test'})
            assert response['statusCode'] == status

    def test_complex_nested_body(self):
        body = {
            'amount': 100.0,
            'from': 'USD',
            'to': 'BRL',
            'rate': 5.2,
            'converted_amount': 520.0,
            'metadata': {
                'timestamp': '2024-01-01T00:00:00',
                'source': 'cache'
            }
        }
        response = create_response(200, body)
        
        parsed_body = json.loads(response['body'])
        assert parsed_body == body


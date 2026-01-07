import pytest
import json
from request_parser import parse_request_body, extract_request_data
from exceptions import RequestParsingError


class TestParseRequestBody:
    def test_body_as_string_json(self):
        body_dict = {'amount': 100, 'from': 'USD', 'to': 'BRL'}
        body_string = json.dumps(body_dict)
        event = {'body': body_string}
        
        result = parse_request_body(event)
        assert result == body_dict

    def test_body_as_dict(self):
        body_dict = {'amount': 100, 'from': 'USD', 'to': 'BRL'}
        event = {'body': body_dict}
        
        result = parse_request_body(event)
        assert result == body_dict

    def test_body_empty(self):
        event = {'body': ''}
        
        result = parse_request_body(event)
        assert result == {}

    def test_body_none(self):
        event = {'body': None}
        
        with pytest.raises(RequestParsingError):
            parse_request_body(event)

    def test_no_body_key(self):
        event = {}
        
        result = parse_request_body(event)
        assert result == {}

    def test_invalid_json(self):
        event = {'body': 'invalid json{'}
        
        with pytest.raises(RequestParsingError) as exc_info:
            parse_request_body(event)
        assert 'Invalid JSON format' in str(exc_info.value)


class TestExtractRequestData:
    def test_extract_all_fields(self):
        body = {'amount': 100, 'from': 'usd', 'to': 'brl'}
        amount, from_currency, to_currency = extract_request_data(body)
        
        assert amount == 100
        assert from_currency == 'USD'
        assert to_currency == 'BRL'

    def test_uppercase_conversion(self):
        body = {'amount': 50, 'from': 'eur', 'to': 'jpy'}
        amount, from_currency, to_currency = extract_request_data(body)
        
        assert from_currency == 'EUR'
        assert to_currency == 'JPY'

    def test_missing_amount(self):
        body = {'from': 'USD', 'to': 'BRL'}
        amount, from_currency, to_currency = extract_request_data(body)
        
        assert amount is None
        assert from_currency == 'USD'
        assert to_currency == 'BRL'

    def test_missing_from(self):
        body = {'amount': 100, 'to': 'BRL'}
        amount, from_currency, to_currency = extract_request_data(body)
        
        assert amount == 100
        assert from_currency == ''
        assert to_currency == 'BRL'

    def test_missing_to(self):
        body = {'amount': 100, 'from': 'USD'}
        amount, from_currency, to_currency = extract_request_data(body)
        
        assert amount == 100
        assert from_currency == 'USD'
        assert to_currency == ''

    def test_empty_body(self):
        body = {}
        amount, from_currency, to_currency = extract_request_data(body)
        
        assert amount is None
        assert from_currency == ''
        assert to_currency == ''

    def test_mixed_case_currencies(self):
        body = {'amount': 100, 'from': 'UsD', 'to': 'BrL'}
        amount, from_currency, to_currency = extract_request_data(body)
        
        assert from_currency == 'USD'
        assert to_currency == 'BRL'


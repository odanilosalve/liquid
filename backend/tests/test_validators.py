import pytest
from validators import validate_amount, validate_currency, validate_conversion_request
from exceptions import ValidationError
from constants import VALID_CURRENCIES, MAX_AMOUNT, MIN_AMOUNT


class TestValidateAmount:
    def test_valid_amount(self):
        amount_float = validate_amount(100.0)
        assert amount_float == 100.0

    def test_valid_amount_string(self):
        with pytest.raises(ValidationError) as exc_info:
            validate_amount('100.5')
        assert 'Invalid amount. Must be a number.' in str(exc_info.value)

    def test_amount_below_minimum(self):
        with pytest.raises(ValidationError) as exc_info:
            validate_amount(0.001)
        assert f'Amount must be at least {MIN_AMOUNT}' in str(exc_info.value)

    def test_amount_above_maximum(self):
        with pytest.raises(ValidationError) as exc_info:
            validate_amount(MAX_AMOUNT + 1)
        assert 'Amount exceeds maximum limit' in str(exc_info.value)

    def test_amount_zero(self):
        with pytest.raises(ValidationError) as exc_info:
            validate_amount(0)
        error_msg = str(exc_info.value)
        assert 'Invalid amount. Must be a number.' in error_msg or f'Amount must be at least {MIN_AMOUNT}' in error_msg

    def test_amount_negative(self):
        with pytest.raises(ValidationError) as exc_info:
            validate_amount(-10)
        assert f'Amount must be at least {MIN_AMOUNT}' in str(exc_info.value)

    def test_amount_none(self):
        with pytest.raises(ValidationError) as exc_info:
            validate_amount(None)
        assert 'Invalid amount. Must be a number.' in str(exc_info.value)

    def test_amount_string_invalid(self):
        with pytest.raises(ValidationError) as exc_info:
            validate_amount('invalid')
        assert 'Invalid amount. Must be a number.' in str(exc_info.value)

    def test_amount_list(self):
        with pytest.raises(ValidationError) as exc_info:
            validate_amount([100])
        assert 'Invalid amount. Must be a number.' in str(exc_info.value)


class TestValidateCurrency:
    def test_valid_currency(self):
        for currency in VALID_CURRENCIES:
            validate_currency(currency)

    def test_invalid_currency(self):
        with pytest.raises(ValidationError) as exc_info:
            validate_currency('INVALID')
        error_msg = str(exc_info.value)
        assert 'Invalid currency' in error_msg
        assert any(c in error_msg for c in VALID_CURRENCIES)

    def test_empty_currency(self):
        with pytest.raises(ValidationError) as exc_info:
            validate_currency('')
        assert 'Invalid currency' in str(exc_info.value)

    def test_none_currency(self):
        with pytest.raises(ValidationError) as exc_info:
            validate_currency(None)
        assert 'Invalid currency' in str(exc_info.value)


class TestValidateConversionRequest:
    def test_valid_request(self):
        amount_float = validate_conversion_request(100, 'USD', 'BRL')
        assert amount_float == 100.0

    def test_same_currencies(self):
        with pytest.raises(ValidationError) as exc_info:
            validate_conversion_request(100, 'USD', 'USD')
        assert 'From and to currencies must be different' in str(exc_info.value)

    def test_invalid_from_currency(self):
        with pytest.raises(ValidationError) as exc_info:
            validate_conversion_request(100, 'INVALID', 'BRL')
        assert 'Invalid currency' in str(exc_info.value)

    def test_invalid_to_currency(self):
        with pytest.raises(ValidationError) as exc_info:
            validate_conversion_request(100, 'USD', 'INVALID')
        assert 'Invalid currency' in str(exc_info.value)

    def test_invalid_amount(self):
        with pytest.raises(ValidationError) as exc_info:
            validate_conversion_request(-10, 'USD', 'BRL')
        assert 'Amount must be at least' in str(exc_info.value)

    def test_all_valid_currencies(self):
        for from_curr in VALID_CURRENCIES:
            for to_curr in VALID_CURRENCIES:
                if from_curr != to_curr:
                    amount_float = validate_conversion_request(100, from_curr, to_curr)
                    assert amount_float == 100.0


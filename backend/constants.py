import os
from exceptions import ConfigurationError
from utils.config_validator import is_production

def get_valid_currencies():
    currencies_str = os.environ.get('CURRENCIES')
    if not currencies_str:
        if is_production():
            raise ConfigurationError('CURRENCIES environment variable is required in production')
        currencies_str = 'USD,BRL,EUR,GBP,JPY'
    return set(currency.strip().upper() for currency in currencies_str.split(','))

def get_max_amount():
    max_amount_str = os.environ.get('MAX_CONVERSION_AMOUNT')
    if not max_amount_str:
        if is_production():
            raise ConfigurationError('MAX_CONVERSION_AMOUNT environment variable is required in production')
        return 1_000_000_000
    return float(max_amount_str)

def get_min_amount():
    min_amount_str = os.environ.get('MIN_CONVERSION_AMOUNT')
    if not min_amount_str:
        if is_production():
            raise ConfigurationError('MIN_CONVERSION_AMOUNT environment variable is required in production')
        return 0.01
    return float(min_amount_str)

VALID_CURRENCIES = get_valid_currencies()
MAX_AMOUNT = get_max_amount()
MIN_AMOUNT = get_min_amount()



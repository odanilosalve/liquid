import logging
from constants import VALID_CURRENCIES, MAX_AMOUNT, MIN_AMOUNT

logger = logging.getLogger()


def validate_amount(amount, request_id=None):
    if not amount or not isinstance(amount, (int, float)):
        logger.warning('Invalid amount type validation failed', extra={
            'request_id': request_id,
            'amount': amount
        })
        return False, 'Invalid amount. Must be a number.', 0.0
    
    amount_float = float(amount)
    
    if amount_float < MIN_AMOUNT:
        logger.warning('Amount below minimum validation failed', extra={
            'request_id': request_id,
            'amount': amount_float,
            'min_amount': MIN_AMOUNT
        })
        return False, f'Amount must be at least {MIN_AMOUNT}.', amount_float
    
    if amount_float > MAX_AMOUNT:
        logger.warning('Amount above maximum validation failed', extra={
            'request_id': request_id,
            'amount': amount_float,
            'max_amount': MAX_AMOUNT
        })
        return False, f'Amount exceeds maximum limit of {MAX_AMOUNT:,.0f}.', amount_float
    
    return True, '', amount_float


def validate_currency(code, request_id=None):
    if code not in VALID_CURRENCIES:
        logger.warning('Invalid currency validation failed', extra={
            'request_id': request_id,
            'currency': code,
            'valid_currencies': list(VALID_CURRENCIES)
        })
        return False, f'Invalid currency. Must be one of: {", ".join(sorted(VALID_CURRENCIES))}.'
    
    return True, ''


def validate_conversion_request(amount, from_currency, to_currency, request_id=None):
    logger.info('Conversion request received', extra={
        'request_id': request_id,
        'amount': amount,
        'from_currency': from_currency,
        'to_currency': to_currency
    })
    
    is_valid, error, amount_float = validate_amount(amount, request_id)
    if not is_valid:
        return False, error, None
    
    is_valid, error = validate_currency(from_currency, request_id)
    if not is_valid:
        return False, f'Invalid from currency. {error}', None
    
    is_valid, error = validate_currency(to_currency, request_id)
    if not is_valid:
        return False, f'Invalid to currency. {error}', None
    
    if from_currency == to_currency:
        logger.warning('Same currency validation failed', extra={
            'request_id': request_id,
            'from_currency': from_currency,
            'to_currency': to_currency
        })
        return False, 'From and to currencies must be different.', None
    
    return True, '', amount_float


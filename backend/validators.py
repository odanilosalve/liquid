import logging
from constants import VALID_CURRENCIES, MAX_AMOUNT, MIN_AMOUNT
from exceptions import ValidationError
from utils.logging_helpers import create_log_extra

logger = logging.getLogger()


def validate_amount(amount, request_id=None):
    if not amount or not isinstance(amount, (int, float)):
        logger.warning('Invalid amount type validation failed', extra=create_log_extra(request_id, amount=amount))
        raise ValidationError('Invalid amount. Must be a number.')
    
    amount_float = float(amount)
    
    if amount_float < MIN_AMOUNT:
        logger.warning('Amount below minimum validation failed', extra=create_log_extra(
            request_id,
            amount=amount_float,
            min_amount=MIN_AMOUNT
        ))
        raise ValidationError(f'Amount must be at least {MIN_AMOUNT}.')
    
    if amount_float > MAX_AMOUNT:
        logger.warning('Amount above maximum validation failed', extra=create_log_extra(
            request_id,
            amount=amount_float,
            max_amount=MAX_AMOUNT
        ))
        raise ValidationError(f'Amount exceeds maximum limit of {MAX_AMOUNT:,.0f}.')
    
    return amount_float


def validate_currency(code, request_id=None):
    if code not in VALID_CURRENCIES:
        logger.warning('Invalid currency validation failed', extra=create_log_extra(
            request_id,
            currency=code,
            valid_currencies=list(VALID_CURRENCIES)
        ))
        raise ValidationError(f'Invalid currency. Must be one of: {", ".join(sorted(VALID_CURRENCIES))}.')


def validate_conversion_request(amount, from_currency, to_currency, request_id=None):
    logger.info('Conversion request received', extra=create_log_extra(
        request_id,
        amount=amount,
        from_currency=from_currency,
        to_currency=to_currency
    ))
    
    try:
        amount_float = validate_amount(amount, request_id)
        validate_currency(from_currency, request_id)
        validate_currency(to_currency, request_id)
        
        if from_currency == to_currency:
            logger.warning('Same currency validation failed', extra=create_log_extra(
                request_id,
                from_currency=from_currency,
                to_currency=to_currency
            ))
            raise ValidationError('From and to currencies must be different.')
        
        return amount_float
    except ValidationError:
        raise
    except (TypeError, ValueError, AttributeError, KeyError) as e:
        logger.error('Error during validation', extra=create_log_extra(
            request_id,
            error_type=type(e).__name__,
            error=str(e)
        ), exc_info=True)
        raise ValidationError(f'Validation failed: {str(e)}')
    except Exception as e:
        logger.error('Unexpected error during validation', extra=create_log_extra(
            request_id,
            error_type=type(e).__name__,
            error=str(e)
        ), exc_info=True)
        raise ValidationError(f'Validation failed: {str(e)}')



import logging
from exceptions import DatabaseError
from responses import create_response
from utils.logging_helpers import create_log_extra

logger = logging.getLogger()


def handle_unexpected_error(e, request_id, context_message, request_origin=None):
    error_type = type(e).__name__
    logger.error(f'Unexpected error {context_message}', extra=create_log_extra(
        request_id,
        error_type=error_type
    ), exc_info=True)
    return create_response(500, {'error': 'Internal server error'}, request_origin)


def handle_configuration_error(e, request_id, request_origin=None):
    error_type = type(e).__name__
    logger.error('Configuration error', extra=create_log_extra(
        request_id,
        error_type=error_type,
        error=str(e)
    ), exc_info=True)
    return create_response(500, {'error': 'Configuration error'}, request_origin)


def handle_unauthorized_error(e, request_id, request_origin=None):
    logger.warning('Unauthorized request', extra=create_log_extra(
        request_id,
        error=str(e)
    ))
    return create_response(401, {'error': str(e)}, request_origin)


def handle_database_error(e, request_id, context_message):
    error_type = type(e).__name__
    logger.error(f'Database error {context_message}', extra=create_log_extra(
        request_id,
        error_type=error_type
    ), exc_info=True)
    raise DatabaseError(f'{context_message}: {str(e)}')


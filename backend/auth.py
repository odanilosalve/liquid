import os
import boto3
import bcrypt
import logging
from datetime import datetime
from botocore.exceptions import BotoCoreError, ClientError
from exceptions import AuthenticationError, DatabaseError, ConfigurationError
from utils.logging_helpers import create_log_extra
from utils.error_handlers import handle_database_error
from utils.config_validator import is_production

logger = logging.getLogger()

dynamodb = boto3.resource('dynamodb')

def get_users_table_name():
    table_name = os.environ.get('USERS_TABLE')
    if not table_name:
        if is_production():
            raise ConfigurationError('USERS_TABLE environment variable is required in production')
        return 'users-dev'
    return table_name

users_table_name = get_users_table_name()
users_table = dynamodb.Table(users_table_name)


def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')


def verify_password(password, password_hash):
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))


def verify_credentials(username, password, request_id=None):
    logger.info('Verifying credentials', extra=create_log_extra(request_id, username=username))
    
    try:
        response = users_table.get_item(
            Key={'user_id': username}
        )
        
        if 'Item' not in response:
            logger.warning('User not found', extra=create_log_extra(request_id, username=username))
            raise AuthenticationError('Invalid credentials')
        
        user = response['Item']
        stored_password_hash = user.get('password_hash')
        
        if not stored_password_hash:
            logger.warning('User has no password hash', extra=create_log_extra(request_id, username=username))
            raise AuthenticationError('Invalid credentials')
        
        if not verify_password(password, stored_password_hash):
            logger.warning('Invalid password', extra=create_log_extra(request_id, username=username))
            raise AuthenticationError('Invalid credentials')
        
        logger.info('Credentials verified successfully', extra=create_log_extra(
            request_id,
            username=username,
            user_id=user.get('user_id')
        ))
        
        return user
        
    except AuthenticationError:
        raise
    except (BotoCoreError, ClientError) as e:
        handle_database_error(e, request_id, 'verifying credentials')
    except Exception as e:
        handle_database_error(e, request_id, 'verifying credentials')


def create_user(username, password, request_id=None):
    logger.info('Creating user', extra=create_log_extra(request_id, username=username))
    
    try:
        password_hash = hash_password(password)
        
        users_table.put_item(
            Item={
                'user_id': username,
                'username': username,
                'password_hash': password_hash,
                'created_at': str(datetime.utcnow().isoformat())
            }
        )
        
        logger.info('User created successfully', extra=create_log_extra(request_id, username=username))
        
    except (BotoCoreError, ClientError) as e:
        handle_database_error(e, request_id, 'creating user')
    except Exception as e:
        handle_database_error(e, request_id, 'creating user')


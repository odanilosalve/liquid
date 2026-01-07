import os
import boto3
import json
import secrets
import string
import logging
from pathlib import Path
from botocore.exceptions import BotoCoreError, ClientError
from auth import create_user
from exceptions import DatabaseError, ConfigurationError, AuthenticationError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_dynamodb_resource():
    region = os.environ.get('AWS_DEFAULT_REGION', 'us-east-1')
    return boto3.resource('dynamodb', region_name=region)

dynamodb = get_dynamodb_resource()
users_table_name = os.environ.get('USERS_TABLE', 'users-dev')
users_table = dynamodb.Table(users_table_name)

USERNAMES = ['admin', 'user1', 'test']


def _generate_secure_password():
    length_str = os.environ.get('SEED_PASSWORD_LENGTH', '16')
    try:
        length = int(length_str)
    except (ValueError, TypeError):
        length = 16
    
    chars_str = os.environ.get('SEED_PASSWORD_CHARS')
    if chars_str:
        alphabet = chars_str
    else:
        alphabet = string.ascii_letters + string.digits + string.punctuation
    
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def _load_passwords_from_config_file():
    config_file_name = os.environ.get('SEED_USERS_CONFIG_FILE', 'seed_users_config.json')
    config_file = Path(config_file_name)
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f'Error reading seed_users_config.json: {e}')
    return {}


def _get_user_password(username):
    env_var_name = f'SEED_USER_{username.upper()}_PASSWORD'
    password = os.environ.get(env_var_name)
    
    if password:
        logger.info(f'Using password from environment variable for {username}')
        return password
    
    config = _load_passwords_from_config_file()
    if username in config and 'password' in config[username]:
        logger.info(f'Using password from config file for {username}')
        return config[username]['password']
    
    generated_password = _generate_secure_password()
    logger.warning(
        f'No password configured for user {username}. '
        f'Generated secure password: {generated_password}'
    )
    logger.warning(
        f'To set a password, use environment variable {env_var_name} '
        f'or add to seed_users_config.json'
    )
    return generated_password


def seed_users():
    logger.info(f'Seeding users table: {users_table_name}')
    
    users_created = 0
    users_failed = 0
    
    for username in USERNAMES:
        try:
            password = _get_user_password(username)
            create_user(username, password)
            logger.info(f'User {username} created successfully')
            users_created += 1
        except (DatabaseError, ConfigurationError, AuthenticationError) as e:
            logger.error(f'Error creating user {username}: {str(e)}', exc_info=True)
            users_failed += 1
        except (BotoCoreError, ClientError) as e:
            logger.error(f'Database connection error creating user {username}: {str(e)}', exc_info=True)
            users_failed += 1
        except Exception as e:
            logger.error(f'Unexpected error creating user {username}: {str(e)}', exc_info=True)
            users_failed += 1
    
    logger.info(f'Users seeding completed. Created: {users_created}, Failed: {users_failed}')

if __name__ == '__main__':
    seed_users()


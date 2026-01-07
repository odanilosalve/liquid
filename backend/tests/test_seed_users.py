import pytest
import os
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, Mock
from seed_users import _get_user_password, _generate_secure_password, _load_passwords_from_config_file, seed_users


class TestGetUserPassword:
    @patch.dict(os.environ, {'SEED_USER_ADMIN_PASSWORD': 'secure-admin-password'}, clear=True)
    def test_get_password_from_env_var(self):
        password = _get_user_password('admin')
        assert password == 'secure-admin-password'
    
    def test_get_password_from_config_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config_file = Path(tmpdir) / 'seed_users_config.json'
            config_file.write_text(json.dumps({
                'admin': {'password': 'config-file-password'}
            }))
            
            with patch('seed_users.Path', return_value=config_file):
                password = _get_user_password('admin')
                assert password == 'config-file-password'
    
    def test_generate_password_when_none_provided(self):
        with patch.dict(os.environ, {}, clear=True):
            password = _get_user_password('nonexistent')
            assert password is not None
            assert len(password) >= 16
            assert isinstance(password, str)
    
    @patch.dict(os.environ, {'SEED_USER_ADMIN_PASSWORD': 'env-password'}, clear=True)
    def test_env_var_takes_priority_over_config(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config_file = Path(tmpdir) / 'seed_users_config.json'
            config_file.write_text(json.dumps({
                'admin': {'password': 'config-password'}
            }))
            
            with patch('seed_users.Path', return_value=config_file):
                password = _get_user_password('admin')
                assert password == 'env-password'


class TestGenerateSecurePassword:
    def test_password_length(self):
        with patch.dict(os.environ, {'SEED_PASSWORD_LENGTH': '16', 'STAGE': 'dev'}, clear=True):
            password = _generate_secure_password()
            assert len(password) == 16
    
    def test_password_randomness(self):
        with patch.dict(os.environ, {'SEED_PASSWORD_LENGTH': '32', 'STAGE': 'dev'}, clear=True):
            password1 = _generate_secure_password()
            password2 = _generate_secure_password()
            assert password1 != password2
    
    def test_password_contains_different_char_types(self):
        with patch.dict(os.environ, {'SEED_PASSWORD_LENGTH': '100', 'STAGE': 'dev'}, clear=True):
            password = _generate_secure_password()
            has_letters = any(c.isalpha() for c in password)
            has_digits = any(c.isdigit() for c in password)
            has_punctuation = any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password)
            assert has_letters or has_digits or has_punctuation


class TestLoadPasswordsFromConfigFile:
    def test_load_valid_config_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config_file = Path(tmpdir) / 'seed_users_config.json'
            config_data = {
                'admin': {'password': 'admin123'},
                'user1': {'password': 'user123'}
            }
            config_file.write_text(json.dumps(config_data))
            
            with patch('seed_users.Path', return_value=config_file):
                config = _load_passwords_from_config_file()
                assert config == config_data
    
    def test_return_empty_dict_when_file_not_exists(self):
        with patch('seed_users.Path') as mock_path:
            mock_path.return_value.exists.return_value = False
            config = _load_passwords_from_config_file()
            assert config == {}
    
    def test_handle_invalid_json_gracefully(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config_file = Path(tmpdir) / 'seed_users_config.json'
            config_file.write_text('invalid json{')
            
            with patch('seed_users.Path', return_value=config_file):
                config = _load_passwords_from_config_file()
                assert config == {}


class TestSeedUsers:
    @patch('seed_users.create_user')
    @patch.dict(os.environ, {
        'SEED_USER_ADMIN_PASSWORD': 'admin123',
        'SEED_USER_USER1_PASSWORD': 'user123',
        'SEED_USER_TEST_PASSWORD': 'test123',
        'USERS_TABLE': 'test-users'
    }, clear=True)
    def test_seed_users_with_env_vars(self, mock_create_user):
        seed_users()
        assert mock_create_user.call_count == 3
        mock_create_user.assert_any_call('admin', 'admin123')
        mock_create_user.assert_any_call('user1', 'user123')
        mock_create_user.assert_any_call('test', 'test123')
    
    @patch('seed_users.create_user')
    @patch.dict(os.environ, {'USERS_TABLE': 'test-users'}, clear=True)
    def test_seed_users_generates_passwords_when_missing(self, mock_create_user):
        seed_users()
        assert mock_create_user.call_count == 3
        for call in mock_create_user.call_args_list:
            username, password = call[0]
            assert password is not None
            assert len(password) >= 16


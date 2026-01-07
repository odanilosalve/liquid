import pytest
from unittest.mock import Mock, patch
from auth import verify_credentials, hash_password, verify_password, create_user
from exceptions import AuthenticationError, DatabaseError


class TestHashPassword:
    def test_hash_password_creates_hash(self):
        password = 'testpassword123'
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        
        assert hash1 != password
        assert hash2 != password
        assert hash1 != hash2

    def test_verify_password_success(self):
        password = 'testpassword123'
        password_hash = hash_password(password)
        
        assert verify_password(password, password_hash) is True

    def test_verify_password_failure(self):
        password = 'testpassword123'
        wrong_password = 'wrongpassword'
        password_hash = hash_password(password)
        
        assert verify_password(wrong_password, password_hash) is False


class TestVerifyCredentials:
    @patch('auth.users_table')
    def test_verify_credentials_success(self, mock_table):
        mock_user = {
            'user_id': 'testuser',
            'username': 'testuser',
            'password_hash': hash_password('password123')
        }
        
        mock_table.get_item.return_value = {'Item': mock_user}
        
        user = verify_credentials('testuser', 'password123')
        
        assert user is not None
        assert user['user_id'] == 'testuser'

    @patch('auth.users_table')
    def test_verify_credentials_user_not_found(self, mock_table):
        mock_table.get_item.return_value = {}
        
        with pytest.raises(AuthenticationError) as exc_info:
            verify_credentials('nonexistent', 'password123')
        assert 'Invalid credentials' in str(exc_info.value)

    @patch('auth.users_table')
    def test_verify_credentials_wrong_password(self, mock_table):
        mock_user = {
            'user_id': 'testuser',
            'username': 'testuser',
            'password_hash': hash_password('correctpassword')
        }
        
        mock_table.get_item.return_value = {'Item': mock_user}
        
        with pytest.raises(AuthenticationError) as exc_info:
            verify_credentials('testuser', 'wrongpassword')
        assert 'Invalid credentials' in str(exc_info.value)

    @patch('auth.users_table')
    def test_verify_credentials_database_error(self, mock_table):
        mock_table.get_item.side_effect = Exception('DynamoDB error')
        
        with pytest.raises(DatabaseError) as exc_info:
            verify_credentials('testuser', 'password123')
        assert 'verifying credentials' in str(exc_info.value)


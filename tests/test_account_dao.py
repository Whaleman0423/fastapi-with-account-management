import pytest
from unittest.mock import Mock
from daos.account_dao import AccountDao

@pytest.fixture
def mock_dynamodb():
    """定義一個 pytest 的 fixture，用於模擬 DynamoDB 客戶端"""
    return Mock()

@pytest.fixture
def mock_logger():
    """定義一個 pytest 的 fixture，用於模擬 logger"""
    return Mock()

@pytest.fixture
def account_dao(mock_dynamodb, mock_logger):
    """定義一個 pytest 的 fixture，用於創建 AccountDao 實例"""
    return AccountDao(mock_dynamodb, mock_logger)

def test_check_account_table_exists(account_dao):
    """測試 check_account_table_exists 方法"""
    table_mock = Mock()
    account_dao.dynamodb.Table.return_value = table_mock
    table_mock.load.return_value = None

    assert account_dao.check_account_table_exists("Account") is True

def test_create_user(account_dao):
    """測試 create_user 方法"""
    table_mock = Mock()
    account_dao.dynamodb.Table.return_value = table_mock

    assert account_dao.create_user("Account", "testuser", "Testpassword1") is True

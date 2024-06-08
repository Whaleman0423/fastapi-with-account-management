import pytest
from unittest.mock import Mock, patch
from services.account_service import AccountService
from schemas.create_account_schema import CreateAccountResponse
from schemas.verify_account_schema import VerifyAccountResponse

@pytest.fixture
def mock_dynamodb():
    """定義一個 pytest 的 fixture，用於模擬 DynamoDB 客戶端"""
    return Mock()

@pytest.fixture
def mock_logger():
    """定義一個 pytest 的 fixture，用於模擬 logger"""
    return Mock()

@pytest.fixture
def account_service(mock_dynamodb, mock_logger):
    """定義一個 pytest 的 fixture，用於創建 AccountService 實例"""
    return AccountService(mock_dynamodb, mock_logger)

def test_create_account_success(account_service):
    """測試 create_account 成功的情況"""
    # 模擬 AccountDao 的方法
    with patch.object(account_service.account_dao, 'check_account_table_exists', return_value=False):
        with patch.object(account_service.account_dao, 'create_account_table', return_value=True):
            with patch.object(account_service.account_dao, 'check_account_exists', return_value=False):
                with patch.object(account_service.account_dao, 'create_user', return_value=True):
                    # 調用 create_account 方法
                    response = account_service.create_account("testuser", "Testpassword1")
                    # 驗證返回的結果
                    assert response == CreateAccountResponse(success=True, reason="帳戶創建成功")

def test_verify_account_success(account_service):
    """測試 verify_account 成功的情況"""
    #  創建一個模擬的帳戶對象
    account_mock = Mock()
    account_mock.password = "Testpassword1"
    account_mock.failed_attempts = 0
    account_mock.last_failed_attempt_time = None

    # 模擬 AccountDao 的方法
    with patch.object(account_service.account_dao, 'check_account_table_exists', return_value=True):
        with patch.object(account_service.account_dao, 'check_account_exists', return_value=True):
            with patch.object(account_service.account_dao, 'get_account', return_value=account_mock):
                with patch.object(account_service.account_dao, 'update_user', return_value=True):
                    # 調用 verify_account 方法
                    response = account_service.verify_account("testuser", "Testpassword1")
                    # 驗證返回的結果
                    assert response == VerifyAccountResponse(success=True, reason="帳戶驗證成功")

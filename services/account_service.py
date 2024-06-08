import logging
from datetime import datetime, timedelta, timezone
from daos.account_dao import AccountDao
from fastapi import HTTPException
from models.account import Account
from schemas.create_account_schema import CreateAccountResponse
from schemas.verify_account_schema import VerifyAccountResponse

class AccountService:
    """定義 AccountService 類別，負責處理帳戶相關的業務邏輯"""
    def __init__(self, dynamodb, logger: logging.Logger):
        # 初始化 AccountDao 和 logger
        self.account_dao = AccountDao(dynamodb, logger)
        self.logger = logger

    def create_account(self, username: str, password: str) -> CreateAccountResponse:
        """創建帳戶的方法"""
        table_name = "Account"
        # 檢查並創建帳戶表格（如果不存在）
        self.create_account_table_if_not_exists(table_name)

        # 創建帳戶時，檢查用戶是否存在，若不存在則創建
        return self.check_user_in_account_table_when_creating_account(
            table_name, 
            username, 
            password
        )

    def verify_account(self, username: str, password: str) -> VerifyAccountResponse:
        """驗證帳戶的方法"""
        table_name = "Account"
        # 檢查並創建帳戶表格（如果不存在）
        self.create_account_table_if_not_exists(table_name)

        # 檢查用戶是否存在於表格中
        is_user_exists_in_table = self.account_dao.check_account_exists(table_name, username)
        if not is_user_exists_in_table:
            return VerifyAccountResponse(success=False, reason="驗證失敗，請確認帳號或密碼是否正確")
        
        # 獲取帳戶資料
        account = self.account_dao.get_account(table_name, username)
        last_failed_attempt_time = account.last_failed_attempt_time
        failed_attempts = account.failed_attempts
        now = datetime.now(timezone.utc)

        # 檢查是否需要等待
        self.check_waiting_time(now, last_failed_attempt_time)

        # 驗證密碼是否正確
        is_password_correct = account.password == password
        if not is_password_correct:
            failed_attempts += 1
            self.check_failed_attempts_over_5(failed_attempts, now, table_name, username)
            return VerifyAccountResponse(success=False, reason="驗證失敗，請確認帳號或密碼是否正確")

        # 更新用戶失敗次數和最後一次失敗時間
        self.account_dao.update_user(
            table_name, 
            username, 
            {
                "failed_attempts": 0,
                "last_failed_attempt_time": None
            }
        )
        return VerifyAccountResponse(success=True, reason="帳戶驗證成功")

    def create_account_table_if_not_exists(self, table_name: str):
        """檢查並創建帳戶表格（如果不存在）"""
        is_table_exists = self.account_dao.check_account_table_exists(table_name)
        if not is_table_exists:
            self.account_dao.create_account_table(table_name)

    def check_user_in_account_table_when_creating_account(self, table_name: str, username: str, password: str) -> CreateAccountResponse:
        """創建帳戶時，檢查用戶是否存在，若不存在則創建"""
        is_user_exists_in_table = self.account_dao.check_account_exists(table_name, username)
        if not is_user_exists_in_table:
            if not self.account_dao.create_user(table_name, username, password):
                return CreateAccountResponse(success=False, reason="帳戶創建失敗")
            return CreateAccountResponse(success=True, reason="帳戶創建成功")
        else:
            return CreateAccountResponse(success=False, reason="帳戶先前已建立")
    
    def check_waiting_time(self, now: datetime, last_failed_attempt_time: datetime):
        """檢查是否需要等待"""
        if last_failed_attempt_time is not None and last_failed_attempt_time + timedelta(minutes=1) > now:
            wait_time = (last_failed_attempt_time + timedelta(minutes=1) - now).seconds
            raise HTTPException(status_code=429, detail=f"Too many failed attempts. Please wait {wait_time} seconds")
    
    def check_failed_attempts_over_5(self, failed_attempts: int, now: datetime, table_name: str, username: str):
        """檢查失敗次數是否超過5次"""
        if failed_attempts >= 5:
            # 初始化用戶失敗次數和更新最後一次失敗時間
            self.account_dao.update_user(
                table_name, 
                username, 
                {
                    "failed_attempts": 0,
                    "last_failed_attempt_time": now.isoformat()
                }
            )
        else:
            # 更新用戶的失敗次數
            self.account_dao.update_user(
                table_name, 
                username, 
                {"failed_attempts": failed_attempts}
            )

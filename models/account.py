from datetime import datetime 
from typing import Optional
from pydantic import BaseModel, Field, validator

class Account(BaseModel):
    """定義帳戶實體"""
    username: str 
    password: str
    failed_attempts: int = 0
    last_failed_attempt_time: Optional[datetime] = None

    def __str__(self):
        """定義 __str__ 方法，返回帳戶的字串表示"""
        return f'''
        Account(
            username={self.username}, 
            password={"*" * len(self.password)}, 
            failed_attempts={self.failed_attempts}, 
            last_failed_attempt_time={self.last_failed_attempt_time}
        )
        '''

    def to_json(self) -> dict:
        """將 Account 轉換為字典格式"""
        return self.model_dump()
    
    @staticmethod
    def from_dict(data: dict) -> "Account":
        """從字典數據創建 Account 實例"""
        return Account(**data)

import re

from pydantic import BaseModel, field_validator

class CreateAccountRequest(BaseModel):
    """定義 CreateAccountRequest 類別，用於處理創建帳戶的請求數據"""
    username: str
    password: str

    @field_validator('username')
    def username_length(cls, v):
        """驗證用戶名的長度"""
        if not (3 <= len(v) <= 32):
            raise ValueError('Username must be between 3 and 32 characters')
        return v

    @field_validator('password')
    def password_strength(cls, v):
        """驗證密碼的強度"""
        if not (8 <= len(v) <= 32):
            raise ValueError('Password must be between 8 and 32 characters')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one number')
        return v
    
class CreateAccountResponse(BaseModel):
    """定義 CreateAccountResponse 類別，用於處理創建帳戶的響應數據"""
    success: bool
    reason: str
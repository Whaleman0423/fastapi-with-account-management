from pydantic import BaseModel

# 驗證帳戶及密碼的請求模型
class VerifyAccountRequest(BaseModel):
    """定義 VerifyAccountRequest 類別，用於處理驗證帳戶的請求數據"""
    username: str
    password: str

class VerifyAccountResponse(BaseModel):
    """定義 VerifyAccountResponse 類別，用於處理驗證帳戶的響應數據"""
    success: bool
    reason: str = None

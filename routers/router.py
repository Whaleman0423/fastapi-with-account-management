from fastapi import APIRouter, Depends

from dependencies import get_account_service
from schemas.create_account_schema import CreateAccountRequest, CreateAccountResponse
from schemas.verify_account_schema import VerifyAccountRequest, VerifyAccountResponse
from services.account_service import AccountService

# 創建一個 FastAPI 路由器實例
router = APIRouter()

@router.get("/ping")
async def hello_world():
    """定義一個 GET 路由，測試服務器是否運行正常"""
    return 'pong'

@router.post("/create_account")
async def create_account(request: CreateAccountRequest, account_service: 
    AccountService = Depends(get_account_service)) -> CreateAccountResponse:
    """定義一個 POST 路由，用於創建帳戶"""
    # 調用 AccountService 的 create_account 方法，並傳入用戶名和密碼
    return account_service.create_account(request.username, request.password)

@router.post("/verify_account")
async def verify_account(request: VerifyAccountRequest, account_service: 
AccountService = Depends(get_account_service)) -> VerifyAccountResponse:
    """定義一個 POST 路由，用於驗證帳戶"""
    # 調用 AccountService 的 verify_account 方法，並傳入用戶名和密碼
    return account_service.verify_account(request.username, request.password)

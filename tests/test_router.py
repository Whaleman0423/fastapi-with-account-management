from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch

# 創建一個 FastAPI 測試客戶端
client = TestClient(app)

def test_create_account():
    """測試創建帳戶的 API"""
    # 使用 patch 模擬 get_account_service 函數
    with patch("routers.router.get_account_service") as mock_service:

        # 設置模擬的 account_service 返回的 create_account 方法的返回值
        mock_service.return_value.create_account.return_value = {
            "success": True, "reason": "帳戶創建成功"
        }

        # 發送 POST 請求到 /create_account 路由，並傳遞 JSON 數據
        response = client.post(
            "/create_account", 
            json={"username": "testuser", "password": "Testpassword1"}
        )

        # 驗證結果
        assert response.status_code == 200
        assert response.json() == {"success": True, "reason": "帳戶創建成功"}

def test_verify_account():
    """測試驗證帳戶的 API"""
    # 使用 patch 模擬 get_account_service 函數
    with patch("routers.router.get_account_service") as mock_service:

        # 設置模擬的 account_service 返回的 verify_account 方法的返回值
        mock_service.return_value.verify_account.return_value = {
            "success": True, "reason": "帳戶驗證成功"
        }

        # 發送 POST 請求到 /verify_account 路由，並傳遞 JSON 數據
        response = client.post(
            "/verify_account", 
            json={"username": "testuser", "password": "Testpassword1"}
        )

        # 驗證結果
        assert response.status_code == 200
        assert response.json() == {"success": True, "reason": "帳戶驗證成功"}

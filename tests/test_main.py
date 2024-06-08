from fastapi.testclient import TestClient
from main import app

# 創建一個 FastAPI 測試客戶端
client = TestClient(app)

def test_ping():
    """測試 /ping 路由"""
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.text == '"pong"'

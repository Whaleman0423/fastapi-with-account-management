# 實作 FastAPI API 基礎入門 + 帳戶創建與驗證密碼功能
此實作使用  FastAPI 快速建立後端 API 系統，實現帳戶創建與驗證密碼功能 API，並添加 web 資料夾作為前端頁面(前端使用 Flutter Web)，方便用戶直接測試 API。  
開發階段使用 dynamoDB Emulator 作為開發測試 NoSQL 資料庫，透過 .env 檔案中的 USE_EMULATOR 來轉換開發與生產階段。

## 檔案目錄結構
```
.
│  .dockerignore
│  .env
│  .gitignore
│  dependencies.py # 依賴注入
│  docker-compose.yaml
│  Dockerfile
│  main.py # 主程式
│  readme.md
│  requirements.txt
│  __init__.py
│
├─daos # 資料讀取寫入
│  │  account_dao.py
│  └─ __init__.py
│
├─models # 資料模型
│  │  account.py
│  └─ __init__.py
│  
├─routers # API 路由設置
│  │  router.py
│  └─ __init__.py
│  
├─schemas # request 與 response 資料模型
│  │  create_account_schema.py
│  │  verify_account_schema.py
│  └─ __init__.py
│  
├─services # 邏輯
│  │  account_service.py
│  └─ __init__.py
│  
├─tests # 單元測試
│  │  test_account_dao.py
│  │  test_account_service.py
│  │  test_main.py
│  │  test_router.py
│  └─ __init__.py
│  
└─web # 前端網頁
```

## 使用流程
1. 拉取程式碼並 Open Folder 開啟專案程式碼資料夾
2. 取得 AWS IAM User Credentials  
a. AWS_ACCESS_KEY_ID  
b. AWS_SECRET_ACCESS_KEY
3. (dev) 設置 .env 環境設定檔案
4. (dev) 啟動容器並運行系統
6. (dev) 手動與單元測試 API  
a. GET Method, /ping  
b. POST Method, /create_account  
c. POST Method, /verify_account  
d. Unit Test - Pytest  
e. 前端網頁測試
7. 觀察 OpenAPI Spec Docs
8. (prod) 生產部署
9. 測試完畢記得移除 AWS IAM USER 金鑰

### 拉取程式碼並 Open Folder 開啟專案程式碼資料夾
```
git clone https://github.com/Whaleman0423/fastapi-with-account-management.git
```

### 取得 AWS IAM User Credentials
為了讓本地開發的程式碼有權訪問雲端資源，需要設置 IAM User 並創建金鑰，讓程式透過金鑰的方式通過 AWS IAM 的驗證，以下是 IAM User 的設置與創建金鑰的流程：

登入 AWS 主控台: https://console.aws.amazon.com/console/home?nc2=h_ct&src=header-signin  

至 IAM User Console: https://us-east-1.console.aws.amazon.com/iam/home?region=ap-northeast-1#/users  

* 操作流程
    * 點選建立使用者
    * 設定使用者名稱: dynamodb-test-user-full-access，下一步
    * 設定許可範圍
        * 使用許可範圍來控制許可上限
        * 選取 AmazonDynamoDBFullAccess
        * 建立使用者
    * 回到 IAM User Console，點選剛所建立的 IAM User
        * 新增許可 - 建立內嵌政策
        * 點選 JSON，開啟政策編輯器，更新政策為以下(需替換帳戶 ID 為自己的帳戶 ID)，完成後點選下一步，設定政策名稱: dynamodb-account-table-policy  

IAM User 政策
```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:DescribeTable",
        "dynamodb:CreateTable",
        "dynamodb:GetItem",
        "dynamodb:PutItem"
      ],
      "Resource": "arn:aws:dynamodb:ap-northeast-1:<請移除左右大小於符號，並替換成自己的帳戶ID>:table/Account"
    }
  ]
}
```
* IAM User 設定完畢後，回到 IAM User Console，點選剛所建立的 IAM User，點選建立存取金鑰
* 選擇本機代碼
* 建立存取金鑰 (金鑰不可外流)

### (dev) 設置 .env 環境設定檔案
取得金鑰的 2 個設定值後，設置 .env 環境設定檔案在專案資料夾根目錄：

.env
```
USE_EMULATOR=True

AWS_ACCESS_KEY_ID=<請移除左右大小於符號，替換成金鑰 AWS_ACCESS_KEY_ID>
AWS_SECRET_ACCESS_KEY=<請移除左右大小於符號，替換成金鑰 AWS_SECRET_ACCESS_KEY>

AWS_DEFAULT_REGION=ap-northeast-1
AWS_DYNAMODB_ENDPOINT_URL=http://dynamodb-emulator:8000
```

### (dev) 啟動容器並運行系統
接著啟動 Docker Desktop 或 Linux 的 Docker server，確認當下 port 並無 5000 與 8000 port 後，執行以下指令：

```
docker compose up -d
```

### (dev) 手動與單元測試 API
以下提供 API 的串接測試，可以使用 Postman 進行 API 測試，或是訪問 http://localhost:5000/ ，使用前端頁面串接後端 API 測試功能。

#### GET Method, /ping
使用 Postman GET 方法訪問或網頁瀏覽: http://localhost:5000/ping

Response: pong

#### POST Method, /create_account
使用 Postman Post 方法訪問: 
http://localhost:5000/create_account  

Body - raw json
```
{
    "username": "Test_account_123",
    "password": "Test_password_123"
}
```

Response
```
# Status: 200
{"success": true | false, "reason": str}
```

#### POST Method, /verify_account
使用 Postman Post 方法訪問: 
http://localhost:5000/verify_account  

Body - raw json
```
{
    "username": "Test_account_123",
    "password": "Test_password_123"
}
```

Response
```
# Status: 200
{"success": true | false, "reason": str}
# Status: 429
{"detail": "Too many failed attempts. Please wait ?? seconds"}
```

#### Unit Test - Pytest
在容器內部執行以下指令:
```
pytest
```
預期結果: 全部通過

#### 前端網頁測試
在啟動 fastapi 系統的前提下，訪問 http://localhost:5000/  
開啟前端網頁後，可以在「創建帳戶區」與「驗證密碼區」分別的輸入框輸入 username 與 password 並點擊按鈕驗證，測試情境參考以下:  
1. 創建帳號:  
a. 不正常 username - username: 1a，password: 1a2b3c4d  
b. 不正常 username - username: 1a2b3c4d，password: 1a2b3c4d  
c. 不正常 password - username: 1a2b3c4D，password: 1a  
d. 皆不正常 - username: 1a，password: 1a  
c. 正常 - username: 1a2b3c4D，password: 1a2b3c4d

2. 驗證密碼  
a. 正常 - username: 1a2b3c4D，password: 1a2b3c4d  
b. 異常訪問超過 5 次 - username: 1a2b3c4D，password: 1a2b3c4dzzz

#### 觀察 OpenAPI Spec Docs
fastapi 會自動生成 API 文件，訪問 http://localhost:5000/docs

#### (prod) 生產部署
提供 Dockerfile 作為 production 所使用。  
將環境變數設定為 .env 所有的環境變數，並設定 USE_EMULATOR=False

#### 測試完畢記得移除 AWS IAM USER 金鑰
記得移除 IAM User 或是其金鑰，避免金鑰外洩風險

## Docker Hub
https://hub.docker.com/r/whaleman0423/fastapi-with-account-management

## Contact Author
Email: sheiyuray@gmail.com
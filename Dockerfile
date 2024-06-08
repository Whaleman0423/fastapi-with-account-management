# 使用官方 Python 3.10.0 映像檔
FROM python:alpine3.19

# 設定工作目錄
WORKDIR /app

# 將本地的應用程式程式碼複製到容器中
COPY . /app

# 安裝應用程式所需的套件
RUN pip install --no-cache-dir -r requirements.txt

# 定義容器啟動時要執行的命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
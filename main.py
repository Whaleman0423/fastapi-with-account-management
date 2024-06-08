from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routers import router
from typing import Optional

app = FastAPI()

# 定義允許的跨域來源
origins = [
    '*'
]

# 添加跨域資源共享（CORS）中介軟體
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# 定義路由
app.include_router(router.router)

# 設定靜態文件目錄
app.mount("/", StaticFiles(directory="web", html=True))

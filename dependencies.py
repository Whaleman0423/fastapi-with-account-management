import os
import boto3
import logging

from fastapi import Depends
from services.account_service import AccountService


def get_dynamodb_client():
    """定義一個函數，用於獲取 DynamoDB 客戶端"""
    # 取出必要環境變數
    region_name = os.getenv('AWS_DEFAULT_REGION', 'ap-northeast-1')
    endpoint_url = os.getenv('AWS_DYNAMODB_ENDPOINT_URL', None) if os.getenv("USE_EMULATOR") == "True" else None

    return boto3.resource('dynamodb', region_name=region_name, endpoint_url=endpoint_url)

def get_logger():
    """定義一個函數，用於獲取 logger 實例"""
    # 創建一個名為 "account_service_logger" 的 logger
    logger = logging.getLogger("account_service_logger")

    # 如果 logger 沒有處理器，則添加一個 StreamHandler
    if not logger.handlers:
        handler = logging.StreamHandler()
        
        # 設定日誌格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # 設定日誌級別為 INFO
        logger.setLevel(logging.INFO)

    return logger

def get_account_service(
        dynamodb=Depends(get_dynamodb_client), 
        logger=Depends(get_logger)
        ):
    """定義一個函數，用於獲取 AccountService 實例"""
    return AccountService(dynamodb, logger)

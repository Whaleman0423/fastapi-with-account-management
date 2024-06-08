import logging

from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from models.account import Account
from typing import Any, Dict, Optional


class AccountDao:
    def __init__(self, dynamodb, logger: logging.Logger):
        """初始化 AccountDao 類別，接收 dynamodb 資源和 logger 作為參數"""
        self.dynamodb = dynamodb
        self.logger = logger

    def _handle_exception(self, e: Exception) -> bool:
        """處理例外情況，並根據例外類型記錄錯誤日誌"""
        if isinstance(e, self.dynamodb.meta.client.exceptions.ResourceNotFoundException):
            self.logger.error("Resource not found.")
        elif isinstance(e, NoCredentialsError):
            self.logger.error("AWS credentials not found.")
        elif isinstance(e, PartialCredentialsError):
            self.logger.error("Incomplete AWS credentials.")
        else:
            self.logger.error(f"An error occurred: {e}")
        return False

    def check_account_table_exists(self, table_name: str) -> bool:
        """檢查指定的表格是否存在"""
        try:
            table = self.dynamodb.Table(table_name)
            table.load()
            self.logger.info(f'Table "{table_name}" exists.')
            return True
        except Exception as e:
            return self._handle_exception(e)

    def create_account_table(self, table_name: str) -> bool:
        """創建新的 DynamoDB 表格"""
        try:
            table = self.dynamodb.create_table(
                TableName=table_name,
                KeySchema=[
                    {'AttributeName': 'username', 'KeyType': 'HASH'}
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'username', 'AttributeType': 'S'}
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )
            # 等待表格創建完成
            table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
            self.logger.info(f'Table "{table_name}" has been created.')
            return True
        except Exception as e:
            return self._handle_exception(e)

    def check_account_exists(self, table_name: str, username: str) -> bool:
        """檢查指定的用戶是否存在於表格中"""
        try:
            table = self.dynamodb.Table(table_name)
            response = table.get_item(Key={'username': username})
            exists = 'Item' in response
            self.logger.info(f'User "{username}" exists: {exists}')
            return exists
        except Exception as e:
            return self._handle_exception(e)

    def create_user(self, table_name: str, username: str, password: str) -> bool:
        """在表格中創建新用戶"""
        try:
            table = self.dynamodb.Table(table_name)
            new_user = Account(username=username, password=password)
            table.put_item(Item=new_user.to_json())
            self.logger.info(f'User "{username}" has been created in table "{table_name}".')
            return True
        except Exception as e:
            return self._handle_exception(e)

    def get_account(self, table_name: str, username: str) -> Optional[Account]:
        """獲取指定用戶的帳戶資料"""
        try:
            table = self.dynamodb.Table(table_name)
            response = table.get_item(Key={'username': username})
            if 'Item' in response:
                account = Account.from_dict(response['Item'])
                self.logger.info(f'Account for user "{username}" retrieved successfully.')
                return account
            else:
                self.logger.info(f'User "{username}" does not exist in table "{table_name}".')
                return None
        except Exception as e:
            self._handle_exception(e)
            return None

    def update_user(self, table_name: str, username: str, updated_data: Dict[str, Any]) -> bool:
        """更新指定用戶的資料"""
        try:
            table = self.dynamodb.Table(table_name)
            update_expression = "SET " + ", ".join(f"{k} = :{k}" for k in updated_data.keys())
            expression_attribute_values = {f":{k}": v for k, v in updated_data.items()}
            
            response = table.update_item(
                Key={'username': username},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values,
                ReturnValues="UPDATED_NEW"
            )
            self.logger.info(f'User "{username}" has been updated in table "{table_name}".')
            return response
        except Exception as e:
            return self._handle_exception(e)

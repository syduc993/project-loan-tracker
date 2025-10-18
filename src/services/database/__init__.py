import requests
from typing import Dict, Any, Optional
from src.core.config import settings
import time

class LarkbaseClient:
    def __init__(self):
        self.app_id = settings.LARK_APP_ID
        self.app_secret = settings.LARK_APP_SECRET
        self.base_id = settings.LARK_BASE_ID
        self.access_token = None
        self.token_expires_at = 0
        self.base_url = "https://open.larksuite.com/open-apis"
    
    def get_access_token(self) -> str:
        """Lấy tenant access token"""
        if self.access_token and time.time() < self.token_expires_at:
            return self.access_token
        
        url = f"{self.base_url}/auth/v3/tenant_access_token/internal"
        payload = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        response = requests.post(url, json=payload)
        data = response.json()
        
        if data.get("code") == 0:
            self.access_token = data["tenant_access_token"]
            self.token_expires_at = time.time() + data["expire"] - 60
            return self.access_token
        else:
            raise Exception(f"Failed to get access token: {data}")
    
    def get_headers(self) -> Dict[str, str]:
        """Tạo headers cho API request"""
        return {
            "Authorization": f"Bearer {self.get_access_token()}",
            "Content-Type": "application/json"
        }
    
    def create_record(self, table_id: str, fields: Dict[str, Any]) -> Dict[str, Any]:
        """Tạo record mới"""
        url = f"{self.base_url}/bitable/v1/apps/{self.base_id}/tables/{table_id}/records"
        payload = {"fields": fields}
        response = requests.post(url, headers=self.get_headers(), json=payload)
        data = response.json()
        
        if data.get("code") == 0:
            return data["data"]["record"]
        else:
            raise Exception(f"Failed to create record: {data}")
    
    def get_records(self, table_id: str, filter_str: Optional[str] = None, 
                   sort: Optional[list] = None, page_size: int = 500) -> list:
        """Lấy danh sách records"""
        url = f"{self.base_url}/bitable/v1/apps/{self.base_id}/tables/{table_id}/records"
        params = {"page_size": page_size}
        
        if filter_str:
            params["filter"] = filter_str
        if sort:
            params["sort"] = sort
        
        all_records = []
        has_more = True
        page_token = None
        
        while has_more:
            if page_token:
                params["page_token"] = page_token
            
            response = requests.get(url, headers=self.get_headers(), params=params)
            data = response.json()
            
            if data.get("code") == 0:
                all_records.extend(data["data"]["items"])
                has_more = data["data"]["has_more"]
                page_token = data["data"].get("page_token")
            else:
                raise Exception(f"Failed to get records: {data}")
        
        return all_records
    
    def update_record(self, table_id: str, record_id: str, fields: Dict[str, Any]) -> Dict[str, Any]:
        """Cập nhật record"""
        url = f"{self.base_url}/bitable/v1/apps/{self.base_id}/tables/{table_id}/records/{record_id}"
        payload = {"fields": fields}
        response = requests.put(url, headers=self.get_headers(), json=payload)
        data = response.json()
        
        if data.get("code") == 0:
            return data["data"]["record"]
        else:
            raise Exception(f"Failed to update record: {data}")
    
    def delete_record(self, table_id: str, record_id: str) -> bool:
        """Xóa record"""
        url = f"{self.base_url}/bitable/v1/apps/{self.base_id}/tables/{table_id}/records/{record_id}"
        response = requests.delete(url, headers=self.get_headers())
        data = response.json()
        
        return data.get("code") == 0

larkbase_client = LarkbaseClient()

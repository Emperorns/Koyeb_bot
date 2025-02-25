import os
import requests
from requests.exceptions import RequestException

class KoyebManager:
    def __init__(self):
        self.base_url = "https://app.koyeb.com/v1"
        self.services = self._load_services()

    def _load_services(self):
        return {
            acc: {
                'key': os.getenv(f"KOYEB_{acc.upper()}_KEY"),
                'service_id': os.getenv(f"KOYEB_{acc.upper()}_SERVICE")
            }
            for acc in os.getenv('KOYEB_ACCOUNTS', '').split(',')
        }

    def _make_request(self, method, endpoint, account):
        try:
            headers = {'Authorization': f'Bearer {self.services[account]["key"]}'}
            response = requests.request(
                method,
                f"{self.base_url}{endpoint}",
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return f"Error: {str(e)}"

    def get_logs(self, account):
        return self._make_request(
            'GET', 
            f"/services/{self.services[account]['service_id']}/logs", 
            account
        )

    def redeploy(self, account):
        return self._make_request(
            'POST', 
            f"/services/{self.services[account]['service_id']}/redeploy", 
            account
        )

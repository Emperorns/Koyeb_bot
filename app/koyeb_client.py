import os
import requests
from requests.exceptions import RequestException

class KoyebManager:
    def __init__(self):
        self.base_url = "https://app.koyeb.com/v1"
        self.accounts = self._load_accounts()

    def _load_accounts(self):
        accounts = {}
        for var in os.environ:
            if var.startswith("KOYEB_") and var.endswith("_KEY"):
                account_id = var[6:-4].lower()
                accounts[account_id] = {
                    'key': os.getenv(var),
                    'service': os.getenv(f"KOYEB_{account_id.upper()}_SERVICE")
                }
        return accounts

    def _make_request(self, method, endpoint, account, data=None):
        try:
            headers = {'Authorization': f'Bearer {self.accounts[account]["key"]}'}
            response = requests.request(
                method,
                f"{self.base_url}{endpoint}",
                headers=headers,
                json=data,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except KeyError:
            return "Error: Account not found"
        except RequestException as e:
            return f"API Error: {str(e)}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"

    def get_logs(self, account):
        if account not in self.accounts:
            return "Invalid account"
        result = self._make_request('GET', f"/services/{self.accounts[account]['service']}/logs", account)
        return result[:4000] if isinstance(result, str) else str(result)

    def redeploy(self, account):
        if account not in self.accounts:
            return "Invalid account"
        return self._make_request('POST', f"/services/{self.accounts[account]['service']}/redeploy", account)

    def list_services(self):
        services = []
        for account, config in self.accounts.items():
            services.append(f"{account}: {config['service']}")
        return "Configured Services:\n" + "\n".join(services) if services else "No services configured"

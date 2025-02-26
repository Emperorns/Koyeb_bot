# app/koyeb_client.py
import os
import logging
import requests
from requests.exceptions import RequestException

class KoyebManager:
    def __init__(self):
        self.base_url = "https://app.koyeb.com/v1"
        self.services = self._load_services()

    def _load_services(self):
        """
        Load Koyeb accounts and their configurations from environment variables.
        
        Returns:
            dict: A dictionary of accounts with their API keys and service IDs.
        """
        accounts = {}
        for var in os.environ:
            if var.startswith("KOYEB_") and var.endswith("_KEY"):
                account_id = var[6:-4].lower()  # Extract account name (e.g., "account1")
                accounts[account_id] = {
                    'key': os.getenv(var),
                    'service_id': os.getenv(f"KOYEB_{account_id.upper()}_SERVICE")
                }
        return accounts

    def _make_request(self, method, endpoint, account):
        """
        Make a request to the Koyeb API.
        
        Args:
            method (str): HTTP method (e.g., "GET", "POST")
            endpoint (str): API endpoint (e.g., "/services/{service_id}/logs")
            account (str): Account identifier (e.g., "account1")
            
        Returns:
            str or dict: API response or error message.
        """
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
        except RequestException as e:
            # Log the full error response
            logging.error(f"API Error: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logging.error(f"Response: {e.response.text}")
            return f"Error: {str(e)}"
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            return f"Unexpected error: {str(e)}"

    def get_logs(self, account):
        """
        Fetch logs for a specific Koyeb service.
        
        Args:
            account (str): Account identifier (e.g., "account1")
            
        Returns:
            str: Logs or error message.
        """
        if account not in self.services:
            return "Invalid account"
        return self._make_request(
            'GET', 
            f"/services/{self.services[account]['service_id']}/logs", 
            account
        )

    def redeploy(self, account):
        """
        Trigger a redeploy for a specific Koyeb service.
        
        Args:
            account (str): Account identifier (e.g., "account1")
            
        Returns:
            str: Redeploy status or error message.
        """
        if account not in self.services:
            return "Invalid account"
        return self._make_request(
            'POST', 
            f"/services/{self.services[account]['service_id']}/redeploy", 
            account
        )

    def list_services(self):
        """
        List all configured Koyeb services.
        
        Returns:
            str: Formatted list of services or error message.
        """
        if not self.services:
            return "No services configured"
        services = []
        for account, config in self.services.items():
            services.append(f"{account}: {config['service_id']}")
        return "Configured Services:\n" + "\n".join(services)

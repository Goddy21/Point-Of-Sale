import os
import requests
from datetime import datetime, timedelta
import json
from quickbooks import QuickBooks


class QuickBooksSessionManager:
    def __init__(self):
        # Load tokens from environment variables or default to empty strings
        self.access_token = os.getenv('ACCESS_TOKEN', "")
        self.refresh_token = os.getenv('REFRESH_TOKEN', "")
        self.client_id = os.getenv('CLIENT_ID', "")
        self.client_secret = os.getenv('CLIENT_SECRET', "")
        
        company_id = os.getenv('COMPANY_ID', "")
        self.company_id = company_id.replace(" ", "") if company_id else ""

        self.token_expires_at = datetime.now() + timedelta(seconds=3600)
        self.load_tokens()

    def load_tokens(self):
        try:
            with open('tokens.json', 'r') as f:
                tokens = json.load(f)
                self.access_token = tokens.get('access_token', self.access_token)
                self.refresh_token = tokens.get('refresh_token', self.refresh_token)
                if expires_at := tokens.get('expires_at'):
                    self.token_expires_at = datetime.fromisoformat(expires_at)
        except FileNotFoundError:
            print("Token file not found; using environment tokens.")
        except Exception as e:
            print(f"Error loading tokens: {e}")

    def is_access_token_valid(self):
        """Check if the access token is still valid."""
        return self.access_token and datetime.now() < self.token_expires_at

    def refresh_access_token(self):
        """Refresh the access token using the refresh token."""
        if not self.refresh_token:
            raise Exception("No refresh token available to refresh access token. Please verify the .env file and tokens.json for a valid refresh token.")
        
        url = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"
        headers = {
            'Authorization': f'Basic {self.encode_client_credentials()}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token
        }

        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            tokens = response.json()
            self.access_token = tokens['access_token']
            self.refresh_token = tokens.get('refresh_token', self.refresh_token)
            self.token_expires_at = datetime.now() + timedelta(seconds=tokens['expires_in'])
            self.save_tokens()
        else:
            print("Failed to refresh access token:", response.status_code, response.text)
            raise Exception(f"Failed to refresh access token: {response.json()}")

    def get_quickbooks_client(self):
        """Get QuickBooks client, refreshing the token if necessary."""
        if not self.is_access_token_valid():
            try:
                self.refresh_access_token()
            except Exception as e:
                print(f"Token refresh failed: {e}")
                raise

        return QuickBooks(
            sandbox=True,
            consumer_key=self.client_id,
            consumer_secret=self.client_secret,
            access_token=self.access_token,
            company_id=self.company_id
        )

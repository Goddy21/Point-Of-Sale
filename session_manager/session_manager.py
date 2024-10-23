import os
import requests
from datetime import datetime, timedelta
from quickbooks import QuickBooks
#Q70G1700700 8F

class QuickBooksSessionManager:
    def __init__(self):
        self.access_token = 'eyJlbmMiOiJBMTI4Q0JDLUhTMjU2IiwiYWxnIjoiZGlyIn0..fRcrNxxTrMbg8s5mO0EoIw.6trr2Bh5i0eII3NFu8salH1IqHzGeUcAwgmztpf_gp7AZjfvkWZi583tszvGy3VVkQsIAXlvC6fniPD03bmkgCLiloWz9b9C6PNq2VxEqQ6oSg2Jhx3pNH9uS5qsuCqXXBaYFNUNDGdMwdwnrWu5eO3rvW_vLIzf_Afd0k9HKDvvlqqcqEuOsGh3jTo3X6pAf0Thgj_unJdwtYjRztuxN3CsbiKD_rGpYkMdP0XSjmvhC2EvNHq7mMv-oGMVcXPlPAX-9eXBgaEKANwQ1o9H3FNuNfulVQXrz9qq1ess1LRoZdmRKGLDaIWMK7Oe__IS0JJBh96YfyFk6YGT5dWoxipc6GTpRI076ZnXgwHZP1ldDTwS4oFhRo3o2z4WAnromckprbNCwCreyP7PbGQJd-2ssYtdnIFkUDj3CF4DvQWAO9Pry2h3lF8cJ2mgRBkodUatzjCU5SfqyLxJfmCCWFr7Xlmi_8w4uUEPuruaLXKXtbZZUbjLKjCtcVdvVLG76FFtGo5uQ9ECAq2MNVOFumP5FZp08a4kKq4O4ExiWDxnJ06kQb8DJPkKXGFUAavgpgngnzQennboFspPfdezHnuq1jVcyvjOL3tZ46CggL5mfAs0VHqC4SeypY1Je92wWMaivoDfJ1gjismlaMmmZ_5-6NVuv0564Nb_fyJZijyv5t3agg4c_0fZKLY3TsvWdvLQ08ftpdlqJSmixQcar_7kkZhfByNVCOcBHn3FCQYxnuvA0dqxQnucxMWmDBFWVf-OHrLKjV1SaAN-fPvh9G7wQ8SCF3SraAcSAYMpEoJpFnH_Uf7F9njf1f4Qzk87oEzALiQR_tYhrTEwKduMWEitTK6ur3CD6cco14sg38b4V3kSRzzShU55IxskruLp.gp204pUxBYX5J85yO-b7JA'
        self.refresh_token = 'AB11737801257u5KVpx8lhzqvsHIR7JgTfWcQsFlWPZDU5gjiZ'
        self.token_expires_at = datetime.now() + timedelta(seconds=3600) 
        self.client_id = os.environ.get('ABoqbaaHvyetO9NFXji3s0bVvf84DQ1WdSl3gchBwVMKgC9YuC')
        self.client_secret = os.environ.get('RUIUp4VXT8A2EkaTD1z5cFoqIHQ65LsLfMj5f768')
        self.company_id = '9341 4533 0129 1022'  # Replace with actual company ID

        # Load stored tokens (if you have a way to store them)
        self.load_tokens()

    def load_tokens(self):
        # Implement loading of tokens from secure storage (file, database, etc.)
        # Example placeholder logic
        try:
            # Load from a file or database
            with open('tokens.json', 'r') as f:
                tokens = json.load(f)
                self.access_token = tokens.get('access_token')
                self.refresh_token = tokens.get('refresh_token')
                self.token_expires_at = datetime.fromisoformat(tokens.get('expires_at'))
        except Exception as e:
            print(f"Error loading tokens: {e}")

    def save_tokens(self):
        # Implement saving of tokens to secure storage
        # Example placeholder logic
        try:
            with open('tokens.json', 'w') as f:
                tokens = {
                    'access_token': self.access_token,
                    'refresh_token': self.refresh_token,
                    'expires_at': self.token_expires_at.isoformat()
                }
                json.dump(tokens, f)
        except Exception as e:
            print(f"Error saving tokens: {e}")

    def is_access_token_valid(self):
        return self.access_token and self.token_expires_at and datetime.now() < self.token_expires_at

    def refresh_access_token(self):
        if not self.refresh_token:
            raise Exception("No refresh token available to refresh access token.")

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
            self.refresh_token = tokens.get('refresh_token', self.refresh_token)  # Update refresh token if returned
            self.token_expires_at = datetime.now() + timedelta(seconds=tokens['expires_in'])
            self.save_tokens()  # Save the new tokens
        else:
            print(f"Failed to refresh access token: {response.json()}")

    def encode_client_credentials(self):
        import base64
        credentials = f"{self.client_id}:{self.client_secret}"
        return base64.b64encode(credentials.encode()).decode()

    def get_quickbooks_client(self):
        if not self.is_access_token_valid():
            self.refresh_access_token()
        
        return QuickBooks(
            sandbox=True,
            consumer_key=self.client_id,
            consumer_secret=self.client_secret,
            access_token=self.access_token,
            company_id=self.company_id
        )
    def refresh_access_token(self):
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
            self.refresh_token = tokens.get('refresh_token', self.refresh_token)  # Update refresh token if provided
            self.token_expires_at = datetime.now() + timedelta(seconds=tokens['expires_in'])
            self.save_tokens()  # Save tokens to secure storage
        else:
            print(f"Error refreshing token: {response.content}")


# Example usage:
session_manager = QuickBooksSessionManager()
qb_client = session_manager.get_quickbooks_client()

# Now you can use qb_client to make API calls

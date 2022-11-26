import os
from google.oauth2.credentials import Credentials

def generate_token_from_cred(credential_path,scopes) -> dict:
    try:
        if os.path.exists(credential_path):
            creds = Credentials.from_authorized_user_file(credential_path, scopes)
        # If there are no (valid) credentials available, try to refresh
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
        return creds.to_json()
    except Exception as e:
        print("Exeption in token generation")
        return None
    

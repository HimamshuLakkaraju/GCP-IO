import os
import json
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request


def validate_token(token_path) -> dict:
    try:
        if os.path.exists(token_path):
            with open(token_path) as token_file:
                token_obj = json.load(token_file)
                creds = Credentials(
                    token_obj.get("token"),
                    refresh_token=token_obj.get("refresh_token"),
                    token_uri=token_obj.get("token_uri"),
                    client_id=token_obj.get("client_id"),
                    client_secret=token_obj.get("client_secret"),
                )
            # If there is no (valid) token available, try to refresh
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                    # Update env var token value with creds.to_json() TODO
            return creds
        else:
            print(f"Utils invalid path")
            # TODO add exception

    except Exception as e:
        print(f"Exeption in token generation\n{e}")
        return None

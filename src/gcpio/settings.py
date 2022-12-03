from os import getenv

## Google Drive APIs #
SCOPES = ["https://www.googleapis.com/auth/drive"]
CRED_FILE_PATH = getenv("CREDENTIALS_PATH")
TOKEN_PATH_GDRIVE = getenv("TOKEN_PATH_GDRIVE")
LOG_FILE_PATH = getenv("LOG_FILE_PATH")
LOG_LEVEL = getenv("LOG_LEVEL")

import os
import sys
from . import utils

## Google Drive APIs #
SCOPES = ["https://www.googleapis.com/auth/drive"]
CRED_FILE_PATH = os.getenv("CREDENTIALS_PATH")
TOKEN_PATH_GDRIVE = os.getenv("TOKEN_PATH_GDRIVE")

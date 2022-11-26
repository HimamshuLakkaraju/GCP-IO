import os
import sys
from . import utils
print(sys.argv)
print("in")

## Google Drive APIs #
SCOPES=["https://www.googleapis.com/auth/drive.metadata.readonly"]
CRED_FILE_PATH = os.getenv("CREDENTIALS_PATH")
TOKEN=utils.generate_token_from_cred(CRED_FILE_PATH,SCOPES)
print(TOKEN)
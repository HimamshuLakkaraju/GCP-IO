from . import settings
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

print("Gdrive")

cred_file_path = settings.CRED_FILE_PATH
token_file_path = settings.TOKEN_PATH_GDRIVE
# credentials = service_account.Credentials.from_service_account_file(cred_file_path)
token = settings.TOKEN
print(f"Gdrive token \n{token}")


def gdrive() -> None:
    try:
        service = build("drive", "v3", credentials=token)

        # Call the Drive v3 API
        results = (
            service.files()
            .list(pageSize=10, fields="nextPageToken, files(id, name)")
            .execute()
        )
        items = results.get("files", [])

        if not items:
            print("No files found.")
            return
        print("Files:")
        for item in items:
            print("{0} ({1})".format(item["name"], item["id"]))
    except Exception as e:
        print(f"exception\n{e}")


if __name__ == "__main__":
    gdrive()

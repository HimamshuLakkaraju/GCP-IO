from . import settings
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
cred_file_path=settings.CRED_FILE_PATH
print(cred_file_path)
credentials = service_account.Credentials.from_service_account_file(cred_file_path)
print(credentials)
def gdrive():
    print("Gdrive")
    print(settings.test_dict["sample"])
    try:
        service = build('drive', 'v3', credentials=credentials)

        # Call the Drive v3 API
        results = service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
            return
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))
    except Exception as e:
        print(f"exception\n{e}")

if __name__ == '__main__':
    gdrive()
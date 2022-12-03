import io
from PIL import Image
from . import utils
from .utils import auth_token
from torch.utils.data import Dataset
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError

# import asyncio

import time


class Gdrive:
    """Google Drive class that has functions to return the metadata of files in a Google Drive folder and generate torch datasets from files in google drive"""

    def __init__(self) -> None:
        print("init")
        self.token = utils.token()

    @auth_token
    def get_files_metadata(
        self,
        folder_name=None,
        folder_id=None,
        page_size=500,
        file_type=None,
        replace_query=None,
    ) -> dict:
        try:
            files = {}
            query = f"parents in '{folder_id}' and mimeType != 'application/vnd.google-apps.folder'"
            print(query)

            if file_type:
                query = query + f"and mimeType='{file_type}'"
            if replace_query:
                query = replace_query

            service = build("drive", "v3", credentials=self.token)
            page_size = page_size
            next_page_token = None
            results = (
                service.files()
                .list(
                    pageSize=page_size,
                    fields="nextPageToken, files(id, name, mimeType, webContentLink)",
                    q=query,
                )
                .execute()
            )
            items = results.get("files", [])
            if not items:
                print("No files found.")
                return

            next_page_token = results.get("nextPageToken")
            while next_page_token:
                results = (
                    service.files()
                    .list(
                        pageToken=next_page_token,
                        pageSize=page_size,
                        fields="nextPageToken, files(id, name, mimeType, webContentLink)",
                        q=query,
                    )
                    .execute()
                )
                items = items + results.get("files", [])
                next_page_token = results.get("nextPageToken")

            files["files"] = items
            files["len"] = len(items)

            return files
        except Exception as e:
            print(f"Exception \n{e}")

    def reformat_response(self, data):
        data_dict = {}
        for obj in data:
            data_dict[obj.get("name").split(".")[0]] = {
                "mimeType": obj.get("mimeType"),
                "id": obj.get("id"),
            }
        return data_dict

    @auth_token
    def create_dataset(
        self,
        data_folder_id,
        labels_folder_id=None,
        data_folder_name=None,
        labels_folder_name=None,
        page_size=500,
        data_file_type=None,
        labels_file_type=None,
        replace_query=None,
        skip_labels=False,
    ) -> None:
        try:
            print("Create dataset")
            if skip_labels:
                print("FLASE")
                data_files_metadata_dict = self.get_files_metadata(
                    data_folder_name,
                    data_folder_id,
                    page_size=page_size,
                    file_type=data_file_type,
                    replace_query=None,
                )
                data_files_metadata_dict.get("files")
            else:
                print(f"In {data_folder_id}")
                data_files_metadata_dict = self.get_files_metadata(
                    data_folder_name,
                    folder_id=data_folder_id,
                    page_size=page_size,
                    file_type=data_file_type,
                    replace_query=replace_query,
                )
                data_files = self.reformat_response(
                    data_files_metadata_dict.get("files")
                )
                print(f"Datafiles\n {data_files}")

                labels_files_metadata_dict = self.get_files_metadata(
                    labels_folder_name,
                    labels_folder_id,
                    page_size=page_size,
                    file_type=labels_file_type,
                    replace_query=replace_query,
                )
                label_files = self.reformat_response(
                    labels_files_metadata_dict.get("files")
                )

                if data_files_metadata_dict.get(
                    "len"
                ) == labels_files_metadata_dict.get("len"):
                    dataset = GdriveDataset(data_files, label_files, self.token)

                elif labels_files_metadata_dict.get("len") == 1:
                    pass

                return data_files, dataset
        except Exception as e:
            print(f"Exception at {e}")


class GdriveDataset(Dataset):
    """Make API calls and create a dataset with file binaries"""

    def __init__(self, data_file_names_list, labels_file_names_list, token) -> None:
        print("Dataset init")
        self.data = data_file_names_list
        self.labels = labels_file_names_list
        self.keys = list(data_file_names_list)
        self.token = token

    def __len__(self) -> int:
        return len(self.keys)

    # async def get_files_from_drive(self, indices) -> dict:
    #     print(time.time())
    #     await (time.sleep(10))
    #     print(indices)

    #     return indices

    # async def test_func(self, index):
    #     await asyncio.gather(*[self.get_files_from_drive(index) for index in index])
    #     return 1

    def download_files_from_drive(self, file_id) -> bytes:
        try:
            print(file_id)
            service = build("drive", "v3", credentials=self.token)
            request = service.files().get_media(fileId=file_id)
            file = io.BytesIO()
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(f"Download {int(status.progress() * 100)}.")

        except HttpError as error:
            print(f"An error occurred: {error}")
            file = None

        return file.getvalue()

    def __getitem__(self, index) -> None:
        """# This function cuurently makes API calls synchronously.
        Making these API calls async would improve the performance significantly
        but that would require updating the Datafetcher functions from the torch dataloader.
        More details about this in the documentation.

        Args:
            index (_type_): For this use case it's better to use a batch index hence a list of numbers
            in range(0, len(data)) with length as batch size from dataloader is expected

        Returns:
            (Images,labels)
        """
        batch_data = []
        batch_labels = []
        for i in index:
            file_name = self.keys[i]
            data_file_id = self.data.get(file_name).get("id")
            label_file_id = self.labels.get(file_name).get("id")
            data_file_b_content = self.download_files_from_drive(data_file_id)
            label_file_b_content = self.download_files_from_drive(label_file_id)

            print(label_file_b_content)

        return None

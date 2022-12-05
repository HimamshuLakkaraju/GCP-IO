from .utils import auth_token, get_logger, token
from google.cloud import storage

logger = get_logger(__name__)


class GCS:
    """Class that has methods to get data from Google cloud storage and convert them into torch datasets. This is not implemented completely and currently can return the blob meta data
    from Google cloud storage for public buckets."""

    def __init__(self, project="BigData") -> None:
        self.storage_client = storage.Client(project=project)

    def get_files_metadata(
        self, bucket_id, page_size=500, file_type=None, replace_query=None
    ) -> None:

        """Get the meta data of files in the given bucket id

        Args:
            bucket_id (_type_): _description_
            page_size (_type_): _description_
            file_type (_type_): _description_
            replace_query (_type_): _description_
        """
        meta_data_list = list(
            self.storage_client.list_blobs(
                bucket_id,
            )
        )
        return meta_data_list

    def create_dataset():
        """Not Implemented yet. This method would return a dataset with the files from bucket id passed.

        Raises:
            NotImplementedError: This is not implemented currently.
        """
        raise NotImplementedError

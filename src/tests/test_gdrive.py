from gcpio.gdrive import Gdrive, GdriveDataset
from torch.utils.data import Dataset
from googleapiclient.errors import HttpError


def test_token() -> None:
    """Create an instance for the class Gdrive and check if the token is being loaded"""
    gdrive = Gdrive()
    assert gdrive.token != None


def test_get_files_metadata() -> dict:
    gdrive = Gdrive()
    folder_id = "1W_JcItr1ScqvwKT-m8LSoFs425XTG9vg"
    response = gdrive.get_files_metadata(folder_id)
    assert isinstance(response, dict)


def test_create_dataset():
    gdrive = Gdrive()
    folder_id = "1W_JcItr1ScqvwKT-m8LSoFs425XTG9vg"
    response = gdrive.create_dataset(folder_id)
    assert response == None


def test_create_dataset_skip_label():
    gdrive = Gdrive()
    folder_id = "1W_JcItr1ScqvwKT-m8LSoFs425XTG9vg"
    response = gdrive.create_dataset(
        folder_id, data_file_type="image/png", skip_labels=True
    )
    assert isinstance(response, Dataset)


def test_create_dataset_working():
    """Valid files to get valid response"""
    gdrive = Gdrive()
    response = gdrive.create_dataset(
        data_folder_id="1W_JcItr1ScqvwKT-m8LSoFs425XTG9vg",
        labels_folder_id="1W_JcItr1ScqvwKT-m8LSoFs425XTG9vg",
        page_size=1000,
        data_file_type="image/png",
        labels_file_type="text/csv",
    )
    assert isinstance(response, Dataset)


def test_create_dataset_working2():
    """sending invalid file types to check if returning None response"""
    gdrive = Gdrive()
    response = gdrive.create_dataset(
        data_folder_id="1W_JcItr1ScqvwKT-m8LSoFs425XTG9vg",
        labels_folder_id="1W_JcItr1ScqvwKT-m8LSoFs425XTG9vg",
        page_size=1000,
        data_file_type="image/pneg",  # should be png testing with invalid file format
        labels_file_type="text/csev",  # should be csv testing with invalid file format
    )
    assert response == None


def test_reformat_response():
    gdrive = Gdrive()
    sample_data = [
        {"name": "Test1", "id": "1", "mimeType": "mimeType"},
        {"name": "Test2", "id": "2", "mimeType": "mimeType2"},
    ]
    response = gdrive.reformat_response(sample_data)
    assert isinstance(response, dict)
    assert list(response.keys()) == ["Test1", "Test2"]
    assert isinstance(response.get("Test1"), dict)
    assert response.get("Test1") == {"id": "1", "mimeType": "mimeType"}


def test_GdriveDataset():
    dataset = GdriveDataset([], [], [])
    assert Exception


def test_download_files_from_drive():
    """Valid file"""
    file_id = "18tU7vyFzu_NTbTYYKYs7GTs6HBDmFY-E"
    gdrive = Gdrive()
    response = gdrive.download_files_from_drive(file_id)
    assert isinstance(response, bytes)


def test_download_files_from_drive_invalid():
    """invalid file"""
    file_id = "18tU7vyFzu_NTbTYYKYs7GTs6HBDmFY"  # invalid file id
    gdrive = Gdrive()
    response = gdrive.download_files_from_drive(file_id)
    assert response == None

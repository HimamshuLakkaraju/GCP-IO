# GCP-IO
Generate PyTorch datasets from files stored in Google cloud storage and Google drive.

## Installation
Run the following to install this package:
```python
pip install gcpio
```

## Environment Variables Required
```
LOG_FILE_PATH: Path to store the logs in a log file
LOG_LEVEL: LOG LEVEL(Example: INFO, DEBUG, ERROR etc)
TOKEN_PATH_GDRIVE: path to the generated token.json file
```
## Example usage:

Google Drive:

```python
from gcpio.gdrive import Gdrive

# Get meta data of files present in a Google Drive folder
GDRIVE = Gdrive()
files=GDRIVE.get_files_metadata(folder_id="XXXXX",page_size=500,file_type="image/png",replace_query=None) # returns a dict with keys['files','len'] where files is a list of objects from the Drive folder

# Create the torch dataset from files
GDRIVE = Gdrive()
dataset = g.create_dataset(
    data_folder_id=folder_id,
    labels_folder_id=folder_id,
    page_size=1000,
    data_file_type="image/png",
    labels_file_type="text/csv",
    skip_labels=skip_labels,
)

dataloader = DataLoader(
    dataset,
    batch_size,
    sampler=BatchSampler(
        SequentialSampler(dataset), batch_size=batch_size, drop_last=True
    ),
)
```

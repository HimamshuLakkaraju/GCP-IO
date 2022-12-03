import os
import json
import logging
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from . import settings

"""
Utils contains the function to get the token file and create a Google Auth credential. This also has few decorator functions that are yet to be implemented.

"""


def get_logger(name):
    log_path = settings.LOG_FILE_PATH
    log_level = settings.LOG_LEVEL

    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    logging_file_handler = logging.FileHandler(log_path)
    logging_file_handler.setFormatter(formatter)
    logger.addHandler(logging_file_handler)

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)
    logger.addHandler(console)

    return logger


utils_logger = get_logger(__name__)


def token() -> Credentials | None:
    token_path = settings.TOKEN_PATH_GDRIVE
    utils_logger.debug(f"Utils - tokenpath- {token_path}")
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
            utils_logger.error(f"Utils invalid path")
            raise Exception(f"Invalid path: {token_path}")
            # TODO add custom exception?

    except Exception as e:
        utils_logger.error(f"Exception in token generation\n{e}")
        return None


def auth_token(func):
    """To be implemented. This can be used to check if the token is valid before making any API calls and refresh the token if necessary. This decorator function is not implemented yet."""

    def wrapper(*args, **kwargs) -> dict:
        files = func(*args, **kwargs)
        return files

    return wrapper

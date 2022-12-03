from gcpio import settings


def test_SCOPE():
    assert settings.SCOPES != None


def test_CRED_FILE_PATH():
    assert settings.CRED_FILE_PATH != None


def test_TOKEN_PATH_GDRIVE():
    assert settings.TOKEN_PATH_GDRIVE != None


def test_LOG_FILE_PATH():
    assert settings.LOG_FILE_PATH != None


def test_LOG_LEVEL():
    assert settings.LOG_LEVEL != None

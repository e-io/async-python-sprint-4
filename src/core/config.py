from logging import config as logging_config
from pathlib import Path

from pydantic import BaseSettings

from .logger import LOGGING

# logging settings
logging_config.dictConfig(LOGGING)

BASE_DIR = Path.cwd().parent.parent
# print('BASE_DIR', BASE_DIR)


class AppSettings(BaseSettings):
    # Don't use this name, set any name in '.env' file.
    PROJECT_NAME: str = "Default app's name"

    class Config:
        env_file = '.env'


app_settings = AppSettings()

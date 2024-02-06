"""
Run through console:

uvicorn src.main:app --host 127.0.0.1 --port 8080
additional notes are in the `../README.md` file
"""
from pathlib import Path

from pydantic import BaseSettings

BASE_DIR = Path.cwd().parent.parent
# print('BASE_DIR', BASE_DIR)


class AppSettings(BaseSettings):
    # Don't use this name, set any name in '.env' file.
    PROJECT_NAME: str = "Default app's name"

    class Config:
        env_file = '.env'


app_settings = AppSettings()

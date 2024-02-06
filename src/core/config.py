from pathlib import Path

from pydantic import BaseSettings

BASE_DIR = Path.cwd().parent.parent
# print('BASE_DIR', BASE_DIR)


class AppSettings(BaseSettings):
    PROJECT_NAME: str  # set any name in '.env' file

    class Config:
        env_file = '.env'


app_settings = AppSettings()

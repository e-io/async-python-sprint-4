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

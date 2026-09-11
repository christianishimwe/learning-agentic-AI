import os
from pydantic_settings import BaseSettings

_ENV_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")


class Settings(BaseSettings):
    gemini_api_key: str
    max_chars: int = 10000
    model_config = {"env_file": _ENV_FILE, "ignore_extra": True}


settings = Settings()

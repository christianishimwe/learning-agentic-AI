from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    gemini_api_key: str
    max_chars: int
    model_config = {"env_file": ".env", "ignore_extra": True}


settings = Settings()

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):
    bot_token: SecretStr
    ollama_api: SecretStr
    model_ollama: SecretStr
    owner: SecretStr

    model_config = SettingsConfigDict(
        env_file="AIO-Natsuki/.env"
    )

config = Settings()
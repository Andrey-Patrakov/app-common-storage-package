from pydantic_settings import BaseSettings, SettingsConfigDict


class StorageSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='STORAGE_')

    URL: str
    BUCKET: str
    ACCESS_KEY: str
    SECRET_KEY: str
    SECURE: bool = False
    REGION_NAME: str = 'ru-moscow'
    CHUNK_SIZE: int = 524288


storage_settings = StorageSettings()

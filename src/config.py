from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal
import os


class Settings(BaseSettings):
    MODE: Literal['TEST', 'LOCAL', 'DEV', 'PROD']

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    REDIS_HOST: str
    REDIS_PORT: int


    @property
    def REDIS_URL(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(env_file=f"{os.path.dirname(os.path.abspath(__file__))}/../.env")
#     env_file = Path(__file__).parent.parent / ".env"


settings = Settings()

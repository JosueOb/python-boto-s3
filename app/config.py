from pydantic import BaseSettings


class Settings(BaseSettings):
    application_name: str = 'python_s3'
    environment: str = 'dev'
    facilities: list = []


config: Settings


def initialize() -> None:
    global config
    config = Settings()

from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    zp_app_key: str = ''

    class Config:
        env_file = '.env'


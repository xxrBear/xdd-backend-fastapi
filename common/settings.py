from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    zp_app_key: str = ''
    zp_call_num: int = 0

    class Config:
        env_file = '.env'

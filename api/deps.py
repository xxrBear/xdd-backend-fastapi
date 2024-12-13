""" 依赖设置
"""
from collections.abc import Generator
from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from core.settings import Settings
from init_db import engine


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]


@lru_cache
def get_settings():
    return Settings()


SettingsDep = Annotated[Settings, Depends(get_settings)]

""" 依赖设置
"""
from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from core.init_db import engine


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]

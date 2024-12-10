import json
import os

from sqlalchemy import text
from sqlalchemy.engine import reflection
from sqlalchemy.orm import Session
from sqlmodel import create_engine, SQLModel

from models import *
from sql.init_data import INIT_SQL

# 数据库文件的相对路径
# db_path = os.path.dirname(os.path.abspath(__file__)) + 'yudada-backend.db'
db_path = 'xdd-backend.db'

# 使用 SQLAlchemy 的 SQLite URL 格式
SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_path}"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)


# 初始化数据库表
def init_db_and_superuser():
    # 检查是否已经有表，避免重复创建
    inspector = reflection.Inspector.from_engine(engine)
    if 'user' not in inspector.get_table_names():  # 如果没有名为 'user' 的表
        SQLModel.metadata.create_all(bind=engine)

        import sqlite3

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        for sql in INIT_SQL.split(';'):
            try:
                cursor.execute(sql)
                conn.commit()
            except Exception as e:
                pass

        cursor.close()


if __name__ == '__main__':
    init_db_and_superuser()

from sqlalchemy.engine import reflection
from sqlmodel import create_engine, SQLModel

from models.user import User

engine = create_engine("sqlite:///./yudada.db", echo=True)


# 初始化数据库表
def init_db_and_superuser():
    # 检查是否已经有表，避免重复创建
    inspector = reflection.Inspector.from_engine(engine)
    if 'user' not in inspector.get_table_names():  # 如果没有名为 'user' 的表
        SQLModel.metadata.create_all(bind=engine)


if __name__ == '__main__':
    init_db_and_superuser()

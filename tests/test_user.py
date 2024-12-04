import pytest
from fastapi.testclient import TestClient
from sqlmodel import create_engine, SQLModel, Session

from main import app
from api.deps import get_db
from models import *

# 使用 SQLite 内存数据库
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///test.db"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})


# 测试专用的数据库依赖
@pytest.fixture(scope="function")
def test_db():
    SQLModel.metadata.create_all(engine)  # 初始化数据库
    with Session(engine) as session:
        yield session
    # SQLModel.metadata.drop_all(engine)  # 清除数据库


@pytest.fixture
def client(test_db):
    # 动态替换数据库依赖
    def override_get_session():
        yield test_db

    app.dependency_overrides[get_db] = override_get_session
    return TestClient(app)


# 测试用例：成功注册用户
def test_register_user_success(client):
    response = client.post("/api/user/register", json={
        "userAccount": "testuser",
        "userPassword": "admin123",
        "checkPassword": "admin123"
    })
    assert response.status_code == 200


# 测试用例：注册用户失败（密码不一致）
def test_register_user_password_mismatch(client):
    response = client.post("/api/user/register", json={
        "userAccount": "testuser",
        "userPassword": "admin123",
        "checkPassword": "wrongpassword"
    })
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["message"] == "两次输入的密码不一致"
    assert json_data["code"] == 40000


# 测试用例：注册用户失败（用户名已存在）
def test_register_user_exists(client):
    response = client.post("/api/user/register", json={
        "userAccount": "testuser",
        "userPassword": "admin123",
        "checkPassword": "admin123"
    })
    json_data = response.json()
    assert response.status_code == 200
    assert json_data["message"] == "用户已存在"
    assert json_data["code"] == 40000


SQLModel.metadata.drop_all(engine)  # 清除数据库

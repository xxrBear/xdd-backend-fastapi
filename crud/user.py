from sqlmodel import Session, select

from common.execptions import ValidateError
from core.utils import encrypt_user_password
from models.user import UserLogin, User, UserCreate


def validate_login_info(session: Session, user_in: UserLogin):
    """
    检查用户登录时的参数
    :param session:
    :param user_in:
    :return:
    """
    user_info = user_in.to_dict()
    user_account = user_info.get('user_account')
    user_password = user_info.get('user_password')

    encrypt_passwd = encrypt_user_password(user_password)
    statement = select(User).where(User.user_account == user_account).where(User.user_password == encrypt_passwd).where(
        User.is_delete == False)
    user_obj = session.exec(statement).first()
    if user_obj:
        return user_obj
    raise ValidateError('用户不存在或密码错误')


def validate_register_info(session: Session, user_create: UserCreate):
    """
    检查用户注册时的参数
    :param session:
    :param user_create:
    :return:
    """
    user_info = user_create.model_dump()
    user_account = user_info.get('userAccount')
    user_password = user_info.get('userPassword')
    check_password = user_info.get('checkPassword')

    if user_password != check_password:
        raise ValidateError('两次输入的密码不一致')

    statement = select(User).where(User.user_account == user_account)
    user_obj = session.exec(statement).first()
    if user_obj:
        raise ValidateError('用户已存在')

    encrypt_passwd = encrypt_user_password(user_password)
    user_dict = user_create.to_dict()
    user_dict.update(user_password=encrypt_passwd)

    user_obj = User(**user_dict)
    session.add(user_obj)
    session.commit()
    session.refresh(user_obj)

    return user_obj

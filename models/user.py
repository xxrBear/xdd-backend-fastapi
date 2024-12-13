from datetime import datetime

from fastapi.encoders import jsonable_encoder
from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    id: int = Field(index=True, primary_key=True, description='用户id')
    user_account: str = Field(..., max_length=32, description='账号')
    union_id: str = Field(default='', max_length=256, description='微信开放平台id', nullable=True)
    mp_open_id: str = Field(default='', max_length=256, description='公众号openId', nullable=True)
    user_name: str = Field(default='', max_length=32, description='用户昵称', nullable=True)
    user_avatar: str = Field(default='', max_length=64, description='用户头像', nullable=True)
    user_profile: str = Field(default='', max_length=512, description='用户简介', nullable=True)
    user_role: str = Field(default='user', max_length=32, description='用户角色：user/admin/ban')
    create_time: datetime = Field(default_factory=datetime.now, description='创建时间')
    update_time: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now},
                                  description='更新时间')
    is_delete: bool = Field(default=False, description='是否删除', nullable=True)


class User(UserBase, table=True):
    """ 用户表
    """
    user_password: str = Field(..., max_length=32, description='密码')

    def to_dict(self):
        field_dict = jsonable_encoder(self)

        return {
            'id': field_dict.get('id'),
            'userAccount': field_dict.get('user_account'),
            'unionId': field_dict.get('union_id'),
            'mpOpenId': field_dict.get('mp_open_id'),
            'userName': field_dict.get('user_name'),
            'userAvatar': field_dict.get('user_avatar'),
            'userProfile': field_dict.get('user_profile'),
            'userRole': field_dict.get('user_role'),
            'createTime': field_dict.get('create_time'),
            'updateTime': field_dict.get('update_time'),
            'isDelete': field_dict.get('is_delete')
        }


class UserCreate(SQLModel):
    userAccount: str = Field(min_length=4, max_length=32, description='账号')
    userPassword: str = Field(min_length=8, max_length=32, description='密码')
    checkPassword: str = Field(min_length=8, max_length=32, description='检验密码')

    def to_dict(self):
        return {
            'user_account': self.userAccount,
            'user_password': self.userPassword,
        }


class UserLogin(SQLModel):
    userAccount: str = Field(min_length=4, max_length=32, description='账号')
    userPassword: str = Field(min_length=8, max_length=32, description='密码')

    def to_dict(self):
        return {
            'user_account': self.userAccount,
            'user_password': self.userPassword,
        }


class UserPage(SQLModel):
    current: int = Field(default=1, description='开始页')
    pageSize: int = Field(default=10, description='总页数')
    userName: str = Field(default='', description='用户名')
    userDesc: str = Field(default='', description='用户描述')
    userProfile: str = Field(default='', description='')


class UserDelete(SQLModel):
    id: int = Field(description='用户id')

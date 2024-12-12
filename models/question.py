from email.policy import default

from fastapi.encoders import jsonable_encoder
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class Question(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, description="id")
    question_content: Optional[str] = Field(default='', description="题目内容（json格式）")
    app_id: int = Field(description="应用 id")
    user_id: int = Field(description="创建用户 id")
    create_time: datetime = Field(default=datetime.now, description="创建时间")
    update_time: datetime = Field(default=datetime.now, sa_column_kwargs={"onupdate": datetime.now},
                                  description="更新时间")
    is_delete: bool = Field(default=False, description="是否删除")

    def to_dict(self):
        fields = jsonable_encoder(self)
        return {
            "id": fields.get('id'),
            "appId": fields.get('app_id'),
            "userId": fields.get('user_id'),
            "createTime": fields.get('create_time'),
            "updateTime": fields.get('update_time'),
            "isDelete": fields.get('is_delete'),
            "questionContent": fields.get('question_content')
        }


class QuestionPub(SQLModel):
    appId:int|str = Field(default=0, description="APP ID")
    pageSize: int = Field(default=10, description="应用 id")
    userId: int|str = Field(default=0, description="userId")
    current: int = Field(default=1, description="创建用户 id")


class QuestionCreate(SQLModel):
    id: int = Field(description="id")
    questionContent: list = Field(default=[], description='问题')


class QuestionDel(SQLModel):
    id: int = Field(description="id")


class QuestionAI(SQLModel):
    appId: int = Field(description="APP ID")
    optionNumber: int = Field(description='选项数量')
    questionNumber: int = Field(description='题目数量')

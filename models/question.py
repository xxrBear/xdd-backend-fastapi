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
    is_delete: int = Field(default=0, description="是否删除")

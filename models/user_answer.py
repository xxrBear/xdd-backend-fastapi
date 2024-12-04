from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class UserAnswer(SQLModel, table=True):
    __tablename__ = "user_answer"

    id: int = Field(primary_key=True, description="id")
    app_id: int = Field(description="应用 id")
    app_type: int = Field(default=0, description="应用类型（0-得分类，1-角色测评类）")
    scoring_strategy: int = Field(default=0, nullable=False, description="评分策略（0-自定义，1-AI）")
    choices: Optional[str] = Field(default='', description="用户答案（JSON 数组）")
    result_id: Optional[int] = Field(default='', description="评分结果 id")
    result_name: Optional[str] = Field(default='', max_length=128, nullable=True, description="结果名称，如物流师")
    result_desc: Optional[str] = Field(default='', nullable=True, description="结果描述")
    result_picture: Optional[str] = Field(default='', max_length=1024, nullable=True, description="结果图标")
    result_score: Optional[int] = Field(default='', nullable=True, description="得分")
    user_id: int = Field(nullable=False, description="用户 id")
    create_time: datetime = Field(default=datetime.now, nullable=False, description="创建时间")
    update_time: datetime = Field(default=datetime.now, sa_column_kwargs={"onupdate": datetime.now},
                                  description="更新时间")
    is_delete: int = Field(default=0, nullable=False, description="是否删除")

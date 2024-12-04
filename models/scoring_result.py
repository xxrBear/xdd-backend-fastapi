from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class ScoringResult(SQLModel, table=True):
    __tablename__ = "scoring_result"

    id: Optional[int] = Field(primary_key=True, description="id")
    result_name: str = Field(max_length=128, nullable=False, description="结果名称，如物流师")
    result_desc: Optional[str] = Field(default='', nullable=True, description="结果描述")
    result_picture: Optional[str] = Field(default='', max_length=1024, nullable=True, description="结果图片")
    result_prop: Optional[str] = Field(default='', max_length=128,
                                       description="结果属性集合 JSON，如 [I,S,T,J]")
    result_score_range: Optional[int] = Field(default=0,
                                              description="结果得分范围，如 80，表示 80及以上的分数命中此结果")
    app_id: int = Field(description="应用 id")
    user_id: int = Field(description="创建用户 id")
    create_time: datetime = Field(default=datetime.now, description="创建时间")
    update_time: datetime = Field(default=datetime.now, sa_column_kwargs={"onupdate": datetime.now},
                                  description="更新时间")
    is_delete: int = Field(default=0, description="是否删除")

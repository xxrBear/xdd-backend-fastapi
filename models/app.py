from fastapi.encoders import jsonable_encoder
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class App(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, description="id")
    app_name: str = Field(max_length=128, description="应用名")
    app_desc: Optional[str] = Field(default='', max_length=2048, description="应用描述")
    app_icon: Optional[str] = Field(default='', max_length=1024, description="应用图标")
    app_type: int = Field(default=0, description="应用类型（0-得分类，1-测评类）")
    scoring_strategy: int = Field(default=0, description="评分策略（0-自定义，1-AI）")
    review_status: int = Field(default=0, description="审核状态：0-待审核, 1-通过, 2-拒绝")
    review_message: Optional[str] = Field(default='', max_length=512, description="审核信息")
    reviewer_id: Optional[int] = Field(description="审核人 id", nullable=True)
    review_time: Optional[datetime] | None = Field(default_factory=None, description="审核时间", nullable=True)
    user_id: int = Field(description="创建用户 id")
    create_time: datetime = Field(default_factory=datetime.now, description='创建时间')
    update_time: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now},
                                  description='更新时间')
    is_delete: int = Field(default=0, description="是否删除")

    def to_dict(self):
        field_dict = jsonable_encoder(self)
        return {
            "id": field_dict.get('id'),
            "appName": field_dict.get('app_name'),
            "appDesc": field_dict.get('app_desc'),
            "appIcon": field_dict.get('app_icon'),
            "appType": field_dict.get('app_type'),
            "scoringStrategy": field_dict.get('scoring_strategy'),
            "reviewStatus": field_dict.get('review_status'),
            "createTime": field_dict.get('create_time'),
            "updateTime": field_dict.get('update_time'),
            "reviewMessage": field_dict.get('review_message'),
            "reviewerId": field_dict.get('reviewer_id'),
            "reviewTime": field_dict.get('review_time'),
        }


class AppSelect(SQLModel):
    current: int = Field(default=1)
    pageSize: int = Field(default=12)
    reviewStatus: int = Field(default=1)
    appName: str = Field(default='')
    appDesc: str = Field(default='')


class AppCreate(SQLModel):
    appName: str = Field(default='', max_length=128, description="应用名")
    appDesc: Optional[str] = Field(default='', max_length=2048, description="应用描述")
    appIcon: Optional[str] = Field(default='', max_length=1024, description="应用图标")
    appType: int = Field(default=0, description="应用类型（0-得分类，1-测评类）")
    scoringStrategy: int = Field(default=0, description="评分策略（0-自定义，1-AI）")

    def to_dict(self):
        field_dict = jsonable_encoder(self)

        return {
            'app_name': field_dict.get('appName'),
            'app_desc': field_dict.get('appDesc'),
            'app_icon': field_dict.get('appIcon'),
            'app_type': field_dict.get('appType'),
            'scoring_strategy': field_dict.get('scoringStrategy')
        }


class AppDelete(SQLModel):
    id: int = Field(..., description="应用ID")


class AppReview(SQLModel):
    id: int = Field(description="应用ID")
    reviewStatus: int = Field(default=1, description='审核状态')
    reviewMessage: str = Field(default='', description='审核信息')

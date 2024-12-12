import json
from datetime import datetime
from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlmodel import SQLModel, Field


class ScoringResult(SQLModel, table=True):
    __tablename__ = "scoring_result"

    id: Optional[int] = Field(primary_key=True, description="id")
    result_name: str = Field(max_length=128, nullable=False, description="结果名称，如物流师")
    result_desc: Optional[str] = Field(default='', nullable=True, description="结果描述")
    result_picture: Optional[str] = Field(default='', max_length=1024, nullable=True, description="结果图片")
    result_prop: Optional[str] = Field(default='', max_length=128, description="结果属性集合 JSON，如 [I,S,T,J]")
    result_score_range: Optional[int] = Field(default=0, description="结果得分范围，如 80，表示 80及以上的分数命中此结果")
    app_id: int = Field(description="应用 id")
    user_id: int = Field(description="创建用户 id")
    create_time: datetime = Field(default_factory=datetime.now, description="创建时间")
    update_time: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now},
                                  description="更新时间")
    is_delete: int = Field(default=0, description="是否删除")

    def to_dict(self):
        fields = jsonable_encoder(self)
        rp = fields.get('result_prop')
        return {
            'id': fields.get('id'),
            'resultName': fields.get('result_name'),
            'resultDesc': fields.get('result_desc'),
            'resultPicture': fields.get('result_picture'),
            'resultProp': json.loads(rp) if rp else None,
            'resultScoreRange': fields.get('result_score_range'),
            'appId': fields.get('app_id'),
            'userId': fields.get('user_id'),
            'createTime': fields.get('create_time'),
            'updateTime': fields.get('update_time'),
            'isDelete': fields.get('is_delete')
        }


class SRIn(SQLModel):
    current: int = Field(description='开始页')
    pageSize: int = Field(description='结束页')
    resultName: str = Field(default='', description='名称')
    resultDesc: str = Field(default='', description='用户描述')
    appId: int | str = Field(default=0, description='APP ID')
    userId: int | str = Field(default=0, description='User ID')
    sortField: str | None = Field(default='id', description='排序字段')
    sortOrder: str | None = Field(default='', description='排序')


class SREdit(SQLModel):
    id: int | None = Field(description='id')
    resultName: str | None = Field(default=None, description='结果名')
    resultDesc: str | None = Field(default=None, description='结果描述')
    resultPicture: str | None = Field(default=None, description='图片')
    resultProp: list = Field(default=[], max_length=128, description="结果属性集合 JSON，如 [I,S,T,J]")
    resultScoreRange: str | None = Field(default=None, description='结果分')
    appId: int | None = Field(default=None, description='APP ID')
    userId: int | None = Field(default=None, description='用户 ID')
    createTime: datetime = Field(default=datetime.now, description="创建时间")
    updateTime: datetime = Field(default=datetime.now, sa_column_kwargs={"onupdate": datetime.now},
                                 description="更新时间")
    isDelete: int | None = Field(default=0, description='是否删除')

    def to_dict(self):
        fields = jsonable_encoder(self)
        return {
            'id': fields.get('id'),
            'result_name': fields.get('resultName'),
            'result_desc': fields.get('resultDesc'),
            'result_picture': fields.get('resultPicture'),
            'result_prop': fields.get('resultProp'),
            'result_score_range': fields.get('resultScoreRange'),
            'app_id': fields.get('appId'),
            'user_id': fields.get('userId'),
            'is_delete': fields.get('isDelete'),
        }


class SRDelete(SQLModel):
    id: int | None = Field(description='id')
    resultName: str | None = Field(default=None, description='结果名')
    resultDesc: str | None = Field(default=None, description='结果描述')
    resultPicture: str | None = Field(default=None, description='图片')
    resultProp: list = Field(default=[], max_length=128, description="结果属性集合 JSON，如 [I,S,T,J]")
    resultScoreRange: str | None = Field(default=None, description='结果分')
    appId: int | None = Field(default=None, description='APP ID')
    userId: int | None = Field(default=None, description='用户 ID')
    createTime: datetime = Field(default=datetime.now, description="创建时间")
    updateTime: datetime = Field(default=datetime.now, sa_column_kwargs={"onupdate": datetime.now},
                                 description="更新时间")
    isDelete: int | None = Field(default=0, description='是否删除')

    def to_dict(self):
        fields = jsonable_encoder(self)
        return {
            'id': fields.get('id'),
            'result_name': fields.get('resultName'),
            'result_desc': fields.get('resultDesc'),
            'result_picture': fields.get('resultPicture'),
            'result_prop': fields.get('resultProp'),
            'result_score_range': fields.get('resultScoreRange'),
            'app_id': fields.get('appId'),
            'user_id': fields.get('userId'),
            'is_delete': fields.get('isDelete'),
        }


class SRCreate(SQLModel):
    appId: int | None = Field(default=None, description='APP ID')
    resultDesc: str = Field(default='', description='答题描述')
    resultName: str = Field(description='答题结果名称')
    resultPicture: Optional[str] = Field(default='', max_length=1024, nullable=True, description="结果图片")
    resultProp: list | None = Field(default=None, max_length=128, description="结果属性集合 JSON，如 [I,S,T,J]")
    resultScoreRange: int = Field(default=0, description='结果得分范围，如 80，表示 80及以上的分数命中此结果')

    def to_dict(self):
        fields = jsonable_encoder(self)
        return {
            'app_id': fields.get('appId'),
            'result_desc': fields.get('resultDesc'),
            'result_picture': fields.get('resultPicture'),
            'result_prop': json.dumps(fields.get('resultProp')),
            'result_score_range': fields.get('resultScoreRange'),
            'result_name': fields.get('resultName'),
        }

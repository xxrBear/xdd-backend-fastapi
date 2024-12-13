import json
import math

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from sqlmodel import select, update
from starlette.requests import Request

from api.deps import SessionDep
from common.resp import json_data
from models import ScoringResult
from models.scoring_result import SRIn, SREdit, SRDelete, SRCreate

router = APIRouter()


@router.post('/list/page')
async def get_scoring_result(session: SessionDep, sr_in: SRIn):
    """
    获取所有得分结果
    :param session:
    :param sr_in:
    :return:
    """
    sql = select(ScoringResult).where(ScoringResult.is_delete == 0)

    if sr_in.resultName:
        like_sql = '%{}%'.format(sr_in.resultName)
        sql = sql.where(ScoringResult.result_name.like(like_sql))
    if sr_in.resultDesc:
        like_sql = '%{}%'.format(sr_in.resultDesc)
        sql = sql.where(ScoringResult.result_desc.like(like_sql))
    if sr_in.appId:
        sql = sql.where(ScoringResult.app_id == sr_in.appId)
    if sr_in.userId:
        sql = sql.where(ScoringResult.user_id == sr_in.userId)

    sr_objs = session.exec(sql).all()
    result_list = []
    for sr in sr_objs:
        result_list.append(sr.to_dict())

    total = len(sr_objs)
    pages = math.ceil(total / sr_in.pageSize)
    size = sr_in.pageSize

    return json_data(data={'records': result_list, 'total': total, 'pages': pages, 'size': size})


@router.post('/list/page/vo')
async def get_scoring_result(session: SessionDep, sr_in: SRIn):
    """
    获取所有得分结果
    :param session:
    :param sr_in:
    :return:
    """
    sql = select(ScoringResult).where(ScoringResult.is_delete == 0)

    if sr_in.resultName:
        like_sql = '%{}%'.format(sr_in.resultName)
        sql = sql.where(ScoringResult.result_name.like(like_sql))
    if sr_in.resultDesc:
        like_sql = '%{}%'.format(sr_in.resultDesc)
        sql = sql.where(ScoringResult.result_desc.like(like_sql))
    if sr_in.appId:
        sql = sql.where(ScoringResult.app_id == sr_in.appId)
    if sr_in.userId:
        sql = sql.where(ScoringResult.user_id == sr_in.userId)

    sr_objs = session.exec(sql).all()
    result_list = []
    for sr in sr_objs:
        result_list.append(sr.to_dict())

    total = len(sr_objs)
    pages = math.ceil(total / sr_in.pageSize)
    size = sr_in.pageSize

    return json_data(data={'records': result_list, 'total': total, 'pages': pages, 'size': size})


@router.post('/edit')
async def edit_scoring_result(session: SessionDep, sr_edit: SREdit):
    # validate_sr_edit_info(sr_edit)

    sr_dict = jsonable_encoder(sr_edit.to_dict())
    result_prop = json.dumps(sr_edit.resultProp)
    sr_dict.update({'result_prop': result_prop})

    sr_id = sr_dict.get('id')
    sql = update(ScoringResult).where(ScoringResult.id == sr_id)
    session.exec(sql.values(**sr_dict))
    session.commit()

    return json_data()


@router.post('/delete')
async def delete_scoring_result(session: SessionDep, sr_del: SRDelete):
    # validate_sr_edit_info(sr_edit)

    id_ = sr_del.id
    sql = select(ScoringResult).where(ScoringResult.id == id_)
    sr_obj = session.exec(sql).one_or_none()
    if sr_obj:
        sr_obj.is_delete = 1
        session.commit()
        session.refresh(sr_obj)

    return json_data(data='删除成功')


@router.post('/add')
async def add_scoring_result(session: SessionDep, request: Request, sr_create: SRCreate):
    # validate_sr_edit_info(sr_edit)
    sr_dict = sr_create.to_dict()
    sr_dict.update({'user_id': request.session.get('user_login_state').get('id')})

    sr_obj = ScoringResult(**sr_dict)
    session.add(sr_obj)
    session.commit()
    session.refresh(sr_obj)

    return json_data(data='添加成功')

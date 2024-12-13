from fastapi import APIRouter
from sqlalchemy import text
from starlette.requests import Request

from api.deps import SessionDep
from common.resp import json_data
from core.utils import adapter_records_info
from crud.app import check_app_info, create_app, get_app_detail, get_passed_app, get_all_app, delete_app_by_id, \
    review_app_by_id
from models.app import AppCreate, AppDelete, AppReview, AppSelect

router = APIRouter()


@router.post('/list/page/vo')
async def get_app_page(session: SessionDep, se: AppSelect):
    """
    获取所有 "已过审" "未删除" APP 供预览
    :param session:
    :param page_info:
    :return:
    """
    records = get_passed_app(session, se)
    data = adapter_records_info(records, se.pageSize)
    data.update({'records': records})
    return json_data(data=data)


@router.post('/list/page')
async def get_list_page(session: SessionDep, se: AppSelect):
    """
    获取所有 APP
    :param session:
    :param page_info:
    :return:
    """
    records = get_all_app(session, se)
    data = adapter_records_info(records, se.pageSize)
    data.update({'records': records})
    return json_data(data=data)


@router.post('/add')
async def add_app(session: SessionDep, request: Request, app_in: AppCreate):
    """
    添加 APP
    :param session:
    :param request:
    :param app_in:
    :return:
    """
    check_app_info(app_in)
    app_obj = create_app(session, request, app_in)
    return json_data(data=app_obj.id)


@router.post('/delete')
async def delete_app(session: SessionDep, app_del: AppDelete):
    """
    删除 APP
    :param session:
    :param app_del:
    :return:
    """
    delete_app_by_id(session, app_del)
    return json_data(message='删除成功')


@router.post('/review')
async def review_app(session: SessionDep, request: Request, app_review: AppReview):
    """
    :param session:
    :param request:
    :param app_review:
    :return:
    """
    review_app_by_id(session, request, app_review)
    return json_data(message='审核成功')


@router.get('/get/vo')
async def get_app_detail_by_id(id: int, session: SessionDep, request: Request):
    """
    查看单一 APP 详情
    :param id:
    :param session:
    :param request:
    :return:
    """
    app_detail = get_app_detail(id, session, request)
    return json_data(data=app_detail)


@router.get('/statistic/answer_count')
async def answer_count(session: SessionDep):
    """
    删除答案
    :param session:
    :param user_del:
    :return:
    """
    sql = """
        select app_id appId, count(user_id) as answerCount from user_answer
        group by app_id order by answerCount desc limit 10;
    """
    result = session.execute(text(sql))
    data = []
    if result:
        data = [{'appId': i.appId, 'answerCount': i.answerCount} for i in result]
    return json_data(data=data)


@router.get('/statistic/answer_result_count')
async def answer_count(appId: int, session: SessionDep):
    """
    删除答案
    :param appId:
    :param session:
    :return:
    """
    data = []

    if appId:
        sql = """
            select result_name resultName, count(user_id) as resultCount from user_answer where app_id = {}
            group by resultName order by resultCount desc;
        """.format(appId)
        result = session.execute(text(sql))
        if result:
            data = [{'resultName': i.resultName, 'resultCount': i.resultCount} for i in result]
    return json_data(data=data)

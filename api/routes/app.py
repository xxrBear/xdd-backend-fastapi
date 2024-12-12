from fastapi import APIRouter
from starlette.requests import Request

from api.deps import SessionDep
from common.resp import json_data
from core.utils import adapter_records_info
from crud.app import check_app_info, create_app, get_app_detail, get_passed_app, get_all_app, delete_app_by_id, \
    review_app_by_id
from models.app import AppCreate, AppDelete, AppReview, AppSelect

router = APIRouter()


@router.post('/list/page/vo')
def get_app_page(session: SessionDep, se: AppSelect):
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
def get_list_page(session: SessionDep, se: AppSelect):
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
def add_app(session: SessionDep, request: Request, app_in: AppCreate):
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
def delete_app(session: SessionDep, app_del: AppDelete):
    """
    删除 APP
    :param session:
    :param app_del:
    :return:
    """
    delete_app_by_id(session, app_del)
    return json_data(message='删除成功')


@router.post('/review')
def review_app(session: SessionDep, request: Request, app_review: AppReview):
    """
    :param session:
    :param request:
    :param app_review:
    :return:
    """
    review_app_by_id(session, request, app_review)
    return json_data(message='审核成功')


@router.get('/get/vo')
def get_app_detail_by_id(id: int, session: SessionDep, request: Request):
    """
    查看单一 APP 详情
    :param id:
    :param session:
    :param request:
    :return:
    """
    app_detail = get_app_detail(id, session, request)
    return json_data(data=app_detail)

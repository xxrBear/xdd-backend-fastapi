from fastapi import APIRouter, Request
from sqlmodel import select

from api.deps import SessionDep
from common.resp import json_data
from core.score import PickScoreType
from core.utils import generate_id, adapter_records_info
from crud.answer import validate_answer_in, create_user_answer
from models import UserAnswer
from models.user_answer import UserAnswerIn, UserAnswerDelete, UserAnswerSelect

router = APIRouter()


@router.get('/generate/id')
async def generate_answer_id():
    """
    自动生成 用户答案 ID
    :return:
    """
    id_ = generate_id()
    return json_data(data=id_)


@router.post('/add')
async def add_user_answer(session: SessionDep, request: Request, answer_in: UserAnswerIn):
    """
    添加用户答案
    :param session:
    :param request:
    :param answer_in:
    :return:
    """
    # 参数检验
    validate_answer_in(answer_in, session)

    # 添加用户答题记录
    answer_obj, app_obj = create_user_answer(session, request, answer_in)

    # 根据不同策略打分
    score_obj = PickScoreType(score_type=app_obj.app_type, scoring_strategy=app_obj.scoring_strategy).choose
    answer_obj_id = score_obj.do_score(app_obj, answer_obj, session)

    return json_data(data=answer_obj_id)


@router.get('/get/vo')
async def get_each_answer(id: int, session: SessionDep, request: Request):
    """
    展示一个答案
    :param session:
    :param id:
    :param request:
    :return:
    """
    sql = select(UserAnswer).where(UserAnswer.is_delete == False).where(UserAnswer.id == id)
    answer_obj = session.exec(sql).first()
    answer_dict = answer_obj.to_dict()

    user_pub = request.session.get('user_login_state')
    answer_dict.update({'user': user_pub})

    return json_data(data=answer_dict)


@router.post('/list/page')
async def get_all_answer_list(session: SessionDep, se: UserAnswerSelect):
    """
    展示所有答案
    :param session:
    :return:
    """
    sql = select(UserAnswer).where(UserAnswer.is_delete == False)
    if se.appId:
        sql = sql.where(UserAnswer.app_id == se.appId)
    if se.resultDesc:
        sql = sql.where(UserAnswer.result_desc.like('%{}%'.format(se.resultDesc)))
    if se.resultName:
        sql = sql.where(UserAnswer.result_name.like('%{}%'.format(se.resultName)))
    if se.userId:
        sql = sql.where(UserAnswer.user_id == se.userId)

    answer_objs = session.exec(sql).all()
    result_list = []
    for answer_obj in answer_objs:
        result_list.append(answer_obj.to_dict())
    data = adapter_records_info(answer_objs, 10)
    data['records'] = result_list
    return json_data(data=data)


@router.post('/my/list/page/vo')
async def get_mine_answer_list(session: SessionDep, request: Request, se: UserAnswerSelect):
    user_pub = request.session.get('user_login_state')
    sql = select(UserAnswer).where(UserAnswer.is_delete == False).where(UserAnswer.user_id == user_pub.get('id'))

    if se.appId:
        sql = sql.where(UserAnswer.app_id == se.appId)
    if se.resultDesc:
        sql = sql.where(UserAnswer.result_desc.like('%{}%'.format(se.resultDesc)))
    if se.resultName:
        sql = sql.where(UserAnswer.result_name.like('%{}%'.format(se.resultName)))

    answer_objs = session.exec(sql).all()
    result_list = []
    for answer_obj in answer_objs:
        result_list.append(answer_obj.to_dict())
    data = adapter_records_info(answer_objs, se.pageSize)
    data['records'] = result_list
    return json_data(data=data)


@router.post('/delete')
async def delete_user_answer(session: SessionDep, user_del: UserAnswerDelete):
    """
    删除答案
    :param session:
    :param user_del:
    :return:
    """
    id_ = user_del.id
    sql = select(UserAnswer).where(UserAnswer.id == id_)
    answer_obj = session.exec(sql).first()
    if answer_obj:
        answer_obj.is_delete = True
        session.commit()
        session.refresh(answer_obj)
    return json_data(data='删除成功')

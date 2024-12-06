import json

from fastapi import APIRouter
from sqlmodel import select
from starlette.requests import Request

from api.deps import SessionDep
from common.resp import json_data
from models import Question, App
from models.question import QuestionPub, QuestionCreate, QuestionDel

router = APIRouter()


@router.post("/list/page/vo")
async def get_question_list(session: SessionDep, ques_pub: QuestionPub):
    """
    显示自己的 APP 题目
    :param session:
    :param request:
    :param ques_pub:
    :return:
    """
    Q = Question
    # 查看题目
    sql = select(Q).where(Q.app_id == ques_pub.appId).where(Q.is_delete == False)
    question_objs = session.exec(sql).all()

    # 封装返回结果
    records = []
    for que in question_objs:
        content = json.loads(que.question_content)
        questionContent = content
        que_dict = {'questionContent': questionContent}

        app_id = que.app_id
        app_sql = select(App).where(App.id == app_id)
        app_obj = session.exec(app_sql).first()
        app_dict = app_obj.to_dict()
        app_dict.update(que_dict)

        records.append(app_dict)

    return json_data(data={'records': records})


@router.post("/edit")
async def create_question(session: SessionDep, request: Request, ques_create: QuestionCreate):
    """
    修改题目
    :param session:
    :param request:
    :param ques_create:
    :return:
    """
    app_id = ques_create.id

    sql = select(Question).where(Question.app_id == app_id)
    q_obj = session.exec(sql).first()
    if q_obj:
        q_obj.question_content = json.dumps(ques_create.questionContent)
        session.commit()
        session.refresh(q_obj)
    else:
        q_dict = {'user_id': request.session.get('user_login_state').get('id'), 'app_id': app_id,
                  'question_content': json.dumps(ques_create.questionContent)}
        q_obj = Question(**q_dict)
        session.add(q_obj)
        session.commit()
        session.refresh(q_obj)

    return json_data()


@router.post("/list/page")
async def list_question(session: SessionDep):
    """
    展示题目
    :param session:
    :param request:
    :param ques_pub:
    :return:
    """
    Q = Question
    # 查看题目
    sql = select(Q).where(Q.is_delete == False)
    question_objs = session.exec(sql).all()

    # 封装返回结果
    records = []
    for que in question_objs:
        records.append(que.to_dict())

    return json_data(data={'records': records})


@router.post("/delete")
async def delete_question(session: SessionDep, q_del: QuestionDel):
    """
    逻辑删除题目
    :param session:
    :param q_del:
    :return:
    """
    qid = q_del.id

    sql = select(Question).where(Question.id == qid)
    q_obj = session.exec(sql).first()
    if q_obj:
        q_obj.is_delete = True
        session.commit()
        session.refresh(q_obj)

    return json_data()

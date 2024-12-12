import json
import re

from fastapi import APIRouter
from sqlmodel import select
from sse_starlette import EventSourceResponse
from starlette.requests import Request

from api.deps import SessionDep, SettingsDep
from common import prompt
from common.prompt import USER_OUT_PROMPT
from common.resp import json_data
from core.ai import send_sync_ai_message, send_sse_ai_message
from crud.question import adapter_user_prompt
from models import Question, App
from models.question import QuestionPub, QuestionCreate, QuestionDel, QuestionAI

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


@router.post("/ai_generate")
async def ai_generate_question(session: SessionDep, q_ai: QuestionAI):
    """
    AI 自动生成题目
    :param session:
    :param q_ai:
    :return:
    """
    user_prompt = adapter_user_prompt(session, q_ai)
    system_prompt = prompt.SYSTEM_OUT_PROMPT

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    resp = send_sync_ai_message(messages)

    # 正则表达式匹配最外层的 JSON 数组
    json_pattern = r"\[(.*)\]"  # 捕获最外层的 [ 和 ]，并提取内容

    # 搜索最外层的 JSON 数组
    match = re.search(json_pattern, resp, re.DOTALL)

    if match:
        data = json.loads(match.group())  # 提取匹配到的完整 JSON 数据
    else:
        data = []
    return json_data(data=data)


@router.get("/ai_generate/sse")
async def ai_generate_sse(appId: int, optionNumber: int, questionNumber: int, session: SessionDep, settings: SettingsDep):

    if settings.zp_call_num >= 50:
        settings.zp_call_num += 1
        return json_data(message='AI使用次数超过上限')

    sql = select(App).where(App.id == appId)
    app_obj = session.exec(sql).first()

    user_prompt = USER_OUT_PROMPT.format(app_obj.app_name, app_obj.app_desc, questionNumber, optionNumber)
    system_prompt = prompt.SYSTEM_OUT_PROMPT
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    resp = send_sse_ai_message(messages)

    data = ''
    count = 0

    async def event_generator(resp):

        while True:
            nonlocal data, count

            for first in resp:
                value = first.choices[0].delta.content.replace(' ', '').replace('\n', '')
                for second in value:
                    if second == '{':
                        count += 1
                    if count > 0:
                        data += second
                    if second == '}':
                        count -= 1
                    if count == 0 and data:
                        # 当JSON结构完整时，发送数据块
                        yield data  # SSE 格式
                        data = ''  # 重置数据
                        count = 0
            break
        yield "Stream completed"

    return EventSourceResponse(event_generator(resp))

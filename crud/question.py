from sqlmodel import select

from api.deps import SessionDep
from common import prompt
from models import App
from models.question import QuestionAI


def adapter_user_prompt(session: SessionDep, q_ai: QuestionAI):
    """
    拼装用户 prompt
    :param session:
    :param q_ai:
    :return:
    """
    app_id = q_ai.appId
    sql = select(App).where(App.id == app_id)
    app_obj = session.exec(sql).first()

    user_prompt = prompt.USER_OUT_PROMPT.format(app_obj.app_name, app_obj.app_desc, q_ai.questionNumber, q_ai.optionNumber)
    return user_prompt

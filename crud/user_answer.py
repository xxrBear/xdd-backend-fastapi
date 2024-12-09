from sqlmodel import select

from api.deps import SessionDep
from common.execptions import ValidateError
from models import UserAnswer, App
from models.user_answer import UserAnswerIn


def validate_answer_in(user_answer: UserAnswerIn, session: SessionDep):
    id_ = user_answer.id
    choices = user_answer.choices
    app_id = user_answer.appId

    sql = select(UserAnswer).where(UserAnswer.id == id_)
    answer_obj = session.exec(sql).first()
    if id_ <= 0 or answer_obj:
        raise ValidateError('参数异常')

    sql2 = select(App).where(App.id == app_id)
    app_obj = session.exec(sql2).first()
    if not app_obj:
        raise ValidateError('参数异常')

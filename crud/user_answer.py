from sqlmodel import select

from api.deps import SessionDep
from common.execptions import validate_request_exception
from models import UserAnswer, App
from models.user_answer import UserAnswerIn


def validate_answer_in(user_answer: UserAnswerIn, session: SessionDep):
    id_ = user_answer.id
    app_id = user_answer.appId

    sql = select(UserAnswer).where(UserAnswer.id == id_)
    answer_obj = session.exec(sql).first()
    validate_request_exception(id_ <= 0 or answer_obj, 'UserAnswer ID 非法')

    sql2 = select(App).where(App.id == app_id)
    app_obj = session.exec(sql2).first()
    validate_request_exception(not app_obj, 'APP ID 非法')

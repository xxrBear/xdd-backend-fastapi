"""
打分模块
"""
import json
import re
from collections import defaultdict

from sqlmodel import select

from api.deps import SessionDep
from common.prompt import USER_SCORE_PROMPT, SYSTEM_SCORE_PROMPT
from core.ai import send_sync_ai_message
from models import Question, ScoringResult


class PickScoreType:
    def __init__(self, score_type: int, scoring_strategy: int):
        self.score_type = score_type
        self.scoring_strategy = scoring_strategy

    @property
    def choose(self):
        if self.score_type == 1 and self.scoring_strategy == 0:
            return CustomerTestScore('自定义测评类')
        elif self.score_type == 0 and self.scoring_strategy == 0:
            return CustomScore('自定义得分类')
        elif self.score_type == 1 and self.scoring_strategy == 1:
            return AICustomerTestScore('AI测评类')
        else:
            raise RuntimeError('未定义的策略')


class AICustomerTestScore:
    """
    AI 自定义测评类
    """

    def __init__(self, name: str):
        self.name = name

    @staticmethod
    def do_score(app_obj, answer_obj, session: SessionDep):

        # 1. 根据 app_id 查询题目和对应的答案
        que_sql = select(Question).where(Question.app_id == app_obj.id).where(Question.is_delete == False)
        question_obj = session.exec(que_sql).first()
        answer_list = json.loads(answer_obj.choices)

        question_content = json.loads(question_obj.question_content)
        result_list = []
        for _i, answer in enumerate(answer_list):
            title = question_content[_i]['title']
            for a_ in question_content[_i]['options']:
                if a_.get('key') == answer:
                    result_list.append({'title': title, 'answer': a_['value']})

        user_score_prompt = USER_SCORE_PROMPT.format(app_obj.app_name, app_obj.app_desc, result_list)

        messages = [
            {"role": "system", "content": SYSTEM_SCORE_PROMPT},
            {"role": "user", "content": user_score_prompt},
        ]
        resp = send_sync_ai_message(messages)
        print(resp)
        # 正则表达式匹配最外层的 JSON 数组
        json_pattern = r"\{(.*)\}"  # 捕获最外层的 { 和 }，并提取内容

        # 搜索最外层的 JSON 数组
        match = re.search(json_pattern, resp, re.DOTALL)

        if match:
            data = json.loads(match.group())  # 提取匹配到的完整 JSON 数据

            answer_obj.result_name = data.get('resultName')
            answer_obj.result_desc = data.get('resultDesc')
            session.commit()
            session.refresh(answer_obj)

        return answer_obj.id


class CustomerTestScore:
    """
    自定义测评类
    """

    def __init__(self, name: str):
        self.name = name

    @staticmethod
    def do_score(app_obj, answer_obj, session: SessionDep):

        # 1. 根据 app_id 查询题目和结果信息
        que_sql = select(Question).where(Question.app_id == app_obj.id).where(Question.is_delete == False)
        question_obj = session.exec(que_sql).first()
        answer_list = json.loads(answer_obj.choices)

        sr_sql = select(ScoringResult).where(ScoringResult.app_id == app_obj.id).where(ScoringResult.is_delete == 0)
        scoring_result_list = session.exec(sr_sql).all()

        # 2. 统计用户每个选择对应的属性个数，如 I = 10 个，E = 5 个
        option_count = defaultdict(int)
        question_content = json.loads(question_obj.question_content)
        for question_content_item in question_content:
            for answer in answer_list:
                for option in question_content_item['options']:
                    if option.get('key', '') == answer:
                        result = option.get('result')
                        option_count[result] += 1

        # 3. 遍历评分结果，计算哪个结果得分更高
        max_score = 0
        max_scoring_result = scoring_result_list[0]

        for scoring_result in scoring_result_list:
            result_props = scoring_result.result_prop  # 假设是 JSON 格式的字段
            score = sum(option_count.get(prop, 0) for prop in result_props)

            if score > max_score:
                max_score = score
                max_scoring_result = scoring_result

        answer_obj.result_id = max_scoring_result.id
        answer_obj.result_name = max_scoring_result.result_name
        answer_obj.result_desc = max_scoring_result.result_desc
        answer_obj.result_picture = max_scoring_result.result_picture
        session.commit()
        session.refresh(answer_obj)

        return answer_obj.id


class CustomScore:
    """
    自定义得分类
    """

    def __init__(self, name: str):
        self.name = name

    @staticmethod
    def do_score(app_obj, answer_obj, session: SessionDep):

        # 查出所有题目，计算总得分
        que_sql = select(Question).where(Question.app_id == app_obj.id).where(Question.is_delete == False)
        question_obj = session.exec(que_sql).first()
        answer_list = json.loads(answer_obj.choices)
        question_content = json.loads(question_obj.question_content)

        total_score = 0
        for question_content_item in question_content:
            for answer in answer_list:
                for option in question_content_item['options']:
                    if option.get('key', '') == answer:
                        total_score += option.get('score', 0)

        # 遍历所有得分，找到得分最接近的结果
        sr_sql = select(ScoringResult).where(ScoringResult.app_id == app_obj.id).where(ScoringResult.is_delete == 0)
        scoring_result_list = session.exec(sr_sql).all()

        max_scoring_result = scoring_result_list[0]
        for scoring_result in scoring_result_list:
            score = scoring_result.result_score_range  # 假设是 JSON 格式的字段

            if total_score > score:
                max_scoring_result = scoring_result

        answer_obj.result_id = max_scoring_result.id
        answer_obj.result_name = max_scoring_result.result_name
        answer_obj.result_desc = max_scoring_result.result_desc
        answer_obj.result_picture = max_scoring_result.result_picture
        session.commit()
        session.refresh(answer_obj)

        # 返回结果
        return answer_obj.id

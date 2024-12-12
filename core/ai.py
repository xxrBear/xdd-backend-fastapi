from zhipuai import ZhipuAI

from api.deps import SettingsDep


def create_ai_client(settings: SettingsDep):
    client = ZhipuAI(api_key=settings.zp_app_key)  # 填写您自己的APIKey
    return client


def send_sync_ai_message(messages, settings: SettingsDep = SettingsDep()):
    ai_client = create_ai_client(settings)

    response = ai_client.chat.completions.create(
        model="glm-4-0520",  # 填写需要调用的模型编码
        messages=messages,
    )
    return response.choices[0].message.content


def send_sse_ai_message(messages, settings: SettingsDep = SettingsDep()):
    ai_client = create_ai_client(settings)

    response = ai_client.chat.completions.create(
        model="glm-4-0520",  # 填写需要调用的模型编码
        messages=messages,
        stream=True,
    )
    return response

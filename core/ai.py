from zhipuai import ZhipuAI


def create_ai_client():
    client = ZhipuAI(api_key="xxx")  # 填写您自己的APIKey
    return client


def send_sync_ai_message(messages):
    ai_client = create_ai_client()

    response = ai_client.chat.completions.create(
        model="glm-4-0520",  # 填写需要调用的模型编码
        messages=messages,
    )
    return response.choices[0].message.content

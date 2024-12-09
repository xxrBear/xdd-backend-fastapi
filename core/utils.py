import hashlib
import time


def generate_id():
    """
    生成增长的 id
    :return:
    """
    id_ = int(time.time())
    return id_


def encrypt_user_password(password: str) -> str:
    encrypt_password = hashlib.sha256(password.encode()).hexdigest()
    return encrypt_password

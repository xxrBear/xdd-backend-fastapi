import hashlib


def encrypt_user_password(password: str) -> str:
    encrypt_password = hashlib.sha256(password.encode()).hexdigest()
    return encrypt_password

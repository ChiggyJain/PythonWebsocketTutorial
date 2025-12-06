import jwt
from jwt import InvalidTokenError

SECRET_KEY = "MY_SUPER_SECRET_KEY"


def authenticate(token: str):
    if not token:
        raise ValueError("Missing token")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except InvalidTokenError:
        raise ValueError("Invalid token")

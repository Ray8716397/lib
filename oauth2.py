# coding=utf-8
# @CREATE_TIME: 2021/7/15 下午5:14
# @LAST_MODIFIED: 2021/7/15 下午5:14
# @FILE: oauth.py
# @AUTHOR: Ray
from tornado.web import HTTPError
from functools import wraps
import jwt
# from werkzeug.security import gen_salt
# client_id = gen_salt(24)
# client_secret = gen_salt(48)
# print(client_id)
# print(client_secret)

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"


def require_oauth(required_scope):
    @wraps(required_scope)
    def decorator(method):
        @wraps(method)
        async def wrapper(self, *args, **kwargs):
            access_token = self.get_argument('access_token', None)
            if access_token:
                try:
                    payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
                    scope: str = payload.get("scope")
                    if scope != required_scope:
                        raise HTTPError(401, "Not authenticated")
                    else:
                        return await method(self, *args, **kwargs)
                except jwt.ExpiredSignatureError:
                    raise HTTPError(401, "Token expired")
                except Exception:
                    raise HTTPError(401, "Could not validate credentials")

            else:
                raise HTTPError(401, "Not authenticated")

        return wrapper

    return decorator


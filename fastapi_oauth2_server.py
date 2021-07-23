from datetime import datetime, timedelta
from typing import Optional

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status, Form, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 1

fake_users_db = {
    "O1GuQ6hfBysRb3nQLjv3mkQF": {
        "scope": "api",
        "client_id": 'O1GuQ6hfBysRb3nQLjv3mkQF',
        "client_secret": '30j7UaUOZDskYA5hJINMnBm1z4eUKN5iNxrfq07tKOowyt13',
        "disabled": False,
    }
}

app = FastAPI()


class Token(BaseModel):
    access_token: str


class TokenParam(BaseModel):
    client_id: str
    client_secret: str
    grant_type: Optional[str] = 'client_credentials'


@app.post("/token", response_model=Token)
async def token(client_id=Form(...), client_secret=Form(...), grant_type=Form(...)):
    if client_id in fake_users_db.keys() and fake_users_db[client_id]['client_secret'] == client_secret:
        to_encode = {"scope": fake_users_db[client_id]['scope'], "exp": datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)}
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return {"access_token": encoded_jwt}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect client_id or client_secret",
            headers={"WWW-Authenticate": "Bearer"},
        )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

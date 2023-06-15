from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import pytz
import schemas.employee as schemas

# Set the default timezone to GMT+8
tz = pytz.timezone('Asia/Singapore')

SECRET_KEY = "P1aNYGQP7at5pTa4WTYiUW0fPgmH/Gy2yC/wVGg/vfA"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(tz=tz) + expires_delta
    else:
        expire = datetime.now(tz=tz) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token:str,credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=email)
    except JWTError:
        raise credentials_exception
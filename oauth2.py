from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
import JWTtoken
from sqlalchemy.orm import Session
from config.db import  get_db
from jose import jwt
import models.employee as models
import schemas.employee as schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="https://back-end-production-3084.up.railway.app/login/")
JWT_SECRET = "myjwtsecret"
SECRET_KEY = "P1aNYGQP7at5pTa4WTYiUW0fPgmH/Gy2yC/wVGg/vfA"
ALGORITHM = "HS256"


def get_current_admin(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return JWTtoken.verify_token(data, credentials_exception)

# async def get_current_user(
#     db: Session = Depends(get_db),
#     token: str = Depends(oauth2_scheme),
# ):
#     try:
#         payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
#         user = db.query(models.Admin).get(payload["id"])
#     except:
#         raise HTTPException(
#             status_code=401, detail="Invalid Email or Password"
#         )

#     return schemas.ShowAdminAuth.from_orm(user)

# Fungsi untuk mencari user berdasarkan email
def get_user(db: Session, email: str):
    return db.query(models.Admin).filter(models.Admin.email == email).first()

# Fungsi untuk memeriksa autentikasi user
def get_current_active_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        token_data = {"email": email}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

    user = get_user(db, email)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    # if user.disabled:
    #     raise HTTPException(status_code=400, detail="Inactive user")
    return user
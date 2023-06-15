from fastapi import APIRouter, Depends, HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
import schemas.employee as schemas
from config.db import  get_db
import models.employee as models
from sqlalchemy.orm import Session
from hashing import Hash
import JWTtoken
from oauth2 import get_current_active_user

router = APIRouter(
    prefix='/login',
    tags=['Authentication']
)

@router.post('/',status_code=status.HTTP_200_OK)
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    admin = db.query(models.Admin).filter(models.Admin.email == request.username).first()
    if not admin:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= "Invalid")
    if not Hash.verify(admin.password, request.password):
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= "Incorrect Password")

    access_token = JWTtoken.create_access_token(
        data={"sub": admin.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}




@router.get('/admin', response_model= schemas.ShowAdminAuth, status_code=status.HTTP_200_OK)
async def read_admin_me(current_user: schemas.Admin = Depends(get_current_active_user)):
    return current_user



    


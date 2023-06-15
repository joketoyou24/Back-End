from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
import schemas.employee as schemas
from config.db import  get_db
import models.employee as models
from sqlalchemy.orm import Session
from hashing import Hash
from oauth2 import get_current_admin

router = APIRouter(
    prefix='/admin',
    tags=['Admin']
)

#Create Admin
@router.post('/', response_model= schemas.ShowAdmin, status_code=status.HTTP_201_CREATED )
def create_admin (request: schemas.Admin, db: Session = Depends (get_db)):
    new_admin = models.Admin(name=request.name, email = request.email, password = Hash.bcrypt(request.password))
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin

#Show all admin
@router.get('/', response_model=List[schemas.ShowAdmin], status_code=status.HTTP_200_OK)
def show_all_admin(db: Session = Depends (get_db),current_admin: schemas.Admin = Depends(get_current_admin)):
    admin = db.query(models.Admin).all()
    return admin

#Show Admin
@router.get('/{id}', response_model= schemas.ShowAdmin, status_code=status.HTTP_200_OK)
def get_admin(id:int, db: Session = Depends (get_db),current_admin: schemas.Admin = Depends(get_current_admin)):
    admin = db.query(models.Admin).filter(models.Admin.id == id).first()
    if not admin:
        if not admin:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"account admin with the id {id} is not available")
    return admin

#Delete Admin
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete (id, db: Session = Depends (get_db), current_admin: schemas.Admin = Depends(get_current_admin)):
    employee = db.query(models.Admin).filter(models.Admin.id == id)
    if not employee.first():
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f'employee with id {id} not found')
    employee.delete(synchronize_session=False)
    db.commit()
    return 'Admin account deleted'


#Update Admin
@router.put('/{id}', response_model= schemas.UpdateAdmin, status_code=status.HTTP_202_ACCEPTED)
def update (id, request: schemas.UpdateAdmin,db: Session = Depends (get_db), current_admin: schemas.Admin = Depends(get_current_admin)):
    admin = db.query(models.Admin).filter(models.Admin.id == id)
    if not admin.first():
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f'admin with id {id} not found')
    
    if request.password :
        request.password=Hash.bcrypt(request.password)
    admin.update(request.dict(exclude_unset=True))
    db.commit()
    return 'updated'
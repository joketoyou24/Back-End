from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
import schemas.employee as schemas
from config.db import  get_db
import models.employee as models
from sqlalchemy.orm import Session
from oauth2 import get_current_admin

router = APIRouter(
    prefix='/attendance_status',
    tags=['Attendance Status']
)

@router.post('/', status_code=status.HTTP_201_CREATED )
def create(request: schemas.InStatus, db: Session = Depends (get_db), current_admin: schemas.Admin = Depends(get_current_admin)):
    new_status = models.Attendance_status(
        status_desc = request.status_desc,
        )
    db.add(new_status)
    db.commit()
    db.refresh(new_status)
    return new_status

#Show status by searching the id
@router.get('/{id}', response_model= schemas.OutStatus, status_code=200,)
def show (id,db: Session = Depends (get_db), current_admin: schemas.Admin = Depends(get_current_admin)):
    show_status = db.query(models.Attendance_status).filter(models.Attendance_status.id == id).first()
    if not show_status:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"status with the id {id} is not available")
    return show_status

#Show Status
@router.get('/', response_model=List[schemas.OutStatus], status_code=status.HTTP_200_OK)
def show_all_status(db: Session = Depends (get_db), current_admin: schemas.Admin = Depends(get_current_admin)):
    status = db.query(models.Attendance_status).all()
    return status

#Update status
@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update (id, request: schemas.InStatus,db: Session = Depends (get_db), current_admin: schemas.Admin = Depends(get_current_admin)):
    status = db.query(models.Attendance_status).filter(models.Attendance_status.id == id)
    if not status.first():
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f'status with id {id} not found')

    status.update(request.dict())
    db.commit()
    return 'updated'

#Delete status
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete (id, db: Session = Depends (get_db), current_admin: schemas.Admin = Depends(get_current_admin)):
    status = db.query(models.Attendance_status).filter(models.Attendance_status.id == id)
    if not status.first():
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f'status with id {id} not found')
    status.delete(synchronize_session=False)
    db.commit()
    return 'done'
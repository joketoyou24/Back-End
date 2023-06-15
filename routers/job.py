from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
import schemas.employee as schemas
from config.db import  get_db
import models.employee as models
from sqlalchemy.orm import Session
from oauth2 import get_current_admin

router = APIRouter(
    prefix='/job',
    tags=['Job']
)

@router.post('/', status_code=status.HTTP_201_CREATED )
def create(request: schemas.InJob, db: Session = Depends (get_db), current_admin: schemas.Admin = Depends(get_current_admin)):
    new_job = models.Job(
        job_role = request.job_role,
        )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job

#Show job by searching the id
@router.get('/{id}', response_model= schemas.OutJob, status_code=200,)
def show (id,db: Session = Depends (get_db), current_admin: schemas.Admin = Depends(get_current_admin)):
    show_job = db.query(models.Job).filter(models.Job.id == id).first()
    if not show_job:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"job with the id {id} is not available")
    return show_job

#Show job
@router.get('/', response_model=List[schemas.OutJob], status_code=status.HTTP_200_OK)
def show_all_job(db: Session = Depends (get_db), current_admin: schemas.Admin = Depends(get_current_admin)):
    job = db.query(models.Job).all()
    return job

#Update job
@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update (id, request: schemas.InJob,db: Session = Depends (get_db), current_admin: schemas.Admin = Depends(get_current_admin)):
    job = db.query(models.Job).filter(models.Job.id == id)
    if not job.first():
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f'job with id {id} not found')

    job.update(request.dict())
    db.commit()
    return 'updated'

#Delete job
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete (id, db: Session = Depends (get_db), current_admin: schemas.Admin = Depends(get_current_admin)):
    job = db.query(models.Job).filter(models.Job.id == id)
    if not job.first():
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f'job with id {id} not found')
    job.delete(synchronize_session=False)
    db.commit()
    return 'done'
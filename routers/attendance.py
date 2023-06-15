from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Response
import schemas.employee as schemas
from config.db import  get_db
import models.employee as models
from sqlalchemy.orm import Session
from oauth2 import get_current_admin

router = APIRouter(
    prefix='/attendance',
    tags=['Attendance']
)

#Show all 
@router.get("/")
def get_employee_attendance(employee_id: Optional[int] = None, date: Optional[str] = None, db: Session = Depends(get_db)):
    attendance_query = db.query(models.Attendance)

    if employee_id:
        attendance_query = attendance_query.filter(models.Attendance.employee_id == employee_id)
    if date:
        attendance_query = attendance_query.filter(models.Attendance.date == date)

    attendance_records = attendance_query.all()
    employee_attendance = []

    for record in attendance_records:
        employee = db.query(models.Employee).filter(models.Employee.id == record.employee_id).first()

        if employee:
            employee_attendance.append(schemas.EmployeeAttendanceSchema(
                employee=schemas.EmployeeAttendance(
                    id=employee.id,
                    NIK=employee.NIK,
                    name=employee.name
                ),
                attendance=[schemas.AllAttendance(
                    id=record.id,
                    date=record.date,
                    absen_1=record.absen_1,
                    absen_2=record.absen_2,
                    absen_3=record.absen_3,
                    absen_4=record.absen_4,
                    employee_id=record.employee_id,
                    attendance_status=record.attendance_status
                )]
            ))

    return employee_attendance



@router.post('/', status_code=status.HTTP_201_CREATED )
def create(request: schemas.Attendance1, db: Session = Depends (get_db)):
    attendance1 = models.Attendance(
        absen_1 = request.absen_1,
        employee_id= request.employee_id,
        attendance_status_id = 1
        )
    db.add(attendance1)
    db.commit()
    db.refresh(attendance1)
    return attendance1

# @router.post("/")
# def create_absen(absen: schemas.AllAttandance, db: Session = Depends(get_db)):
#     # Get last entry in the absen table
#     last_absen = db.query(models.Attendance).order_by(models.Attendance.date.desc()).first()

#     # Get the current date in Singapore timezone
#     singapore_tz = pytz.timezone("Asia/Singapore")
#     current_date = datetime.now(singapore_tz).date()

#     if last_absen is None or last_absen.date != current_date:
#         # If there is no entry in the absen table or the last entry is not for the current date
#         # Create a new entry in the absen table
#         absen_db = models.Attendance(**absen.dict())
#         db.add(absen_db)
#         db.commit()
#         db.refresh(absen_db)
#         return absen_db
#     else:
#         # If the last entry in the absen table is for the current date
#         # Update the last entry with the absen data
#         last_absen.absen_1 = absen.absen_1
#         last_absen.absen_2 = absen.absen_2
#         last_absen.absen_3 = absen.absen_3
#         last_absen.absen_4 = absen.absen_4
#         db.commit()
#         db.refresh(last_absen)
#         return last_absen

#Delete attendance
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete (id, db: Session = Depends (get_db), current_admin: schemas.Admin = Depends(get_current_admin)):
    attendance = db.query(models.Attendance).filter(models.Attendance.id == id)
    if not attendance.first():
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f'employee with id {id} not found')
    attendance.delete(synchronize_session=False)
    db.commit()
    return 'done'

#Update status attendance
@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update (id, request: schemas.UpdateAttendance,db: Session = Depends (get_db), current_admin: schemas.Admin = Depends(get_current_admin)):
    attendance = db.query(models.Attendance).filter(models.Attendance.id == id)
    if not attendance.first():
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f'attendance with id {id} not found')

    attendance.update(request.dict())
    db.commit()
    return 'updated'

#Show attendance by id
@router.get('/{id}', status_code=status.HTTP_200_OK)
def show (id, db: Session = Depends (get_db), current_admin: schemas.Admin = Depends(get_current_admin)):
    show_attendance = db.query(models.Attendance).filter(models.Attendance.id == id).first()
    if not show_attendance:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"employee with the id {id} is not available")
    return show_attendance

@router.get("/")
def get_employee_attendance(employee_id: Optional[int] = None, date: Optional[str] = None, db: Session = Depends(get_db)):
    attendance_query = db.query(models.Attendance)

    if employee_id:
        attendance_query = attendance_query.filter(models.Attendance.employee_id == employee_id)
    if date:
        attendance_query = attendance_query.filter(models.Attendance.date == date)

    attendance_records = attendance_query.all()
    employee_attendance = []

    for record in attendance_records:
        employee = db.query(models.Employee).filter(models.Employee.id == record.employee_id).first()

        if employee:
            employee_attendance.append(schemas.EmployeeAttendanceSchema(
                employee=schemas.EmployeeAttendance(
                    id=employee.id,
                    NIK=employee.NIK,
                    name=employee.name
                ),
                attendance=[schemas.AllAttendance(
                    id=record.id,
                    date=record.date,
                    absen_1=record.absen_1,
                    absen_2=record.absen_2,
                    absen_3=record.absen_3,
                    absen_4=record.absen_4,
                    employee_id=record.employee_id,
                    attendance_status=record.attendance_status
                )]
            ))

    return employee_attendance


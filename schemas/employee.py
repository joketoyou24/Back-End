from datetime import datetime,date
from typing import List, Optional
from pydantic import BaseModel, validator
import pytz
# from fastapi_utils.openapi import schema
tz = pytz.timezone('Asia/Singapore')

class InEmployee(BaseModel):
    name:str
    # NIK:schema.ExclusiveIntGe(min_value=0, max_value=2**64-1, multiple_of=1)
    NIK : int
    @validator('NIK')
    def validate_column_name(cls, v):
        if len(str(v)) != 16:
            raise ValueError('NIK harus 16 digit')
        return v
    gender:str
    job_id:int
    general_status_id:int
    class Config():
        orm_mode = True

class UpdateEmployee(BaseModel):
    NIK: int
    name: str
    job_id:int
    general_status_id:int
    class Config():
        orm_mode = True

class InStatus(BaseModel):
    status_desc : str
    class Config():
        orm_mode = True

class OutStatus(BaseModel):
    id : int
    status_desc : str
    created_date: datetime
    class Config():
        orm_mode = True

class InJob(BaseModel):
    job_role : str
    class Config():
        orm_mode = True

class OutJob(BaseModel):
    id : int
    job_role : str
    created_date: datetime
    class Config():
        orm_mode = True

class Admin(BaseModel):
    name : str
    email : str
    password : str

class ShowAdmin(BaseModel):
    id : int
    name : str
    email : str
    created_date : datetime
    class Config():
        orm_mode = True

class ShowAdminAuth(BaseModel):
    email : str
    id : int
    class Config():
        orm_mode = True

class AllEmployee(BaseModel):
    id:int
    name:str
    NIK:int
    gender:str
    job:InJob
    status:InStatus
    created_date:datetime
    
    class Config():
        orm_mode = True

class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
   username: Optional[str] = None

class UserInDB(Admin):
    hashed_password: str

class UpdateAdmin(BaseModel):
    name : Optional[str] = None
    email : Optional[str] = None
    password : Optional[str] = None
    class Config():
        orm_mode = True

class Image(BaseModel):
    id: str
    filename: str

class Inattendance(BaseModel):
    status_desc : str
    class Config():
        orm_mode = True

class AllAttendance(BaseModel):
    id: int
    date: Optional[date]
    absen_1: datetime = None
    absen_2: datetime = None
    absen_3: datetime = None
    absen_4: datetime = None
    employee_id: int
    # attendance_status_id : int = 1
    attendance_status: Inattendance

    class Config():
        orm_mode = True

class UpdateAttendance(BaseModel):
    attendance_status_id : int

    class Config():
        orm_mode = True

class EmployeeAttendance(BaseModel):
    id: int
    NIK: int
    name: str

class EmployeeAttendanceSchema(BaseModel):
    employee: EmployeeAttendance
    attendance: List[AllAttendance]

    
class Attendance1(BaseModel):
    date = datetime.now(tz=tz)
    absen_1: datetime=datetime.now(pytz.timezone('Asia/Singapore'))
    absen_2: datetime=None
    absen_3: datetime=None
    absen_4: datetime=None
    employee_id:  int

class Attendance2(BaseModel):
    date = datetime.now(tz=tz)
    absen_1: datetime=None
    absen_2: datetime=datetime.now(pytz.timezone('Asia/Singapore'))
    absen_3: datetime=None
    absen_4: datetime=None
    employee_id:  int

class Attendance3(BaseModel):
    date = datetime.now(tz=tz)
    absen_1: datetime=None
    absen_2: datetime=None
    absen_3: datetime=datetime.now(pytz.timezone('Asia/Singapore'))
    absen_4: datetime=None
    employee_id:  int

class Attendance4(BaseModel):
    date = datetime.now(tz=tz)
    absen_1: datetime=None
    absen_2: datetime=None
    absen_3: datetime=None
    absen_4: datetime=datetime.now(pytz.timezone('Asia/Singapore'))
    employee_id:  int


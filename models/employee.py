import pytz
from sqlalchemy import Column, DateTime, Integer, Sequence, String , BigInteger, ForeignKey,Date
from config.db import Base
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType

# Set the default timezone to GMT+8
tz = pytz.timezone('Asia/Singapore')

#table structure
class Employee(Base):
    __tablename__ = 'TabelPegawai'

    # image = relationship('Dataset', backref='TabelDataset')
    id = Column(Integer, primary_key=True, index=True)
    
    name = Column(String(255), index=True)
    NIK = Column(BigInteger, unique = True)
    gender = Column(String(255), index=True)
    
    created_date = Column(DateTime(), default=datetime.now(tz=tz))
    # # define a one-to-many relationship with the Status model
    status = relationship('General_status', backref='TabelPegawai')
    general_status_id = Column(Integer, ForeignKey('TabelStatus.id'))

    job = relationship('Job', backref='TabelPegawai')
    job_id = Column(Integer, ForeignKey('TabelJob.id'))
                            
    attendance= relationship('Attendance', backref='TabelAttendance')
    
class General_status(Base):
    __tablename__ = 'TabelStatus'
    id = Column(Integer, primary_key=True, index=True)
    status_desc = Column(String(255))
    created_date = Column(DateTime, default=datetime.now(tz=tz))

class Job(Base):
    __tablename__ = 'TabelJob'
    id = Column(Integer, primary_key=True, index=True)
    job_role = Column(String(255))
    created_date = Column(DateTime, default=datetime.now(tz=tz))

class Attendance(Base):
    __tablename__ = 'TabelAttendance'
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, default=datetime.now(tz=tz))
    absen_1 = Column(DateTime, default=datetime.now(tz=tz), nullable = True)
    absen_2 = Column(DateTime, nullable = True)
    absen_3 = Column(DateTime, nullable = True)
    absen_4 = Column(DateTime, nullable = True)
    employee_id = Column(Integer, ForeignKey('TabelPegawai.id'))
    attendance_status= relationship('Attendance_status', backref='TabelAttendance')
    attendance_status_id = Column(Integer, ForeignKey('TabelStatusKehadiran.id'))
    

class Dataset(Base):
    __tablename__= 'TabelDataset'
    id = Column(Integer, primary_key=True, index=True)
    img_employe = Column(String(255))
    employee_id = Column(Integer)

class Admin(Base):
    __tablename__ = 'TabelAkunAdmin'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    email = Column(EmailType)
    password = Column(String(255))
    created_date = Column(DateTime, default=datetime.now(tz=tz))

class Attendance_status(Base):
    __tablename__ = 'TabelStatusKehadiran'
    id = Column(Integer, primary_key=True, index=True)
    status_desc = Column(String(255))
    created_date = Column(DateTime, default=datetime.now(tz=tz))
    
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pymysql.cursors

host='containers-us-west-110.railway.app'
user='root'
port= 6395
password='5awcXt09ZHlr1xwxZLie'
db='railway'
# SQLALCHEMY_DATABASE_URL = ("mysql+pymysql://<username>:<password>@<host>/<dbname>[?<options>]")
SQLALCHEMY_DATABASE_URL = (f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}")
# # membuat koneksi ke MySQL
# connection = pymysql.connect(
#     host='localhost',
#     user='root',
#     password='password',
#     db='database_name',
#     cursorclass=pymysql.cursors.DictCursor
# )

# database_config = {
#     "host": "localhost",
#     "username": "root",
#     "password": "",
#     "dbname": "absensi_db",
# }

# connection = pymysql.connect(
#     host='localhost',
#     user='root',
#     password='',
#     db='absensi_db',
#     charset='utf8mb4',
#     cursorclass=pymysql.cursors.DictCursor
# )

# #create engine
# engine = create_engine(
#         SQLALCHEMY_DATABASE_URL.format(**database_config)
#     )

#create engine
engine = create_engine(
        SQLALCHEMY_DATABASE_URL
    )

#sessionmaker
SessionLocal = sessionmaker (bind=engine ,autocommit=False, autoflush=False, )

#mapped
Base = declarative_base()

def get_db():
    db = SessionLocal() 
    try:
        yield db
    finally:
        db.close()

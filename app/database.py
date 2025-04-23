from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker 

from app.config import settings

# import psycopg2
# from psycopg2.extras import RealDictCursor
# while True:
#     try:
#         conn = psycopg2.connect(
#         host='localhost',
#         port='5433',
#         database='fastAPI',
#         user='postgres',
#         password='Ritish1995',
#         cursor_factory=RealDictCursor
#         )
#         cursor = conn.cursor()
#         print("Database connection successful")
#         break
#     except Exception as error:
#         print("Database connection failed:")
#         print(error)
#         time.sleep(2)

# SQLALCHEMY_DATABSE_URL = 'postgresql://<username>:<password>@<ip-address/hostname:PORT>/<database_name>'

SQLALCHEMY_DATABSE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABSE_URL)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
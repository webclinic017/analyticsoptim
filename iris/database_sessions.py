from pathlib import Path
from sqlalchemy import create_engine, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from database.postgres_sql_connect import config

params = config(filename="iris/database.ini")
print(params)
SQLALCHEMY_DATABASE_URL = f"postgresql://{params['user']}:{params['password']}@{params['host']}/{params['database']}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
# from database import  db_models
Base.metadata.create_all(bind=engine)
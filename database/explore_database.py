from sqlalchemy.orm import sessionmaker
import sqlalchemy as db #import create_engine, MetaData, func,and_, Table
import pandas as pd

from database.postgres_sql_connect import config
# params = config(filename="../frontend/database.ini")
# SQLALCHEMY_DATABASE_URL = f"postgresql://{params['user']}:{params['password']}@{params['host']}/{params['database']}"
# engine = db.create_engine(SQLALCHEMY_DATABASE_URL)
# connection = engine.connect()
# metadata = db.MetaData()
# census = db.Table('stocks', metadata, autoload=True, autoload_with=engine)
# print(census.columns.keys())
# query = db.select([census]).where(census.columns.symbol == 'GNUS')
# res = connection.execute(query)
# print(pd.DataFrame (res.fetchall()))
# # session = sessionmaker()
# # session.configure(bin(engine))
# # mysession = session()
import yfinance as yf
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from database.database_helper import get_time_and_symbols


def add_new_data(symbols, start="2020-08-02", end="2020-08-19"):
    # params = config(filename="../frontend/database.ini")
    # SQLALCHEMY_DATABASE_URL = f"postgresql://{params['user']}:{params['password']}@{params['host']}/{params['database']}"
    SQLALCHEMY_DATABASE_URL = "postgresql://postgres:reallyStrongPwd123@192.168.0.108/testdb1"

    engine = db.create_engine(SQLALCHEMY_DATABASE_URL)
    connection = engine.connect()
    session = sessionmaker()
    session.configure(bind=engine)
    Base = declarative_base()
    Base.metadata.create_all(bind=engine)
    metadata = db.MetaData()

    df = yf.download(symbols, start=start, end=end)
    df.columns = df.columns.swaplevel(0, 1)
    df = df.stack(0)
    df.index.names = ["date", "symbol"]
    df.reset_index(inplace=True)
    df.columns = map(str.lower, df.columns)
    df = df.rename({"adj close": "adj_close"}, axis=1)
    df.to_sql("StockData", con=engine, schema="incertae", index=False, if_exists='append')


def update_data():
    start, end, symbols = get_time_and_symbols()
    print(start, end, start > end)
    if start >= end:
        print("data is up to date")
    else:
        add_new_data(symbols, start, end)


if __name__ == "__main__":
    update_data()
# curs.execute(("""select 'stocks' from information_schema.tables WHERE table_schema='incertae'"""))
# print(curs.fetchall())
# curs.execute(("""select * from information_schema.tables WHERE table_schema='incertae'"""))
# print(curs.fetchall())

# from database.postgres_sql_connect import config
# params = config(filename="../frontend/database.ini")
# SQLALCHEMY_DATABASE_URL = f"postgresql://{params['user']}:{params['password']}@{params['host']}/{params['database']}"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:reallyStrongPwd123@192.168.0.108/testdb1"
# engine = db.create_engine(SQLALCHEMY_DATABASE_URL)
# connection = engine.connect()
# Session = sessionmaker()
# Session.configure(bind = engine)
# metadata = db.MetaData()
# session = Session()
# census = db.Table('stocdata', metadata, autoload=True, autoload_with=engine,schema="incertae")
# subq = session.query(
#     census.symbol,
#     db.func.max(census.Date).label('maxdate')
# ).group_by(census.symbol)
# res = connection.execute(subq)
# print(res.fetchall())
#

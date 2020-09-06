from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import engine, create_engine, MetaData
import sqlalchemy as db
import os ,  sys
from pathlib import Path
import pandas as pd
import chardet

from database.postgres_sql_connect import config
from database.db_models import StockData

params = config(filename="../frontend/database.ini")
print(params)
SQLALCHEMY_DATABASE_URL = f"postgresql://{params['user']}:{params['password']}@{params['host']}/{params['database']}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
connection = engine.connect()
session = sessionmaker()
session.configure(bind=engine)
Base = declarative_base()
Base.metadata.create_all(bind=engine)
metadata = MetaData()

mysession = session()

# sp500folder = "./daily"
# onlyfiles = [f for f in os.listdir(sp500folder) if os.path.isfile(os.path.join(sp500folder, f))]
# for file in onlyfiles[:10]:
#     fullpath = os.path.join(sp500folder, file)
#     df = pd.read_csv(fullpath)#,encoding=cdt)
#     df["symbol"] = file.split(".")[0]
#     df = df.rename({"Adj Close":"Adj_Close"}, axis = 1)
#     df.to_sql('stocdata', con=engine,index=False,if_exists="append")
#     # query = db.update(StockData).where(StockData.Data)
#     # connection.execute(query)
#
#     print(df.head())
import pandas as pd
symbols = pd.read_csv("sp500.csv",header=None, names=["symbol","name"])
symbols["name"]=symbols["name"].astype(str)
symbols["sp500"] = '1'
# with open("sp500.csv", "r") as file:
#     symbols = file.read().splitlines()
symbols.to_sql("Symbols",con=engine,schema="incertae", index=False,if_exists='append')
connection.close()
from database.postgres_sql_connect import config, engine, SessionLocal, Base
from iris.router import iris_classifier_router
from database.db_models import Stocks


stock = Stocks()
stock.symbol = "F"
print("adfafopasifdpoipasifppaspfpsadfpopods")
print(stock.symbol)
sess = SessionLocal()
sess.add(stock)
sess.commit()
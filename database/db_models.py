import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper

# from frontend.database_sessions import Base

Base = declarative_base()
metadata = db.MetaData()

stocks = db.Table("stocks", metadata,
                  db.Column("id", db.Integer, primary_key=True, index=True),
                  db.Column("symbol", db.String, unique=True, index=True),
                  db.Column("price", db.Numeric(10, 4)),
                  db.Column("forward_pe", db.Numeric(10, 4)),
                  db.Column("forward_eps", db.Numeric(10, 4)),
                  db.Column("dividend_yield", db.Numeric(10, 4)),
                  db.Column("ma50", db.Numeric(10, 4)),
                  db.Column("ma200", db.Numeric(10, 4)),
                  schema="incertae")


class Stocks(object):
    pass


mapper(Stocks, stocks)
# class Stocks(Base):
#     __tablename__ = "incertae.stocks"
#     id = db.Column(db.Integer, primary_key=True, index=True)
#     symbol = db.Column(db.String, unique=True, index=True)
#     price = db.Column(db.Numeric(10, 4))
#     forward_pe = db.Column(db.Numeric(10, 4))
#     forward_eps = db.Column(db.Numeric(10, 4))
#     dividend_yield = db.Column(db.Numeric(10, 4))
#     ma50 = db.Column(db.Numeric(10, 4))
#     ma200 = db.Column(db.Numeric(10, 4))


class StockData(Base):
    __tablename__ = "StockData"
    id = db.Column(db.Integer, primary_key=True, index=True)
    Date = db.Column(db.Date)
    symbol = db.Column(db.String, unique=True, index=True)
    Open = db.Column(db.Numeric(10, 4))
    High = db.Column(db.Numeric(10, 4))
    Low = db.Column(db.Numeric(10, 4))
    Close = db.Column(db.Numeric(10, 4))
    Adj_Close = db.Column(db.Numeric(10, 4))
    Volume = db.Column(db.Numeric(10, 4))


class Symbols(Base):
    __tablename__ = "Symbols"
    id = db.Column(db.Integer, primary_key=True, index=True)
    symbol = db.Column(db.String, unique=True, index=True)
    name = db.Column(db.String)
    sp500 = db.Column(db.BOOLEAN)

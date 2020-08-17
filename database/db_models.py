import sqlalchemy as db  # import Boolean, db.Column, ForeignKey, db.Integer, db.String,db.Numeric,Date
from sqlalchemy.ext.declarative import declarative_base

# from iris.database_sessions import Base
Base = declarative_base()


class Stocks(Base):
    __tablename__ = "stocks"
    id = db.Column(db.Integer, primary_key=True, index=True)
    symbol = db.Column(db.String, unique=True, index=True)
    price = db.Column(db.Numeric(10, 4))
    forward_pe = db.Column(db.Numeric(10, 4))
    forward_eps = db.Column(db.Numeric(10, 4))
    dividend_yield = db.Column(db.Numeric(10, 4))
    ma50 = db.Column(db.Numeric(10, 4))
    ma200 = db.Column(db.Numeric(10, 4))


class StockData(Base):
    __tablename__ = "stocdata"
    id = db.Column(db.Integer, primary_key=True, index=True)
    Date = db.Column(db.Date)
    symbol = db.Column(db.String, unique=True, index=True)
    Open = db.Column(db.Numeric(10, 4))
    High = db.Column(db.Numeric(10, 4))
    Low = db.Column(db.Numeric(10, 4))
    Close = db.Column(db.Numeric(10, 4))
    Adj_Close = db.Column(db.Numeric(10, 4))
    Volume = db.Column(db.Numeric(10, 4))

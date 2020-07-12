from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,Numeric
from database.postgres_sql_connect import Base

class Stocks(Base):
    __tablename__ = "stocks"
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True)
    price = Column(Numeric(10,4))
    forward_pe = Column(Numeric(10, 4))
    forward_eps = Column(Numeric(10, 4))
    dividend_yield = Column(Numeric(10, 4))
    ma50 = Column(Numeric(10, 4))
    ma200 = Column(Numeric(10, 4))

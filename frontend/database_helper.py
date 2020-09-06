from database.db_models import Stocks
import yfinance
from .database_sessions import SessionLocal

def fetch_stock_data(id: int):
    db = SessionLocal()
    _stock = db.query(Stocks).filter(Stocks.id == id).first()
    yahoo_daata = yfinance.Ticker(_stock.symbol)
    _stock.price = yahoo_daata.info['previousClose']
    _stock.forward_pe = yahoo_daata.info['forwardPE']
    _stock.forward_eps = yahoo_daata.info['forwardEps']
    if yahoo_daata.info['dividendYield'] is not None:
        _stock.dividend_yield = yahoo_daata.info['dividendYield'] * 100
    _stock.ma50 = yahoo_daata.info['fiftyDayAverage']
    _stock.ma200 = yahoo_daata.info['twoHundredDayAverage']
    print(_stock)
    db.add(_stock)
    db.commit()
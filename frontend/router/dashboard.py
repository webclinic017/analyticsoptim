from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from frontend.database_sessions import SessionLocal
from fastapi import FastAPI, Request, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from database.db_models import Stocks
from fastapi import APIRouter, HTTPException
templates = Jinja2Templates(directory="template")

router = APIRouter()

class StocksRequest(BaseModel):
    symbol: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/dashboard")
async def dashboard(request: Request, forward_pe=None, dividend_yield=None, ma50=None, ma200=None,
                    db: Session = Depends(get_db)):
    print("\n\n\n\n\n\n\n\n shit \n\n\n\n\n\n\n\n")
    stocks_fetched = db.query(Stocks)
    # stocks_fetched = db.query(Stocks).all()

    # if (forward_pe is not None) and forward_pe != '' :
    if forward_pe:
        stocks_fetched = stocks_fetched.filter(Stocks.forward_pe < forward_pe)
        print(forward_pe)
    if dividend_yield:
        stocks_fetched = stocks_fetched.filter(Stocks.dividend_yield > dividend_yield)
    if ma50:
        stocks_fetched = stocks_fetched.filter(Stocks.price > Stocks.ma50)
    if ma200:
        stocks_fetched = stocks_fetched.filter(Stocks.price > Stocks.ma200)
    print(stocks_fetched)
    return templates.TemplateResponse("dashboard.html",
                                      {"request": request,
                                       "stocks": stocks_fetched,
                                       "divident_yield": dividend_yield,
                                       "forward_pe": forward_pe,
                                       "ma50": ma50,
                                       "ma200": ma200
                                       })



@router.post("/stock")
async def create_stock(stock_request: StocksRequest, background_tasks: BackgroundTasks,
                       db: Session = Depends(get_db)):
    """
    add one or more tickers to the database
    background task to use yfinance and load key statistics
    """

    stock = Stocks()
    # print("stock request is", stock_request)
    stock.symbol = stock_request.symbol
    db.add(stock)
    db.commit()

    background_tasks.add_task(dbh.fetch_stock_data_form_yfinance, stock.id)

    return {
        "code": "success",
        "message": f"stock {stock.symbol} was added to the database"
    }

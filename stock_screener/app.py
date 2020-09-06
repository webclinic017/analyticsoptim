from frontend.router import iris_classifier_router
from database.db_models import Stocks
from fastapi import FastAPI, Request, Depends, BackgroundTasks
from enum import Enum
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import BaseModel
import json
from .database_sessions  import SessionLocal
from database.database_helper import  fetch_stock_data_form_yfinance
from .patterns import patterns

templates = Jinja2Templates(directory="template")
app = FastAPI()
app.include_router(iris_classifier_router.router, prefix='/frontend')

class StocksRequest(BaseModel):
    symbol: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/dashboard")
async def dashboard(request: Request, forward_pe=None, dividend_yield=None, ma50=None, ma200=None,
                    db: Session = Depends(get_db)):
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

@app.get("/books")
async def get_books(books="books"):
    with open("./database/books.json") as file:
        books = json.load(file)
    return {books}

@app.get("/books/{title}")
async def get_books(title):
    with open("./database/books.json") as file:
        books = json.load(file)
    book = [b for b in books if b["title"] == title]
    return {"books": book}

@app.post("/stock")
async def create_stock(stock_request: StocksRequest, background_tasks: BackgroundTasks,
                       db: Session = Depends(get_db)):
    """
    add one or more tickers to the database
    background task to use yfinance and load key statistics
    """

    stock = Stocks()
    print("stock request is", stock_request)
    stock.symbol = stock_request.symbol
    db.add(stock)
    db.commit()

    background_tasks.add_task(fetch_stock_data_form_yfinance, stock.id)

    return {
        "code": "success",
        "message": f"stock {stock.symbol} was added to the database"
    }


# order matters
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/model/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    return {"model_name": model_name, "message": "Have some residuals"}

@app.get('/healthcheck', status_code=200)
async def healthcheck():
    return 'Iris classifier is all ready to go!'

# @app.get("/")
# def home(request: Request, forward_pe=None, dividend_yield=None, ma50=None, ma200=None, db: Session = Depends(get_db)):
#     """
#     show all stocks in the database and button to add more
#     button next to each stock to delete from database
#     filters to filter this list of stocks
#     button next to each to add a note or save for later
#     """
#
#     stocks = db.query(Stocks)
#
#     if forward_pe:
#         stocks = stocks.filter(Stocks.forward_pe < forward_pe)
#
#     if dividend_yield:
#         stocks = stocks.filter(Stocks.dividend_yield > dividend_yield)
#
#     if ma50:
#         stocks = stocks.filter(Stocks.price > Stocks.ma50)
#
#     if ma200:
#         stocks = stocks.filter(Stocks.price > Stocks.ma200)
#
#     stocks = stocks.all()
#
#     return templates.TemplateResponse("home.html", {
#         "request": request,
#         "stocks": stocks,
#         "dividend_yield": dividend_yield,
#         "forward_pe": forward_pe,
#         "ma200": ma200,
#         "ma50": ma50
#     })


@app.get("/")
async def home(request:Request):
    with open("./database/sp500.csv", "r") as file:
        symbols = file.read().splitlines()
    # for c in symbols:
    #     symb = c.split(",")[0]
    #     data = yfinance.download(symb,start="2020-01-01", end="2020-08-11")
    #     data.to_csv(f"./database/daily/{symb}.csv")
    return templates.TemplateResponse("home.html",{"request":request,
                                                   "patterns":patterns})


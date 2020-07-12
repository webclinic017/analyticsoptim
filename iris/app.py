from database.postgres_sql_connect import config, engine, SessionLocal, Base
from iris.router import iris_classifier_router
from database.db_models import Stocks

from fastapi import FastAPI, Request, Depends
from enum import Enum
import psycopg2

from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from pydantic import BaseModel

# params = config()
# SQLALCHEMY_DATABASE_URL = f"postgresql://{params['user']}:{params['password']}@{params['host']}/{params['database']}"
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="template")

app = FastAPI()
app.include_router(iris_classifier_router.router, prefix='/iris')


class StocksRequest(BaseModel):
    symbol: str


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/stock")
async def create_stock(sr: StocksRequest, db: Session = Depends(get_db)):
    stock = Stocks()
    stock.symbol = sr.symbol
    print("adfafopasifdpoipasifppaspfpsadfpopods")
    print (stock.symbol)
    db.add(stock)
    db.commit()
    return {"code": "success",
            "message": " stock created"}


@app.post("/stock")
def create_stock():
    return {"code": "success.",
            "message": "stock created"
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


@app.get("/sql")
async def read_database():
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        # conn = psycopg2.connect(host="192.168.0.108",database="testdb1", user="postgres", password="reallyStrongPwd123")

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()

        print(db_version)

        cur.execute("SELECT   first_name,     last_name,    email FROM    customer;")
        examplequery = cur.fetchmany(10)
        # close the communication with the PostgreSQL
        cur.close()
        return examplequery
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

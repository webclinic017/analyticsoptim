from iris.router import iris_classifier_router, dash_graph

import database.database_helper as dbh
from .patterns import patterns
from .dashfigs import *
from iris.router import dashboard, dash_graph

from fastapi import Request, FastAPI
from fastapi.templating import Jinja2Templates
import json
from starlette.middleware.wsgi import WSGIMiddleware

templates = Jinja2Templates(directory="template")
app = FastAPI()
app.include_router(iris_classifier_router.router, prefix='/iris')
app.include_router(dashboard.router)
app.mount("/dash", WSGIMiddleware(dash_graph.dashapp.server))


@app.get("/")
async def home(request: Request):
    last, today, symbols = get_time_and_symbols()
    is_potential = ["Ha", "na"]
    for symb in symbols[:20]:
        df = get_stock_data_from_db(last, symbs=symb)
        _, _is_potential = dbh.add_bands(df)
        if _is_potential:
            is_potential.append(symb)
            print(symb)

    df = get_stock_data_from_db(last, "MSFT")
    return templates.TemplateResponse("home.html", {"request": request,
                                                    "patterns": patterns,
                                                    "is_potential": is_potential,
                                                    "stockdata": df.tail()})

import dash_core_components as dcc
import dash_html_components as html
import dash

import pandas as pd

from database.database_helper import get_stock_data_from_db, get_time_and_symbols

dashapp = dash.Dash(__name__, requests_pathname_prefix="/dash/")

def get_fig_test(dashapp):
    pass
years = list(range(1940, 2021, 1))
temp_high = [x / 20 for x in years]
temp_low = [x - 20 for x in temp_high]
df = pd.DataFrame({"Year": years, "TempHigh": temp_high, "TempLow": temp_low})

slider = dcc.RangeSlider(
id="slider",
value=[df["Year"].min(), df["Year"].max()],
min=df["Year"].min(),
max=df["Year"].max(),
step=5,
marks={
    1940: "1940",
    1945: "1945",
    1950: "1950",
    1955: "1955",
    1960: "1960",
    1965: "1965",
    1970: "1970",
    1975: "1975",
    1980: "1980",
    1985: "1985",
    1990: "1990",
    1995: "1995",
    2000: "2000",
    2005: "2005",
    2010: "2010",
    2015: "2015",
    2020: "2020",
},
)

dashapp.layout = html.Div(
children=[
    dcc.Location(id='url', refresh=True),
    dcc.Link('Navigate to "/"', href='/'),
    # html.Br(),
    # dcc.Link('Navigate to "/page-2"', href='/page-2'),

    html.H1(children="Stock Screener Dashboard"),
    html.Div(children="High/Low Temperatures Over Time"),
    dcc.Graph(id="temp-plot"),
    dcc.Graph(id="myfig"),
    slider,
]
)


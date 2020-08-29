import dash_core_components as dcc
import dash_html_components as html


import pandas as pd

def make_layout():
    years = list(range(1940, 2021, 1))
    temp_high = [x / 20 for x in years]
    temp_low = [x - 20 for x in temp_high]
    df = pd.DataFrame({"Year": years, "TempHigh": temp_high, "TempLow": temp_low})

    slider = dcc.RangeSlider(
        id="slider",
        value=["2020-01-01", "2020-08-28"],
        min="2020-01-01",
        max="2020-08-28",
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


    layout = html.Div(
        children=[
            dcc.Location(id='url', refresh=True),
            dcc.Link('Navigate to "/"', href='/'),
            # html.Br(),
            # dcc.Link('Navigate to "/page-2"', href='/page-2'),

            html.H1(children="Stock Screener Dashboard"),
            html.Div(children="Plot Bollinger and Ketlner bands"),
            dcc.Input(id="input_symbol", type='text', placeholder="input type symbol"),
            html.Button("Submit", id="submit_symbol_b", n_clicks=0),
            dcc.Graph(id="temp-plot"),
            dcc.Graph(id="myfig"),
            slider,
        ]
    )
    return layout, slider
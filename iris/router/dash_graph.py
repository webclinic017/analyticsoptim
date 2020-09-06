import dash_core_components as dcc
import dash_html_components as html
import dash
from dash.dependencies import Input, Output, State
import plotly.graph_objs as obj
import plotly.graph_objs as go
import pandas as pd

# fetch_stock_data_form_yfinance, add_bands, get_time_and_symbols
import database.database_helper as dbh

dashapp = dash.Dash(__name__, requests_pathname_prefix="/dash/")

def get_fig_test(dashapp):
    pass

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


dashapp.layout, slider = make_layout()


@dashapp.callback(Output("temp-plot", "figure"),
                  [Input("slider", "value"),
                   Input("submit_symbol_b", "n_clicks"),
                   State("input_symbol", "value"),
                   ])
def add_graph(slider, n_clicks, input_symbol):
    last, today, symbols = dbh.get_time_and_symbols()
    input_symbol = input_symbol.upper()
    if input_symbol not in symbols:
        print("Symbol is not in S&P500, Please input a correct symbol")
        trace_high = obj.Scatter(x=[1, 3, 5], y=[2, 3, 1], mode="markers", name="High Temperatures")
        figure = obj.Figure(data=[trace_high])
        return figure 

    df_stock = dbh.get_stock_data_from_db(last, symbs=input_symbol)
    # df = df.droplevel(1)
    print(__name__, input_symbol, n_clicks, not df_stock is None)
    if not df_stock is None:
        df_stock, _ = dbh.add_bands(df_stock)
        df_stock.sort_index(inplace=True)
        df_stock = df_stock.droplevel('symbol')

        candlestic = go.Candlestick(x=df_stock.index, open=df_stock['open'],
                                    high=df_stock['high'], low=df_stock['low'], close=df_stock['close'])
        upper_band = go.Scatter(x=df_stock.index, y=df_stock['upperbollinger'], name="Upper Bollinger Band",
                                line={'color': 'red'})
        lower_band = go.Scatter(x=df_stock.index, y=df_stock['lowerbollinger'], name="Lower Bollinger Band",
                                line={'color': 'red'})
        upper_keltner = go.Scatter(x=df_stock.index, y=df_stock['upperkeltner'], name="Upper Keltner Band",
                                   line={'color': 'blue'})
        lower_keltner = go.Scatter(x=df_stock.index, y=df_stock['lowerkeltner'], name="Lower Keltner Band",
                                   line={'color': 'blue'})

        sma = go.Scatter(x=df_stock.index, y=df_stock['20sma'], name="Moving Average")
        tes = go.Scatter(x=df_stock.index, y=df_stock['close'], name='close')
        fig1 = go.Figure(data=[candlestic, upper_band, lower_band, upper_keltner, lower_keltner, sma])
        # fig1 = go.Figure(data=[candlestic, sma, tes])
        # fig1 = go.Figure(data=[candlestic])
        # # fig1.update_layout(  # autosize=False, margin=dict(l=50,r=50, b=100,  t=100, pad=4 ),
        # #     height=1000,  # height=1000,  paper_bgcolor="LightSteelBlue",
        # # )
        # # print("giving figure out")
        return fig1
    else:
        trace_high = obj.Scatter(x=[1, 3, 5], y=[2, 3, 1], mode="markers", name="High Temperatures")
        # trace_low = obj.Scatter(x=df["Year"], y=df["TempLow"], mode="markers", name="Low Temperatures")
        # layout = obj.Layout(xaxis=dict(range=[slider[0], slider[1]]), yaxis={"title": "Temperature"})
        figure = obj.Figure(data=[trace_high])
        return figure

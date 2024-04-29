from datetime import datetime

import pandas as pd
import argparse

import requests
from dash import Dash, dcc, html, Output, Input, callback_context, State
from flask import request

from static import *

data = pd.read_csv("assets/result.csv").sort_values(by="data")
data = data.sort_values(by="data").assign(data=lambda x: pd.to_datetime(x["data"]))

act_data = pd.read_csv("assets/acts.csv")
act_data = act_data.sort_values(by='begin').assign(data=lambda x: pd.to_datetime(x['begin']))
act_data.begin = pd.to_datetime(act_data.begin)

app = Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

act_graph = dcc.Graph(
    id='act',
    config={"displayModeBar": False},
    figure={
        "data": [
            {
                "x": data["data"],
                "y": data["dollar_curs"],
                "type": "lines",
                "hovertemplate": (
                    "₽%{y:.2f}<extra></extra>"
                ),
                "name": "Тиньков"
            },
            {
                "x": data["data"],
                "y": data["euro_curs"],
                "type": "lines",
                "hovertemplate": (
                    "₽%{y:.2f}<extra></extra>"
                ),
                "name": "КекДжиДрайв"
            },
            {
                "x": data["data"],
                "y": data["yuan_curs"],
                "type": "lines",
                "hovertemplate": (
                    "₽%{y:.2f}<extra></extra>"
                ),
                "name": "Насонафнаф"
            },
            {
                "x": data["data"],
                "y": data["pound_curs"],
                "type": "lines",
                "hovertemplate": (
                    "₽%{y:.2f}<extra></extra>"
                ),
                "name": "Овощи"
            }
        ],
        "layout": {
            "title": {
                "text": "Курсы валют",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {
                "tickprefix": "₽",
                "fixedrange": True,
            },
            "colorway": ["#17b897", "red", "blue", "green"],
        }
    }
)

header = html.Div(
            children=[
                html.P(children="💵", className="header-emoji"),
                html.H1(
                    children="HelloBank", className="header-title"
                ),
                html.P(
                    children=(
                        "Банк Вам в помощь!"
                    ),
                    className="header-description",
                ),
            ],
            className="header"
)
graph1 = html.Div(
    children=dcc.Graph(
        id="price",
        config={"displayModeBar": False},
        figure={
            "data": [
                {
                    "x": data["data"],
                    "y": data["dollar_curs"],
                    "type": "lines",
                    "hovertemplate": (
                        "₽%{y:.2f}<extra></extra>"
                    ),
                    "name": "Доллар"
                },
                {
                    "x": data["data"],
                    "y": data["euro_curs"],
                    "type": "lines",
                    "hovertemplate": (
                        "₽%{y:.2f}<extra></extra>"
                    ),
                    "name": "Евро"
                },
                {
                    "x": data["data"],
                    "y": data["yuan_curs"],
                    "type": "lines",
                    "hovertemplate": (
                        "₽%{y:.2f}<extra></extra>"
                    ),
                    "name": "Юань"
                },
                {
                    "x": data["data"],
                    "y": data["pound_curs"],
                    "type": "lines",
                    "hovertemplate": (
                        "₽%{y:.2f}<extra></extra>"
                    ),
                    "name": "Фунт"
                }
            ],
            "layout": {
                "title": {
                    "text": "Курсы валют",
                    "x": 0.05,
                    "xanchor": "left",
                },
                "xaxis": {"fixedrange": True},
                "yaxis": {
                    "tickprefix": "₽",
                    "fixedrange": True,
                },
                "colorway": ["#17b897", "red", "blue", "green"],
            },
        },
    ),
    className="card",
)
graph2 = html.Div(
    children=dcc.Graph(
        id="actions",
        config={"displayModeBar": False},
        figure={
            "data": [
                {
                    "x": data["data"],
                    "y": data["dollar_curs"],
                    "type": "lines",
                    "hovertemplate": (
                        "₽%{y:.2f}<extra></extra>"
                    ),
                    "name": "Тиньков"
                },
                {
                    "x": data["data"],
                    "y": data["euro_curs"],
                    "type": "lines",
                    "hovertemplate": (
                        "₽%{y:.2f}<extra></extra>"
                    ),
                    "name": "КекДжиДрайв"
                },
                {
                    "x": data["data"],
                    "y": data["yuan_curs"],
                    "type": "lines",
                    "hovertemplate": (
                        "₽%{y:.2f}<extra></extra>"
                    ),
                    "name": "Насонафнаф"
                },
                {
                    "x": data["data"],
                    "y": data["pound_curs"],
                    "type": "lines",
                    "hovertemplate": (
                        "₽%{y:.2f}<extra></extra>"
                    ),
                    "name": "Овощи"
                }
            ],
            "layout": {
                "title": {
                    "text": "Ацкии компаний",
                    "x": 0.05,
                    "xanchor": "left",
                },
                "xaxis": {"fixedrange": True},
                "yaxis": {
                    "tickprefix": "₽",
                    "fixedrange": True,
                },
                "colorway": ["#17b897", "red", "blue", "green"],
            },
        },
    ),
    className="card",
)
graph3 = html.Div(
    children=dcc.Graph(
        id="rate",
        config={"displayModeBar": False},
        figure={
            "data": [
                {
                    "x": data["data"],
                    "y": data["inflation"],
                    "type": "lines",
                    "hovertemplate": (
                        "%{y:.2f}%<extra></extra>"
                    ),
                    "name": "Инфляция"
                },
                {
                    "x": data["data"],
                    "y": data["rate"],
                    "type": "lines",
                    "hovertemplate": (
                        "%{y:.2f}%<extra></extra>"
                    ),
                    "name": "Ключевая ставка"
                }
            ],
            "layout": {
                "title": {
                    "text": "Ключевая ставка ЦБ",
                    "x": 0.05,
                    "xanchor": "left",
                },
                "xaxis": {"fixedrange": True},
                "yaxis": {
                    "tickprefix": "%",
                    "fixedrange": True,
                },
                "colorway": ["#17b897", "red", "blue", "green"],
            },
        },
    ),
    className="card",
)
graph4 = html.Div(
    children=dcc.Graph(
        id="preds-graph",
        config={"displayModeBar": False},
        figure={
            "data": [],
            "layout": {
                "title": {
                    "text": "Предсказания",
                    "x": 0.05,
                    "xanchor": "left",
                },
                "xaxis": {"fixedrange": True},
                "yaxis": {
                    "tickprefix": "₽",
                    "fixedrange": True,
                },
                "colorway": ["#17b897", "red", "blue", "green"],
            },
        },
    ),
    className="card",
)
menu = html.Div(
    children=[
        html.Div(
            children=[
                html.Div(children="Тип", className="menu-title"),
                dcc.Checklist(
                    id="type-filter",
                    options=types,
                    className="checklist",
                    value=[]
                ),
            ],
        ),
        # html.Div(
        #     children=[
        #         html.Div(children="Предсказания", className="menu-title"),
        #         dcc.Checklist(
        #             id="preds-type-filter",
        #             options=types,
        #             className="checklist"
        #         ),
        #     ],
        # ),
        html.Div(
            children=[
                html.Div(
                    children="Даты", className="menu-title"
                ),
                dcc.DatePickerRange(
                    id="date-range",
                    min_date_allowed=data["data"].min().date(),
                    max_date_allowed=data["data"].max().date(),
                    start_date=data["data"].min().date(),
                    end_date=data["data"].max().date(),
                ),
            ]
        ),
        html.Button('Скачать данные', id='price-button'),
        dcc.Download(id="price-download")
    ],
    className="menu",
)
second_menu = html.Div(
    children=[
        html.Div(
            children=[
                html.Div(children="Type", className="menu-title"),
                dcc.Dropdown(
                    id="action-filter",
                    options=act_types,
                    value="none",
                    clearable=False,
                    className="dropdown",
                ),
            ],
        ),
        # html.Div(
        #     children=[
        #         html.Div(children="Предсказания", className="menu-title"),
        #         dcc.Dropdown(
        #             id="preds-action-filter",
        #             options=[
        #                 {"label": "Да", 'value': "yes"},
        #                 {"label": "Нет", 'value': "no"}
        #             ],
        #             value="no",
        #             clearable=False,
        #             className="dropdown",
        #         ),
        #     ],
        # ),
        html.Div(
            children=[
                html.Div(
                    children="Date Range", className="menu-title"
                ),
                dcc.DatePickerRange(
                    id="act-date-range",
                    min_date_allowed=act_data["begin"].min().date(),
                    max_date_allowed=act_data["begin"].max().date(),
                    start_date=act_data["begin"].min().date(),
                    end_date=act_data["begin"].max().date(),
                ),
            ]
        ),
        html.Button('Скачать данные', id='acts-button'),
        dcc.Download(id="acts-download"),
    ],
    className="children-menu",
)

third_menu = html.Div(
    children=[
        html.Div(
            children=[
                html.Div(children="Type", className="menu-title"),
                dcc.Checklist(
                    id="rate-type-filter",
                    options=rate_types,
                    className="checklist",
                    value=[]
                ),
            ],
        ),
        # html.Div(
        #     children=[
        #         html.Div(children="Предсказания", className="menu-title"),
        #         dcc.Checklist(
        #             id="preds-rate-type-filter",
        #             options=rate_types,
        #             className="checklist"
        #         ),
        #     ],
        # ),
        html.Div(
            children=[
                html.Div(
                    children="Date Range", className="menu-title"
                ),
                dcc.DatePickerRange(
                    id="rate-date-range",
                    min_date_allowed=data["data"].min().date(),
                    max_date_allowed=data["data"].max().date(),
                    start_date=data["data"].min().date(),
                    end_date=data["data"].max().date(),
                ),
            ]
        ),
        html.Button('Скачать данные', id='rate-button'),
        dcc.Download(id="rate-download")
    ],
    className="children-menu",
)
wrapper = html.Div(
    children=[
        graph1
    ],
    className="wrapper",
)
wrapper2 = html.Div(
    children=[
        graph2
    ],
    className="wrapper"
)
wrapper3 = html.Div(
    children=[
        graph3
    ],
    className="wrapper"
)

wrapper4 = html.Div(
    children=[
        graph4
    ],
    className="wrapper"
)
form = html.Div(
    children=[
        html.Div(
            children=[
                html.Div(children="Type", className="menu-title"),
                dcc.Dropdown(
                    id="preds-type-filter",
                    options=act_types,
                    className="checklist",
                    value=[],
                    placeholder="Выберите объект"
                )
            ],
        ),
        dcc.Input(
            id='count-input',
            type='number',
            placeholder='Введите количество'
        ),
        html.Button('Скачать данные', id='preds-button'),
        dcc.Download(id="preds-download")
    ],
    className="children-menu",
)
app.layout = html.Div(
    children=[
        header,
        menu,
        wrapper,
        second_menu,
        wrapper2,
        third_menu,
        wrapper3,
        form,
        wrapper4
    ]
)


@app.callback(
    Output("preds-graph", 'figure'),
    Input('preds-button', 'n_clicks'),
    Input('preds-type-filter', 'value'),
    Input('count-input', 'value')
)
def get_preds(n_clicks, pred_type, count):
    ctx = callback_context
    print(n_clicks, pred_type, count)
    # pred_type = value[0]
    # count = value[1]
    # if not ctx.triggered or n_clicks is None:
    #     return
    if pred_type == '' or not pred_type or pred_type is None:
        return
    if count is None or count == "" or not str(count).isdigit():
        return
    count = int(count)
    if count <= 0:
        return
    preds = requests.post(
        "http://api:9462/model/api/v1/get_preds/",
        json={
            "value": pred_type,
            "steps": count
        }
    )
    preds = preds.json()["result"]
    date_range = list(map(lambda x: str(x.strftime('%Y-%d-%m')), pd.date_range(datetime.today().date(), periods=count).tolist()))
    data3 = pd.DataFrame()
    data3['date'] = date_range
    data3['preds'] = preds

    callback_context.response.set_cookie('last-preds', ";".join(map(str, preds)))

    price = {
        "data": [
            {
                "x": data3["date"],
                "y": data3['preds'],
                "type": "lines",
                "hovertemplate": (
                    "%{y:.2f}%<extra></extra>"
                ),
                "name": "Инфляция"
            },
        ],
        "layout": {
            "title": {
                "text": "Ключевая ставка ЦБ",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {
                "tickprefix": "%",
                "fixedrange": True,
            },
            "colorway": ["#17b897", "red", "blue", "green"],
        }
    }
    return price


@app.callback(
    Output("price", "figure"),
    [Output("type-filter", "value")],
    [Input(f"type-filter", "value")],
    # [Input("preds-type-filter", "value")],
    Input("date-range", "start_date"),
    Input("date-range", "end_date"),
)
def update_charts(value, start_date, end_date):
    if not value:
        cookie = request.cookies.to_dict()
        if len(cookie.keys()) != 0:
            value = cookie["price-value"].split(";")
            start_date = cookie["price-start-date"]
            end_date = cookie["price-end-date"]
        else:
            value = ["dollar_curs"]
            callback_context.response.set_cookie('price-start-date', start_date)
            callback_context.response.set_cookie('price-end-date', end_date)
            callback_context.response.set_cookie('price-value', ";".join(value))
    else:
        callback_context.response.set_cookie('price-start-date', start_date)
        callback_context.response.set_cookie('price-end-date', end_date)
        callback_context.response.set_cookie('price-value', ";".join(value))
    filtered_data = data.loc[
        (data.data >= start_date) & (data.data <= end_date)
        ]

    price_data = []
    for i in value:
        label = ""
        for j in range(len(types)):
            if types[j]["value"] == i:
                label = types[j]["label"]
                break
        price_data.append(
            {
                "x": filtered_data["data"],
                "y": filtered_data[i],
                "type": "lines",
                "hovertemplate": (
                    "₽%{y:.2f}<extra></extra>"
                ),
                "name": label
            }
        )
    price = {
        "data": price_data,
        "layout": {
            "title": {
                "text": "Курсы валют",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {
                "tickprefix": "₽",
                "fixedrange": True,
            },
            "colorway": ["#17b897", "blue", "red", "yellow", "green"],
        },
    }
    # print(price)
    return price, [i["value"] for i in types if i["value"] in value]


@app.callback(
    Output("rate", "figure"),
    [Output("rate-type-filter", "value")],
    [Input("rate-type-filter", "value")],
    Input("rate-date-range", "start_date"),
    Input("rate-date-range", "end_date"),
)
def update_rate(value, start_date, end_date):
    if not value:
        cookie = request.cookies.to_dict()
        if len(cookie.keys()) != 0:
            value = cookie["rate-value"].split(";")
            start_date = cookie["rate-start-date"]
            end_date = cookie["rate-end-date"]
        else:
            value = ["rate", "inflation"]
            callback_context.response.set_cookie('rate-start-date', start_date)
            callback_context.response.set_cookie('rate-end-date', end_date)
            callback_context.response.set_cookie('rate-value', ";".join(value))
    else:
        callback_context.response.set_cookie('rate-start-date', start_date)
        callback_context.response.set_cookie('rate-end-date', end_date)
        callback_context.response.set_cookie('rate-value', ";".join(value))

    filtered_data = data.loc[
        (data.data >= start_date) & (data.data <= end_date)
        ]
    callback_context.response.set_cookie('rate-start-date', start_date)
    callback_context.response.set_cookie('rate-end-date', end_date)
    callback_context.response.set_cookie('rate-value', ";".join(value))

    rate_data = []
    for i in value:
        label = ""
        for j in range(len(rate_types)):
            if rate_types[j]["value"] == i:
                label = rate_types[j]["label"]
                break
        rate_data.append(
            {
                "x": filtered_data["data"],
                "y": filtered_data[i],
                "type": "lines",
                "hovertemplate": (
                    "%{y:.2f}%<extra></extra>"
                ),
                "name": label
            }
        )
    rate = {
        "data": rate_data,
        "layout": {
            "title": {
                "text": "Ключевая ставка",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {
                "tickprefix": "%",
                "fixedrange": True,
            },
            "colorway": ["#17b897", "blue", "red", "yellow", "green"],
        },
    }
    return rate, [i["value"] for i in rate_types if i["value"] in value]


@app.callback(
    Output("actions", "figure"),
    Output("action-filter", "value"),
    Input("action-filter", "value"),
    Input("act-date-range", "start_date"),
    Input("act-date-range", "end_date")
)
def update_action(value, start_date, end_date):
    if value == "none":
        cookie = request.cookies.to_dict()
        if len(cookie.keys()) != 0:
            value = cookie["actions-value"]
            start_date = cookie["actions-start-date"]
            end_date = cookie["actions-end-date"]
        else:
            value = "YNDX"
            callback_context.response.set_cookie('actions-start-date', start_date)
            callback_context.response.set_cookie('actions-end-date', end_date)
            callback_context.response.set_cookie('actions-value', value)
    else:
        callback_context.response.set_cookie('actions-start-date', start_date)
        callback_context.response.set_cookie('actions-end-date', end_date)
        callback_context.response.set_cookie('actions-value', value)
    filtered_data = act_data.loc[
        (act_data.begin >= start_date) & (act_data.begin <= end_date)
        ]

    act_name = ""
    for i in act_types:
        if i["value"] == value:
            act_name = i["label"]

    callback_context.response.set_cookie('actions-start-date', start_date)
    callback_context.response.set_cookie('actions-end-date', end_date)
    callback_context.response.set_cookie('actions-value', value)

    rate_data = [{
        "x": filtered_data["begin"],
        "y": filtered_data[value],
        "type": "lines",
        "hovertemplate": (
            "₽%{y:.2f}<extra></extra>"
        ),
        "name": act_name
    }]
    rate = {
        "data": rate_data,
        "layout": {
            "title": {
                "text": f"Цена акции компании {act_name}",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {
                "tickprefix": "₽",
                "fixedrange": True,
            },
            "colorway": ["#17b897", "blue", "red", "yellow", "green"],
        },
    }

    return rate, [i["value"] for i in act_types if i["value"] == value][0]


@app.callback(
    Output("acts-download", "data"),
    Input("acts-button", "n_clicks"),
)
def acts_download(n_clicks):
    ctx = callback_context
    cookies = request.cookies.to_dict()
    if not ctx.triggered or n_clicks is None:
        return

    download_acts = act_data.loc[
        (act_data.begin >= cookies["actions-start-date"]) & (act_data.begin <= cookies["actions-end-date"])
        ][["begin"] + [cookies["actions-value"]]]

    return dict(content=download_acts.to_csv(index=False), filename="acts.csv")


@app.callback(
    Output("rate-download", "data"),
    Input("rate-button", "n_clicks"),
)
def rate_download(n_clicks):
    ctx = callback_context
    cookies = request.cookies.to_dict()
    if not ctx.triggered or n_clicks is None:
        return

    download_acts = data.loc[
        (data.data >= cookies["rate-start-date"]) & (data.data <= cookies["rate-end-date"])
        ][["data"] + cookies["rate-value"].split(";")]

    return dict(content=download_acts.to_csv(index=False), filename="rate.csv")


@app.callback(
    Output("preds-download", "data"),
    Input("preds-button", "n_clicks"),
)
def preds_download(n_clicks):
    ctx = callback_context
    cookies = request.cookies.to_dict()
    if not ctx.triggered or n_clicks is None:
        return

    d_data = pd.DataFrame()
    d_data["preds"] = cookies["last-preds"].split(";")

    return dict(content=d_data.to_csv(index=False), filename="rate.csv")


@app.callback(
    Output("price-download", "data"),
    Input("price-button", "n_clicks"),
)
def price_download(n_clicks):
    ctx = callback_context
    cookies = request.cookies.to_dict()
    if not ctx.triggered or n_clicks is None:
        return

    download_acts = data.loc[
        (data.data >= cookies["price-start-date"]) & (data.data <= cookies["price-end-date"])
        ][["data"] + cookies["price-value"].split(";")]

    return dict(content=download_acts.to_csv(index=False), filename="price.csv")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='flask data')

    parser.add_argument('--host', help='host', default='0.0.0.0')
    parser.add_argument('--port', help='port', type=int, default=5001)
    parser.add_argument('--debug', help='debug', type=bool, default=True)
    args = parser.parse_args()

    app.run_server(host=args.host, port=args.port, debug=args.debug)

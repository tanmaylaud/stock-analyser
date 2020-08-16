import finnhub as fin
import pandas as pd
import streamlit as st
from bokeh.models.tools import HoverTool
import os
import random

finnhub_client = fin.Client(api_key=os.environ['FINHUB_API_KEY'])

# Stock candles

# Get the latest stock data from finnhub for given date range


@st.cache(show_spinner=False)
def get_initial_symbol():
    return random.choice(['GOOG', 'AMZN', 'AAPL', 'TSLA'])


@st.cache(show_spinner=False)
def get_stock_candles(code, resolution, start, end):
    return finnhub_client.stock_candles(code, resolution, start, end)

# Get the latest prices from finnhub for given date range


@st.cache(show_spinner=False)
def get_price(code, resolution, start, end):
    df = pd.DataFrame(get_stock_candles(
        code, resolution, start, end))
    df.set_index('t')
    df.t = pd.to_datetime(df.t, unit='s')
    return df

# Get the latest volumes from finnhub for given date range


@st.cache(show_spinner=False)
def get_volume(code, resolution, start, end):
    df = pd.DataFrame(get_stock_candles(
        code, resolution, start, end))
    df.set_index('t')
    df.t = pd.to_datetime(df.t, unit='s')
    return df[['v', 't']]


@st.cache(show_spinner=False)
def get_symbols(exchange='US'):
    symbols = finnhub_client.stock_symbols(exchange)
    if len(symbols) != 0:
        print('received symbols')
        return pd.DataFrame(symbols)
    return None


def is_valid_symbol(symbol) -> bool:
    symbols = get_symbols()
    print(symbols)
    return symbol in list(symbols['displaySymbol'])


def get_symbol_info(symbol) -> bool:
    symbols = get_symbols()
    df = symbols[symbols['displaySymbol'] == symbol].set_index(
        'description').drop(columns='displaySymbol')
    df.columns = ['Currency', 'Symbol', 'Type']
    return df


@st.cache(show_spinner=False)
def get_company_profile(symbol):
    profile = finnhub_client.company_profile2(symbol=symbol)
    if len(profile) == 0:
        return pd.DataFrame(), None
    json = pd.json_normalize(profile)
    df = pd.DataFrame(
        json, columns=['exchange', 'finnhubIndustry', 'marketCapitalization'])
    df.columns = ['Exchange', 'Industry', 'Market Cap']
    df = df.set_index('Exchange')
    return df, json.logo[0]


def get_hover_tool():
    TOOLTIPS = [
        ("Date", "$x{%F}"),
        ("y", "$y{^-09.3f}"),
    ]
    return HoverTool(
        tooltips=TOOLTIPS,

        formatters={
            '$x': 'datetime',  # use 'datetime' formatter for '@date' field
            # use default 'numeral' formatter for other fields
        },
    )

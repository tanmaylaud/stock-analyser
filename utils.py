import finnhub as fin
import pandas as pd
import streamlit as st
import os
finnhub_client = fin.Client(api_key=os.environ['FINHUB_API_KEY'])

# Stock candles

# Get the latest stock data from finnhub for given date range


@st.cache
def get_stock_candles(code, resolution, start, end):
    return finnhub_client.stock_candles(code, resolution, start, end)

# Get the latest prices from finnhub for given date range


@st.cache
def get_price(code, resolution, start, end):
    df = pd.DataFrame(get_stock_candles(
        code, resolution, start, end))
    df.set_index('t')
    df.t = pd.to_datetime(df.t, unit='s')
    return df

# Get the latest volumes from finnhub for given date range


@st.cache
def get_volume(code, resolution, start, end):
    df = pd.DataFrame(get_stock_candles(
        code, resolution, start, end))
    df.set_index('t')
    df.t = pd.to_datetime(df.t, unit='s')
    return df[['v', 't']]


@st.cache
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
    return symbols[symbols['displaySymbol'] == symbol].set_index('description')

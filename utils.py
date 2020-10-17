import finnhub as fin
import pandas as pd
import streamlit as st

import os
import random

finnhub_client = fin.Client(api_key='bsrptnv48v6tucpgjv7g')

# Stock candles

# Get the latest stock data from finnhub for given date range


@st.cache(show_spinner=False)
def get_initial_symbol():
    return random.choice(['GOOG', 'AMZN', 'AAPL', 'TSLA'])


@st.cache(show_spinner=False)
def get_candles(code, resolution, start, end, isCrypto):
    if isCrypto:
        return finnhub_client.crypto_candles(code, resolution, start, end)
    return finnhub_client.stock_candles(code, resolution, start, end)


@st.cache(show_spinner=False)
def get_crypto_symbols():
    return pd.DataFrame(finnhub_client.crypto_symbols('BINANCE'))


@st.cache(show_spinner=False)
def get_stock_symbols(exchange='US'):
    symbols = finnhub_client.stock_symbols(exchange)
    if len(symbols) != 0:
        print('received symbols')
        return pd.DataFrame(symbols)
    return None

# Get the latest prices from finnhub for given date range


@st.cache(show_spinner=False)
def get_price(code, isCrypto, resolution, start, end):
    df = pd.DataFrame(get_candles(
        code, resolution, start, end, isCrypto))
    df.set_index('t')
    df.t = pd.to_datetime(df.t, unit='s')
    return df

# Get the latest volumes from finnhub for given date range


@st.cache(show_spinner=False)
def get_volume(code, isCrypto, resolution, start, end):
    df = pd.DataFrame(get_candles(
        code, resolution, start, end, isCrypto))
    df.set_index('t')
    df.t = pd.to_datetime(df.t, unit='s')
    return df[['v', 't']]


def get_symbols(isCrypto):
    symbols = None
    if isCrypto:
        symbols = get_crypto_symbols()
    else:
        symbols = get_stock_symbols()
    return symbols


def is_valid_symbol(symbol, isCrypto) -> bool:
    symbols = get_symbols(isCrypto)
    return symbol in list(symbols[get_symbol_column(isCrypto)])


def get_symbol_info(symbol, isCrypto) -> bool:
    symbols = get_symbols(isCrypto)
    df = symbols[symbols[get_symbol_column(isCrypto)] == symbol].set_index(
        'description').drop(columns='displaySymbol')
    print(df)
    if len(df.columns) == 3:
        df.columns = ['Currency', 'Symbol', 'Type']
    return df


def get_symbol_column(isCrypto):
    if isCrypto:
        return 'symbol'
    return 'displaySymbol'


@ st.cache(show_spinner=False)
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

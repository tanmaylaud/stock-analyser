# Description: This is a stock market dashboard to show some charts and data on some stock

# Import the libraries
from bokeh.plotting import figure
import streamlit as st
import pandas as pd
from PIL import Image
from utils import *
from charts import get_price_chart, get_volume_chart
from datetime import datetime as dt, timedelta
import random
MAX_DATE_RANGE = 365*10
today = dt.now().replace(second=0, microsecond=0)


def get_symbol(isCrypto):
    if isCrypto:
        return st.sidebar.selectbox('Select Coin', options=get_crypto_symbols()['symbol'])
    return st.sidebar.text_input(
        'Input Ticker (eg. GOOG,AAPL,AMZN)', value=get_initial_symbol()).upper()


# Adding title and image
st.title("Stock Price Analyser")
st.write("""
   <----** Provide ticker/symbol as input**
""")

#image = Image.open()
#st.image(image, use_column_width=True)

st.sidebar.header('Stockkerr')
category = st.sidebar.radio('Select Category', ['Stocks', 'Crypto'], index=0)
print(category)
isCrypto = category == 'Crypto'
print(isCrypto)
symbol = get_symbol(isCrypto)

start_input = st.sidebar.slider(
    'Select Date Range',
    min_value=today - timedelta(MAX_DATE_RANGE),
    max_value=today-timedelta(5),
    value=today-timedelta(400))

st.sidebar.markdown('Start Date:' + start_input.strftime("%m/%d/%Y"))

end_input = st.sidebar.slider(
    'Select Date Range',
    min_value=today-timedelta(MAX_DATE_RANGE+50),
    max_value=today,
    value=today)


st.sidebar.markdown('End Date:' + end_input.strftime("%m/%d/%Y"))

displayO = st.sidebar.checkbox('Open Price', value=True)
displayC = st.sidebar.checkbox('Close Price')
displayH = st.sidebar.checkbox('High Price')
displayL = st.sidebar.checkbox('Low Price')

priceChartVisible = displayO or displayC or displayH or displayL

start_date = dt.timestamp(start_input)
end_date = dt.timestamp(end_input)

if is_valid_symbol(symbol, isCrypto):

    price = get_price(symbol, isCrypto, 'D', int(start_date), int(end_date))
    volumes = get_volume(symbol, isCrypto, 'D', int(start_date), int(end_date))
    company = get_symbol_info(symbol, isCrypto)
    profile, logo = get_company_profile(symbol)

    if logo:
        st.image(logo, width=40)

    st.write(company)

    if not profile.empty:
        st.write(profile)

    if priceChartVisible:
        st.write("## Stock Price")
        p = None
        p = get_price_chart(symbol, price, displayO,
                            displayC, displayL, displayH)
        st.bokeh_chart(p, use_container_width=True)

    st.write("## Stock Volume")
    v = get_volume_chart(symbol, volumes)
    st.bokeh_chart(v, use_container_width=True)

else:
    st.write("This symbol is not present in our database. Please try another symbol")

# Description: This is a stock market dashboard to show some charts and data on some stock

# Import the libraries
from bokeh.plotting import figure
import streamlit as st
import pandas as pd
from PIL import Image
from utils import get_symbols, get_price, get_volume, is_valid_symbol, get_symbol_info, get_hover_tool
from datetime import datetime as dt, timedelta

MAX_DATE_RANGE = 365*10
today = dt.now().replace(second=0, microsecond=0)

TOOLTIPS = [
    ("Date", "$x{%F}"),
    ("y", "$y{^-09.3f}"),
]

price_hover_tool = get_hover_tool()
volume_hover_tool = get_hover_tool()
# Adding title and image
st.title("Stock Price Analyser")
st.write("""
   <----** Provide ticker/symbol as input**
""")

#image = Image.open()
#st.image(image, use_column_width=True)

st.sidebar.header('User Input')


symbol = st.sidebar.text_input(
    'Input Ticker (eg. GOOG,AAPL,AMZN', value='GOOG').upper()

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
start_date = dt.timestamp(start_input)
end_date = dt.timestamp(end_input)
if is_valid_symbol(symbol):

    price = get_price(symbol, 'D', int(start_date), int(end_date))
    volumes = get_volume(symbol, 'D', int(start_date), int(end_date))
    company = get_symbol_info(symbol)

    st.write(company)
    p = figure(
        title=symbol,
        x_axis_label='Time',
        y_axis_label='Price',
        x_axis_type='datetime',
    )
    p.add_tools(price_hover_tool)
    if displayO:
        p.line(x=price['t'], y=price['o'], legend='Open Price',
               line_color='blue', line_width=2)
    if displayC:
        p.line(x=price['t'], y=price['c'],
               legend='Close Price', line_color='orange', width=2)
    if displayH:
        p.line(x=price['t'], y=price['h'], legend='High Price',
               line_color='green', line_width=2)
    if displayL:
        p.line(x=price['t'], y=price['l'], legend='Low Price',
               line_color='red', line_width=2)

    st.write("## Stock Price")

    st.bokeh_chart(p, use_container_width=True)

    v = figure(
        title=symbol,
        x_axis_label='Time',
        y_axis_label='Volume',
        x_axis_type='datetime')
    v.add_tools(volume_hover_tool)
    v.line(x=volumes['t'], y=volumes['v'], legend='Volume',
           line_color='blue', line_width=2)

    st.write("## Stock Volume")
    st.bokeh_chart(v, use_container_width=True)

else:
    st.write("This symbol is not present in our database. Please try another symbol")

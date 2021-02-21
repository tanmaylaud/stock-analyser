# Welcome to Stockkerr :wave:

A python based webapp to analyse historical prices of stocks

# Link to Webapp

https://stockkerr.herokuapp.com/

# Set up Local Environment

```python
  # Create virtual environment
  virtualenv venv

  # Activate environment
  source venv/bin/activate

  # Install dependencies
  pip install -r requirements.txt
```

# Run the Streamlit app

```python
streamlit run StockWebapp.py

# App launching on port 8051...
```

# Libraries

| Name           | Type   | Description                                                                                                                                                                                                          |
| -------------- | ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| bokeh          | 2.1.1  | Bokeh is an interactive visualization library for modern web browsers. It provides elegant, concise construction of versatile graphics, and affords high-performance interactivity over large or streaming datasets. |
| numpy          | 1.19.1 | Powerful n-dimensional arrays                                                                                                                                                                                        |
| pandas         | 1.1.0  | Data Manipulation and Analysis                                                                                                                                                                                       |
| streamlit      | 0.65.2 | Open-source app framework for Machine Learning and Data Science teams. Create beautiful data apps in hours, not weeks. All in pure Python.                                                                           |
| finnhub-python | 2.2.0  | Free stock API for realtime market data, global company fundamentals, economic data, and alternative data.                                                                                                           |

# License

Licensed under the [GNU General Public License v3.0](https://github.com/tanmaylaud/stock-analyser/blob/master/LICENSE)

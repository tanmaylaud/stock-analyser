from bokeh.plotting import figure
from bokeh.models.tools import HoverTool


def get_hover_tool(id):
    TOOLTIPS = [
        ("Date", "$x{%F}"),
        ("y", "$y{^-09.3f}"),
    ]
    return HoverTool(
        tooltips=TOOLTIPS,
        id=id,
        formatters={
            '$x': 'datetime',  # use 'datetime' formatter for '@date' field
            # use default 'numeral' formatter for other fields
        },
    )


def get_price_chart(symbol, price, displayO, displayC, displayL, displayH):
    price_hover_tool = get_hover_tool('price')
    p = figure(
        title=symbol,
        x_axis_label='Time',
        y_axis_label='Price ($)',
        x_axis_type='datetime',
    )
    p.add_tools(price_hover_tool)
    if displayO:
        p.line(x=price['t'], y=price['o'], legend_label='Open Price',
               line_color='blue', line_width=2)
    if displayC:
        p.line(x=price['t'], y=price['c'],
               legend_label='Close Price', line_color='orange', width=2)
    if displayH:
        p.line(x=price['t'], y=price['h'], legend_label='High Price',
               line_color='green', line_width=2)
    if displayL:
        p.line(x=price['t'], y=price['l'], legend_label='Low Price',
               line_color='red', line_width=2)
    return p


def get_volume_chart(symbol, volumes):
    volume_hover_tool = get_hover_tool('volume')
    v = figure(
        title=symbol,
        x_axis_label='Time',
        y_axis_label='Volume',
        x_axis_type='datetime')
    v.add_tools(volume_hover_tool)
    v.line(x=volumes['t'], y=volumes['v'], legend_label='Volume',
           line_color='blue', line_width=2)
    return v

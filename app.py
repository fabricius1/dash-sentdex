import pandas_datareader.data as web
import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input

app = dash.Dash()

stock = 'TSLA'


app.layout = html.Div(children=[
    html.H1(children='Dashboard Example'),

    html.Div(children='''
        Stocks line graph
    '''),

    dcc.Input(id='input', value='', type='text'),
    html.Div(id='output-graph')

])


@ app.callback(Output('output-graph', 'children'),
               [Input('input', 'value')])
def update_graph(symbol):
    start = datetime.datetime(2010, 1, 1)
    end = datetime.datetime.now()
    df = web.DataReader(symbol, 'yahoo', start, end)
    df.reset_index(inplace=True)
    df.set_index("Date", inplace=True)
    if "Symbol" in df.columns:
        df = df.drop("Symbol", axis=1)

    return dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': df.index, 'y': df.Close, 'type': 'line', 'name': stock},
            ],
            'layout': {
                'title': f'{symbol} stocks'
            }
        }
    )


if __name__ == '__main__':
    app.run_server(debug=True)

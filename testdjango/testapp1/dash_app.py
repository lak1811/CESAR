import dash
from dash import dcc
from dash import html
def appen():
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    app.layout = html.Div(children=[
        html.H1(children='Hello Dash'),

        html.Div(children='''
            Dash: A web application framework for Python.
        '''),

        dcc.Graph(
            id='example-graph',
            # figure=fig  # commented out to make the example runnable
        ),

        
    ])

    if __name__ == '__main__':
        app.run_server(debug=True, port=8049, host='127.0.0.1')

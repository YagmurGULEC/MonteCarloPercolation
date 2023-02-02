
from dash import Dash, html, dcc, Input, Output, ctx, State, dash_table
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
from dash.exceptions import PreventUpdate
from percolation import Percolation
import plotly.graph_objects as go
from percolationstats import collectstats
import json
import time
import numpy as np

app = Dash(__name__,
           external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
           meta_tags=[
               {"name": "viewport", "content": "width=device-width, initial-scale=1"}
           ]
           )

server = app.server
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [

                        dbc.Col(dbc.NavbarBrand(
                            "Plotly Dash App for Monte Carlo Simulation for Percolation", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="#",
                style={"textDecoration": "none"},
            ),
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        html.I(className="bi bi-github icon"),

                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://github.com/YagmurGULEC/MonteCarloPercolation",
                style={"textDecoration": "none"},
            ),
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        html.I(className="bi bi-linkedin icon"),

                    ],
                    align="center",
                    className="g-1",
                ),
                href="https://www.linkedin.com/in/ya%C4%9Fmur-g%C3%BCle%C3%A7-a52111204/",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),

        ]
    ),
    color="dark",
    dark=True,
)

# all inputs to be constructed from dictionary in a loop
row_1 = [{'value': 10, 'id': 'nrows', 'placeholder': 'Number of rows',
          'className': 'inputs', 'type': 'number'},
         {'value': 10, 'id': 'ncols', 'className': 'inputs',
             'placeholder': 'Number of columns', 'type': 'number'},
         {'value': 0.6, 'id': 'prob', 'className': 'inputs',
             'min': 0.0, 'max': 1.0, 'placeholder': 'Site vacancy probability', 'type': 'number'},
         {'value': 1000, 'id': 'no_trials', 'className': 'inputs',
             'placeholder': 'Trials', 'type': 'number'},
         {'value': 0.1, 'id': 'prob_interval', 'className': 'inputs',
          'placeholder': 'Probability interval', 'type': 'number'},

         ]


row_content = [
    dbc.Row([html.H6(i['placeholder']), dcc.Input(**i)],
            className="row justify-content-md-center mx-3")
    for i in row_1[0:3]

]
row_content.append(dbc.Row([html.H4(""), html.Button(
    'Run simulation', id='run', n_clicks=0, className="btn btn-primary")], className="row justify-content-md-center mx-3"))

row_content_2 = [
    dbc.Row([html.H6(i['placeholder']), dcc.Input(**i)],
            className="row justify-content-md-center mx-3")
    for i in row_1[3:5]

]
row_content_2.append(dbc.Row([html.H4(""), html.Button(
    'Add', id='trial', n_clicks=0, className="btn btn-primary")], className="row justify-content-md-center mx-3"))
row_content_2.append(dbc.Row([html.H4(""), html.Button(
    'Plot statistics', id='statistics', n_clicks=0, className="btn btn-primary")], className="row justify-content-md-center mx-3"))


# application layout
def serve_layout():

    return html.Div(children=[

        navbar,
        dbc.Container(
            [
                dbc.Col(
                    row_content,
                    className="row justify-content-md-center mb-3 col1"

                ),
                dbc.Col(
                    className="row", id="heatmap")
            ], className='mt-3 div1'),

        dbc.Container(
            [

                dbc.Col(
                    row_content_2,
                    className=""

                ),
                dbc.Col(
                    [html.Div(
                        id="div-storage",
                        children=json.dumps(
                            {"action_stack": []}
                        ),
                    ),
                    ],
                    id="percplot",
                    className="row")
            ], className='container  mt-3 mb-3 div1'),
        dbc.Container(id='statistical_plot'),
    ],)


app.layout = serve_layout()


@ app.callback(
    Output('heatmap', 'children'),
    State('nrows', 'value'),
    State('ncols', 'value'),
    State('prob', 'value'),
    Input('run', 'n_clicks'),
)
def create_simulation(nrows, ncols,  p, n_clicks):

    p = Percolation(nrows=nrows, ncols=ncols, prob=p)
    p.open_sites()
    if p.percolates():

        title = 'Percolates'
    else:
        title = 'Does not percolate'

    fig = px.imshow(p.open, color_continuous_scale='gray')

    fig.update_layout(
        xaxis=dict(showticklabels=False),
        yaxis=dict(showticklabels=False),
        coloraxis_showscale=False,
        showlegend=False,

        autosize=False
    )
    fig.add_annotation(dict(font=dict(color="black", size=18),

                            x=0.5, y=-0.2,
                            text="bottom",
                            xref='paper',
                            yref='paper',
                            showarrow=False),
                       )
    fig.add_annotation(dict(font=dict(color="black", size=18),

                            x=0.5, y=1.2,
                            text="top",
                            xref='paper',
                            yref='paper',
                            showarrow=False),
                       )

    return [html.H6(title, className="text-center"), dcc.Graph(className="plot", figure=fig)]


@ app.callback(
    Output('percplot', 'children'),
    State('nrows', 'value'),
    State('ncols', 'value'),
    State('prob', 'value'),
    State('no_trials', 'value'),
    State('prob_interval', 'value'),
    State('div-storage', 'children'),
    Input('trial', 'n_clicks'),
)
def run_trial(nrows, ncols,  p, trial, dp, storage, n_clicks):
    d = dict(nrows=nrows, ncols=ncols, trials=trial, dp=dp)
    start_time = time.time()
    data = collectstats(**d)
    stop_time = time.time()
    storage = json.loads(storage)
    table = storage['action_stack']

    d['execution_time'] = stop_time-start_time
    d['data'] = data
    keys_to_extract = ['nrows', 'ncols', 'dp', 'trials']
    is_same = False
    if len(table) > 0:
        dict_compare = dict(
            filter(lambda item: item[0] in keys_to_extract, d.items()))
        for i in table:
            res = dict(
                filter(lambda item: item[0] in keys_to_extract, i.items()))
            isSame = (res == dict_compare)
            if (isSame == True):
                break
        if (isSame == False):
            table.append(d)

    else:
        table.append(d)

    df = pd.DataFrame(table)
    df.drop(columns=['data'], inplace=True)
    return [
        dbc.Table.from_dataframe(
            df, striped=True, bordered=True, hover=True, id="table"),
        html.Div(
            id="div-storage", children=json.dumps(storage)
        ),
    ]


# plot percolation statistics
@ app.callback(
    Output('statistical_plot', 'children'),
    State('div-storage', 'children'),
    Input('statistics', 'n_clicks'),
)
def percolation_plot(storage, n_clicks):
    storage = json.loads(storage)
    fig = go.Figure()
    for i in storage['action_stack']:
        probability = np.linspace(0, 1, len(i['data']), endpoint=True)
        fig.add_traces(
            go.Scatter(x=probability, y=i['data'], name="Trials {} nrows {} and ncols {}, prob. {}".format(
                i['trials'], i['nrows'], i['ncols'], i['dp']))
        )

    fig.add_vline(x=0.593)
    fig.update_layout(

        xaxis_title="Site vacancy probability",
        yaxis_title="Percolation probability",
    )
    return [dcc.Graph(figure=fig)]


if __name__ == "__main__":
    app.run_server(debug=False)

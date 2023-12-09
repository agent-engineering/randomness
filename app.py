#!/usr/bin/env/python
# -*- coding: utf-8 -*-
"""
    __author__: archie
    Created Date: Tue, 28 Mar 2023; 22:24:47
"""
import hashlib
import random
import time

import dash_bootstrap_components as dbc
import pandas as pd
from config import neetCode
from dash import Dash, dash_table, dcc, html
from dash.dependencies import Input, Output, State
from utils import goWild, problemSetCombo

random.seed(518123)
df = pd.read_csv(neetCode)
# df["Star"] = df["Star"].apply(lambda x: '🥷 )

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(name=__name__, external_stylesheets=[
    dbc.themes.SLATE] + external_stylesheets)


app.layout = html.Div([
    dcc.Store(id='problemSet',
              data=df.to_dict('records')),
    dcc.Store(id='lastRandomClick',
              data=None),
    dcc.Store(id='temp',
              data=df.to_dict('records')),
    html.Div(

        className="p-3 rounded-3", style={"width": "auto", "height": "100px", "align": "centre"}
    ),

    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    [dbc.Row(
                        [
                            #     dbc.Col(dcc.Dropdown(
                            #     id="topic",
                            #     placeholder="Topic",
                            # ), width={"size": "2", "align": "centre"}
                            # ),
                            dbc.Col(
                                dcc.Dropdown(['Easy', 'Medium', 'Hard'],
                                             id='difficulty_level',
                                             searchable=False,
                                             placeholder="Select Difficulty"),

                                width={"size": "2", "align": "centre"}
                            ),
                            dbc.Col(dcc.Dropdown(["5E", "3E1M", "1E2M", "1E1M1H", "1E2M1H", "Ninja"],
                                                 id="select_problems",
                                                 searchable=False,
                                                 placeholder="Problem Set Combination"),
                                    width={"size": "2", "align": "centre"}
                                    ),
                            dbc.Col(dbc.Button("Choose Random",
                                               id="randomChoice",
                                               color="danger"),

                                    width={"size": "auto", "align": "centre"}),
                            # dbc.Col(dbc.Button("Reset",
                            #                    id="reset",
                            #                    color="primary"),

                            #         width={"size": "auto", "align": "centre"}),
                        ], justify="end",

                        style={"padding": "10px"}
                    ),
                        dash_table.DataTable(id='problem_set',
                                             data=df.to_dict(
                                                'records'),
                                             columns=[
                                                 {"name": "#",
                                                     "id": "#"},
                                                 {"name": "Status",
                                                     "id": "Status"},
                                                 {"name": "Star", "id": "Star",
                                                  "hideable": True, 'presentation': 'dropdown'},
                                                 {"name": "Problem", "id": "Problem",
                                                  'presentation': 'markdown'},
                                                 {"name": "Difficulty",
                                                  "id": "Difficulty", "hideable": True},
                                                 {"name": "Score", "id": "Score"},
                                                 {"name": "Category",
                                                  "id": "Category", "hideable": True},
                                                 {"name": "Pattern",
                                                  "id": "Pattern", "hideable": True, }
                                             ],
                                             style_cell={
                                                 #  'overflow': 'hidden',
                                                 #  'textOverflow': 'ellipsis',
                                                 'whiteSpace': 'normal',
                                                 'height': 'auto',
                                                 'height': 'auto',
                                                 'color': '#2E3440',
                                                 'backgroundColor': '#D8DEE9',
                                             },
                                             style_cell_conditional=[
                                                 {'if': {'column_id': '#'},
                                                  'textAlign': 'center', "width": "5%"},
                                                 {'if': {'column_id': 'Problem'},
                                                  'textAlign': 'left', "width": "25%"},
                                                 {'if': {'column_id': 'Status'},
                                                  'textAlign': 'center'},
                                                 {'if': {'column_id': 'Star'},
                                                  'textAlign': 'center'},
                                                 {'if': {'column_id': 'Difficulty'},
                                                  'textAlign': 'center', "width": "auto"},
                                                 {'if': {'column_id': 'Score'},
                                                  'textAlign': 'right', "width": "auto"},
                                                 {'if': {'column_id': 'Category'},
                                                  'textAlign': 'left'},
                                                 {'if': {'column_id': 'Pattern'}, 'overflow': 'hidden',
                                                  'textAlign': 'left', "width": "40%",
                                                  'textOverflow': 'ellipsis', 'textAlign': 'left', 'caretPosition': 'start'}
                                             ],
                                             style_header={
                                                 'textAlign': 'center',
                                                 'color': '#ECEFF4',
                                                 'backgroundColor': '#2E3440',
                                             },
                                             style_data_conditional=[
                                                 {
                                                     "if": {"state": "selected"},
                                                     "backgroundColor": "#ECEFF4",
                                                     "border": "0px",
                                                     'textAlign': 'center'
                                                 },
                                                 {
                                                     'if': {
                                                         'filter_query': '{Status} = TODO',
                                                         'column_id': 'Status'
                                                     },
                                                     'backgroundColor': '#EBCB8B',
                                                     'color': '#2E3440',
                                                     'fontWeight': 'bold'
                                                 },
                                                 {
                                                     'if': {
                                                         'filter_query': '{Status} = REPEAT',
                                                         'column_id': 'Status'
                                                     },
                                                     'backgroundColor': '#D08770',
                                                     'color': '#2E3440',
                                                     'fontWeight': 'bold'
                                                 },
                                                 {
                                                     'if': {
                                                         'filter_query': '{Status} = DONE',
                                                         'column_id': 'Status'
                                                     },
                                                     'backgroundColor': '#A3BE8C',
                                                     'color': '#2E3440',
                                                     'fontWeight': 'bold'
                                                 },
                                                 {
                                                     'if': {
                                                         'filter_query': '{Star} = y',
                                                         'column_id': 'Status'
                                                     },
                                                     'backgroundColor': '#A3BE8C',
                                                     'color': '#2E3440',
                                                     'fontWeight': 'bold'
                                                 }
                                             ],
                                             # style_data={
                                             #     'border': '1px #D8DEE9'},
                                             editable=True,
                                             # style_as_list_view=True,
                                             #  tooltip_data=[
                                             #      {
                                             #          "Pattern": {'value': str(row["Pattern"]), 'type': 'markdown'}
                                             #      } for row in df.to_dict('records')
                                             #  ],
                                             #  tooltip_duration=None,
                                             page_current=0,
                                             page_size=30,
                                             sort_action="native",
                                             sort_mode="multi",
                                             column_selectable="single",
                                             dropdown={
                                                 'Star': {
                                                     'options': [
                                                         {'label': '🥷🏽',
                                                             'value': True},
                                                         {'label': "",
                                                             'value': False},
                                                     ]
                                                 },
                                                 #  'Status': {
                                                 #      'options': [{'label': i, 'value': i} for i in ["TODO", "REPEAT", "DONE"]]
                                                 #  }
                                             }
                                             ),
                    ],
                    className="card-body rounded-9"
                ),
                className="card-body rounded-9 shadow-lg p-3 mb-5 rounded"
            ),
            width={"size": "10", "align": "centre"}
        )
    ],
        justify="center"
    )
], )


@ app.callback(Output('temp', 'data'),
               Input('problem_set', 'data'),
               Input('temp', 'data'))
def checkCurrData(modified, df):
    df = pd.DataFrame(df)
    modified = pd.DataFrame(modified)
    print(modified)
    print(df.shape, modified.shape)
    updated = df.merge(modified, how="left", on="#",
                       suffixes=(None, "_"))[df.columns]
    # print(updated)
    prev_data_hash = hashlib.sha256(str(df).encode()).hexdigest()
    data_hash = hashlib.sha256(str(updated).encode()).hexdigest()

    if prev_data_hash == data_hash:
        return df.to_dict("records")
    return updated.to_dict("records")


@ app.callback(
    Output('problem_set', 'data'),
    Output('lastRandomClick', 'data'),
    Input("select_problems", "value"),
    Input("difficulty_level", "value"),
    Input("randomChoice", "n_clicks_timestamp"),
    State('problemSet', 'data'),
    State('lastRandomClick', 'data'))
def display_output(combo, difficulty, randomChoice, intitialData, lastRandomChoice):

    # print("second callback", pd.DataFrame(intitialData), sep="\n")
    if combo is None and difficulty is None and randomChoice == lastRandomChoice:
        return intitialData, randomChoice

    elif combo is not None:
        df = pd.DataFrame(intitialData)
        if combo != "Ninja":
            randomProbs = goWild(df, problemSetCombo[combo])
        else:
            randomProbs = goWild(df)
        return randomProbs, randomChoice

    elif difficulty is not None:
        df = pd.DataFrame(intitialData)
        df = df[df["Difficulty"] == difficulty]

        if randomChoice is not None or (lastRandomChoice is not None and lastRandomChoice < randomChoice):
            idx = [random.choice(df.index) for _ in range(5)]
            df = df.loc[idx]
            return df.to_dict("records"), randomChoice

        return df.to_dict("records"), randomChoice

    elif combo is None and randomChoice is not None:
        df = pd.DataFrame(intitialData)
        randomProbs = goWild(df)
        return randomProbs, randomChoice

    return intitialData, None


if __name__ == '__main__':
    app.run_server(debug=True)

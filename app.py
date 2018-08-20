# -*- coding: utf-8 -*-
import dash
from plotly import tools
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.figure_factory as ff
from dash.dependencies import Input, Output
import numpy as np
import json

import pandas as pd
from data_reader.DataReader import DataReader

count = 0
colors = {
    'background': '#fff',
    'text': 'rgb(77, 99, 127)'
}


# HELPER METHODS

def get_hover_data(df):
    """
    Creates and formats the hover string over the map data points
    :param df: Pandas dataframe
    :return: list: A string of dataframe row information formatted for hover.
    """
    details_labels = ["needothers","detailmed", "detailrescue"]
    hover_string_list = []
    for index, row in df.iterrows():
        info_string = row['location'] + "<br>" + "Phone:" +row['requestee_phone'] + "<br>"
        details_string_list = []
        for i in details_labels:
            if row[i]:
                details_string_list.append(i + ":" + str(row[i]).strip())
        details_string = "<br>".join(details_string_list)
        hover_string_list.append(info_string + details_string)
    return hover_string_list


# DASH APP
app = dash.Dash()
server = app.server

data_cl = DataReader('data/data.json')

def get_layout():
    layout = html.Div(style={'backgroundColor': colors['background']},
        children=[
            html.Div(
                children =[
                    html.H3(
                        children='Kerala Rescue Dashboard',
                        style={
                        'textAlign': 'left',
                        'color': colors['text'],
                        'font-family': 'Poppins',
                        }
                    ),
                    html.Div(children='  ', style={
                        'textAlign': 'left',
                        'color': colors['text'],
                    }),
                    html.Br(),
                    html.Div(
                        children=[
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            dcc.Dropdown(id='incident_dropdown',
                                                multi=True,
                                                value=['needrescue'],
                                                options=[{'label':'Need Rescue','value':'needrescue'},\
                                                 {'label':'Need Medicines','value':'needmed'},\
                                                  {'label':'Need Food & Water','value':'needfoodandwater'}]),
                                        ], className='twelve columns' )
                            ], className='row' ),

                            html.Br(),

                            html.Div([
                                dcc.RadioItems(
                                    id = 'charts_radio',
                                    options=[
                                        dict( label='All', value='All' ),
                                        dict( label='Requested within last 3 hours', value='requested_within_3_hours' ),
                                        dict( label='Requested today', value='requested_today' ),
                                        dict( label='Requested from yesterday', value='requested_yesterday' ),
                                        dict( label='Old requests', value='2_days_back' ),
                                    ],
                                    labelStyle = dict(display='inline-block'),
                                    value='All'
                                ),
                            ]),
                            html.Div(children=
                                [
                                    dcc.Graph(
                                    id='map-graph',
                                    config={
                                        'displayModeBar': False
                                        }
                                    ),
                                ],
                                className='column',
                                style = {
                                    'width' : '50%',
                                    'margin-left':'0%',
                                    'align':'center'
                                    }
                                ),
                            html.Div(children=
                                    [
                                        dcc.Graph(
                                        id='graph-bar',
                                        config={
                                            'displayModeBar': False
                                            }
                                        ),
                                    ],
                                    className='column',
                                    style = {
                                        'width' : '50%',
                                        'margin-left':'0%'
                                        }
                                    ),
                        ],
                        className='row'
                    ),
                    html.Div(
                        children=[
                            html.Div(children=
                                [
                                    dcc.Graph(
                                    id='graph-bar-2',
                                    config={
                                        'displayModeBar': False
                                        }
                                    ),
                                ],
                                className='column',
                                style = {
                                    'width' : '45%',
                                    'margin-left':'5%'
                                    }
                                ),
                            html.Div(children=
                                [
                                    dcc.Graph(
                                    id='map-graph-2',
                                    config={
                                        'displayModeBar': False
                                        }
                                    ),
                                ],
                                className='column',
                                style = {
                                    'width' : '45%',
                                    'margin-left':'5%',
                                    'align':'center'
                                    }
                                ),

                        ],
                        className='row'
                    ),
                    html.Div([
                        html.Pre(id='hover-data', style={'paddingTop':35})
                        ], style={'width':'30%'})
                    ],
                    style={
                    'padding': '5px',
                    }
                ),
            ]
        )
    return layout

app.layout = get_layout()

@app.callback(Output("map-graph", "figure"),
              [Input("incident_dropdown", "value"), Input('charts_radio', 'value')])
def update_map(dr_value, rad_value):
    df = data_cl.get_plot_data(dr_value, rad_value)
    return go.Figure(
            data=[go.Scattermapbox(
                lat=df['LatValid'].tolist(),
                lon=df['LonValid'].tolist(),
                mode='markers',
                hoverinfo='text',
                text=get_hover_data(df),
                marker=dict(
                    size=10,
                    color = 'rgba(255, 77, 77, 0.5)',
                ),
            )
            ],
        layout=go.Layout(
            autosize=True,
            height=550,
            hovermode='closest',
            margin=go.Margin(l=0, r=0, t=0),
            mapbox=dict(
                accesstoken='pk.eyJ1IjoiamFja2x1byIsImEiOiJjajNlcnh3MzEwMHZtMzNueGw3NWw5ZXF5In0.fk8k06T96Ml9CLGgKmk81w',
                bearing=0,
                style='light',
                center=dict(
                    lat='8.682756',
                    lon='76.909565',
                ),
                zoom=7
            ),
        )
    )

@app.callback(Output("graph-bar", "figure"),
              [Input("incident_dropdown", "value"), Input('charts_radio', 'value')])
def update_bar(dr_value, rad_value):
    df = data_cl.get_plot_data(dr_value, rad_value)
    d_series = df.groupby('district').count()
    d_series.sort_values(['id'], ascending=0, inplace=True)
    return go.Figure(
            data=[go.Bar(
                y=d_series['id'],
                x=list(d_series.index),
                marker={'color':'rgba(26, 118, 255, 0.5)',
                      'line':{
                        'color':'rgb(8,48,107)',
                        'width':1.5,
                        }
                }
            )
            ],
            layout=go.Layout(
                title='Requests by District (Click to see detailed location in bottom graph)',
                barmode='grouped',
                bargroupgap=0.2,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
        )

@app.callback(
    Output('graph-bar-2', 'figure'), [Input("incident_dropdown", "value"),\
     Input('charts_radio', 'value'), Input('graph-bar', 'clickData')])
def update_bar_location(dr_value, rad_value, clickData):
    district = clickData['points'][0]['x']
    df = data_cl.get_plot_per_dist(dr_value, rad_value, district)
    d_series = df.groupby('location').count()
    d_series.sort_values(['id'], ascending=0, inplace=True)
    return go.Figure(
            data=[go.Bar(
                y=d_series['id'].tolist()[0:15],
                x=list(d_series.index)[0:15],
                marker={'color':'rgba(26, 118, 255, 0.5)',
                      'line':{
                        'color':'rgb(8,48,107)',
                        'width':1.5,
                        }
                }
            )
            ],
            layout=go.Layout(
                title='Requests by Location for District Selected Above',
                barmode='grouped',
                bargroupgap=0.2,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
        )

@app.callback(Output("map-graph-2", "figure"),
              [Input("incident_dropdown", "value"), Input('charts_radio', 'value'), Input('graph-bar-2', 'clickData')])
def update_map(dr_value, rad_value, clickData):
    location = clickData['points'][0]['x']
    df = data_cl.get_plot_per_loc(dr_value, rad_value, location)
    return go.Figure(
            data=[go.Scattermapbox(
                lat=df['LatValid'].tolist(),
                lon=df['LonValid'].tolist(),
                mode='markers',
                hoverinfo='text',
                text=get_hover_data(df),
                marker=dict(
                    size=10,
                    color = 'rgba(25, 25, 25, 0.5)',
                ),
            )
            ],
        layout=go.Layout(
            title='Details mapped on geo-location (contain location details for request for others)',
            autosize=True,
            height=550,
            hovermode='closest',
            margin=go.Margin(l=10, r=10, t=30),
            mapbox=dict(
                accesstoken='pk.eyJ1IjoiamFja2x1byIsImEiOiJjajNlcnh3MzEwMHZtMzNueGw3NWw5ZXF5In0.fk8k06T96Ml9CLGgKmk81w',
                bearing=0,
                style='light',
                center=dict(
                    lat='8.682756',
                    lon='76.909565',
                ),
                zoom=6
            ),
        )
    )

external_css = ["https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",
                "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"]

for css in external_css:
    app.css.append_css({"external_url": css})

external_js = ["https://code.jquery.com/jquery-3.2.1.min.js"]

if __name__ == '__main__':
    app.run_server(debug=True)

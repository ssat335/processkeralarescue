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
from data_reader.CampDataReader import CampDataReader

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
app.config['suppress_callback_exceptions']=True

data_cl = DataReader('data/data.json')
get_updated_info = data_cl.getLastEntry()

data_relief = CampDataReader('data/camp_details/rescuecamp.csv')

def get_menu():
    menu = html.Div([

        dcc.Link('Click here for Rescue Dashboard |', href='/rescue', className="tab first", \
        style = {
            'width' : '50%',
            'margin-left':'0%',
            'font-size':'160%'
            }
        ),

        dcc.Link('| Click here for Relief Camps Dashboard ', href='/relief', className="tab", \
        style = {
            'width' : '50%',
            'margin-left':'0%',
            'align':'right',
            'font-size':'160%'
            }
        ),

    ], className="row ")
    return menu

def get_rescue():
    layout = html.Div(style={'backgroundColor': colors['background']},
        children=[

            get_menu(),
            html.Br(),
            html.Div(
                children =[
                    html.H3(
                        children='Kerala Rescue Dashboard (Data updated on ' + get_updated_info + ')',
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

def get_relief():
    relief = html.Div(style={'backgroundColor': colors['background']},
        children=[

            get_menu(),
            html.Div(
                children =[
                    html.H3(
                        children='Kerala Relief Camp Details Dashboard',
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
                                            dcc.Dropdown(id='people_type',
                                                multi=True,
                                                value=['Total people'],
                                                options=[{'label': 'All People', 'value':'Total people'}]),
                                        ], className='twelve columns' )
                            ], className='row' ),

                            html.Br(),

                            html.Div(children=
                                [
                                    dcc.Graph(
                                    id='graph-districts',
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
                                        id='graph-taluk',
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
                            html.Div([
                                    dcc.Graph(
                                    id='table-dist-details',
                                    config={
                                        'displayModeBar': False
                                        }
                                    ),
                            ],
                            className='column',
                            style = {
                                'width' : '50%',
                                'margin':'0%'
                                }
                            ),
                            html.Div(children=
                                    [
                                        dcc.Graph(
                                        id='graph-village-heatmap',
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
                        className='twelve columns',
                        style = {
                            'width' : '100%',
                            'margin-left':'0%'
                            }
                    ),

                    ],
                    style={
                    'padding': '5px',
                    }
                ),
            ]
        )
    return relief

def get_nopage():
    noPage = html.Div([  # 404

        html.P(["404 Page not found"])

    ], className="no-page")
    return noPage
# app.layout = get_rescue()

# Describe the layout, or the UI, of the app
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Update page
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/' or pathname == '/rescue':
        return get_rescue()
    elif pathname == '/relief':
        return get_relief()
    else:
        return get_nopage()


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

@app.callback(Output("graph-districts", "figure"),
              [Input("people_type", "value")])
def update_bar(dr_value):
    d_series = data_relief.get_plot_data(dr_value)
    values = d_series.sort_values(ascending=0)
    return go.Figure(
            data=[go.Bar(
                y=values,
                x=list(values.index),
                marker={'color':'rgba(26, 118, 255, 0.5)',
                      'line':{
                        'color':'rgb(8,48,107)',
                        'width':1.5,
                        }
                }
            )
            ],
            layout=go.Layout(
                title='People in Camps by District (Click to see detailed location in bottom graph)',
                barmode='grouped',
                bargroupgap=0.2,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
        )

@app.callback(
    Output('graph-taluk', 'figure'), [Input("people_type", "value"),\
     Input('graph-districts', 'clickData')])
def update_bar_location(dr_value, clickData):
    district = clickData['points'][0]['x']
    d_series = data_relief.get_plot_per_dist(dr_value, district)
    values = d_series.sort_values(ascending=0)
    return go.Figure(
            data=[go.Bar(
                y=values,
                x=list(values.index),
                marker={'color':'rgba(26, 118, 255, 0.5)',
                      'line':{
                        'color':'rgb(8,48,107)',
                        'width':1.5,
                        }
                }
            )
            ],
            layout=go.Layout(
                title='People by Taluk for ' + district + ' district',
                barmode='grouped',
                bargroupgap=0.2,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
        )

@app.callback(
    Output('table-dist-details', 'figure'),
    [Input('graph-districts', 'clickData')])
def update_table(clickData):
    district = clickData['points'][0]['x']
    df = data_relief.get_all_dist_data(district)
    total_camp_count = df.count()['name']
    total_people = df.sum()['total_people']
    total_males = df.sum()['total_males']
    total_females = df.sum()['total_females']
    return go.Figure(
        data=[go.Table(
            header=dict(values=['', 'Values'],
                        line = dict(color='#7D7F80'),
                        fill = dict(color='#a1c3d1'),
                        align = ['left'] * 5),
            cells=dict(values=[['# of Camps', '# of People Displaced', '# of Males', '# of Females'],
            [total_camp_count, total_people, total_males, total_females]],
                       line = dict(color='#7D7F80'),
                       fill = dict(color='#EDFAFF'),
                       align = ['left'] * 5))

        ],
        layout=go.Layout(
            title = 'Details for ' + district + ' district',
            font=dict(family='Poppins', size=12, color='#7f7f7f')
        )
    )

@app.callback(
    Output('graph-village-heatmap', 'figure'),
    [Input('graph-districts', 'clickData')])
def update_table(clickData):
    district = clickData['points'][0]['x']
    df = data_relief.get_all_dist_data(district)
    df = df[np.isfinite(df['total_people'])]
    df = df.groupby('village').sum()
    return go.Figure(
            data=[go.Heatmap(
                z=df.values,
                x=df.columns,
                y=df.index,
                colorscale='magma',
                )
            ],
        layout=go.Layout(
            title = 'Heat map of count of people by village in ' + district + ' district',
            xaxis=dict(
                showgrid=False,
                zeroline=False,
                showline=False,
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                showline=False,
            ),
            autosize=True,
            height=550,
            hovermode='closest',
            margin=go.Margin(l=150, r=0, t=50),
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

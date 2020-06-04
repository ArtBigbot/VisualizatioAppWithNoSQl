import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from collections import deque
from dash.dependencies import Output, Input, State
import plotly
import dash_daq as daq
import psycopg2
import datetime as dt
import plotly.graph_objects as go
from time import time

conn = psycopg2.connect(host="dev.vk.edu.ee", port=5432, database="dbhitsa2019", user="ruuvi_sel", password="ruuvisel")
cursor = conn.cursor()
query = "SELECT * FROM vw_sensorsdata WHERE room ='208' ORDER BY date_time DESC"
cachedDataFrame = pd.read_sql_query(query, conn)

cachedDataFrame['valuetypeAndSensor'] = cachedDataFrame["valuetype"]+',' + cachedDataFrame["sensor"]
available_indicators = cachedDataFrame['valuetypeAndSensor'].unique()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app1 = dash.Dash(__name__, assets_folder='assets', include_assets_files=True)

server = app.server

app.layout = html.Div([

    html.H4('dbhitsa2019'),

    dcc.Interval(
        id='update',
        interval=300000

    ),

    html.Div(id='intermediate-value', style={'display': 'none'}),
    dcc.Tabs([

        dcc.Tab(label='data monitoring: sensors', children=[

            html.Div([

                html.Div([

                    daq.Gauge(
                        showCurrentValue=True,
                        id='gaugeTemperatureAndHumiditySensor',
                        color="#050df5",
                        label={
                            'label': 'Temperature',
                            'style': {
                                'fontSize': 19
                            }
                        },
                        min=0,
                        units='C',
                        max=50,
                        size=200,
                        theme='dark',
                        style={'display': 'block'},

                    ),
                ], style={'position': 'absolute', 'top': '20%', 'width': '200px', 'height': '250px', 'left': '5%'}),
                html.Label('Temperature and Humidity Sensor',
                           style={'position': 'absolute', 'top': '47%', 'left': '2%', 'fontSize': 19}),

                html.Div((

                    daq.Gauge(
                        showCurrentValue=True,
                        id='gaugeHighAccuracySensor',
                        color="#050df5",

                        label={
                            'label': 'Temperature',
                            'style': {
                                'fontSize': 19
                            }
                        },

                        min=0,
                        units='C'
                        ,
                        max=50,
                        size=200,
                        theme='dark',
                        style={'display': 'block'}
                    ),
                ), style={'position': 'absolute', 'top': '20%', 'left': '25%', 'width': '200px', 'height': '250px'}),
                html.Label('High Accuracy Sensor',
                           style={'position': 'absolute', 'top': '47%', 'left': '25%', 'fontSize': 19}),

                html.Div([
                    daq.Gauge(showCurrentValue=True,
                              id='humidityGauge',
                              units="%",

                              color="#050df5",

                              label={
                                  'label': 'Humidity',
                                  'style': {
                                      'fontSize': 19
                                  }
                              },
                              max=70,
                              min=0,
                              size=200,

                              style={'display': 'block', 'stroke-width': '20px'})
                ], style={'position': 'absolute', 'top': '60%', 'left': '5%', 'width': '200px', 'height': '250px', }),
                html.Label('Temperature and Humidity sensor',
                           style={'position': 'absolute', 'top': '87%', 'left': '2%', 'fontSize': 19}),

                html.Div([
                    daq.Gauge(showCurrentValue=True,
                              id='lumenGauge',
                              units="lm",
                              color="#050df5",
                              label={
                                  'label': 'Lumen',
                                  'style': {
                                      'fontSize': 19
                                  }
                              },

                              max=1000,
                              min=0,
                              size=200)
                ], style={'position': 'absolute', 'top': '20%', 'left': '45%', 'rigth': '80%', 'width': '200px',
                          'height': '250px'}),
                html.Label('Sunlight Sensor',
                           style={'position': 'absolute', 'top': '47%', 'left': '47%', 'fontSize': 19}),

                html.Div([
                    daq.Gauge(showCurrentValue=True,
                              id='ultravioletGauge',
                              units="Uv",
                              color="#050df5",
                              label={
                                  'label': 'Ultraviolet index',
                                  'style': {
                                      'fontSize': 19
                                  }
                              },
                              max=1,
                              min=0,
                              size=200)
                ], style={'position': 'absolute', 'top': '60%', 'left': '25%', 'rigth': '80%', 'width': '200px',
                          'height': '250px'}),
                html.Label('Sunlight Sensor',
                           style={'position': 'absolute', 'top': '87%', 'left': '27%', 'fontSize': 19}),

                html.Div([
                    daq.Gauge(showCurrentValue=True,
                              id='IlluminanceGauge',
                              units="Lux",
                              color="#050df5",

                              label={
                                  'label': 'Illuminance',
                                  'style': {
                                      'fontSize': 19
                                  }
                              },
                              max=100,
                              min=0,
                              size=200)
                ], style={'position': 'absolute', 'top': '60%', 'left': '68%', 'rigth': '35%', 'width': '200px',
                          'height': '250px'}),
                html.Label('Light Sensor',
                           style={'position': 'absolute', 'top': '87%', 'left': '71%', 'fontSize': 19}),
                html.Div([
                    daq.Gauge(showCurrentValue=True,
                              id='TotalVoletileOrganicCompoundsGauge',
                              units='PPB',
                              color="#050df5",
                              label={
                                  'label': 'TVOC',
                                  'style': {
                                      'fontSize': 19
                                  }
                              },
                              max=10,
                              min=0,
                              size=200)
                ], style={'position': 'absolute', 'top': '20%', 'left': '68%', 'rigth': '35%', 'width': '200px',
                          'height': '590px'}),
                html.Label('Grove VOC and eCO2 Gas Sensor',
                           style={'position': 'absolute', 'top': '47%', 'left': '66%', 'fontSize': 19}),
                html.Div([
                    daq.Gauge(showCurrentValue=True,
                              id='detsibellGauge',
                              units="DB",
                              color="#050df5",
                              label={
                                  'label': 'Detsibell',
                                  'style': {
                                      'fontSize': 19
                                  }
                              },
                              max=200,
                              min=0,
                              size=200)
                ], style={'position': 'absolute', 'top': '60%', 'left': '45%', 'rigth': '80%', 'width': '200px',
                          'height': '250px'}),
                html.Label('Loudness Sensor',
                           style={'position': 'absolute', 'top': '87%', 'left': '47%', 'fontSize': 19}),

                html.Div([
                    daq.Gauge(showCurrentValue=True,
                              id='CarbonDioxideEquivalentCO2Gauge',
                              units='PPM',

                              # style={'font-size': '30px'},
                              color="#050df5",

                              label={
                                  'label': 'CO2',
                                  'style': {
                                      'fontSize': 19
                                  }
                              },
                              # label={},
                              max=1,
                              min=0,
                              size=200,
                              style={'fontSize': '30%'}
                              ),

                ], style={'position': 'absolute', 'top': '60%', 'left': '83%', 'rigth': '5%', 'width': '300px',
                          'height': '500px'}),
                html.Label('CarbonDioxideEquivalent Sensor CO2',
                           style={'position': 'absolute', 'top': '87%', 'left': '85%', 'fontSize': 19}),

                html.Div([
                    daq.Gauge(showCurrentValue=True,
                              id='PirOn',

                              color="#050df5",
                              units='BITT',
                              label={
                                  'label': 'The existance of movement',
                                  'style': {
                                      'fontSize': 19
                                  }
                              },
                              max=1,
                              min=0,
                              size=200)
                ], style={'position': 'absolute', 'top': '20%', 'left': '85%', 'rigth': '5%', 'width': '200px',
                          'height': '250px'}),
                html.Label('PIR motion Sensor PIR on',
                           style={'position': 'absolute', 'top': '49%', 'left': '85%', 'fontSize': 19}),

            ]),
        ]),

        # html.Div([

        dcc.Tab(label='data monitoring: graphs', children=[

            html.Div([

                dcc.RadioItems(
                    id='graph_type_tempetureTemperatureAndHymiditySensor',
                    options=[{'label': i, 'value': i} for i in ['Daily average', 'Current']],
                    value='Daily average',
                    labelStyle={'display': 'inline-block'}
                ),

                dcc.Graph(
                    id='graphTempetureTemperatureAndHymiditySensor')
            ], style={'display': 'inline-block', 'width': '30%',
                      'top': '700%', 'left': '330%', 'right': '20%'
                      }
            ),
            html.Div([

                dcc.RadioItems(
                    id='graph_type_tempetureHighAccuracySensor',
                    options=[{'label': i, 'value': i} for i in ['Daily average', 'Current']],
                    value='Daily average',
                    labelStyle={'display': 'inline-block'}
                ),

                dcc.Graph(
                    id='graphTempetureHighAccuracySensor')
            ], style={'display': 'inline-block', 'width': '30%',
                      'top': '700%', 'left': '330%', 'right': '20%'
                      }
            ),

            html.Div([

                dcc.RadioItems(
                    id='graph_type_lumens',
                    options=[{'label': i, 'value': i} for i in ['Daily average', 'Current']],
                    value='Daily average',
                    labelStyle={'display': 'inline-block'}
                ),

                dcc.Graph(
                    id='graphLumens')
            ], style={'display': 'inline-block', 'width': '30%', 'top': '700%', 'left': '330%', 'right': '20%'}),

            html.Div([

                dcc.RadioItems(
                    id='graph_type_tvoc',
                    options=[{'label': i, 'value': i} for i in ['Daily average', 'Current']],
                    value='Daily average',
                    labelStyle={'display': 'inline-block'}
                ),

                dcc.Graph(
                    id='graphTVOC')
            ], style={'display': 'inline-block', 'width': '30%', 'top': '700%', 'left': '330%', 'right': '20%'}),

            html.Div([

                dcc.RadioItems(
                    id='graph_type_humidity',
                    options=[{'label': i, 'value': i} for i in ['Daily average', 'Current']],
                    value='Daily average',
                    labelStyle={'display': 'inline-block'}
                ),

                dcc.Graph(
                    id='graphHumidity')
            ], style={'display': 'inline-block', 'width': '30%', 'top': '700%', 'left': '330%', 'right': '20%'}),

            html.Div([

                dcc.RadioItems(
                    id='graph_type_ultra_violetindex',
                    options=[{'label': i, 'value': i} for i in ['Daily average', 'Current']],
                    value='Daily average',
                    labelStyle={'display': 'inline-block'}
                ),

                dcc.Graph(
                    id='graphUltraVioletIndex')
            ], style={'display': 'inline-block', 'width': '30%', 'top': '700%', 'left': '330%', 'right': '20%'}),

            html.Div([

                dcc.RadioItems(
                    id='graph_type_detsibel',
                    options=[{'label': i, 'value': i} for i in ['Daily average', 'Current']],
                    value='Daily average',
                    labelStyle={'display': 'inline-block'}
                ),

                dcc.Graph(
                    id='graphDetsibel')
            ], style={'display': 'inline-block', 'width': '30%', 'top': '700%', 'left': '330%', 'right': '20%'}),

            html.Div([

                dcc.RadioItems(
                    id='graph_type_illuminanceIR',
                    options=[{'label': i, 'value': i} for i in ['Daily average', 'Current']],
                    value='Daily average',
                    labelStyle={'display': 'inline-block'}
                ),

                dcc.Graph(
                    id='graphIlluminanceIR')
            ], style={'display': 'inline-block', 'width': '30%', 'top': '700%', 'left': '330%', 'right': '20%'}),
            html.Div([

                dcc.RadioItems(
                    id='graph_type_illuminanceVisible',
                    options=[{'label': i, 'value': i} for i in ['Daily average', 'Current']],
                    value='Daily average',
                    labelStyle={'display': 'inline-block'}
                ),

                dcc.Graph(
                    id='graphIlluminanceVisible')
            ], style={'display': 'inline-block', 'width': '30%', 'top': '700%', 'left': '330%', 'right': '20%'}),

            html.Div([

                dcc.RadioItems(
                    id='graph_type_co2',
                    options=[{'label': i, 'value': i} for i in ['Daily average', 'Current']],
                    value='Daily average',
                    labelStyle={'display': 'inline-block'}
                ),

                dcc.Graph(
                    id='graphCO2')
            ], style={'display': 'inline-block', 'width': '30%', 'top': '700%', 'left': '330%', 'right': '20%'}),

            html.Div([

                dcc.RadioItems(
                    id='graph_type_piron',
                    options=[{'label': i, 'value': i} for i in ['Daily average', 'Current']],
                    value='Daily average',
                    labelStyle={'display': 'inline-block'}
                ),

                dcc.Graph(
                    id='graphPIRon')
            ], style={'display': 'inline-block', 'height': '15%', 'width': '30%', 'top': '700%', 'left': '330%',
                      'right': '20%'}),
            # ], style={'padding': '120px 20px 20px 20px', })
        ]),

        dcc.Tab(label='Data averages', children=[
            html.Div([
                dcc.Dropdown(
                    id='indicator',
                    options=[{'label': i, 'value': i} for i in available_indicators],
                     value=available_indicators[0]
                ),
                dcc.DatePickerRange(
                    id="datePickerId",
                    start_date_placeholder_text="Start Period",
                    start_date_id="startDateId",
                    end_date_id="endDateId",
                    start_date='2020-04-28',
                    end_date='2020-04-30',
                    display_format='MMM Do, YY',
                    end_date_placeholder_text="End Period",
                )
            ], style={'width': '30%'}, ),

            html.Div([

                dcc.Dropdown(
                    id='dropDownList',
                    options=[
                        {'label': 'Hour average', 'value': 'Hour average'},
                        {'label': 'Day average', 'value': 'Day average'},

                    ],
                    placeholder="Select a parameter",
                    value="Hour average"
                ),
                dcc.Graph(
                    id='graph'
                )], style={'position': 'absolute', 'top': '20%', 'left': '15%', 'width': '1700px'}),
            html.Div([dash_table.DataTable(
                id='data_table',
                columns=[{'id': c, 'name': c, 'hideable': True} for c in cachedDataFrame.columns[1:7]],
                export_format='xlsx',
                export_headers='display',
                style_table={
                    'maxHeight': '700px',
                    'maxWidth': '1700px',
                    'overflowY': 'scroll',
                    'overflowX': 'scroll'},
                style_cell={
                    'width': '190px',
                    'height': '60px',
                    'font-size': '20px',
                    'textAlign': 'center'}
            )], style={'position': 'absolute', 'top': '90%', 'left': '15%', 'rigth': '80%', 'width': '1700px',
                       'height': '700px', 'border': '9B51E0'}),

        ]),

        dcc.Tab(label='General Table', children=[
            html.Div([dash_table.DataTable(
                id='generalTable',
                columns=[{'id': c, 'name': c, 'hideable': True} for c in cachedDataFrame.columns[1:7]],
                export_format='xlsx',
                export_headers='display',
                style_table={
                    'maxHeight': '700px',
                    'maxWidth': '1700px',
                    'overflowY': 'scroll',
                    'overflowX': 'scroll'
                },
                style_cell={
                    'width': '190px',
                    'height': '60px',
                    'font-size': '20px',
                    'textAlign': 'center'
                }
            )], style={'position': 'absolute', 'top': '18%', 'left': '15%', 'rigth': '80%', 'width': '1700px',
                       'height': '700px', 'border': '9B51E0'}),

        ]), dcc.Tab(label='Correlation of two parameters', children=[
            html.Div([
                html.Div([
                    dcc.Dropdown(
                        id='crossfilter-xaxis-column',
                        options=[{'label': i, 'value': i} for i in available_indicators], style={'width': '75%'},
                        value='T'
                    ),

                ],
                    style={'width': '49%', 'display': 'inline-block'}),
                html.Div([
                    dcc.Dropdown(
                        id='crossfilter-yaxis-column',
                        options=[{'label': i, 'value': i} for i in available_indicators],
                        style={'top': '10%', 'left': '60%', 'width': '75%'},
                        value='Humidity'
                    ),

                ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
                dcc.DatePickerRange(
                    id="datePickerRangeId",
                    # start_date=""
                    start_date_placeholder_text="Start Period",
                    start_date_id="startDateId",
                    end_date_id="endDateId",
                    start_date='2020-04-01',
                    end_date='2020-04-10',
                    display_format='MMM Do, YY',
                    end_date_placeholder_text="End Period",

                ),

            ], style={
                'borderBottom': 'thin lightgrey solid',
                'backgroundColor': 'rgb(250, 250, 250)',
                'padding': '10px 5px'
            }),

            html.Div([
                dcc.Graph(
                    id='crossfilterParameterGraph',
                    hoverData={'points': [{'customdata': ''}]}
                )
            ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
            # ),

            #  ],
            html.Div([
                dcc.Graph(id='x-time-series'),
                dcc.Graph(id='y-time-series'),
            ], style={'display': 'inline-block', 'width': '49%'}),

        ])
    ])

])


# ])


# @cache.memoize(timeout=TIMEOUT)
@app.callback(dash.dependencies.Output('intermediate-value', 'children'),
              [dash.dependencies.Input('update', 'n_intervals')])
def create_pandas_table(database=conn):
    query1 = "SELECT * FROM vw_sensorsdata WHERE room ='208' ORDER BY date_time DESC"
    table = pd.read_sql_query(query1, conn)
    newTableDataJson = table.to_json(orient='split')
    return newTableDataJson


@app.callback(dash.dependencies.Output('graphTempetureTemperatureAndHymiditySensor', 'figure'),
              [dash.dependencies.Input('graph_type_tempetureTemperatureAndHymiditySensor', 'value'),
               dash.dependencies.Input('intermediate-value', 'children')])
def update_graph_tempeture(graph_type_tempeture, jsonified_data):
    if graph_type_tempeture == 'Current':
        return draw_graphLine('Temperature', 'T', jsonified_data, 'Temperature and Humidity Sensor Pro')
    elif graph_type_tempeture == 'Daily average':
        return draw_graphBar('Temperature', 'T', jsonified_data, 'Temperature and Humidity Sensor Pro')

@app.callback(dash.dependencies.Output('graphTempetureHighAccuracySensor', 'figure'),
              [dash.dependencies.Input('graph_type_tempetureHighAccuracySensor', 'value'),
               dash.dependencies.Input('intermediate-value', 'children')])
def update_graph_tempeture(graph_type_tempeture, jsonified_data):
    if graph_type_tempeture == 'Current':
        return draw_graphLine('Temperature', 'T', jsonified_data, 'High Accuracy Temperature')
    elif graph_type_tempeture == 'Daily average':
        return draw_graphBar('Temperature', 'T', jsonified_data, 'High Accuracy Temperature')


@app.callback(dash.dependencies.Output('graphLumens', 'figure'),
              [dash.dependencies.Input('graph_type_lumens', 'value'),
               dash.dependencies.Input('intermediate-value', 'children')])
def update_graph_lumens(graph_type_lumens, jsonified_data):
    if graph_type_lumens == 'Current':
        return draw_graphLine('Lumens', 'Lumen', jsonified_data, 'Sunlight Sensor')
    elif graph_type_lumens == 'Daily average':
        return draw_graphBar('Lumens', 'Lumen', jsonified_data, 'Sunlight Sensor')


@app.callback(dash.dependencies.Output('graphTVOC', 'figure'),
              [dash.dependencies.Input('graph_type_tvoc', 'value'),
               dash.dependencies.Input('intermediate-value', 'children')])
def update_graph_tvoc(graph_type_tvoc, jsonified_data):
    if graph_type_tvoc == 'Current':
        return draw_graphLine('Total Volatile Organic Compunds', 'Total Volatile Organic Compounds', jsonified_data,'Grove VOC and eCO2 Gas Sensor')
    elif graph_type_tvoc == 'Daily average':
        return draw_graphBar('Total Volatile Organic Compunds', 'Total Volatile Organic Compounds', jsonified_data,'Grove VOC and eCO2 Gas Sensor')


@app.callback(dash.dependencies.Output('graphHumidity', 'figure'),
              [dash.dependencies.Input('graph_type_humidity', 'value'),
               dash.dependencies.Input('intermediate-value', 'children')])
def update_graph_humidity(graph_type_tvoc, jsonified_data):
    if graph_type_tvoc == 'Current':
        return draw_graphLine('Humidity', 'Humidity', jsonified_data,'Temperature and Humidity Sensor Pro')
    elif graph_type_tvoc == 'Daily average':
        return draw_graphBar('Humidity', 'Humidity', jsonified_data,'Temperature and Humidity Sensor Pro')


@app.callback(dash.dependencies.Output('graphUltraVioletIndex', 'figure'),
              [dash.dependencies.Input('graph_type_ultra_violetindex', 'value'),
               dash.dependencies.Input('intermediate-value', 'children')])
def update_graph_uvIndex(graph_type_ultra_violetindex, jsonified_data):
    if graph_type_ultra_violetindex == 'Current':
        return draw_graphLine('Ultraviolet index', 'Ultraviolet index', jsonified_data, 'Sunlight Sensor')
    elif graph_type_ultra_violetindex == 'Daily average':
        return draw_graphBar('Ultraviolet index', 'Ultraviolet index', jsonified_data, 'Sunlight Sensor')


@app.callback(dash.dependencies.Output('graphDetsibel', 'figure'),
              [dash.dependencies.Input('graph_type_detsibel', 'value'),
               dash.dependencies.Input('intermediate-value', 'children')])
def update_graph_detsibell(graph_type_detsibel, jsonified_data):
    if graph_type_detsibel == 'Current':
        return draw_graphLine('Decibel', 'Detsibell', jsonified_data,'Loudness Sensor')
    elif graph_type_detsibel == 'Daily average':
        return draw_graphBar('Decibel', 'Detsibell', jsonified_data,'Loudness Sensor')


@app.callback(dash.dependencies.Output('graphIlluminanceIR', 'figure'),
              [dash.dependencies.Input('graph_type_illuminanceIR', 'value'),
               dash.dependencies.Input('intermediate-value', 'children')
               ])
def update_graph_Illuminance(graph_type_illuminance, jsonified_data):
    if graph_type_illuminance == 'Current':
        return draw_graphLine('Illuminance (IR)', 'Illuminance (IR)', jsonified_data,'Sunlight Sensor')
    elif graph_type_illuminance == 'Daily average':
        return draw_graphBar('Illuminance (IR)', 'Illuminance (IR)', jsonified_data,'Sunlight Sensor')


@app.callback(dash.dependencies.Output('graphIlluminanceVisible', 'figure'),
              [dash.dependencies.Input('graph_type_illuminanceVisible', 'value'),
               dash.dependencies.Input('intermediate-value', 'children')
               ])
def update_graph_Illuminance(graph_type_illuminance, jsonified_data):
    if graph_type_illuminance == 'Current':
        return draw_graphLine('Illuminance (Visible)', 'Illuminance (Visible)', jsonified_data, 'Light Sensor')
    elif graph_type_illuminance == 'Daily average':
        return draw_graphBar('Illuminance (Visible)', 'Illuminance (Visible)', jsonified_data, 'Light Sensor')


@app.callback(dash.dependencies.Output('graphCO2', 'figure'),
              [dash.dependencies.Input('graph_type_co2', 'value'),
               dash.dependencies.Input('intermediate-value', 'children')])
def update_graph_Carbon(graph_type_co2, jsonified_data):
    if graph_type_co2 == 'Current':
        return draw_graphLine('Carbon dioxide equivalent CO2eq', 'Carbon dioxide equivalent CO2eq', jsonified_data,'Grove VOC and eCO2 Gas Sensor')
    elif graph_type_co2 == 'Daily average':
        return draw_graphBar('Carbon dioxide equivalent CO2eq', 'Carbon dioxide equivalent CO2eq', jsonified_data,'Grove VOC and eCO2 Gas Sensor')


@app.callback(dash.dependencies.Output('graphPIRon', 'figure'),
              [dash.dependencies.Input('graph_type_piron', 'value'),
               dash.dependencies.Input('intermediate-value', 'children')
               ])
def update_graph_PIROn(graph_type_piron, jsonified_data):
    if graph_type_piron == 'Current':
        return draw_graphLine('PIR on', 'PIR on', jsonified_data,'PIR Motion Sensor')
    elif graph_type_piron == 'Daily average':
        return draw_graphBar('PIR on', 'PIR on', jsonified_data,'PIR Motion Sensor')


@app.callback(
    Output(component_id='data_table', component_property='data'),
    [
        Input(component_id='indicator', component_property='value'),
        Input(component_id='datePickerId', component_property='start_date'),
        Input(component_id='datePickerId', component_property='end_date'),
        dash.dependencies.Input('intermediate-value', 'children')
    ]
)
def update_table(parameter, start_date, end_date, jsonified_data):
    splitedParameter= parameter.split(',')[0]
    sensor = parameter.split(',')[1]
    df = pd.read_json(jsonified_data, orient='split')
    dataFrameTable = pd.DataFrame.from_dict(df)
    filtered_df = dataFrameTable[(dataFrameTable['valuetype'] == splitedParameter) & (dataFrameTable['sensor'] ==sensor) &
                                 (dataFrameTable['date_time'].between(start_date, end_date))]
    return filtered_df.to_dict('records')


@app.callback(
    Output(component_id='generalTable', component_property='data'),
    [dash.dependencies.Input('intermediate-value', 'children')]
)
def updateGeneralTable(jsonified_data):
    df = pd.read_json(jsonified_data, orient='split')
    dataFrameTable = pd.DataFrame.from_dict(df)
    return dataFrameTable.to_dict('records')


@app.callback(
    dash.dependencies.Output('gaugeTemperatureAndHumiditySensor', 'value'),
    [dash.dependencies.Input('update', 'n_intervals'),
     dash.dependencies.Input('intermediate-value', 'children')
     ]
)
def update_GaugeTempFromTemperatureAndHumiditySensor(value, jsonified_data):
    df = pd.read_json(jsonified_data, orient='split')
    dataFrameTable = pd.DataFrame.from_dict(df)
    filtered_df = dataFrameTable.query('valuetype=="T"  & '
                                       'sensor =="Temperature and Humidity Sensor Pro"')
    tempeture = filtered_df.iat[0, 6]
    return tempeture


@app.callback(
    dash.dependencies.Output('gaugeHighAccuracySensor', 'value'),
    [dash.dependencies.Input('update', 'n_intervals'),
     dash.dependencies.Input('intermediate-value', 'children')
     ]
)
def update_GaugeTempFromHighAccuracySensor(value, jsonified_data):

    df = pd.read_json(jsonified_data, orient='split')
    dataFrameTable = pd.DataFrame.from_dict(df)
    filtered_df = dataFrameTable.query('valuetype=="T" & room == 208 & sensor =="High Accuracy Temperature"')
    tempeture = filtered_df.iat[0, 6]

    return tempeture


@app.callback(
    dash.dependencies.Output('humidityGauge', 'value'),
    [dash.dependencies.Input('update', 'n_intervals'),
     dash.dependencies.Input('intermediate-value', 'children')
     ]
)
def update_GaugeHumidity(value, jsonified_data):
    df = pd.read_json(jsonified_data, orient='split')
    dataFrameTable = pd.DataFrame.from_dict(df)
    filtered_df = dataFrameTable.query('valuetype=="Humidity" & room == 208')
    humidity = filtered_df.iat[0, 6]

    return humidity


@app.callback(
    dash.dependencies.Output('lumenGauge', 'value'),
    [dash.dependencies.Input('update', 'n_intervals'),
     dash.dependencies.Input('intermediate-value', 'children')
     ]
)
def update_LumenGauge(value, jsonified_data):
    df = pd.read_json(jsonified_data, orient='split')
    dataFrameTable = pd.DataFrame.from_dict(df)
    filtered_df = dataFrameTable.query('valuetype=="Lumen" & room == 208 & sensor == "Sunlight Sensor"')
    lumens = filtered_df.iat[0, 6]
    return lumens


@app.callback(
    dash.dependencies.Output('ultravioletGauge', 'value'),
    [dash.dependencies.Input('update', 'n_intervals'),
     dash.dependencies.Input('intermediate-value', 'children')
     ]
)
def update_ultravioletGauge(value, jsonified_data):
    df = pd.read_json(jsonified_data, orient='split')
    dataFrameTable = pd.DataFrame.from_dict(df)
    filtered_df = dataFrameTable.query('valuetype=="Ultraviolet index" & room == 208 & sensor == "Sunlight Sensor"')
    uvIndex = filtered_df.iat[0, 6]
    return uvIndex


@app.callback(
    dash.dependencies.Output('PirOn', 'value'),
    [dash.dependencies.Input('update', 'n_intervals'),
     dash.dependencies.Input('intermediate-value', 'children')
     ]
)
def update_PirOnGauge(value, jsonified_data):
    df = pd.read_json(jsonified_data, orient='split')
    dataFrameTable = pd.DataFrame.from_dict(df)
    filtered_df = dataFrameTable.query('valuetype=="PIR on" & room == 208')
    piron = filtered_df.iat[0, 6]

    return piron


@app.callback(
    dash.dependencies.Output('IlluminanceGauge', 'value'),
    [dash.dependencies.Input('update', 'n_intervals'),
     dash.dependencies.Input('intermediate-value', 'children')
     ]
)
def update_IlluminanceGauge(value, jsonified_data):
    df = pd.read_json(jsonified_data, orient='split')
    dataFrameTable = pd.DataFrame.from_dict(df)
    filtered_df = dataFrameTable.query('valuetype=="Illuminance (IR)" & room == 208 & sensor == "Sunlight Sensor"')
    illuminance = filtered_df.iat[0, 6]
    return illuminance


@app.callback(
    dash.dependencies.Output('CarbonDioxideEquivalentCO2Gauge', 'value'),
    [dash.dependencies.Input('update', 'n_intervals'),
     dash.dependencies.Input('intermediate-value', 'children')
     ]
)
def update_CO2Gauge(value, jsonified_data):
    df = pd.read_json(jsonified_data, orient='split')
    dataFrameTable = pd.DataFrame.from_dict(df)
    filtered_df = dataFrameTable.query('valuetype=="Carbon dioxide equivalent CO2eq" & room == 208')
    co2 = filtered_df.iat[0, 6]
    return co2


@app.callback(
    dash.dependencies.Output('detsibellGauge', 'value'),
    [dash.dependencies.Input('update', 'n_intervals'),
     dash.dependencies.Input('intermediate-value', 'children')
     ]
)
def update_detsibellGauge(value, jsonified_data):
    df = pd.read_json(jsonified_data, orient='split')
    dataFrameTable = pd.DataFrame.from_dict(df)
    filtered_df = dataFrameTable.query('valuetype=="Detsibell" & room == 208')
    detsibell = filtered_df.iat[0, 6]
    return detsibell


@app.callback(
    dash.dependencies.Output('TotalVoletileOrganicCompoundsGauge', 'value'),
    [dash.dependencies.Input('update', 'n_intervals'),
     dash.dependencies.Input('intermediate-value', 'children')
     ]
)
def update_TVOCGauge(value, jsonified_data):
    df = pd.read_json(jsonified_data, orient='split')
    dataFrameTable = pd.DataFrame.from_dict(df)
    filtered_df = dataFrameTable.query('valuetype=="Total Volatile Organic Compounds" & room == 208')
    tvoc = filtered_df.iat[0, 6]
    return tvoc


def draw_graphLine(name, parameter, jsonified_data,sensor):
    dataSQL = []
    X = deque(maxlen=20)
    Y = deque(maxlen=20)
    dataframe = pd.read_json(jsonified_data, orient='split')
    filtered_df = dataframe[(dataframe['valuetype'] == parameter) & (dataframe['sensor'] == sensor)]
    rows = filtered_df.head(20)
    for row in filtered_df:
        dataSQL.append(list(row))
        labels = ['date_time', 'valuetype', 'data', 'dimension']
        df = pd.DataFrame.from_dict(dataSQL)
        dff = rows[rows['valuetype'] == parameter]
        X = rows['date_time']
        Y = rows['data']
        dim = rows['dimension'].unique()
        data = plotly.graph_objs.Scatter(
        x=list(X),
        y=list(Y),
        name='Scatter',
        mode='lines+markers'
        )
    return {'data': [data], 'layout': go.Layout(title=go.layout.Title(text='{}, {}'.format(name,dim, sensor )),
                                                xaxis=dict(range=[min(X), max(X)]),
                                                yaxis=dict(range=[min(Y) - 1, max(Y) + 1]))}


def draw_graphBar(name, parameter, jsonified_data, sensor):
    dataframe = pd.read_json(jsonified_data, orient='split')
    filtered_df = dataframe[(dataframe['valuetype'] == parameter) &(dataframe['sensor'] == sensor)]
    dim = filtered_df['dimension'].unique()
    dff1 = filtered_df.loc[:, ['date_time', 'data']]
    dff1['date_time'] = pd.to_datetime(dff1['date_time'])
    dff1['date'] = dff1['date_time'].dt.date
    data2 = dff1.groupby(['date']).mean()
    data = go.Bar(x=data2.index.map(str), y=list(data2['data']))
    return {'data': [data],
            'layout': go.Layout(title=go.layout.Title(text='{}, {}'.format(name,dim,sensor)))}


@app.callback(dash.dependencies.Output('graph', 'figure'),
              [Input(component_id='indicator', component_property='value'),
               Input(component_id='dropDownList', component_property='value'),
               Input(component_id='datePickerId', component_property='start_date'),
               Input(component_id='datePickerId', component_property='end_date'),
               Input('intermediate-value', 'children')])
def drawGraphBarAverage(parameter, dropDownList, startDate, endDate, jsonified_data):
    splitedParameter = parameter.split(',')[0]
    sensor = parameter.split(',')[1]
    df = pd.read_json(jsonified_data, orient='split')
    dataFrameTable = pd.DataFrame.from_dict(df)
    filtered_df = dataFrameTable[
        (dataFrameTable['valuetype'] == splitedParameter) & (dataFrameTable['sensor']== sensor) & (dataFrameTable['date_time'].between(startDate, endDate))]
    dim = filtered_df['dimension'].unique()
    dff2 = filtered_df.loc[:, ['date_time', 'data']]
    dff2['date_time'] = pd.to_datetime(dff2['date_time'])
    if dropDownList == 'Hour average':
        dff2['hours'] = dff2['date_time'].dt.hour
        dff2['dates'] = dff2['date_time'].dt.date
        data4 = dff2.groupby(['dates', 'hours'], as_index=False).mean()
        data4['dateAndHours'] = data4['dates'].astype(str).apply(
            lambda x: dt.datetime.strptime(x, '%Y-%m-%d')) + pd.to_timedelta(data4['hours'], unit='h')
        data = go.Bar(x=list(data4['dateAndHours']), y=list(data4['data']))
    elif dropDownList == 'Day average':
        dff2['hours'] = dff2['date_time'].dt.hour
        dff2['dates'] = dff2['date_time'].dt.date
        data4 = dff2.groupby(['dates']).mean()
        data = go.Bar(x=data4.index.map(str), y=list(data4['data']))

   # else:
       # dff2['hours'] = dff2['date_time'].dt.hour
       # dff2['dates'] = dff2['date_time'].dt.date
       # data4 = dff2.groupby(['dates', 'hours'], as_index=False).mean()
       # data4['dateAndHours'] = data4['dates'].astype(str).apply(
        #    lambda x: dt.datetime.strptime(x, '%Y-%m-%d')) + pd.to_timedelta(data4['hours'], unit='h')
       # data = go.Bar(x=list(data4['dateAndHours']), y=list(data4['data']))
    return {'data': [data],
            'layout': go.Layout(title=go.layout.Title(text=': {}, {}'.format(parameter, dim)))}


@app.callback(
    dash.dependencies.Output('crossfilterParameterGraph', 'figure'),
    [dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('datePickerRangeId', 'start_date'),
     dash.dependencies.Input('datePickerRangeId', 'end_date'),
     dash.dependencies.Input('intermediate-value', 'children')
     ])
def updateGraph(firstParameter_xaxis, secondParameter_yaxis,  startDatePeriod, endDatePeriod, jsonified_data):
    splitedFirstParameter = firstParameter_xaxis.split(',')[0]
    splitedSecondParameter = secondParameter_yaxis.split(',')[0]
    df = pd.read_json(jsonified_data, orient='split')
    dataFrameTable = pd.DataFrame.from_dict(df)

    filtered_df = dataFrameTable[(dataFrameTable['date_time'].between(startDatePeriod, endDatePeriod))]


    return {
        'data': [dict(
            x=filtered_df[filtered_df['valuetype'] == splitedFirstParameter]['data'],
            y=filtered_df[filtered_df['valuetype'] == splitedSecondParameter]['data'],
            text=filtered_df[filtered_df['valuetype'] == secondParameter_yaxis]['dimension'],
            customdata=filtered_df[filtered_df['valuetype'] == secondParameter_yaxis]['sensor'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': dict(
            xaxis={
                'title': splitedFirstParameter,

            },
            yaxis={
                'title': splitedSecondParameter,

            },
            margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
            height=450,
            hovermode='closest'
        )
    }


def create_series(dff,title):
    return {
        'data': [dict(
            x=dff['date_time'],
            y=dff['data'],
            mode='lines+markers'
        )],
        'layout': {
            'height': 225,
            'margin': {'l': 20, 'b': 30, 'r': 10, 't': 10},
            'annotations': [{
                'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': title
            }],
            #'yaxis': {'type': 'linear' if axis_type == 'Linear' else 'log'},
            'xaxis': {'showgrid': False}

        }
    }


@app.callback(
    dash.dependencies.Output('x-time-series', 'figure'),
    [dash.dependencies.Input('crossfilterParameterGraph', 'hoverData'),
     dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('intermediate-value', 'children')
     ])
def update_x_timeseries(hoverData, firstParameter_xaxis,  jsonified_data):
    splitedFirstParameter = firstParameter_xaxis.split(',')[0]
    df = pd.read_json(jsonified_data, orient='split')

   # parameterName = hoverData['points'][0]['customdata']
   # dff = df[df['valuetype'] == parameterName]
    dff = df[df['valuetype'] == splitedFirstParameter]
    title = '<b>{}</b><br>{}'.format(dff['sensor'].iloc[0], splitedFirstParameter)
    return create_series(dff,title)


@app.callback(
    Output('y-time-series', 'figure'),
    [Input('crossfilterParameterGraph', 'hoverData'),
     Input('crossfilter-yaxis-column', 'value'),

     Input('intermediate-value', 'children')
     ])
def update_y_timeseries(hoverData, secondParameter_yaxis, jsonified_data):
    splitedSecondParameter = secondParameter_yaxis.split(',')[0]
    df = pd.read_json(jsonified_data, orient='split')
   # dataFrameTable = pd.DataFrame.from_dict(df)

    # df = pd.DataFrame.from_records(dataSQL, columns=labels)
   # dff = df[df['valuetype'] == secondParameter_yaxis]
   # parameterName = hoverData['points'][0]['customdata']
   # dff = df[df['valuetype'] == parameterName]
    dff = df[df['valuetype'] == splitedSecondParameter]
    title = '<b>{}</b><br>{}'.format(dff['sensor'].iloc[0], splitedSecondParameter)
    return create_series(dff,  title)


if __name__ == '__main__':
    app.run_server(debug=True)

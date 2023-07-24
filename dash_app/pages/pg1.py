import os
from urllib.request import urlopen
import json
import pandas as pd
import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State
import plotly.express as px
import dash_bootstrap_components as dbc

# Register the page
dash.register_page(__name__, path='/', name='Race') # '/' is home page

# Load the geoJSON data
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

# Load geoJSON for states choropleth
with urlopen('https://eric.clst.org/assets/wiki/uploads/Stuff/gz_2010_us_040_00_5m.json') as response:
    states = json.load(response)

# Define a dictionary to store the state name and its corresponding FIPS code
state_to_fips = {feature['properties']['NAME']: feature['properties']['STATE'] 
                 for feature in states['features'] 
                 if feature['properties']['NAME'] not in ['Alaska', 'Puerto Rico']}
state_to_fips['United States'] = 'ALL'

# Create FIPS to state name dictionary for chart title functionality
fips_to_state = {v: k for k, v in state_to_fips.items()}

# Function to load the workbooks and store them into pandas dataframes
def load_workbooks_into_dataframes(dataframe_labels_dict):
    dataframes = {}
    statistics_folder = 'Statistics_Dataframes'
    for name in dataframe_labels_dict:
        filename = os.path.join(statistics_folder, f"{name}.xlsx")
        df = pd.read_excel(filename,dtype={'Location':str,
                                           'State':str,
                                           'County':str,
                                           'FIPS': str})
        dataframes[name] = df
    return dataframes

# Create a dictionary to map the dataframes to their names
dataframe_labels_dict = {
    'DF_total_all':('All Races','Expected Total'),
    'DF_total_whi':('White','Total'),
    'DF_total_baa':('Black or African American','Total'),
    'DF_total_aian':('American Indian & Alaska Native','Total'),
    'DF_total_aa':('Asian','Total'),
    'DF_total_nhop':('Native Hawaiian & Other Pacific Islander','Total'),
    'DF_total_hol':('Hispanic or Latino','Total'),
    'DF_total_sor':('Some Other Race','Total'),
    'DF_total_tom':('Two or More Races','Total')
}

# Load the workbooks into dataframes
dataframes = load_workbooks_into_dataframes(dataframe_labels_dict)

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(
                        id='race-dropdown', 
                        options=[{'label': v[0], 'value': k} 
                                 for k, v in dataframe_labels_dict.items()],
                        value='DF_total_all'
                    ),
                    width=12
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H3('Title Block-1'),  # Add your title here
                        dcc.Dropdown(
                            id='state-dropdown',
                            options=[{'label': state, 'value': fips} 
                                     for state, fips in state_to_fips.items()],
                            value=list(state_to_fips.values())[0]
                        )
                    ],
                    width=6
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H3('Title Block-2'),  # Add your title here
                        dcc.Graph(id='choropleth-map')
                    ], 
                    width=6
                ),
                dbc.Col(
                    [
                        html.H3('Title Block-3'),  # Add your title here
                        dcc.Graph(id='alaska-map')
                    ], 
                    width=6
                ),
            ]
        )
    ]
)

# Define the callback to update the choropleth map based on the selected race and state
@callback(
    Output('choropleth-map', 'figure'),
    [Input('race-dropdown', 'value'),
     Input('state-dropdown', 'value')]
)
def update_choropleth(selected_race, selected_state_fips):
    df = dataframes[selected_race]

    if selected_state_fips != 'ALL' and selected_state_fips not in df['State'].unique():
        raise dash.exceptions.PreventUpdate

    if selected_state_fips == 'ALL':
        geojson_data = counties
        state_title = 'USA'
    else:
        selected_county_features = [feature for feature in counties['features'] if feature['properties']['STATE'] == selected_state_fips]
        geojson_data = {
            'type': counties['type'],
            'features': selected_county_features
        }
        df = df[df['State'] == selected_state_fips]  # filter df to only include rows for the selected state
        state_title = fips_to_state.get(selected_state_fips, 'Unknown State')

    # Prepare the title
    race_title = dataframe_labels_dict[selected_race][0]
    title = f"{race_title} - {state_title}"

    color_column = dataframe_labels_dict[selected_race][1]
    min_color = df[color_column].min()
    max_color = df[color_column].max()

    fig = px.choropleth(df, 
                        geojson=geojson_data, 
                        locations='FIPS', 
                        color=color_column,
                        hover_name='Location',
                        hover_data=[color_column],
                        color_continuous_scale="YlOrRd",
                        range_color=(min_color, max_color),  # set the color range
                        scope="usa",
                        labels={color_column: color_column}
                       )
    fig.update_layout(
        margin={"r":0,"t":50,"l":0,"b":0},  
        title={
            'text': title,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(
                size=24,
                color='rgb(107, 107, 107)'
            )
        },
        paper_bgcolor='#D3D3D3',
        plot_bgcolor='#D3D3D3',
    )

    if selected_state_fips != 'ALL':
        fig.update_geos(fitbounds="locations", visible=False)

    return fig

# Define the callback to update the Alaska map based on the selected race
@callback(
    Output('alaska-map', 'figure'),
    [Input('race-dropdown', 'value')]
)
def update_alaska_map(selected_race):
    df = dataframes[selected_race]
    selected_county_features = [feature for feature in counties['features'] if feature['properties']['STATE'] == '02']
    geojson_data = {
        'type': counties['type'],
        'features': selected_county_features
    }

    fig_1 = px.choropleth(df, 
                          geojson=geojson_data, 
                          locations='FIPS', 
                          color=dataframe_labels_dict[selected_race][1],
                          hover_name='Location',
                          hover_data=[dataframe_labels_dict[selected_race][1]],
                          color_continuous_scale="YlOrRd",
                          labels={dataframe_labels_dict[selected_race][1]: dataframe_labels_dict[selected_race][1]},
                          )
    fig_1.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                        paper_bgcolor='#D3D3D3',
                        plot_bgcolor='#D3D3D3',
                        )
    fig_1.update_geos(
        lonaxis_range=[20, 380],
        projection_scale=6,
        center=dict(lat=61),
        visible=False)

    return fig_1
import os
from urllib.request import urlopen
import json
import pandas as pd
import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/', name='Race') # '/' is home page

# page 1 data
dataframe_labels_dict = {'DF_total_all':('All Races','Expected Total'),
                         'DF_total_whi':('White','Total'),
                         'DF_total_baa':('Black or African American','Total'),
                         'DF_total_aian':('American Indian & Alaska Native','Total'),
                         'DF_total_aa':('Asian','Total'),
                         'DF_total_nhop':('Native Hawaiian & Other Pacific Islander','Total'),
                         'DF_total_hol':('Hispanic or Latino','Total'),
                         'DF_total_sor':('Some Other Race','Total'),
                         'DF_total_tom':('Two or More Races','Total')
                         }

# race_dropdown_labels = ['All Races','White','Black or African American',
#                    'American Indian & Alaska Native','Asian',
#                    'Native Hawaiian & Other Pacific Islander',
#                    'Hispanic or Latino','Some Other Race','Two or More Races'
#                    ]

state_dropdown_dict = {'United States':'ALL',
                       'Alabama':'01',
                       'Alaska':'02',
                       'Arizona':'04',
                       'Arkansas':'05',
                       'California':'06',
                       'Colorado':'08',
                       'Connecticut':'09',
                       'Delaware':'10',
                       'Florida':'12',
                       'Georgia':'13',
                       'Hawaii':'15',
                       'Idaho':'16',
                       'Illinois':'17',
                       'Indiana':'18',
                       'Iowa':'19',
                       'Kansas':'20',
                       'Kentucky':'21',
                       'Louisiana':'22',
                       'Maine':'23',
                       'Maryland':'24',
                       'Massachusetts':'25',
                       'Michigan':'26',
                       'Minnesota':'27',
                       'Mississippi':'28',
                       'Missouri':'29',
                       'Montana':'30',
                       'Nebraska':'31',
                       'Nevada':'32',
                       'New Hampshire':'33',
                       'New Jersey':'34',
                       'New Mexico':'35',
                       'New York':'36',
                       'North Carolina':'37',
                       'North Dakota':'38',
                       'Ohio':'39',
                       'Oklahoma':'40',
                       'Oregon':'41',
                       'Pennsylvania':'42',
                       'Rhode Island':'44',
                       'South Carolina':'45',
                       'South Dakota':'46',
                       'Tennessee':'47',
                       'Texas':'48',
                       'Utah':'49',
                       'Vermont':'50',
                       'Virginia':'51',
                       'Washington':'53',
                       'West Virginia':'54',
                       'Wisconsin':'55',
                       'Wyoming':'56'
                       }
state_names = list(state_dropdown_dict.keys())

#Load geoJSON for choropleth
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

# Function to load workbooks and store variables with their names
def load_workbooks_into_dataframes():
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

dataframes = load_workbooks_into_dataframes()

# Layout for Race page
layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                        dcc.Dropdown(
                            id='race-dropdown', 
                            options=[{'label': v[0], 'value': k} 
                                     for k, v in dataframe_labels_dict.items()],
                                     value='DF_total_all',
                                    #  style={'backgroundColor': '#D3D3D3'}
                        ),
                ),
                # dbc.Col(
                #     dcc.Dropdown(id='state_dropdown',
                #         options=[{'label': state_name, 'value': fips_code} for state_name, 
                #                  fips_code in state_dropdown_dict.items()],
                #                  # The default value (index of the first item in the list)
                #                  value='ALL',
                #         ),
                # ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id='choropleth-map')
                    ], width=12
                )
            ]
        )
    ]
)


# Update the choropleth map based on the selected race and state
@callback(
    dash.dependencies.Output('choropleth-map', 'figure'),
    [dash.dependencies.Input('race-dropdown', 'value'),
    #  dash.dependencies.Input('state_dropdown', 'value')
     ]
)
def update_choropleth(selected_value):
    df = dataframes[selected_value]
    fig = px.choropleth(df, 
                    geojson=counties, 
                    locations='FIPS', # use 'FIPS' column from df for locations
                    color=dataframe_labels_dict[selected_value][1], # use selected column from df for color
                    hover_name='Location', # title to add to hover information
                    hover_data=[dataframe_labels_dict[selected_value][1]], # other column to add to hover information
                    color_continuous_scale="YlOrRd", # select color scale
                    scope="usa", # limit map scope to USA
                    labels={dataframe_labels_dict[selected_value][1]: dataframe_labels_dict[selected_value][1]} # label for color bar
                   )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

# def update_choropleth_map(selected_race, selected_fips_code):
#     # Use the selected_race directly to get the actual DataFrame
#     selected_dataframe = dataframes[selected_race]

#     # Set the locations to the 'FIPS' column to show data for all counties
#     locations = selected_dataframe['FIPS'].tolist()  

#     # Create the choropleth map using Plotly Express
#     fig = px.choropleth(
#         data_frame=selected_dataframe,
#         geojson=counties,  # Path to the GeoJSON file
#         locations=locations,  # Use the locations based on the selected state or 'ALL'
#         featureidkey="properties.GEO_ID",  # Key in GeoJSON properties that corresponds to the FIPS code
#         color='Total',  # Column in your DataFrame containing the data values to visualize
#         hover_name='State',  # Column in selected_dataframe for hover labels
#         hover_data=['Total'],
#         labels={'Total': 'Data Value'},  # Label for the color scale
#         title=f'Choropleth Map for {selected_fips_code}',  # Title for the map
#     )

#     # If a specific state is selected, adjust the zoom and center of the map to focus on that state
#     if selected_fips_code != 'ALL':
#         selected_state_df = selected_dataframe[selected_dataframe['State'] == selected_fips_code]
#         center_lat = selected_state_df['Latitude'].mean()  # Replace 'Latitude' with the actual column name
#         center_lon = selected_state_df['Longitude'].mean()  # Replace 'Longitude' with the actual column name
#         fig.update_geos(center=dict(lat=center_lat, lon=center_lon), scope='usa', showcountries=False)

#     return fig
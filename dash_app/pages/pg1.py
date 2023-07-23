import os
import pandas as pd
import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/', name='Race') # '/' is home page

# page 1 data
dataframe_labels_dict = {'DF_total_all':'All Races',
                         'DF_total_whi':'White',
                         'DF_total_baa':'Black or African American',
                         'DF_total_aian':'American Indian & Alaska Native',
                         'DF_total_aa':'Asian',
                         'DF_total_nhop':'Native Hawaiian & Other Pacific Islander',
                         'DF_total_hol':'Hispanic or Latino',
                         'DF_total_sor':'Some Other Race',
                         'DF_total_tom':'Two or More Races'
                         }

race_dropdown_labels = ['All Races','White','Black or African American',
                   'American Indian & Alaska Native','Asian',
                   'Native Hawaiian & Other Pacific Islander',
                   'Hispanic or Latino','Some Other Race','Two or More Races'
                   ]

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

# Function to load workbooks and store variables with their names
def load_workbooks_into_dataframes():
    dataframes = {}
    statistics_folder = 'Statistics_Dataframes'
    for name in dataframe_labels_dict:
        filename = os.path.join(statistics_folder, f"{name}.xlsx")
        df = pd.read_excel(filename)
        dataframes[name] = df
    return dataframes

dataframes = load_workbooks_into_dataframes()

# Layout for Race page
layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(id='race_dropdown',
                        options=[{'label': label, 'value': i} for i, 
                                 label in enumerate(race_dropdown_labels)],
                                 # The default value (index of the first item in the list)
                                 value=0,
                        ),
                dbc.Col(id='state_dropdown',
                        options=[{'label': state_name, 'value': fips_code} for state_name, 
                                 fips_code in state_dropdown_dict.items()],
                                 # The default value (index of the first item in the list)
                                 value=0,
                        )
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
@app.callback(
    dash.dependencies.Output('choropleth-map', 'figure'),
    [dash.dependencies.Input('race_dropdown', 'value'),
     dash.dependencies.Input('state_dropdown', 'value')
     ]
)
def update_choropleth_map(selected_race, selected_fips_code):
    # Get the selected DataFrame based on the selected_race
    selected_dataframe = dataframe_labels_dict[selected_race]

    # Check if the value from the 'state_dropdown' is 'ALL'
    if selected_fips_code == 'ALL':
        # If 'ALL' is selected, show the entire United States (including Alaska and Hawaii)
        # Set the scope to 'usa'
        scope = 'usa'
        # Set the locations to an empty list to show the entire United States
        locations = []
    else:
        # If a specific state is selected, set the scope to the selected FIPS code
        scope = selected_fips_code
        # Find the column labeled 'FIPS' from the selected DataFrame and get its values
        locations = selected_dataframe['FIPS'].tolist()

    # Create the choropleth map using Plotly Express
    fig = px.choropleth(
        selected_dataframe,
        geojson='us_states.geojson',  # Path to the GeoJSON file
        locations=locations,  # Use the locations based on the selected state or 'ALL'
        featureidkey="properties.postal",  # Key in GeoJSON properties that corresponds to state codes
        color='value_column',  # Replace 'value_column' with the actual column name in your DataFrame containing the data values to visualize
        scope=scope,  # Set the scope to the selected state or 'usa'
        hover_name='FIPS',  # Column in selected_dataframe for hover labels
        hover_data=['value_column'],  # Replace 'value_column' with the actual column name in your DataFrame for additional hover info
        labels={'value_column': 'Data Value'},  # Label for the color scale
        title=f'Choropleth Map for {selected_fips_code}',  # Title for the map
    )

    return fig
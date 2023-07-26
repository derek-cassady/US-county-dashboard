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

age_cols = ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14',
            '15','16','17','18','19','20','21','22','23','24','25','26','27',
            '28','29','30','31','32','33','34','35','36','37','38','39','40',
            '41','42','43','44','45','46','47','48','49','50','51','52','53',
            '54','55','56','57','58','59','60','61','62','63','64','65','66',
            '67','68','69','70','71','72','73','74','75','76','77','78','79',
            '80','81','82','83','84','85','86','87','88','89','90','91','92',
            '93','94','95','96','97','98','99','102','107','110'
           ]

perc_cols = ['0_perc','1_perc','2_perc','3_perc','4_perc','5_perc','6_perc',
             '7_perc','8_perc','9_perc','10_perc','11_perc','12_perc',
             '13_perc','14_perc','15_perc','16_perc','17_perc','18_perc',
             '19_perc','20_perc','21_perc','22_perc','23_perc','24_perc',
             '25_perc','26_perc','27_perc','28_perc','29_perc','30_perc',
             '31_perc','32_perc','33_perc','34_perc','35_perc','36_perc',
             '37_perc','38_perc','39_perc','40_perc','41_perc','42_perc',
             '43_perc','44_perc','45_perc','46_perc','47_perc','48_perc',
             '49_perc','50_perc','51_perc','52_perc','53_perc','54_perc',
             '55_perc','56_perc','57_perc','58_perc','59_perc','60_perc',
             '61_perc','62_perc','63_perc','64_perc','65_perc','66_perc',
             '67_perc','68_perc','69_perc','70_perc','71_perc','72_perc',
             '73_perc','74_perc','75_perc','76_perc','77_perc','78_perc',
             '79_perc','80_perc','81_perc','82_perc','83_perc','84_perc',
             '85_perc','86_perc','87_perc','88_perc','89_perc','90_perc',
             '91_perc','92_perc','93_perc','94_perc','95_perc','96_perc',
             '97_perc','98_perc','99_perc','102_perc','107_perc','110_perc'
             ]

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H3('Race Group Selection'),
                        dcc.Dropdown(
                            id='race-dropdown', 
                            options=[{'label': v[0], 'value': k} 
                                     for k, v in dataframe_labels_dict.items()],
                            value='DF_total_all'
                        )
                    ],
                    width=12
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H3('State Selection'),
                        dcc.Dropdown(
                            id='state-dropdown',
                            options=[{'label': state, 'value': fips} 
                                     for state, fips in state_to_fips.items()],
                            value=state_to_fips['United States']
                        )
                    ],
                    width=6
                ),
                dbc.Col(
                    [
                        html.H3('Alaska'),
                        dcc.Textarea(id='text-box',
                                     value="Alaska is not treated by Plotly Express in the same manner as other states, so it has its' own graph.",
                                     style={'width': '100%', 
                                            'fontWeight': 'bold', 
                                            'textAlign': 'center'
                                    },
                                    readOnly=True
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
                        dcc.Graph(id='choropleth-map')
                    ], 
                    width=6
                ),
                dbc.Col(
                    [
                        dcc.Graph(id='alaska-map')
                    ], 
                    width=6
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(html.H3('NIH Age groups of...', style={'text-align': 'center'}), width=4),
                dbc.Col(html.H3('Age distribution of...', style={'text-align': 'center'}), width=8),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id='pie-chart'), width=4),
                dbc.Col(dcc.Graph(id='bar-chart'), width=8),
            ]
        ),
    # Hidden div to store information for charts
    html.Div(id='selected-race', style={'display': 'none'}),
    html.Div(id='location-clicked', style={'display': 'none'}),
    ]
)

# Define the callback to update the selected race hidden div when a new race is selected
@callback(
    Output('selected-race', 'children'),
    [Input('race-dropdown', 'value')]
)
# Taking current selection from 'race-dropdown', 
# updating 'children' property of 'selected-race' div
def update_selected_race(selected_race):
    return selected_race

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
        # Sets the chart background color. (LightGray, #D3D3D3)
        paper_bgcolor='#D3D3D3',
    )

    fig.update_geos(
        bgcolor='#D3D3D3',
        
        # Boolean value that determines whether or not coastlines are displayed.
        showcoastlines=True,
        # Sets the coastline color.
        coastlinecolor="Black",
        # Sets the coastline line width (in px).
        coastlinewidth=3,
        
        # Boolean value that determines whether or not lakes are displayed.
        showlakes=True,
        # Sets the lake color.
        lakecolor="Aqua",
        
        # Boolean value that determines whether or not rivers are displayed.
        showrivers=True,
        # Sets the river color.
        rivercolor="Blue",
        # Sets the river line width (in px).
        riverwidth=1,
        
        # Boolean value that determines whether or not land is displayed.
        showland=True,
        # Sets the land color. (DarkGreen, #006400)
        landcolor="#006400",
        
        # Boolean value that determines whether or not state borders are displayed.
        showsubunits=True,
        # Sets the state border color.
        subunitcolor="Blue",
        # Sets the state border line width (in px).
        subunitwidth=1,

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
    df_alaska = df[df['State'] == '02']  # Filter the dataframe to get only Alaska data

    min_alaska = df_alaska[dataframe_labels_dict[selected_race][1]].min()  # Calculate min
    max_alaska = df_alaska[dataframe_labels_dict[selected_race][1]].max()  # Calculate max

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
                          range_color=[min_alaska, max_alaska]  # Set the range_color to min and max of Alaska data
                          )
    fig_1.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                        paper_bgcolor='#D3D3D3',
                        # plot_bgcolor='#D3D3D3',
                        )
    fig_1.update_geos(
        lonaxis_range=[20, 380],
        projection_scale=6,
        center=dict(lat=61),
        visible=False,
        # Sets the chart background color. (LightGray, #D3D3D3)
        bgcolor='#D3D3D3',
        
        # Boolean value that determines whether or not coastlines are displayed.
        showcoastlines=True,
        # Sets the coastline color.
        coastlinecolor="Black",
        # Sets the coastline line width (in px).
        coastlinewidth=3,
        
        # Boolean value that determines whether or not lakes are displayed.
        showlakes=True,
        # Sets the lake color.
        lakecolor="Aqua",
        
        # Boolean value that determines whether or not rivers are displayed.
        showrivers=True,
        # Sets the river color.
        rivercolor="Blue",
        # Sets the river line width (in px).
        riverwidth=1,
        
        # Boolean value that determines whether or not land is displayed.
        showland=True,
        # Sets the land color. (DarkGreen, #006400)
        landcolor="#006400",
        
        # Boolean value that determines whether or not state borders are displayed.
        showsubunits=True,
        # Sets the state border color.
        subunitcolor="Black",
        # Sets the state border line width (in px).
        subunitwidth=2,

)

    return fig_1

# Define the callback to update the pie chart
@callback(
    [Output('location-clicked', 'children'),
     Output('pie-chart', 'figure')],
    [Input('choropleth-map', 'clickData'),
     Input('alaska-map', 'clickData'),
     Input('selected-race', 'children')]
)
def update_pie_chart(choropleth_clickData, alaska_clickData, selected_race):
    # Get the clicked county FIPS from either of the maps
    if choropleth_clickData is not None:
        clicked_county_FIPS = choropleth_clickData['points'][0]['location']
    elif alaska_clickData is not None:
        clicked_county_FIPS = alaska_clickData['points'][0]['location']
    else:
        raise dash.exceptions.PreventUpdate  # Don't update the chart if no county is clicked

    # Get the data for the clicked county
    df = dataframes[selected_race]  # Use the selected race here
    df = df[df['FIPS'] == clicked_county_FIPS]

    # Create a new dataframe with the age group and the corresponding percentage
    age_df = pd.DataFrame({
        'Age Group': age_cols,
        'Percentage': df[perc_cols].values[0]  # Assuming there's only one row for each FIPS code
    })

    # Assign NIH age categories
    bins = [-1, 1, 12, 17, 64, float('inf')]  # Adjust the bins to reflect the changes in the age categories
    labels = ['Neonates, Newborns, & Infants', 'Children', 'Adolescents', 'Adults', 'Older Adults']
    age_df['Age Group'] = pd.to_numeric(age_df['Age Group'], errors='coerce')
    age_df['Age Category'] = pd.cut(age_df['Age Group'], bins=bins, labels=labels)

    # Group by NIH age categories and sort the dataframe
    pie_df = age_df.groupby('Age Category')['Percentage'].sum().reset_index()
    pie_df = pie_df.sort_values('Percentage', ascending=False)

    location_name = 'Unknown'
    if choropleth_clickData is not None:
        location_name = choropleth_clickData['points'][0]['hovertext']
    elif alaska_clickData is not None:
        location_name = alaska_clickData['points'][0]['hovertext']

    race_title = dataframe_labels_dict[selected_race][0]
    title = f"{race_title} - {location_name}"

    # Create the pie chart
    fig_2 = px.pie(pie_df, values='Percentage', names='Age Category')

# Add the labels to the pie chart and remove the legend
    fig_2.update_traces(textinfo='percent+label', textfont_size=14, textposition='outside', insidetextorientation='radial')
    fig_2.update_layout(showlegend=False)

    fig_2.update_layout(
    margin={"r": 0, "t": 50, "l": 0, "b": 0},
    title={
        'text': title,
        'x': 0.5,
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

    return location_name, fig_2

# Define the callback to update the histogram
@callback(
    Output('bar-chart', 'figure'),
    [Input('location-clicked', 'children'),
     Input('selected-race', 'children')]
)
def update_histogram(clicked_county_FIPS, selected_race):
    if clicked_county_FIPS is None:
        raise dash.exceptions.PreventUpdate  # Don't update the chart if no county is clicked

    # Get the data for the clicked county
    df = dataframes[selected_race].copy()  # Use the selected race here and create a copy to avoid modifying original df
    clicked_county_df = df[df['Location'] == clicked_county_FIPS]

    # Check if any data exists for the clicked county
    if clicked_county_df.empty:
        raise dash.exceptions.PreventUpdate

    # Extract average age
    average_age = clicked_county_df['Average_Age'].values[0]

# Create a new dataframe with the age group, the corresponding count, average age, and percentage
    age_df = pd.DataFrame({
        'Age': age_cols,
        'Population': clicked_county_df[age_cols].values[0],
        'Average_Age': [float(average_age)] * len(age_cols),
        '_perc': clicked_county_df[perc_cols].values[0].astype(float),
        })
    
    # Convert 'Age' to integer
    age_df['Age'] = age_df['Age'].astype(int)
    
    # Create the figure
    fig_3 = px.bar(age_df, x='Age', y='Population',
                         hover_data={'Average_Age': ':.2f', 
                                     '_perc': ':.2%'},
                         labels={'Average_Age': 'Avg Age', 
                                 '_perc': 'Percentage'})

    race_title = dataframe_labels_dict[selected_race][0]

    # Update the layout
    fig_3.update_layout(
        title={
            'text': f"{race_title} - {clicked_county_df['Location'].iloc[0]}",
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(
                size=24,
                color='rgb(107, 107, 107)'
            )
        },
        paper_bgcolor='#D3D3D3',
        plot_bgcolor='#D3D3D3'
    )

    fig_3.update_xaxes(tickangle=315)  # rotate x-axis labels by 45 degrees

    return fig_3


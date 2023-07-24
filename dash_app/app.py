import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# Create Dash instance, True for multipage app
app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.DARKLY])

navbar = dbc.Nav(
            [
                dbc.NavLink(
                    [
                        html.Div(page['name'], className='ms-2')
                        ],
                        href=page['path'],
                        active= 'exact',
                        )
                        for page in dash.page_registry.values()
            ],
            vertical = False,
            pills= True,
            className= 'bg=light',
)
# Layout of the app
# Container holds to page
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Div("Selected Demographic for US Counties",
                         style={'fontSize':50, 'textAlign':'center'}))
    ]),

    html.Hr(),
    dbc.Row(
        # Contents of Row and size relative to screen size
        [navbar]),
    dbc.Row(
        # Contents of each page to be displayed
        # Contents of Row and size relative to screen size
        [dash.page_container])
        ],fluid=True
    )


# Execute
if __name__ == "__main__":
    app.run(debug=True)
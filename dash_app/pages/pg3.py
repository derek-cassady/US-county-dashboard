import dash
from dash import dcc, html

# Page Registry
dash.register_page(__name__)

layout = html.Div(
    [
        dcc.Markdown('# This will be the content of Page 3 and much more!')
    ]
)

# layout = html.Div(
#     [
#         dcc.Markdown('# This will be the content of Page 3')
#     ]
# )
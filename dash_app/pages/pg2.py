import dash
from dash import dcc, html
import plotly.express as px

# Page Registry
dash.register_page(__name__)

layout = html.Div(
    [
        dcc.Markdown('# This will be the content of Page 2 and much more!')
    ]
)
# df = px.data.tips()

# layout = html.Div(
#     [
#         dcc.RadioItems([x for x in df.day.unique()], id='day-choice'),
#         dcc.Graph(id='bar-fig',
#                   figure=px.bar(df, x='smoker', y='total_bill'))
#     ]
# )
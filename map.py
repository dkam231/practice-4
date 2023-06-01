from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

df=pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_us_cities.csv')
app = Dash(__name__)
pear=df['pop'].astype(str)
df['text']=df['name'] +' has a population of '+ df['pop'].astype(str)
fig = go.Figure(data=go.Scattergeo(
    lon=df['lon'],
    lat=df['lat'],
    text=df['text'],
    mode='markers',
))

fig.update_layout(
    geo_scope='usa'
)
app.layout = html.Div(children=[
    html.Div(className='row', children='My First App with a Map of the United States',
             style={'textAlign': 'center', 'color': 'black', 'fontSize': 30}),

    dcc.Graph(
        id='example-map',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
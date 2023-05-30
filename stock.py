from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

df = pd.read_csv('https://raw.githubusercontent.com/datasets/s-and-p-500-companies/main/data/constituents.csv')
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.layout=html.Div([
    html.Div(className='row', children='My First App with timeline graph',
             style={'textAlign': 'center', 'color': 'black', 'fontSize': 30}),
    dash_table.DataTable(
        id='table-multicol-sorting',
        columns=[
            {"name": i, "id": i} for i in sorted(df.columns)
        ],
        page_current=0,
        page_size=20,
        page_action='custom',
        sort_action='custom',
        sort_action='alphabetic'
        sort_mode='multi',
        sort_by=[]
    )
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
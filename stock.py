from numpy import argsort
import pandas as pd
import plotly.graph_objects as go
from geopy.geocoders import Nominatim as nm
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import threading

df = pd.read_csv('constituents.csv')
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)
geolocator = nm(user_agent=__name__)
count = 0


def geocode_location(row):
    headq = f"{row['Headquarters']}"
    try:
        location = geolocator.geocode(headq)
        row['lat'] = location.latitude
        row['lon'] = location.longitude
    except:
        row['lat'] = None
        row['lon'] = None
    return row


def geocode_dataframe(df):
    threads = []
    i=0
    for i in range(500):
        row=df.iloc(i)
        t = threading.Thread(target=geocode_location, args=(row))
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()


df_with_coords = df.apply(geocode_dataframe, axis=1)

fig = go.Figure(data=go.Scattergeo(
    lat=df_with_coords['lat'],
    lon=df_with_coords['lon'],
    text=df_with_coords['Headquarters'],
    mode='markers',
))

fig.update_layout(
    title='Company Headquarters',
    geo=dict(
        scope='world',
        showland=True,
        landcolor='rgb(217, 217, 217)',
        showcountries=True,
        countrycolor='rgb(255, 255, 255)',
        showocean=True,
        oceancolor='rgb(166, 202, 240)',
        showcoastlines=True,
        coastlinecolor='rgb(28, 28, 28)',
        projection_type='equirectangular'
    ),
)

app.layout = html.Div([
    dcc.Graph(figure=fig),
    dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": True, "selectable": True} for i in df.columns
        ],
        data=df_with_coords.to_dict('records'),
        editable=False,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        row_selectable="multi",
        row_deletable=True,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current=0,
        page_size=10,
    )
])


@app.callback(
    Output('datatable-interactivity', 'style_data_conditional'),
    Input('datatable-interactivity', 'selected_columns')
)
def update_styles(selected_columns):
    return [{
        'if': {'column_id': i},
        'background_color': '#D2F3FF'
    } for i in selected_columns]


if __name__ == '__main__':
    app.run_server(debug=True)

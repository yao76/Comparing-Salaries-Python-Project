import pandas as pd

import plotly

import plotly.graph_objs as go


	
import plotly.offline as offline

from plotly.graph_objs import *

from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot


df = pd.read_csv('data.csv')

df_year = df[(df['Year']== 2016 )]


for col in df_year.columns:
    df_year[col] = df_year[col].astype(str)

df_year['text'] = df_year['STATE']+'ST: ' + df_year['ST'] + ' Job Title: '+df_year['OCC_TITLE'] + df_year['A_MEAN']

# df_year['text'] = df_year['STATE'] + '<br>' + df_year['ST'] + '<br>'  + ' Job ' + '<br>' + df_year['OCC_TITLE'] + '<br>' + df_year['A_MEAN']
    # 'Fruits ' + df['total fruits'] + ' Veggies ' + df['total veggies'] + '<br>' + \
    # 'Wheat ' + df['wheat'] + ' Corn ' + df['corn']

fig = go.Figure(data=go.Choropleth(
    locations=df_year['ST'],
    z=df['A_MEAN'],
    locationmode='USA-states',
    colorscale='Greens',
    autocolorscale=False,
    text=df_year['text'], # hover text
    marker_line_color='white', # line markers between states
    colorbar_title="USD"
))

fig.update_layout(
    title_text='Butthole<br>(Hover for breakdown)',
    geo = dict(
        scope='usa',
        projection=go.layout.geo.Projection(type = 'albers usa'),
        showlakes=False, # lakes
        lakecolor='rgb(255, 255, 255)'),
)

fig.show()

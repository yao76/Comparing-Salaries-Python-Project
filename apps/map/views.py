import pandas as pd
import plotly
import numpy as np
import plotly.graph_objs as go
import plotly.offline as offline
from plotly.graph_objs import *
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from django.shortcuts import render, HttpResponse
import datetime

# Create your views here.


def index(request):
    df = pd.read_csv('data2018.csv')
    # df_year = df[(df['Year'] == 2018)]

    for col in df.columns:
        df.loc[col] = df[col].astype(str)

    # x = "State: " + df['ST'] + '<br>' + 'Job Title: ' + \
    #     df['OCC_TITLE'] + '<br>' + 'Annual Sal: ' + '$' + df['A_MEAN']

    # df_year['text'] = df_year['STATE'] + '<br>' + df_year['ST'] + '<br>'  + ' Job ' + '<br>' + df_year['OCC_TITLE'] + '<br>' + df_year['A_MEAN']
    # 'Fruits ' + df_year['total fruits'] + ' Veggies ' + df_year['total veggies'] + '<br>' + \
    # 'Wheat ' + df_year['wheat'] + ' Corn ' + df_year['corn']

    fig = go.Figure(data=go.Choropleth(
        locations=df['ST'],
        z=df['A_MEAN'],
        locationmode='USA-states',
        colorscale="greens",
        autocolorscale=False,
        # text=x,  # hover text
        marker_line_color='white',  # line markers between states
        colorbar_title="USD"
    ))

    fig.update_layout(
        title_text='Average Salary of Computer/Technical Jobs',
        geo=dict(
            scope='usa',
            projection=go.layout.geo.Projection(type='albers usa'),
            showlakes=False,  # lakes
            lakecolor='rgb(255, 255, 255)'),
        margin=dict(t=5,b=5,r=5,l=5)
    )

    def calc_annual_AVG(csv):
        data = pd.read_csv(csv)

        codedata = data[(data['OCC_CODE'] == "15-0000")]
        testArr = codedata['A_MEAN'].tolist()
        total =0
        length = len(testArr)
        for i in range(length):
            total += int(testArr[i])

        annual_avg = int(total/length)
        return annual_avg

    avg2018 = calc_annual_AVG("data2018.csv")
    avg2017 = calc_annual_AVG("data2017.csv")
    avg2016 = calc_annual_AVG("data2016.csv")
    print(avg2016, avg2017, avg2018)
        
    # fig.show()
    sal_map = offline.plot(fig, include_plotlyjs=False, output_type='div')

    years = [datetime.datetime(year=2016, month=1, day=1),
            datetime.datetime(year=2017, month=1, day=1),
            datetime.datetime(year=2018, month=1, day=1)]
    
    graph = go.Figure()
    graph.add_trace(go.Scatter(x=years, y=[80000, 83500, 96000], name="2018"))
    graph.add_trace(go.Scatter(x=years, y=[50000, 63500, 76000], name="2017"))
    graph.update_layout(
        xaxis_range=[datetime.datetime(2016,1,1), datetime.datetime(2018,1,1)],
        autosize=True,
        height=200,
        margin=dict(t=5,b=5,r=5,l=5)
        )
    
    states = {
        "Alabama":0,
        "Alaska":1,
        "Arizona":2,
        "Arkansas":3,
        "California":4,
        "Colorado":5,
        "Connecticut":6,
        "Delaware":7,
        "Florida":8,
        "Georgia":9,
        "Hawaii":10,
        "Idaho":11,
        "Illinois":12,
        "Indiana":13,
        "Iowa":14,
        "Kansas":15,
        "Kentucky":16,
        "Louisiana":17,
        "Maine":18,
        "Maryland":19,
        "Massachusetts":20,
        "Michigan":21,
        "Minnesota":22,
        "Mississippi":23,
        "Missouri":24,
        "Montana":25,
        "Nebraska":26,
        "Nevada":27,
        "New Hampshire":28,
        "New Jersey":29,
        "New Mexico":30,
        "New York":31,
        "North Carolina":32,
        "North Dakota":33,
        "Ohio":34,
        "Oklahoma":35,
        "Oregon":36,
        "Pennsylvania":37,
        "Rhode Island":38,
        "South Carolina":39,
        "South Dakota":40,
        "Tennessee":41,
        "Texas":42,
        "Utah":43,
        "Vermont":44,
        "Virginia":45,
        "Washington":46,
        "West Virginia":47,
        "Wisconsin":48,
        "Wyoming":49
    }
    statesNoWA = {
        "Alabama":0,
        "Alaska":1,
        "Arizona":2,
        "Arkansas":3,
        "California":4,
        "Colorado":5,
        "Connecticut":6,
        "Delaware":7,
        "Florida":8,
        "Georgia":9,
        "Hawaii":10,
        "Idaho":11,
        "Illinois":12,
        "Indiana":13,
        "Iowa":14,
        "Kansas":15,
        "Kentucky":16,
        "Louisiana":17,
        "Maine":18,
        "Maryland":19,
        "Massachusetts":20,
        "Michigan":21,
        "Minnesota":22,
        "Mississippi":23,
        "Missouri":24,
        "Montana":25,
        "Nebraska":26,
        "Nevada":27,
        "New Hampshire":28,
        "New Jersey":29,
        "New Mexico":30,
        "New York":31,
        "North Carolina":32,
        "North Dakota":33,
        "Ohio":34,
        "Oklahoma":35,
        "Oregon":36,
        "Pennsylvania":37,
        "Rhode Island":38,
        "South Carolina":39,
        "South Dakota":40,
        "Tennessee":41,
        "Texas":42,
        "Utah":43,
        "Vermont":44,
        "Virginia":45,
        "Washington":46,
        "West Virginia":47,
        "Wisconsin":48,
        "Wyoming":49
    }
    
    line_graph = offline.plot(graph, include_plotlyjs=False, output_type='div')
    context = {
    'map': sal_map,
    'line_graph' : line_graph,
    "states": states,
    "statesNoWA": statesNoWA
    }
    return render(request, "map/index.html", context)


# pd.options.mode.chained_assignment = None

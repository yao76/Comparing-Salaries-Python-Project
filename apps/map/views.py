import pandas as pd
import plotly
import numpy as np
import plotly.graph_objs as go
import plotly.offline as offline
from plotly.graph_objs import *
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from django.shortcuts import render, HttpResponse
import datetime
import json

# Create your views here.


def index(request):
    df = pd.read_csv('data2018.csv')
    # df_year = df[(df['Year'] == 2018)]

    for col in df.columns:
        df.loc[col] = df[col].astype(str)

    x = "State: " + df['ST'] + '<br>' + 'Job Title: ' + \
        df['OCC_TITLE'] + '<br>' + 'Annual Sal: ' + '$' + df['A_MEAN']


    fig = go.Figure(data=go.Choropleth(
        locations=df['ST'],
        z=df['A_MEAN'],
        locationmode='USA-states',
        colorscale="greens",
        autocolorscale=False,
        text=x,  # hover text
        marker_line_color='white',  # line markers between states
        colorbar_title="USD"
    ))
    all_jobs = ["15-0000",'15-1121','15-1131','15-1132','15-1133','15-1134','15-1141','15-1142','15-1143','15-1151','15-1152','15-1199','15-1111','15-1122']

    fig.update_layout(
        title_text='Average Salary of Computer/Technical Jobs',
        geo=dict(
            scope='usa',
            projection=go.layout.geo.Projection(type='albers usa'),
            showlakes=False,  # lakes
            lakecolor='rgb(255, 255, 255)'),
        margin=dict(t=5,b=5,r=5,l=5)
    )

    state_conv_list = {
        0:'AL',
        1:'AK',
        2:'AZ',
        3:'AR',
        4:'CA',
        5:'CO',
        6:'CT',
        7:'DE',
        8:'FL',
        9:'GA',
        10:'HI',
        11:'ID',
        12:'IL',
        13:'IN',
        14:'IA',
        15:'KS',
        16:'KY',
        17:'LA',
        18:'ME',
        19:'MD',
        20:'MA',
        21:'MI',
        22:'MN',
        23:'MS',
        24:'MO',
        25:'MT',
        26:'NE',
        27:'NV',
        28:'NH',
        29:'NJ',
        30:'NM',
        31:'NY',
        32:'NC',
        33:'ND',
        34:'OH',
        35:'OK',
        36:'OR',
        37:'PA',
        38:'RI',
        39:'SC',
        40:'SD',
        41:'TN',
        42:'TX',
        43:'UT',
        44:'VT',
        45:'VA',
        46:'WA',
        47:'WV',
        48:'WI',
        49:'WY'}

    def state_annual_AVG(year, ST_num):
        annual_avg = 0
        allSTList = []
        jobList = []
        data = pd.read_csv("data"+str(year)+".csv")
        codedata = data[(data['OCC_CODE']== '15-0000')]
        allSTList = codedata['A_MEAN'].tolist()
        annual_avg = allSTList[ST_num]
        return annual_avg

    def state_jobs(ST_num, jobs=all_jobs):
        annual_avgs = []
        addSTList = []
        jobList = []
        data = pd.read_csv("data2018.csv")
        for i in range(len(jobs)):
            codedata = data[(data['OCC_CODE']== jobs[i])]
            addSTList = codedata[(codedata['ST'] == state_conv_list[ST_num])]
            # print(addSTList)
            annual_avgs.append([addSTList['OCC_CODE'].tolist(), addSTList['A_MEAN'].tolist()])
        return annual_avgs

    def calc_annual_AVG(year):
        data = pd.read_csv("data"+str(year)+".csv")
        codedata = data[(data['OCC_CODE'] == "15-0000")]
        testArr = codedata['A_MEAN'].tolist()
        total =0
        length = len(testArr)
        for i in range(length):
            total += int(testArr[i])

        annual_avg = int(total/length)
        return annual_avg

    avg2018 = calc_annual_AVG(2018)
    avg2017 = calc_annual_AVG(2017)
    avg2016 = calc_annual_AVG(2016)
    st_avg2018 = state_annual_AVG(2018, 0)
    st_avg2017 = state_annual_AVG(2017, 0)
    st_avg2016 = state_annual_AVG(2016, 0)
    # print(avg2016,avg2017,avg2018)
    # print(st_avg2016,st_avg2017,st_avg2018)

    print(state_jobs(5))
    # fig.show()
    sal_map = offline.plot(fig, include_plotlyjs=False, output_type='div')

    years = [datetime.datetime(year=2016, month=1, day=1),
            datetime.datetime(year=2017, month=1, day=1),
            datetime.datetime(year=2018, month=1, day=1)]
    
    graph = go.Figure()
    graph.add_trace(go.Scatter(x=years, y=[st_avg2016, st_avg2017, st_avg2018], name="Alabama"))
    graph.add_trace(go.Scatter(x=years, y=[avg2016, avg2017, avg2018], name="National Average"))
    graph.update_layout(
        xaxis_range=[datetime.datetime(2016,1,1), datetime.datetime(2018,1,1)],
        autosize=True,
        height=200,
        margin=dict(t=5,b=5,r=5,l=5)
        
        )

    line_graph = offline.plot(graph, include_plotlyjs=False, output_type='div')
    context = {
    'map': sal_map,
    'line_graph' : line_graph
    }
    return render(request, "map/index.html", context)


# pd.options.mode.chained_assignment = None

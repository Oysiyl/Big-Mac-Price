#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 12 20:07:00 2018

@author: dmitriy
"""
import pandas as pd
import numpy as np
import random
import plotly
import plotly.graph_objs as go

df = pd.read_csv("Big Mac Index.csv", usecols=["date", "iso_a3", "name",
                                               "dollar_price", "USD_raw"])
df["date"] = pd.to_datetime(df["date"])
df.rename(columns={"iso_a3": "country"}, inplace=True)
df["USD_raw"] = df["USD_raw"]*100

df = df.round({"dollar_price": 2, "USD_raw": 1, "EUR_raw": 1, "GBP_raw": 1,
               "JPY_raw": 1, "CNY_raw": 1})
print(df.head(5))
print(df.dtypes)
usa = df[df["name"] == "United States"].reset_index(drop=True)
rus = df[df["name"] == "Russia"].reset_index(drop=True)
print(usa)
print(rus)
df2 = pd.DataFrame({"country1": usa["name"],
                    "country2": rus["name"],
                    "price1": usa["dollar_price"],
                    "price2": rus["dollar_price"]})
print(df2)
df3 = df.groupby(["name"])["date"].count()
print(df3)
countrynames = [*np.unique(df["name"])]
print(countrynames)
print(len(countrynames))
colors = np.random.rand(len(countrynames))


def random_color():
    levels = range(32, 256, 32)
    return "rgb" + str(tuple(random.choice(levels) for _ in range(3)))


print(random_color())


def tracing(countryname):
    eachcountry = df[df["name"] == countryname]
    trace = go.Bar(
        x=eachcountry["date"],
        y=eachcountry["dollar_price"],
        name=countryname,
        text=countryname,
        textposition='auto',
        hoverinfo="x+y",
        marker=dict(
            line=dict(
                color='rgba(0,0,0,1.0)',
                width=1
            ),
            color=random_color()
        )
    )
    del eachcountry
    return trace


data = []
for i in range(len(countrynames)):
    trace = tracing(countrynames[i])
    data.append(trace)
layout = go.Layout(
    title='Big Mac index through the years',
    xaxis=dict(
        title='Years',
        tickfont=dict(
            size=14,
            color='rgb(107, 107, 107)'
        )
    ),
    yaxis=dict(
        title='Dollar price for one burger',
        titlefont=dict(
            size=16,
            color='rgb(107, 107, 107)'
        ),
        tickfont=dict(
            size=14,
            color='rgb(107, 107, 107)'
        )
    ),
    legend=dict(
        x=1.0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    )
)

fig = go.Figure(data=data, layout=layout)
plotly.offline.plot(fig, filename='BigMac.html', auto_open=False)

import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
# brought in fastapi just in case real time data is to be implemented
from fastapi import FastAPI


df = pd.read_csv("./data_date.csv")
st.dataframe(df)
'''
sort based on country
provide a search or select option to choose country and display the table accordingly
generate graph showing the different variation in the time series data for each country
various graphs can include 
bar chart -> categories for the status part
line chart -> aqi value variation for each country
altair chart -> clusters of aqi and status
pie chart -> proportion of countries based on count of status and highest contribution in AQI 
'''
# sorting data based on country

# chart functions
def bar_chart(df):
    chart = alt.Chart(df).mark_bar().encode(
        x='count(status):Q',
        y='Status:N',
        color='Status:N'
    ).interactive()
    st.altair_chart(chart)
    
def line_chart(df,option):
    df_country = df[df.Country == option]
    chart = alt.Chart(df_country).mark_line().encode(
        x='Date:N'
        ,y='AQI Value:Q')    
    st.altair_chart(chart)
        
def altair_chart():
    pass
def pie_chart_type_1(df):
    # based on status
    k={}
    x=[]
    for i in df['Status']:
        x.append(i)       
    for i in x:
        k[i] = x.count(i)
    print(k,x)
    fig = go.Figure(data=[go.Pie(labels=list(set(x)),values=list(k.values()), textinfo='label+percent',insidetextorientation='radial')])
    st.plotly_chart(fig)
        
def pie_chart_type_2():
    pass

st.header("Number of countries in each Status group")
bar_chart(df)
st.header("Proportion of countries in each status")
pie_chart_type_1(df)
st.header("Change in AQI date wise and Country wise")
option = st.selectbox(label="Choose country",options=df['Country'].unique())
if option:
    line_chart(df,option)
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
        y='count(status):Q',
        x='Status:N',
        color='Status:N'
    ).interactive()
    st.altair_chart(chart)
    
def line_chart(df,option):
    df_country = df[df.Country == option]
    chart = alt.Chart(df_country).mark_line().encode(
        x='Date:N'
        ,y='AQI Value:Q')    
    st.altair_chart(chart)
        
def altair_chart(df):
    k={'Country':[],'Avg AQI':[],'Status':[]}
    for i in df.Country:
        x=df[df.Country == i]
        if i not in k['Country']:
            k['Country'].append(i)
            k['Avg AQI'].append(sum(x['AQI Value'])/len(x))
            
            if sum(x['AQI Value'])//len(x) in range(0,51):
                k['Status'].append('Good')
            elif sum(x['AQI Value'])//len(x) in range(51,101):
                k['Status'].append('Moderate')
            elif sum(x['AQI Value'])//len(x) in range(101,151):
                k['Status'].append('Unhealthy for Sensitive Groups')
            elif sum(x['AQI Value'])//len(x) in range(151,201):
                k['Status'].append('Unhealthy')
            elif sum(x['AQI Value'])//len(x) in range(201,301):
                k['Status'].append('Very Unhealthy')
            elif sum(x['AQI Value'])//len(x) >300:
                k['Status'].append('Hazardous')
                
    a=pd.DataFrame(data=k,columns=['Country','Avg AQI','Status'])
    st.dataframe(a)
    chart = alt.Chart(data=a).mark_circle(size=60).encode(
        x='Avg AQI'
        ,y='Status:N'
        ,color='Country:N'
    )
    st.altair_chart(chart)
    
def pie_chart_type_1(df):
    # based on status
    k={}
    x=[]
    for i in df['Status']:
        x.append(i)       
    for i in x:
        k[i] = x.count(i)

    x = list(set(x))
    fig = go.Figure(data=[go.Pie(labels=x,values=list(k.values()), textinfo='label+percent',insidetextorientation='radial')])
    st.plotly_chart(fig)
        
def pie_chart_type_2():
    k={}

    for i in df.Country:
        x=df[df.Country == i]
        k[i]= sum(x['AQI Value'])/len(x)
    
    x=df['Country']
    x = list(set(x))
    fig = go.Figure(data=[go.Pie(labels=x,values=list(k.values()), textinfo='label+percent',insidetextorientation='radial')])
    st.plotly_chart(fig)

st.header("Number of countries in each Status group")
bar_chart(df)
st.header("Proportion of countries in each status")
pie_chart_type_1(df)
st.header("Change in AQI date wise and Country wise")
option = st.selectbox(label="Choose country",options=df['Country'].unique())
if option:
    line_chart(df,option)

st.header("Pie Chart of average AQI per country")
pie_chart_type_2()

st.header("Clusters of average AQI per country and status")
altair_chart(df)

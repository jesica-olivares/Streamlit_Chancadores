from altair.vegalite.v4.schema.core import Align
import streamlit as st
import altair as alt
import datetime


from mpl_toolkits.axes_grid1 import host_subplot
from mpl_toolkits import axisartist
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")

#add_slider =st.sidebar.slider("Fecha",value=[100,400])
add_slider =st.sidebar.slider("Fecha",value=[datetime.date(2021,1,1),datetime.date(2021,7,1)])

d = st.sidebar.date_input(
         "Seleccione Fechas",
              value=[datetime.date(2021, 1, 1),datetime.date(2021, 2, 1)], 
              min_value=datetime.date(2021, 1, 1),max_value=datetime.date(2021, 7, 1))

fech_inic=pd.Timestamp(add_slider[0])
fech_fin=pd.Timestamp(add_slider[1])

#fech_inic=datetime.date(add_slider[0])
#fech_fin=datetime.date(add_slider[1])

df_status=pd.read_csv("Status.csv",sep=";")
#Convertimos en fecha timestamp
df_status['TIMESTAMP_IOT_2']=pd.to_datetime(df_status["Timestamp"],dayfirst='True')
#en base al error obtenido convertimos el valor encontrado por nan
df_status=df_status.replace('[-11059] No Good Data For Calculation', np.nan, regex=False)
df_status['Throuput']=df_status['Throuput'].astype(float)

df_1h=pd.read_csv("df_1h_power.csv",sep=";",decimal=".").drop(columns='Unnamed: 0')
df_1h['TIMESTAMP_IOT_2']=pd.to_datetime(df_1h["TIMESTAMP_IOT_2"],dayfirst='True')

df_status_filt=df_status[(df_status["TIMESTAMP_IOT_2"]>=fech_inic)&(df_status["TIMESTAMP_IOT_2"]<=fech_fin)].copy()
df_1h_filt=df_1h[(df_1h["TIMESTAMP_IOT_2"]>=fech_inic)&(df_1h["TIMESTAMP_IOT_2"]<=fech_fin)].copy()

thr_mean=round(df_status_filt['Throuput'].mean(),0)

nominal=6000

#Tiempos

import datetime
#data1 = datetime.datetime(2021, 1, 1,0,0,0)
#data2 = datetime.datetime(2021, 7, 1,0,0,0)

data1 = fech_inic
data2 = fech_fin
diff = data2 - data1

days, seconds = diff.days, diff.seconds
hours = days * 24 + seconds // 3600
minutes = (seconds % 3600) // 60
seconds = seconds % 60

available_time=hours



# Use the full page instead of a narrow central column

col1, col2, col3 = st.beta_columns((1,3,1))


with col1:

    #Grafico 1 pie chart status
    pie_chart_status=df_status_filt['Run'].value_counts()
    explode = (0, 0, 0, 0)
    run_time=pie_chart_status[0]/pie_chart_status.sum()

    fig1, ax1 = plt.subplots(figsize=(2, 2))
    ax1.pie(pie_chart_status, explode=explode, labels=pie_chart_status.index,
        shadow=False, startangle=100,colors=['midnightblue','lightgray','lightblue','royalblue'], 
        textprops={'fontsize': 3},autopct=None )
        
    #transformar en donut
    my_circle=plt.Circle( (0,0), 0.7, color='white')
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    #Texto interior
    ax1.text(0., 0., "{:.1%}".format(round(run_time,2)), horizontalalignment='center', 
    verticalalignment='center',size=8)
    ax1.patch.set_edgecolor('black')  

    p=plt.gcf()
    p.gca().add_artist(my_circle)

    st.pyplot(fig1)

with col2:
    st.title("Chancadores Caserones")
    st.subheader("Throuput [TPH]")
    #c=alt.Chart(df_status).mark_line().encode(
    #x=alt.X('TIMESTAMP_IOT_2:T'),# axis=alt.Axis(alt.Scale(interval= 'day', step= 30))),
    #axis=alt.Axis(values=list(range(datetime.datetime(2021, 1, 1,0,0,0), datetime.datetime(2021, 6, 6,0,0,0), 10)))),
    #y='Throuput')
    #axis=alt.Axis(alt.Scale(interval= 'day', step= 30))),
    #st.altair_chart(c, use_container_width=True)
    #plt.axhline(y = thr_mean, color = 'r', linestyle = '--')
    #horline = alt.Chart().mark_rule().encode(
    #y='a:Q')
    #alt.layer(
    #c, horline,
    #data=df_status
    #).transform_calculate(
    #a="300"
    #).facet(
    #row='site'
    #)
    fig1, ax = plt.subplots(figsize=(3,1))
    #ax=plt.axes((0, 0, 1, 1))
    plt.grid(True, axis='y',linewidth=0.2, color='gray', linestyle='-')
    plt.plot(df_status_filt["TIMESTAMP_IOT_2"],df_status_filt['Throuput'],linewidth =0.4, color='midnightblue')
    plt.axhline(y = thr_mean, color = 'r', linestyle = '--',linewidth =0.4)
    fig1.text(0.7,0.4,'Average: '+str(round(thr_mean)),color='red',size=4)
    #fig1.text(2,4,'This text starts at point (2,4)')
    plt.ylabel("", fontsize=3)
    #plt.xlim(fech_inic, fech_fin)
    #plt.xlabel('', fontsize=3)
    ax.tick_params(axis='both', which='major', labelsize=3,width=0.2)
    #ax.patch.set_edgecolor('red')  
    #ax.patch.set_linewidth('0.2')
      #removing top and right borders
    ax.spines['top'].set_linewidth('0.3') 
    ax.spines['right'].set_linewidth('0.3') 
    ax.spines['bottom'].set_linewidth('0.3') 
    ax.spines['left'].set_linewidth('0.3') 
    st.pyplot(fig1)


with col3:
    #Grafico 2 pie chart performance
    utilizacion=thr_mean/nominal

    fig1, ax1 = plt.subplots(figsize=(2, 2))
    ax1.pie([thr_mean,nominal-thr_mean],  labels=('Promedio','Restante'),
        shadow=False, startangle=100,colors=['midnightblue','lightgray'], 
        textprops={'fontsize': 3},autopct=None )
        
    #transformar en donut
    my_circle=plt.Circle( (0,0), 0.7, color='white')
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    #Texto interior
    ax1.text(0., 0., "{:.1%}".format(round(utilizacion,2)), horizontalalignment='center', 
    verticalalignment='center',size=8)
    ax1.patch.set_edgecolor('black')  

    p=plt.gcf()
    p.gca().add_artist(my_circle)

    st.pyplot(fig1)

cola, colb, colc, cold = st.beta_columns((1,1,1,1))

uptime=round(available_time*pie_chart_status[0]/pie_chart_status.sum(),0)


with cola:
    st.write("Uptime Hours",Align='center')
    st.header(uptime)

with colb:
    st.write("Available Hours",Align='center')
    st.header(hours)

with colc:
    st.write("Throuput",Align='center')
    st.header(thr_mean)

with cold:
    st.write("Nominal",Align='center')
    st.header(nominal)


col21, col22 = st.beta_columns((1,1))

df_status_filt['Run2']=np.where(df_status_filt['Run']=='ON',1,0)
with col21:
    #st.write("Chancadores Caserones",,Align='center')
    st.subheader("Status")
    c=alt.Chart(df_status_filt).mark_line().encode(
    x=alt.X('TIMESTAMP_IOT_2:T'),# axis=alt.Axis(alt.Scale(interval= 'day', step= 30))),
    #axis=alt.Axis(values=list(range(datetime.datetime(2021, 1, 1,0,0,0), datetime.datetime(2021, 6, 6,0,0,0), 10)))),
    y='Run2')
    #axis=alt.Axis(alt.Scale(interval= 'day', step= 30))),
    st.altair_chart(c, use_container_width=True)

with col22:
    df_filt=df_1h_filt[df_1h_filt["SIGNAL_NAME"]=="Power"].copy()
    #st.write("Chancadores Caserones",,Align='center')
    st.subheader("Power")
    c=alt.Chart(df_filt).mark_line().encode(
    x=alt.X('TIMESTAMP_IOT_2:T'),# axis=alt.Axis(alt.Scale(interval= 'day', step= 30))),
    #axis=alt.Axis(values=list(range(datetime.datetime(2021, 1, 1,0,0,0), datetime.datetime(2021, 6, 6,0,0,0), 10)))),
    y='AVG_MEASUREMENT')
    #axis=alt.Axis(alt.Scale(interval= 'day', step= 30))),
    st.altair_chart(c, use_container_width=True)

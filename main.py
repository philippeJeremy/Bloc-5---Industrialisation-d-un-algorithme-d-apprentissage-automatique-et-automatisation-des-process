import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px 
import plotly.graph_objects as go


DATA = "get_around_pricing_project.csv"
DATA2 = "get_around_delay_analysis.xlsx"

st.set_page_config(
    page_title="GetAround",
    page_icon="🚗",
    layout="wide"
)

st.markdown("<h1 style='text-align: center; color: white;'>Dashbord GetAround</h1>", unsafe_allow_html=True)

@st.cache
def load_data():
    data = pd.read_csv(DATA)
    return data

@st.cache
def load_data2():
    data2 = pd.read_excel(DATA2)
    return data2

data_load_state = st.text('Loading data...')
data = load_data()
data_load_state.text("")

data_load_state = st.text('Loading data...')
data2 = load_data2()
data_load_state.text("")

checkbox1, checkbox2 = st.columns(2)


with checkbox1:
    if st.checkbox('Viz data 1'):
        st.subheader('Raw data')
        st.write(data)

with checkbox2:
    if st.checkbox('Viz data 2'):
        st.subheader('Raw data')
        st.write(data2)


st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown("")
    model_key = data["model_key"].value_counts()
    
    fig = px.bar(model_key, title="Marque les plus louer")
    fig.update_layout(bargap=0.2)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("")
    car_type = data["car_type"].value_counts()
    
    fig = px.bar(car_type, title="Type de voiture les plus louer")
    fig.update_layout(bargap=0.2)
    st.plotly_chart(fig, use_container_width=True)

col4, col5 = st.columns(2)

with col4:
    st.markdown("")
    checkin_type = data2["checkin_type"].value_counts()
    
    fig = px.bar(checkin_type, title="Mode de location")
    fig.update_layout(bargap=0.2)
    st.plotly_chart(fig, use_container_width=True)

with col5:
    st.markdown("")
    fuel = data["fuel"].value_counts()
    
    fig = px.bar(fuel, title="Energie la plus louer")
    fig.update_layout(bargap=0.2)
    st.plotly_chart(fig, use_container_width=True)
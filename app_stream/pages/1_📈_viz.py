import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px 
import plotly.graph_objects as go



DATA = "get_around_delay_analysis.xlsx"

@st.cache
def load_data():
    data = pd.read_excel(DATA)
    # suppression des colonnes 91% de donnees manquantes
    data.drop(columns=["previous_ended_rental_id","time_delta_with_previous_rental_in_minutes"], inplace=True)
    data.dropna(inplace=True)
    data = data.reset_index(drop=True)
    return data



data_load_state = st.text('Loading data...')
data = load_data()
data_load_state.text("")


st.markdown("<h1 style='text-align: center; color: white;'>Dashbord GetAround</h1>", unsafe_allow_html=True)




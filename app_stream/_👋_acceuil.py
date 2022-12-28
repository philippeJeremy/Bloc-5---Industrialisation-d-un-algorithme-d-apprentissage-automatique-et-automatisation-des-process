import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px 
import plotly.graph_objects as go

from PIL import Image



DATA = "get_around_delay_analysis.xlsx"

st.set_page_config(
    page_title="GetAround",
    page_icon="🚗",
    layout="wide"
)

image = Image.open("istockphoto-1448987777-1024x1024.jpg")

st.markdown("<h1 style='text-align: center; color: white;'>Bienvenue sur la page d'acceuil du rapport GetAround</h1>", unsafe_allow_html=True)
st.markdown("")
st.markdown("")

col1, col2, col3 = st.columns([2,6,2])

with col1:
    st.write("")
with col2:
    st.image(image)
with col3:
    st.write("")



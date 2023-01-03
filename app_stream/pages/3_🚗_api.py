import requests

import numpy as np
import pandas as pd
import streamlit as st

DATA = "./get_around_pricing_project.csv"

@st.cache
def load_data():
    data = pd.read_csv(DATA)
    return data

data_load_state = st.text('Loading data...')
data = load_data()
data_load_state.text("")

def requette(donnees):
    response = requests.post("https://api-getaround.herokuapp.com/predict", json=donnees)
    return response.json()
       
with st.form("my_form"):
    model_key = st.selectbox("Model de voitures", data["model_key"].sort_values().unique())
    mileage = st.number_input("Kilometrage",min_value=0, value=0)
    engine_power = st.number_input("Puissance",min_value=0, value=0)
    fuel = st.selectbox("Fuel", data["fuel"].sort_values().unique())
    paint_color = st.selectbox("Couleur", data["paint_color"].sort_values().unique())
    car_type = st.selectbox("Type de vehicule", data["car_type"].sort_values().unique())
    private_parking_available = st.selectbox("Parcking privée", data["private_parking_available"].sort_values().unique())
    has_gps = st.selectbox("Gps", data["has_gps"].sort_values().unique())
    has_air_conditioning = st.selectbox("Climatisation", data["has_air_conditioning"].sort_values().unique())
    automatic_car = st.selectbox("Vehicule automatic", data["automatic_car"].sort_values().unique())
    has_getaround_connect = st.selectbox("GetAround connect", data["has_getaround_connect"].sort_values().unique())
    has_speed_regulator = st.selectbox("Regulateur de vitesse", data["has_speed_regulator"].sort_values().unique())
    winter_tires = st.selectbox("Pneux neige", data["winter_tires"].sort_values().unique())

    submit = st.form_submit_button(label="submit")

    json ={ 
        'model_key': model_key, 
        'mileage': mileage, 
        'engine_power': engine_power, 
        'fuel': fuel, 
        'paint_color': paint_color,
        'car_type': car_type, 
        'private_parking_available': bool(private_parking_available), 
        'has_gps': bool(has_gps),
        'has_air_conditioning': bool(has_air_conditioning), 
        'automatic_car': bool(automatic_car), 
        'has_getaround_connect': bool(has_getaround_connect),
        'has_speed_regulator': bool(has_speed_regulator),
        'winter_tires': bool(winter_tires)
        }
    
    if submit:
        prix = requette(json)
        st.markdown(f"le prix conseiller a la journee est de : {prix}" )




  
    



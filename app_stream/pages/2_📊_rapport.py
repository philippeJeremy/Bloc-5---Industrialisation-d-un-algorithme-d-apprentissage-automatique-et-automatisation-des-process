import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px 
import plotly.graph_objects as go

DATA = "get_around_delay_analysis.xlsx"

@st.cache
def load_data():
    data = pd.read_excel(DATA)
    return data

data_load_state = st.text('Loading data...')
data = load_data()
data_load_state.text("")

# New dataFrame including only delays
data_retard = data[~data["delay_at_checkout_in_minutes"].isnull()]

data_mobile = data_retard[data_retard["checkin_type"] == "mobile"]
retour_mobil = data_mobile["delay_at_checkout_in_minutes"].mean()

data_connect = data_retard[data_retard["checkin_type"] == "connect"]
retour_connect = data_connect["delay_at_checkout_in_minutes"].mean()

# Real delay does not take into account negative values ​​since they are returned in advance.
histo_checkout_reel = data[(data["delay_at_checkout_in_minutes"] > 0) & (data["delay_at_checkout_in_minutes"] < 1440)]

retard_mobil = histo_checkout_reel[histo_checkout_reel["checkin_type"] == "mobile"]
retard_mobil = retard_mobil["delay_at_checkout_in_minutes"].mean()

retard_connect = histo_checkout_reel[histo_checkout_reel["checkin_type"] == "connect"]
retard_connect = retard_connect["delay_at_checkout_in_minutes"].mean()

st.markdown("<h1 style='text-align: center; color: white;'>Data analysis report</h1>", unsafe_allow_html=True)


st.write(f"The average return time for the mobile version is {round(retour_mobil)} minutes from the indicated return time.")

st.write(f"The average return time for the connect version is {round(retour_connect)} minutes from the time indicated for return.")

st.write("To get a real idea of ​​​​the delays, you have to remove the returns in advance to see the real impact of the delays.")

st.write(f"The average time of a delay for the mobile version is {round(retard_mobil)} minutes compared to the time indicated back.")

st.write(f"The average time of a delay for the connect version is {round(retard_connect)} minutes from the time indicated back.")

st.write("If we apply an average delay on mobile, they will lose 44% of revenue.")

st.write("If we apply an average delay on the connects, they will lose 31% of the revenue.")
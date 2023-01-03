import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px 
import plotly.graph_objects as go

from plotly.subplots import make_subplots



DATA = "get_around_delay_analysis.xlsx"

@st.cache
def load_data():
    data = pd.read_excel(DATA)
    return data



data_load_state = st.text('Loading data...')
data = load_data()
data_load_state.text("")

# ratio en % des type de location
ratio_checking_type = data["checkin_type"].value_counts(normalize=True).round(3)

ratio_state = data["state"].value_counts(normalize=True).round(3)

# ratio d'annulation selon type de location
mobile = data[data["checkin_type"] == "mobile"]
mobile_ratio_state = mobile["state"].value_counts(normalize=True).round(3)

connect = data[data["checkin_type"] == "connect"]
connect_ratio_state = connect["state"].value_counts(normalize=True).round(3)

# new dataFrame incluant que les retards
data_retard = data[~data["delay_at_checkout_in_minutes"].isnull()]

data_mobile = data_retard[data_retard["checkin_type"] == "mobile"]
retour_mobil = data_mobile["delay_at_checkout_in_minutes"].mean()

data_connect = data_retard[data_retard["checkin_type"] == "connect"]
retour_connect = data_connect["delay_at_checkout_in_minutes"].mean()

# histogramme sur 24h
histo_checkout = data[(data["delay_at_checkout_in_minutes"] > -1440) & (data["delay_at_checkout_in_minutes"] < 1440)]
histo_delta = data[(data["time_delta_with_previous_rental_in_minutes"] > -1440) & (data["time_delta_with_previous_rental_in_minutes"] < 1440)]

# reel retard ne prend pas en compte les valeur negatif vue qu'il sont rendue en avance
histo_checkout_reel = data[(data["delay_at_checkout_in_minutes"] > 0) & (data["delay_at_checkout_in_minutes"] < 1440)]

retard_mobil = histo_checkout_reel[histo_checkout_reel["checkin_type"] == "mobile"]
retard_mobil = retard_mobil["delay_at_checkout_in_minutes"].mean()

retard_connect = histo_checkout_reel[histo_checkout_reel["checkin_type"] == "connect"]
retard_connect = retard_connect["delay_at_checkout_in_minutes"].mean()

# ratio en % des types d annulation
ratio_checking_type_retard = histo_checkout_reel["checkin_type"].value_counts(normalize=True).round(3)

# evaluation des perte si application delay
perte_global = data[~data["time_delta_with_previous_rental_in_minutes"].isnull()]
perte_global = perte_global[~perte_global["delay_at_checkout_in_minutes"].isnull()]
perte_global["eval"] = perte_global['time_delta_with_previous_rental_in_minutes'].apply(lambda x: 'perdu' if x <= 129 else 'pas perdu')
perte_global = perte_global["eval"].value_counts(normalize=True)

perte_mobile = data[~data["time_delta_with_previous_rental_in_minutes"].isnull()]
perte_mobile = perte_mobile[~perte_mobile["delay_at_checkout_in_minutes"].isnull()]
perte_mobile["eval"] = perte_mobile['time_delta_with_previous_rental_in_minutes'].apply(lambda x: 'perdu' if x <= 129 else 'pas perdu')
perte_mobile = perte_mobile["eval"].value_counts(normalize=True)

perte_connect = data[~data["time_delta_with_previous_rental_in_minutes"].isnull()]
perte_connect = perte_connect[~perte_connect["delay_at_checkout_in_minutes"].isnull()]
perte_connect["eval"] = perte_connect['time_delta_with_previous_rental_in_minutes'].apply(lambda x: 'perdu' if x <= 77 else 'pas perdu')
perte_connect = perte_connect["eval"].value_counts(normalize=True)

st.markdown("""<h1 style='text-align: center; color: white; -webkit-box-shadow: 7px -5px 10px 0px #4B0082, 11px -9px 10px 0px #0000FF, 16px -14px 10px 0px #00FF00, 20px -17px 10px 0px #FFFF00, 
            24px -19px 10px 0px #FF7F00, 27px -23px 10px 0px #FF0000, 5px 5px 15px 5px rgba(0,0,0,0), 5px 5px 15px 5px rgba(0,0,0,0); 
            box-shadow: 7px -5px 10px 0px #4B0082, 11px -9px 10px 0px #0000FF, 16px -14px 10px 0px #00FF00, 20px -17px 10px 0px #FFFF00, 24px -19px 10px 0px #FF7F00, 27px -23px 10px 0px #FF0000, 
            5px 5px 15px 5px rgba(0,0,0,0), 5px 5px 15px 5px rgba(0,0,0,0);background: #9400D3;}'>Dashbord GetAround</h1>""", unsafe_allow_html=True)
st.markdown("###")

st.markdown("<h3 style='text-align: center; color: white;'>proportion des type de location et % </h3>", unsafe_allow_html=True)

pie_1 = go.Figure()
pie_1.add_trace(go.Pie(values=ratio_checking_type,
                        labels=['Mobile', 'Connect '],
                        marker_colors = ['#202EBD','#13E7E3'],))

pie_1.update_layout(
                width=1200,
                legend=dict(
                font=dict(
                    size=16
                )))

st.plotly_chart(pie_1)

st.markdown("---")

st.markdown("<h3 style='text-align: center; color: white;'>proportion des annulation de location</h3>", unsafe_allow_html=True)

pie_2 = go.Figure()
pie_2.add_trace(go.Pie(values=ratio_state,
                        labels=['Non annulée', 'Annulée'],
                        marker_colors = ['#202EBD','#13E7E3'],))

pie_2.update_layout(
                width=1200,
                legend=dict(
                font=dict(
                    size=16
                )))

st.plotly_chart(pie_2)

st.markdown("---")

st.markdown("<h3 style='text-align: center; color: white;'>proportion des annulation par type de location</h3>", unsafe_allow_html=True)
pie_3 = make_subplots(rows=1, cols=2, specs=[[{"type": "pie"},{"type": "pie"}]],shared_yaxes = True,
                       subplot_titles=["Global", "Mobile", "Connect"])


pie_3.add_trace(go.Pie( values=mobile_ratio_state,
                        labels=['Non annulée', 'Annulée'],
                        marker_colors = ['#20BD2E','#FF3333'],),
                        row=1, col=1)

pie_3.add_trace(go.Pie(values=connect_ratio_state,
                        labels=['Non annulée', 'Annulée'],
                        marker_colors = ['#20BD2E','#FF3333'],),
                        row=1, col=2)

pie_3.update_layout(
                width=1200,
                legend=dict(
                font=dict(
                size=16
            )))

st.plotly_chart(pie_3)

st.markdown("---")

st.write(f"Le delay moyen d'un retour pour la version mobil est de {round(retour_mobil)} minutes par rapport a l'heure indiquer de retour")

st.write(f"Le delay moyen d'un retour pour la version connect est de {round(retour_connect)} minutes par rapport a l'heure indiquer de retour")

st.markdown("---")

st.markdown("<h3 style='text-align: center; color: white;'>histogramme sur 24 heures du temps entre les reservations</h3>", unsafe_allow_html=True)
fig = px.histogram(histo_delta, x="time_delta_with_previous_rental_in_minutes",                   
                    color = 'checkin_type',
                    barmode ='group',
                    width= 1200,
                    height = 500
                    ) 
fig.update_layout(
                legend=dict(
                    font=dict(
                size=16
                ))) 
                            
st.plotly_chart(fig)

st.markdown("---")

st.markdown("<h3 style='text-align: center; color: white;'>histogramme sur 24 heures des delais de retour</h3>", unsafe_allow_html=True)
fig = px.histogram(histo_checkout, x="delay_at_checkout_in_minutes",
                    color = 'checkin_type',
                    barmode ='group',
                    width= 1200,
                    height = 500
                    ) 
fig.update_layout(
                legend=dict(
                    font=dict(
                size=16
                ))) 
      
st.plotly_chart(fig)

st.markdown("---")

st.write("Pour se faire une veritable idée sur les retard il faut enlever les retour en avance pur voir le réel impact des retard")

st.write(f"Le delay moyen d'un retard pour la version mobil est de {round(retard_mobil)} minutes par rapport a l'heure indiquer de retour")

st.write(f"Le delay moyen d'un retard pour la version connect est de {round(retard_connect)} minutes par rapport a l'heure indiquer de retour")


st.markdown("<h3 style='text-align: center; color: white;'>histogramme sur 24 heures des retards</h3>", unsafe_allow_html=True)
fig = px.histogram(histo_checkout_reel, x="delay_at_checkout_in_minutes",
                    color = 'checkin_type',
                    barmode ='group',
                    width= 1200,
                    height = 500
                    ) 
fig.update_layout(
                legend=dict(
                    font=dict(
                size=16
                ))) 
      
st.plotly_chart(fig)

st.markdown("---")

st.markdown("<h3 style='text-align: center; color: white;'>proportion des annulation par type de location en tenan compte que des retards</h3>", unsafe_allow_html=True)
pie_4 = go.Figure()
pie_4.add_trace(go.Pie(values=perte_global,
                        labels=['location conserver', 'location perdu'],
                        marker_colors = ['#202EBD','#13E7E3'],))

pie_4.update_layout(
                width=1200,
                legend=dict(
                font=dict(
                    size=16
                )))

st.plotly_chart(pie_4)


st.write("si nous appliquon un delay 44% des revenue serai impacter")

st.markdown("---")

st.markdown("<h3 style='text-align: center; color: white;'>proportion des annulation par type de location</h3>", unsafe_allow_html=True)
pie_5 = make_subplots(rows=1, cols=2, specs=[[{"type": "pie"},{"type": "pie"}]],shared_yaxes = True,
                       subplot_titles=["Mobile", "Connect"])


pie_5.add_trace(go.Pie( values=perte_mobile,
                        labels=['location conserver', 'location perdu'],
                        marker_colors = ['#20BD2E','#FF3333'],),
                        row=1, col=1)

pie_5.add_trace(go.Pie(values=perte_connect,
                        labels=['location conserver', 'location perdu'],
                        marker_colors = ['#20BD2E','#FF3333'],),
                        row=1, col=2)

pie_5.update_layout(
                width=1200,
                legend=dict(
                 font=dict(
                    size=16
                )))

st.plotly_chart(pie_5)

st.write("si nous appliquons un delay moyen sur les mobile, ils perderont 44% des revenue")

st.write("si nous appliquons un delay moyen sur les connect, ils perderont 31% des revenue")

st.markdown("---")

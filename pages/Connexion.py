import streamlit as st
import datetime
from database import Database

db = Database()

st.set_page_config(
    layout="wide",
)

a, b = st.columns([1, 4])


if len(st.experimental_get_query_params()) > 0: 
    if st.button('Se déconnecter'):
        st.experimental_set_query_params()
else:
    a.title("Connexion")
    with st.form("formulaire_connexion"):
        today = datetime.date.today()
        nom = st.text_input('Nom')
        submitted = st.form_submit_button("Submit")
        if submitted:
            db.login(nom)

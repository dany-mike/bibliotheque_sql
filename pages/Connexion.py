import streamlit as st
import datetime
from database import Database

db = Database()

st.set_page_config(
    layout="wide",
)

a, b = st.columns([1, 4])

a.title("Connexion")

with st.form("formulaire_connexion"):
    today = datetime.date.today()

    nom = st.text_input('Nom')

    submitted = st.form_submit_button("Submit")
    if submitted:
        db.login(nom)

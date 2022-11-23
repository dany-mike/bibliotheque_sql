import streamlit as st
import datetime
from database import Database

db = Database()

st.set_page_config(
    layout="wide",
)

a, b = st.columns([1, 4])

a.title("Création d'un compte membre")

with st.form("formulaire_compte"):
    today = datetime.date.today()

    nom = st.text_input('Nom')

    d = st.date_input(
        "Date de naissance",
        datetime.date(int(str(today).split('-')[0]), int(str(today).split('-')[1]), int(str(today).split('-')[2])))

    submitted = st.form_submit_button("Submit")
    if submitted:
        date_tuple = (int(str(d).split('-')[0]), int(str(d).split('-')[1]), int(str(d).split('-')[2]))
        db.creer_compte_membre(nom, date_tuple)

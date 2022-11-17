import streamlit as st

from database import Database

db = Database()

db.test()
st.set_page_config(
    layout="wide",
)

a, b = st.columns([1, 4])

a.title("Accueil bibliotheque")

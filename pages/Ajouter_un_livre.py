import streamlit as st

from database import Database

db = Database()

st.set_page_config(
    layout="wide",
)

a, b = st.columns([1, 4])

a.title("Accueil bibliotheque")

if len(st.experimental_get_query_params()) > 0: 
    personne_id = int(st.experimental_get_query_params()["personne_id"][0])
    db.renderAddBookPage(personne_id)
else :
    st.text('Vous devez être connecté pour ajouter un livre')
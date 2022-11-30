import streamlit as st
from personne import Personne
from database import Database

st.set_page_config(
    layout="wide",
)

a, b = st.columns([1, 4])

a.title("Supprimer compte")
if len(st.experimental_get_query_params()) > 0: 
    if st.button('Supprimer compte'):
        personne_id = int(st.experimental_get_query_params()["personne_id"][0])
        db = Database()
        p = Personne(personne_id, db)
        p.deleteAccount(personne_id)
        st.experimental_set_query_params()
else:
    st.text("Vous devez être connecté pour supprimer votre compte")
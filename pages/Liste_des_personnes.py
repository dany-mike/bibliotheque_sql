import streamlit as st

from database import Database
from personne import Personne

db = Database()

st.set_page_config(
    layout="wide",
)

a, b = st.columns([1, 4])

a.title("Liste des personnes")

if len(st.experimental_get_query_params()) > 0:
    personne_id = int(st.experimental_get_query_params()["personne_id"][0])
    p = Personne(personne_id, db)
    personne = p.getCurrentUser()
    if personne[5] == 'admin':
        p.renderMembersList()
        p.renderAdminsList()
    else:
        st.text(
            "Vous devez être connecté en tant qu'admin pour voir la liste des personnes")
else:
    st.text('Vous devez être connecté pour voir la liste des personnes')

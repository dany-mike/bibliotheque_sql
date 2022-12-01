import streamlit as st

from database import Database
from book import Book

db = Database()

st.set_page_config(
    layout="wide",
)

a, b = st.columns([1, 4])

a.title("Liste des likes")

book = Book(db)

if len(st.experimental_get_query_params()) > 0: 
    personne_id = int(st.experimental_get_query_params()["personne_id"][0])
    if len(book.getLikedBooks(personne_id)) > 0:
        book.renderLikedBooks(personne_id)
    else:
        st.text("Vous n'avez liké aucun livre")
else:
    st.text("Vous n'êtes pas connecté")

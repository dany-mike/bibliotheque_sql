import streamlit as st

from database import Database
from book import Book

db = Database()

st.set_page_config(
    layout="wide",
)

a, b = st.columns([1, 4])

a.title("Emprunter un livre")

if len(st.experimental_get_query_params()) > 0: 
    personne_id = int(st.experimental_get_query_params()["personne_id"][0])
    book = Book(db)
    book.renderBorrowBookForm(personne_id, book.getAvailableBooks())
else :
    st.text('Vous devez être connecté pour ajouter un livre')
import streamlit as st

from database import Database
from book import Book

db = Database()

st.set_page_config(
    layout="wide",
)

a, b = st.columns([1, 4])

a.title("Rendre un livre")
if len(st.experimental_get_query_params()) > 0:
    book = Book(db)
    personne_id = int(st.experimental_get_query_params()["personne_id"][0])
    unreturnedBooks = book.getUnreturnedBooks(personne_id)
    if len(st.experimental_get_query_params()) > 0:
        if len(unreturnedBooks) > 0:
            personne_id = int(st.experimental_get_query_params()["personne_id"][0])
            book.renderReturnBookForm(personne_id, unreturnedBooks)
        else:
            st.subheader("(Vous n'avez aucun livre à rendre)")
else:
    st.text('Vous devez être connecté pour rendre un livre')

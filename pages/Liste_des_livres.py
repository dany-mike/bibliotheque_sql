import streamlit as st

from database import Database
from book import Book

db = Database()

st.set_page_config(
    layout="wide",
)

a, b = st.columns([1, 4])

a.title("Liste des livres")

book = Book(db)
if len(book.getUnavailableBooks()) > 0 or len(book.getAvailableBooks()) > 0:
        bookName = book.renderSearchBar()
        if bookName:
            book.renderBooksByName(bookName)
            if st.button('Annuler la recherche'):
                bookName = ''
        else:
            book.renderAvailableBooks()
            book.renderUnavailableBooks()
else:
    st.text("Il n'y a pas de livres dans la librairie")

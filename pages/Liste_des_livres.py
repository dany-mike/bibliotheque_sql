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
books = book.getBooks()
print(books)
if len(books) > 0:
    book.renderBooks(books)
else :
    st.text("Il n'y a pas de livres dans la librairie")
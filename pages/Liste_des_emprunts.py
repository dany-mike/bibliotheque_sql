import streamlit as st
import pandas as pd

from database import Database
from book import Book

db = Database()

st.set_page_config(
    layout="wide",
)

a, b = st.columns([1, 4])

a.title("Liste des emprunts")

if len(st.experimental_get_query_params()) > 0:
    print('Liste des emprunts')
    book = Book(db)
    unreturnedBooks = book.getUnreturnedBooks()
    print(len(unreturnedBooks))
    st.subheader('Liste des livres non rendus')
    if len(unreturnedBooks) > 0:
        st.write(pd.DataFrame(book.formatBorrows(unreturnedBooks)))
    else:
        st.text("(Vous n'avez aucun livre en cours d'emprunt)")

    returnedBooks = book.getReturnedBooks()
    st.subheader('Liste des livres rendus')

    if len(returnedBooks) > 0:
        st.write(pd.DataFrame(book.formatBorrows(returnedBooks)))
    else:
        st.text("(Vous n'avez rendu aucun livre)")
else:
    st.text('Vous devez être connecté pour voir la liste des emprunts')

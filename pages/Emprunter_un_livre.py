import streamlit as st

from database import Database
from book import Book
from personne import Personne

db = Database()

st.set_page_config(
    layout="wide",
)

a, b = st.columns([1, 4])

a.title("Emprunter un livre")

if len(st.experimental_get_query_params()) > 0: 
    personne_id = int(st.experimental_get_query_params()["personne_id"][0])
    book = Book(db)
    unreturnedBooks = book.getUnreturnedBooks()
    p = Personne(personne_id, db)
    if p.isBlacklisted(unreturnedBooks):
        p.blacklistUser()
    
    personne = p.getCurrentUser()

    blacklisted_field = personne[4]

    if blacklisted_field:
        st.text('You are blacklisted you are not allowed to borrow a book')
    else:
        book.renderBorrowBookForm(personne_id, book.getAvailableBooks())
else :
    st.text('Vous devez être connecté pour ajouter un livre')
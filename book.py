import streamlit as st
import datetime
from personne import Personne
import psycopg2
import pandas as pd


class Book:
    def __init__(self, db):
        self.db = db

    def getUnavailableBooks(self):
        self.db.cur.execute(
            "SELECT * FROM livre WHERE quantite <= 0;")
        return self.db.cur.fetchall()

    def getAvailableBooks(self):
        self.db.cur.execute(
            "SELECT * FROM livre WHERE quantite > 0;")
        return self.db.cur.fetchall()

    def formatBooks(self, items):
        formattedList = []
        for item in items:
            formattedList.append({
                'ISBN': item[0],
                'Titre': item[1],
                'Quantite': item[2],
                'Auteur': item[3],
                'Date de publication': item[4],
            })
        return formattedList

    def renderAvailableBooks(self):
        availableBooks = self.getAvailableBooks()
        if len(availableBooks) > 0:
            st.subheader("Liste des livres disponibles")
            st.write(pd.DataFrame(self.formatBooks(availableBooks)))
        else:
            st.subheader("Il n'y a plus de livres disponibles")

    def renderUnavailableBooks(self):
        unavailableBooks = self.getUnavailableBooks()
        if len(unavailableBooks) > 0:
            st.subheader('Liste des livres non disponibles')
            st.write(pd.DataFrame(self.formatBooks(unavailableBooks)))

    def renderAddBookForm(self, personne_id):
        p = Personne(personne_id, self.db)
        role = p.getUserRole()
        if role == 'admin':
            with st.form("formulaire_ajout_livre"):
                today = datetime.date.today()
                isbn = st.text_input('ISBN')
                title = st.text_input('Titre')
                date_publication = st.date_input("Date de publication", datetime.date(int(str(
                    today).split('-')[0]), int(str(today).split('-')[1]), int(str(today).split('-')[2])))
                quantity = st.number_input('Quantité', min_value=0, step=1)
                auteur = st.text_input('Auteur')
                option = st.selectbox('Catégorie', ('Fantastique', 'Policier', 'Biographie',
                                      'Roman comtemporain', 'Philosophie', 'Roman historique'))
                submitted = st.form_submit_button("Submit")
                if submitted:
                    self.addBook(isbn, title, date_publication,
                                 quantity, auteur, option)
        else:
            st.text('Seul les admins peuvent ajouter un livre')

    def renderBorrowBookForm(self, personne_id, books):
        today = datetime.date.today()
        option = st.selectbox('Liste des livres', ({
            'ISBN': "1",
        }, {
            'ISBN': "2",
        }))
        submitted = st.form_submit_button("Submit")
        if submitted:
            print('borrow book')
            # self.addBook(isbn, title, date_publication,
            #              quantity, auteur, option)

    def addBook(self, isbn, title, date_publication, quantity, auteur, categorie_name):
        try:
            self.db.cur.execute("INSERT INTO livre (isbn, titre, quantite, auteur, date_publication) VALUES (%s, %s, %s, %s, %s)",
                                (isbn, title, quantity, auteur, date_publication))
            self.createCategory(categorie_name, isbn)
            self.db.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            self.db.conn.rollback()

    def createCategory(self, categorie_name, livre_isbn):
        self.db.cur.execute("INSERT INTO categorie (categorie_name, livre_isbn) VALUES (%s, %s)",
                            (categorie_name, livre_isbn))

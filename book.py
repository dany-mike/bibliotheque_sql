import streamlit as st
import datetime
from personne import Personne
import psycopg2

class Book:
    def __init__(self, db):
        self.db = db

    def getBooks(self):
        self.db.cur.execute(
            "SELECT * FROM livre;")
        return self.db.cur.fetchall()
    
    def renderAddBookForm(self, personne_id):
        p = Personne(personne_id, self.db)
        role = p.getUserRole()
        if role == 'admin':
            with st.form("formulaire_ajout_livre"):
                today = datetime.date.today()
                isbn = st.text_input('ISBN')
                title = st.text_input('Titre')
                date_publication = st.date_input("Date de publication", datetime.date(int(str(today).split('-')[0]), int(str(today).split('-')[1]), int(str(today).split('-')[2])))
                quantity = st.number_input('Quantité', min_value=1, step=1)
                auteur = st.text_input('Auteur')
                option = st.selectbox('Catégorie', ('Fantastique', 'Policier', 'Biographie', 'Roman comtemporain', 'Philosophie', 'Roman historique'))
                submitted = st.form_submit_button("Submit")
                if submitted:
                    self.addBook(isbn, title, date_publication, quantity, auteur, option)
        else:
            st.text('Seul les admins peuvent ajouter un livre')
    
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
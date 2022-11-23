#!/usr/bin/python
import psycopg2
from config import config
from utils import get_date
import streamlit as st
import pandas as pd
from personne import Personne
import datetime

class Database:
    def __init__(self):
        self.conn = self.connect()
        self.cur = self.conn.cursor()

    def connect(self):
        """ Connect to the PostgreSQL database server """
        conn = None
        try:
            # read connection parameters
            params = config()

            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            conn = psycopg2.connect(**params)

            # create a cursor
            cur = conn.cursor()

            # execute a statement
            print('PostgreSQL database version:')
            cur.execute('SELECT version()')

            # display the PostgreSQL database server version
            db_version = cur.fetchone()
            print(db_version)

            # close the communication with the PostgreSQL
            cur.close()
            return conn
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def close_connection(self):
        self.db.close()

    def creer_compte_membre(self, nom: str, date_de_naissance: tuple[int, int, int]):
        try:
            self.register(nom, date_de_naissance, "membre")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            self.conn.rollback()

    def creer_compte_admin(self, nom: str, date_de_naissance: tuple[int, int, int]):
        try:
            self.register(nom, date_de_naissance, "admin")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            self.conn.rollback()

    def register(self, nom, date_de_naissance, role):
        self.cur.execute("INSERT INTO personne (nom, limite, date_naissance, isBlacklisted) VALUES (%s, %s, %s, FALSE)",
                         (nom, 5, get_date(date_de_naissance)
                          ))
        p = Personne(0, self)
        personne_id = p.getPersonneIdByName(nom)

        self.cur.execute("INSERT INTO role (role_name, personne_id) VALUES (%s, %s)",
                         (role, personne_id))
        self.conn.commit()

        st.experimental_set_query_params(
            personne_id=personne_id
        )

    def login(self, nom):
        p = Personne(0, self)
        personne_id = p.getPersonneIdByName(nom)
        st.experimental_set_query_params(
            personne_id=personne_id
        )

    def renderUser(self, personne_id):
        p = Personne(personne_id, self)
        personne = p.getCurrentUser()
        role = p.getUserRole()
        st.text("Information de l'utilisateur")
        st.write(pd.DataFrame({
            'ID': [personne[0]],
            'Nom': [personne[1]],
            'Limite emprunt': [personne[2]],
            'date de naissance': [personne[3]],
            'Blacklisté ?': [personne[4]],
            'Role': [role]
        }))

    def addBook(self, isbn, title, date_publication, quantity, auteur, categorie_name):
        try:
            self.cur.execute("INSERT INTO livre (isbn, titre, quantite, auteur, date_publication) VALUES (%s, %s, %s, %s, %s)",
                         (isbn, title, quantity, auteur, date_publication))
            self.createCategory(categorie_name, isbn)
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            self.conn.rollback()
    
    def createCategory(self, categorie_name, livre_isbn):
        self.cur.execute("INSERT INTO categorie (categorie_name, livre_isbn) VALUES (%s, %s)",
                         (categorie_name, livre_isbn))

    def renderAddBookPage(self, personne_id):
        p = Personne(personne_id, self)
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

if __name__ == '__main__':
    db = Database()
    db.connect()

#!/usr/bin/python
import psycopg2
from config import config
from utils import get_date
import streamlit as st
# from streamlit_extras.switch_page_button import switch_page

# want_to_contribute = st.button("I want to contribute!")
# if want_to_contribute:
#     switch_page("Contribute")


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

    def register(self, nom, date_de_naissance ,role):
        self.cur.execute("INSERT INTO personne (nom, limite, date_naissance, isBlacklisted) VALUES (%s, %s, %s, FALSE)",
                             (nom, 5, get_date(date_de_naissance)
                              ))
        self.cur.execute("SELECT * FROM personne WHERE nom = %s", (nom,))

        personne_id = self.cur.fetchone()[0]

        self.cur.execute("INSERT INTO role (role_name, personne_id) VALUES (%s, %s)",
                            (role, personne_id))
        self.conn.commit()

        st.experimental_set_query_params(
            personne_id=personne_id
        )

    def login(self, nom):
        self.cur.execute("SELECT * FROM personne WHERE nom = %s", (nom,))
        personne_id = self.cur.fetchone()[0]
        st.experimental_set_query_params(
            personne_id=personne_id
        )

if __name__ == '__main__':
    db = Database()
    db.connect()

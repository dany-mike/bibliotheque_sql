#!/usr/bin/python
import psycopg2
from config import config
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

    def test(self):
        print('test')

    def creer_membre(self):
        print('creer membre')
    
    def creer_membre(self, nom: str, date_de_naissance: tuple[int, int, int]):
        try:
            self.cur.execute("INSERT INTO personne (nom, limite, date_naissance, isBlacklisted) VALUES (%s, %s, %s, FALSE)",
                             (nom, 5, datetime(date_de_naissance)))
            
            personne_id = self.cur.fetchone()[0]

            self.cur.execute("INSERT INTO role (role_name, personne_id) VALUES (%s, %s)",
                             ("membre", personne_id))
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            self.conn.rollback()


if __name__ == '__main__':
    db = Database()
    db.connect()

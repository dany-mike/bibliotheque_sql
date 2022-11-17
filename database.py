#!/usr/bin/python
import psycopg2
from config import config


class Database:
    def __init__(self):
        self.conn = self.connect()
        # self.cur = self.conn.cursor()

    def connect(self):
        conn = None
        try:
            params = config()

            print('Connecting to the PostgreSQL database...')
            conn = psycopg2.connect(**params)

            cur = conn.cursor()
            print('PostgreSQL database version:')
            db_version = cur.fetchone()
            print(db_version)
            print(cur.statusmessage)
            cur.close()
            return conn
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')

    def close_connection(self):
        self.db.close()

    def test(self):
        print('test')


if __name__ == '__main__':
    db = Database()
    db.connect()
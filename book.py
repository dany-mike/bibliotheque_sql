import streamlit as st
import datetime
from personne import Personne
import psycopg2
import pandas as pd
from utils import get_next_month_date


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

    def getBookByISBN(self, isbn):
        self.db.cur.execute(
            "SELECT * FROM livre WHERE isbn = %s;", (isbn,))
        return self.db.cur.fetchone()

    def getUnreturnedBooks(self):
        self.db.cur.execute(
            "SELECT * FROM emprunt LEFT JOIN livre ON emprunt.livre_isbn = livre.isbn LEFT JOIN personne ON emprunt.personne_id = personne.id WHERE date_rendu IS NULL;")
        return self.db.cur.fetchall()

    def getReturnedBooks(self):
        self.db.cur.execute(
            "SELECT * FROM emprunt LEFT JOIN livre ON emprunt.livre_isbn = livre.isbn LEFT JOIN personne ON emprunt.personne_id = personne.id WHERE date_rendu IS NOT NULL;")
        return self.db.cur.fetchall()

    def updateBookQty(self, updated_qty, isbn):
        self.db.cur.execute(
            "UPDATE livre SET quantite = %s WHERE isbn = %s;", (updated_qty, isbn))

    def setBookReturnDate(self, date_rendu, emprunt_id):
        self.db.cur.execute(
            "UPDATE emprunt SET date_rendu = %s WHERE id = %s;", (date_rendu, emprunt_id))

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

    def formatBorrows(self, items):
        formattedList = []
        for item in items:
            formattedList.append({
                "ID de l'emprunt": item[0],
                'ISBN du livre': item[1],
                'Titre du livre': item[6],
                'Auteur du livre': item[8],
                "Date de l'emprunt": item[3],
                "Date de rendu maximum": get_next_month_date(item[3])
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
                # option = st.selectbox('Catégorie', ('Fantastique', 'Policier', 'Biographie',
                #                       'Roman comtemporain', 'Philosophie', 'Roman historique'))
                options = st.multiselect(
                    'Catégories du livre',
                    ['Fantastique', 'Policier', 'Biographie',
                     'Roman comtemporain', 'Philosophie', 'Roman historique'],
                    [])

                st.write('You selected:', options)
                submitted = st.form_submit_button("Submit")
                if submitted:
                    self.addBook(isbn, title, date_publication,
                                 quantity, auteur, options)
        else:
            st.text('Seul les admins peuvent ajouter un livre')

    def renderBorrowBookForm(self, personne_id, books):
        with st.form("formulaire_emprunt"):
            today = datetime.date.today()
            availableBooks = self.formatBooks(books)
            bookLabel = st.selectbox('Liste des livres disponibles',
                                     (self.renderBorrowLabel(availableBooks)))
            submitted = st.form_submit_button("Submit")
            if submitted:
                self.borrowBook(bookLabel, personne_id, today)

    def renderReturnBookForm(self, personne_id, books):
        with st.form("formulaire_de_retour"):
            today = datetime.date.today()
            unreturnedBooks = self.formatBorrows(books)
            bookLabel = st.selectbox('Liste des livres non rendus',
                                     (self.renderUnreturnedLabel(unreturnedBooks)))
            submitted = st.form_submit_button("Submit")
            if submitted:
                self.returnBook(bookLabel, personne_id, today)

    def returnBook(self, bookLabel, personne_id, date_rendu):
        try:
            p = Personne(personne_id, self.db)
            personne = p.getCurrentUser()
            emprunt_id = int(self.getLabelId(bookLabel))
            isbn = bookLabel.split()[6]
            updated_limite = personne[2] + 1
            updated_book_qty = self.getBookByISBN(isbn)[2] + 1
            self.setBookReturnDate(date_rendu, emprunt_id)
            p.updateUserLimite(updated_limite, personne_id)
            self.updateBookQty(updated_book_qty, isbn)
            p.unblacklistUser()
            self.db.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            self.db.conn.rollback()

    def borrowBook(self, bookLabel, personne_id, date_emprunt):
        try:
            p = Personne(personne_id, self.db)
            personne = p.getCurrentUser()
            isbn = self.getLabelId(bookLabel)
            self.db.cur.execute("INSERT INTO emprunt (livre_isbn, personne_id, date_emprunt) VALUES (%s, %s, %s)",
                                (isbn, personne_id, date_emprunt))
            updated_limite = personne[2] - 1
            updated_book_qty = self.getBookByISBN(isbn)[2] - 1
            p.updateUserLimite(updated_limite, personne_id)
            self.updateBookQty(updated_book_qty, isbn)
            self.db.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            self.db.conn.rollback()

    def getLabelId(self, bookLabel):
        return bookLabel.split()[-1]

    def renderBorrowLabel(self, books):
        borrowLabel = []
        for book in books:
            borrowLabel.append(
                "Titre: " + book["Titre"] + " ISBN: " + book["ISBN"])
        return borrowLabel

    def renderUnreturnedLabel(self, books):
        unreturnedLabel = []
        for book in books:
            unreturnedLabel.append(
                "Titre: " + book["Titre du livre"] + " ISBN: " + book["ISBN du livre"] + " ID de l'emprunt: " + str(book["ID de l'emprunt"]))
        return unreturnedLabel

    def addBook(self, isbn, title, date_publication, quantity, auteur, categories):
        try:
            self.db.cur.execute("INSERT INTO livre (isbn, titre, quantite, auteur, date_publication) VALUES (%s, %s, %s, %s, %s)",
                                (isbn, title, quantity, auteur, date_publication))
            for category in categories:
                self.createCategory(category, isbn)
            self.db.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            self.db.conn.rollback()

    def createCategory(self, categorie_name, livre_isbn):
        self.db.cur.execute("INSERT INTO categorie (categorie_name, livre_isbn) VALUES (%s, %s)",
                            (categorie_name, livre_isbn))

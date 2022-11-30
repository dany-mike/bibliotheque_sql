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
            "SELECT * FROM livre LEFT JOIN categorie ON categorie.livre_isbn = livre.isbn WHERE quantite <= 0;")
        return self.db.cur.fetchall()

    def getAvailableBooks(self):
        self.db.cur.execute(
            "SELECT * FROM livre LEFT JOIN categorie ON categorie.livre_isbn = livre.isbn WHERE quantite > 0;")
        return self.db.cur.fetchall()

    def getBookByISBN(self, isbn):
        self.db.cur.execute(
            "SELECT * FROM livre LEFT JOIN categorie ON categorie.livre_isbn = livre.isbn WHERE isbn = %s;", (isbn,))
        return self.db.cur.fetchone()

    def getBooksByAuthor(self, author):
        self.db.cur.execute(
            "SELECT * FROM livre LEFT JOIN categorie ON categorie.livre_isbn = livre.isbn WHERE auteur = %s;", (author,))
        return self.db.cur.fetchall()

    def getBooksByName(self, bookName):
        self.db.cur.execute(
            "SELECT * FROM livre LEFT JOIN categorie ON categorie.livre_isbn = livre.isbn WHERE titre = %s;", (bookName,))
        return self.db.cur.fetchall()

    def getBooksByDate(self, date):
        self.db.cur.execute(
            "SELECT * FROM livre LEFT JOIN categorie ON categorie.livre_isbn = livre.isbn  WHERE date_publication = %s;", (date,))
        return self.db.cur.fetchall()

    def getBooksByCategory(self, categorieName):
        self.db.cur.execute(
            "SELECT * FROM livre LEFT JOIN categorie ON categorie.livre_isbn = livre.isbn WHERE categorie_name = %s;", (categorieName,))
        return self.db.cur.fetchall()

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
                'Catégorie': item[5]
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

    def renderBooks(self, bookName):
        books = self.getBooksByName(bookName)
        if len(books) > 0:
            st.subheader("Livres avec le nom %s", bookName)
            st.write(pd.DataFrame(self.formatBooks(books)))

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

    def renderSearchBarName(self):
        bookName = st.text_input('Chercher un livre par nom: ', '')
        if st.button('Chercher par titre'):
            return bookName

    def renderSearchBarAuthor(self):
        authorName = st.text_input('Chercher un livre par auteur: ', '')
        if st.button('Chercher par auteur'):
            return authorName

    def renderSearchBarCategory(self):
        categorieName = st.text_input('Chercher un livre par catégorie: ', '')
        if st.button('Chercher par catégorie'):
            return categorieName

    def renderCalendarInput(self):
        date = st.date_input(
            "Chercher un livre par date",
            datetime.date(2012, 11, 23))
        if st.button('Chercher par date'):
            return date

    def renderBooksByAuthor(self, author):
        books = self.getBooksByAuthor(author)
        if len(books) > 0:
            st.subheader('Liste des livres qui ont pour auteur ' + author)
            st.write(pd.DataFrame(self.formatBooks(books)))
        else:
            st.write("Il n'y a aucun livre qui a l'auteur " + author)

    def renderBooksByName(self, bookName):
        books = self.getBooksByName(bookName)
        if len(books) > 0:
            st.subheader('Liste des livres avec le nom ' + bookName)
            st.write(pd.DataFrame(self.formatBooks(books)))
        else:
            st.write("Il n'y a aucun livre avec le titre " + bookName)

    def renderBooksByDate(self, date):
        books = self.getBooksByDate(date)
        if len(books) > 0:
            st.subheader('Liste des livres avec la date ' + str(date))
            st.write(pd.DataFrame(self.formatBooks(books)))
        else:
            st.write("Il n'y a aucun livre avec la date " + str(date))

    # def renderBooksByYear(self, bookYear):
    #     books = self.getBooksByBookYear(bookYear)
    #     if len(books) > 0:
    #         st.subheader("Liste des livres avec l'année " + bookYear)
    #         st.write(pd.DataFrame(self.formatBooks(books)))
    #     else:
    #         st.write("Il n'y a aucun qui a été publié en " + bookYear)

    def renderBooksByCategory(self, category):
        categories = self.getBooksByCategory(category)
        if len(categories) > 0:
            st.subheader("Liste des livres avec l'année " + category)
            st.write(pd.DataFrame(self.formatBooks(categories)))
        else:
            st.write("Il n'y a pas de livre avec la catégorie " + category)

    def renderAddBookForm(self, personne_id):
        p = Personne(personne_id, self.db)
        personne = p.getCurrentUser()
        if personne[5] == 'admin':
            booksToAdd = st.number_input(
                'Number of books to add', min_value=1, step=1)
            if booksToAdd > 0:
                with st.form("formulaire_ajout_livres"):
                    today = datetime.date.today()
                    isbnList = []
                    titleList = []
                    dateList = []
                    quantityList = []
                    auteurList = []
                    optionsList = []
                    for item in range(booksToAdd):
                        bookNumber = item + 1
                        st.text('Book ' + str(bookNumber))
                        isbn = st.text_input('ISBN ' + str(bookNumber))
                        isbnList.append(isbn)
                        title = st.text_input('Titre ' + str(bookNumber))
                        titleList.append(title)
                        date_publication = st.date_input("Date de publication " + str(bookNumber), datetime.date(int(str(
                            today).split('-')[0]), int(str(today).split('-')[1]), int(str(today).split('-')[2])))
                        dateList.append(date_publication)
                        quantity = st.number_input(
                            'Quantité ' + str(bookNumber), min_value=0, step=1)
                        quantityList.append(quantity)
                        auteur = st.text_input('Auteur ' + str(bookNumber))
                        auteurList.append(auteur)
                        categoryValues = st.multiselect(
                            'Catégories du livre ' + str(bookNumber),
                            ['Fantastique', 'Policier', 'Biographie',
                             'Roman comtemporain', 'Philosophie', 'Roman historique'],
                            [])
                        optionsList.append(categoryValues)
                    submitted = st.form_submit_button("Submit")

                    if submitted:
                        bookValues = self.getValuesToInsert(
                            isbnList, titleList, dateList, quantityList, auteurList, booksToAdd)
                        categoryValues = self.getCategoriesToInsert(
                            isbnList, optionsList, booksToAdd)
                        self.addBooks(bookValues, categoryValues, booksToAdd)
        else:
            st.text('Seul les admins peuvent ajouter un livre')

    def getCategoriesToInsert(self, isbnList, optionsList, booksToAdd):
        fields = []
        for i in range(booksToAdd):
            fields.append([])
            fields[i].append(optionsList[i])
            fields[i].append(isbnList[i])
        categories = []
        for element in fields:
            categories.append(self.getValuesCategory(element[0], element[1]))

        result = "VALUES"

        for item in categories:
            for element in item:
                result += str(element) + ','
        l = len(result)
        return result[:l-1] + ';'

    def getValuesToInsert(self, isbnList, titleList, dateList, quantityList, auteurList, booksToAdd):
        fields = []
        for i in range(booksToAdd):
            fields.append([])
            fields[i].append(isbnList[i])
            fields[i].append(titleList[i])
            fields[i].append(quantityList[i])
            fields[i].append(auteurList[i])
            fields[i].append(dateList[i])
        values = []
        for element in fields:
            values.append(self.getValuesBook(
                element[0], element[1], element[2], element[3], element[4]))
        result = "VALUES"
        for index, value in enumerate(values):
            if index == len(values) - 1:
                result += str(value) + ';'
            else:
                result += str(value) + ', '
        return result

    def getBorrowsToInsert(self, isbnList, personneId, booksToBorrow, today):
        fields = []
        for i in range(booksToBorrow):
            print(isbnList)
            fields.append([])
            fields[i].append(isbnList[i])
            fields[i].append(personneId)
        values = []
        for element in fields:
            values.append(self.getValuesBorrow(element[0], element[1], today))
        result = "VALUES"
        for index, value in enumerate(values):
            if index == len(values) - 1:
                result += str(value) + ';'
            else:
                result += str(value) + ', '
        print(result)
        return result

    def getValuesBorrow(self, isbn, personne_id, today):
        return "('{0}', '{1}', '{2}')".format(isbn, personne_id, today)

    def getValuesCategory(self, categories, isbn):
        elements = []
        for c in categories:
            elements.append("('{0}', '{1}')".format(c, isbn))
        return elements

    def getValuesBook(self, isbn, title, quantity, auteur, date):
        return "('{0}', '{1}', {2}, '{3}', '{4}')".format(isbn, title, quantity, auteur, date)

    def renderBorrowBookForm(self, personne_id, books):
        booksToBorrow = st.number_input(
            'Number of books to borrow', min_value=1, step=1)
        if booksToBorrow > 0:
            with st.form("formulaire_emprunt"):
                today = datetime.date.today()
                availableBooks = self.formatBooks(books)
                isbnList = []
                for index in range(0, booksToBorrow):
                    bookLabel = st.selectbox('Liste des livres disponibles' + str(index + 1),
                                             (self.renderBorrowLabel(availableBooks)))
                    isbn = self.getLabelId(bookLabel)
                    isbnList.append(isbn)
                submitted = st.form_submit_button("Submit")
                if submitted:
                    values = self.getBorrowsToInsert(
                        isbnList, personne_id, booksToBorrow, today)
                    self.borrowBooks(values, personne_id,
                                     booksToBorrow, isbnList)

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

    def borrowBooks(self, values, personne_id, booksToBorrow, isbnList):
        try:
            p = Personne(personne_id, self.db)
            personne = p.getCurrentUser()
            self.db.cur.execute(
                "INSERT INTO emprunt (livre_isbn, personne_id, date_emprunt) " + values)
            updated_limite = personne[2] - booksToBorrow
            if not updated_limite > 0:
                st.text("Vous dépassez la limite de livre que vous pouvez emprunter")
                return
            p.updateUserLimite(updated_limite, personne_id)
            for isbn in isbnList:
                updated_book_qty = self.getBookByISBN(isbn)[2] - 1
                self.updateBookQty(updated_book_qty, isbn)
            self.db.conn.commit()
            st.text("Emprunt(s) fait avec succès !")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            st.text("Il y a eu un echec lors de l'ajout des emprunts")
            st.text(error)
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

    def addBooks(self, bookValues, categoryValues, booksToAdd):
        try:
            self.db.cur.execute(
                "INSERT INTO livre (isbn, titre, quantite, auteur, date_publication) " + bookValues)
            self.db.cur.execute(
                "INSERT INTO categorie (categorie_name, livre_isbn) " + categoryValues)
            self.db.conn.commit()
            st.text(str(booksToAdd) + ' livres ont été ajouté avec succès !')
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            st.text("L'ajout de livre(s) a échoué")
            st.text(error)
            self.db.conn.rollback()

    def createCategory(self, categorie_name, livre_isbn):
        self.db.cur.execute("INSERT INTO categorie (categorie_name, livre_isbn) VALUES (%s, %s)",
                            (categorie_name, livre_isbn))

# from book import Book
class Personne:
    def __init__(self, personne_id, db):
        self.id = personne_id
        self.db = db
        self.isBlacklisted()

    # def isBlacklisted(self):
    #     book = Book(self.db)

    def getCurrentUser(self):
        self.db.cur.execute(
            "SELECT * FROM personne WHERE id = %s", (self.id,))
        return self.db.cur.fetchone()

    def getUserRole(self):
        self.db.cur.execute(
            "SELECT * FROM role WHERE personne_id = %s", (self.id,))
        return self.db.cur.fetchone()[0]
    
    def getPersonneIdByName(self, nom):
        self.db.cur.execute("SELECT * FROM personne WHERE nom = %s", (nom,))
        return self.db.cur.fetchone()[0]

    def updateUserLimite(self, updated_limite, personne_id):
        self.db.cur.execute("UPDATE personne SET limite = %s WHERE id = %s;", (updated_limite, personne_id))

from utils import get_next_month_date
import datetime

class Personne:
    def __init__(self, personne_id, db):
        self.id = personne_id
        self.db = db

    def isBlacklisted(self, unreturnedBooks):
        for book in unreturnedBooks:
            date = book[3]
            date_rendu_prevu = get_next_month_date(date)
            today = datetime.date.today()
            if date_rendu_prevu < today:
                return True

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
        self.db.cur.execute(
            "UPDATE personne SET limite = %s WHERE id = %s;", (updated_limite, personne_id))

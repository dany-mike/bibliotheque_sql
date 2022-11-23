class Personne:
    def __init__(self, personne_id, db):
        self.id = personne_id
        self.db = db

    def getCurrentUser(self):
        self.db.cur.execute(
            "SELECT * FROM personne WHERE id = %s", (self.id,))
        return self.db.cur.fetchone()

    def getUserRole(self):
        self.db.cur.execute(
            "SELECT * FROM role WHERE personne_id = %s", (self.id,))
        return self.db.cur.fetchone()[0]
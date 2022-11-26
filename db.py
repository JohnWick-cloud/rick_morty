import sqlite3

class Sqlite:
    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    def add_users(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT or IGNORE INTO 'users' VALUES (?)",(user_id,))
    
    def add_sezon(self, sezon, count):
        with self.connection:
            return self.cursor.execute("INSERT or IGNORE INTO 'sezons' VALUES (?,?)",(sezon,count))

    def add_cartoon(self, f_id, sezon, chapter):
        with self.connection:
            return self.cursor.execute("INSERT INTO 'cartoons' VALUES (?,?,?)",(f_id,sezon,f'{chapter} серия'))
    
    def get_sezon(self):
        with self.connection:
            self.sezons = self.cursor.execute("SELECT sezon FROM 'sezons'").fetchall()
            self.sezons_last = []
            for sezon in self.sezons:
                self.sezons_last.append(sezon[0])
            return self.sezons_last

    def get_count(self, sezon):
        with self.connection:
            return self.cursor.execute("SELECT count FROM 'sezons' WHERE sezon = ?",(sezon,)).fetchall()[0]
            # self.count_last = []
            # for count in self.counts:
            #     self.count_last.append(count[0])
            # return self.count_last

    def get_cartoon(self, sezon,chapter):
        with self.connection:
            self.cartoons = self.cursor.execute("SELECT id FROM 'cartoons' WHERE sezon = ? and chapter = ?",(sezon,chapter)).fetchall()
            self.cartoon_last = []
            for cartoon in self.cartoons:
                self.cartoon_last.append(cartoon)
            return self.cartoon_last

    def get_user(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM 'users'").fetchall()

    def update_sezon(self, sezon, count):
        with self.connection:
            return self.cursor.execute(f"UPDATE 'sezons' SET count = {count} WHERE sezon = '{sezon}'")

    
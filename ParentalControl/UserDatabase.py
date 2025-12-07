import sqlite3
import hashlib

class UserDatabase:
    def __init__(self, db_name="users.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )
            """)

    def check_user(self,username,password):
        hash_password = hashlib.sha256(password.encode()).hexdigest()
        self.cursor.execute("SELECT 1 FROM users WHERE username = ? AND password = ?", (username,hash_password))
        return self.cursor.fetchone() is not None



    def add_user(self, username, password):
        hash_password = hashlib.sha256(password.encode()).hexdigest()
        print (hash_password)
        try:
            self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                                (username, hash_password))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # username already exists

    def get_table(self):
        self.cursor.execute("Select * FROM users")
        return self.cursor.fetchall()

    def reset_table(self):
        self.cursor.execute("DELETE FROM users")
        self.cursor.execute("DELETE FROM sqlite_sequence WHERE name='users'")  # reset id
        self.conn.commit()
if __name__=="__main__":
    db=UserDatabase()
    db.add_user("nadav","1234")
    print (db.get_table())

    print (db.check_user("nadav","1234"))

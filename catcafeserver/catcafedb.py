import sqlite3
DATABASE_NAME = "catcafe.db"

def get_db():
    conn = sqlite3.connect(DATABASE_NAME)  #CONEXION
    return conn


def create_tables():
    tables = {
        """CREATE TABLE IF NOT EXISTS admins(
            id_admin INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL,
            password TEXT NOT NULL
            )
            """,
        
        """CREATE TABLE IF NOT EXISTS users(
            id_user INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL
            )
            """
    }
    
    db = get_db()
    cursor = db.cursor()
    for table in tables:
        cursor.execute(table)
        



create_tables()
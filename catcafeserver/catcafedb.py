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
        
        """CREATE TABLE IF NOT EXISTS gatos(
            id_gato INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            race TEXT NOT NULL
            )
            """,
            
        """CREATE TABLE IF NOT EXISTS solicitudes(
            id_solicitud INTEGER PRIMARY KEY AUTOINCREMENT,
            id_gato INTEGER,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            FOREIGN KEY(id_gato) REFERENCES gatos(id_gato)
            )"""
    }
    
    db = get_db()
    cursor = db.cursor()
    for table in tables:
        cursor.execute(table)
        



create_tables()
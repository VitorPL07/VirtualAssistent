import sqlite3

conn = sqlite3.connect("Niver.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Aniversario(
    Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    Nome TEXT NOT NULL,
    Data TEXT NOT NULL
);
""")
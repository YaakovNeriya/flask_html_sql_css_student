import sqlite3

def connect():
    return sqlite3.connect('schol.db')

def students_table(conn):
    conn.execute('''CREATE TABLE IF NOT EXISTS students
                 (id INTEGER PRIMARY KEY,
                 name VARCHAR (50) NOT NULL,
                 age INTEGER NOT NULL);''')
    









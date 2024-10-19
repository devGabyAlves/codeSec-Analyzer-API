import sqlite3

conn = sqlite3.connect('example.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
''')

def add_user(username, password):
    cursor.execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')")
    conn.commit()

def authenticate(username, password):
    cursor.execute(f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'")
    user = cursor.fetchone()
    if user:
        print("Autenticado com sucesso!")
    else:
        print("Falha na autenticação!")

username = input("Digite seu nome de usuário: ")
password = input("Digite sua senha: ")

add_user(username, password)
authenticate(username, password)

conn.close()

import sqlite3

# Conectar ao banco de dados SQLite
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# Criar uma tabela de usuários
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
''')

# Inserir um novo usuário (exemplo vulnerável)
def add_user(username, password):
    cursor.execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')")
    conn.commit()

# Autenticar usuário (exemplo vulnerável)
def authenticate(username, password):
    cursor.execute(f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'")
    user = cursor.fetchone()
    if user:
        print("Autenticado com sucesso!")
    else:
        print("Falha na autenticação!")

# Exemplo de uso
username = input("Digite seu nome de usuário: ")
password = input("Digite sua senha: ")

add_user(username, password)
authenticate(username, password)

conn.close()

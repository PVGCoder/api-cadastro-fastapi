from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# Criar banco de dados e tabela
conn = sqlite3.connect("usuarios.db")
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    )
''')
conn.commit()
conn.close()

# Modelo de dados
class Usuario(BaseModel):
    nome: str
    email: str

# Criar usuário
@app.post("/usuarios/")
def criar_usuario(usuario: Usuario):
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (nome, email) VALUES (?, ?)", (usuario.nome, usuario.email))
        conn.commit()
        return {"mensagem": "Usuário cadastrado!"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    finally:
        conn.close()

# Listar usuários
@app.get("/usuarios/")
def listar_usuarios():
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    conn.close()
    return usuarios

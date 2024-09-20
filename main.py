import sqlite3
from colorama import Fore, Style
import re
import time

def validar(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def verificar(senha):
    if len(senha) < 8:
        print(Fore.RED + 'Senha deve ter pelo menos 8 caracteres.' + Style.RESET_ALL)
        return False
    return (re.search(r'[A-Z]', senha) and
            re.search(r'[a-z]', senha) and
            re.search(r'[0-9]', senha) and
            re.search(r'[!@#$%^&*(),.?":{}|<>]', senha))

def iniciar_db():
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            email TEXT NOT NULL UNIQUE,
                            senha TEXT)''')

def usuario_existe(email):
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        return cursor.fetchone() is not None

def cadastrar_usuario(email, senha):
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (email, senha) VALUES (?, ?)", (email, senha))
        conn.commit()

def inicio():
    iniciar_db()  

    tentativas = 0
    while tentativas <= 3:
        if tentativas >= 3:
            print(Fore.RED + 'Número máximo de tentativas atingido. Tente novamente após 5 segundos!' + Style.RESET_ALL)
            for i in range(5, -1, -1):
                print(f'Voltando em {i} segundos...', end="\r")
                time.sleep(1)
            tentativas = 0
            continue

        email = input('\nDigite o e-mail: ')
        senha = input('Digite a senha: ')
        senha2 = input('Confirme sua senha: ')

        if validar(email) and verificar(senha):
            if usuario_existe(email):
                print(Fore.LIGHTRED_EX + 'Email já existe. Tente novamente' + Style.RESET_ALL)
                tentativas += 1
                continue
            
            if senha != senha2:
                print(Fore.LIGHTRED_EX + 'As senhas não coincidem. Tente novamente' + Style.RESET_ALL)
                tentativas += 1
                continue
            
            
            print(Fore.GREEN + f'E-mail e senha cadastrados com sucesso! E-mail: {email}' + Style.RESET_ALL)
            cadastrar_usuario(email, senha)
            break
        else:
            print(Fore.RED + 'E-mail inválido ou senha inválida. Tente novamente.' + Style.RESET_ALL)
            tentativas += 1

    else:
        sair = input("Digite 's' para repetir ou qualquer outra tecla para sair: ")
        if sair.lower() == 's':
            inicio()
        else:
            print('Obrigado por usar nosso sistema!')

def consultar_dados():
    """Consulta todos os dados da tabela 'users.db'."""
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        resultados = cursor.fetchall()
        for resultado in resultados:
            print(resultado)

inicio()
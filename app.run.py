"""Finalidade: Sistema de Gerenciamento de Documentos - GED.
Aluna: Amanda Queiroz
Aluno: Cleber Batista Ribeiro
Aluno: Diogo da Silveira Ribeiro
Aluna: Mariane Dantas Cardoso
Aluno: Moabe Pereira de Melo
Data: 02/06/2023
Versão: 1.0
Python versão: 3.11
Link do repositório no GitHub para analisar o código
 -> https://github.com/Sogoid/Projeto_Integrador_2023_N2
"""

from database import Session
from models import Usuarios
from werkzeug.security import generate_password_hash


def app():
    session = Session()

    # Leia a entrada do usuário
    login_usuario = input('Digite o nome do usuário: ')
    email_usuario = input('Digite o email do usuário: ')
    senha_usuario = input('Digite o senha do usuário: ')
    status_usuario = "A"
    tipo = "U"

    # Gere um hash seguro da senha
    senha_hash = generate_password_hash(senha_usuario)

    # Crie um objeto User e adicione-o ao banco de dados
    new_user = Usuarios(login_usuario=login_usuario, email_usuario=email_usuario, senha_usuario=senha_hash,
                        status_usuario=status_usuario, tipo=tipo)
    session.add(new_user)
    session.commit()

    # Feche a sessão quando terminar de usá-la
    session.close()


if __name__ == "__main__":
    app()

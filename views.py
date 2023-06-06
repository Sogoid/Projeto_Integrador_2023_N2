from getpass import getpass

from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash

from database import Session
from helpers import cadastro_password, getch, clear_terminal, tempo_sleep, titulo_sistema, linha, sair_sistema, \
    titulo_principal, nome_user
from models import Usuarios, Grupos


# O sistema deverá conter as seguintes telas para atender aos requisitos.


# TODO: 5. Uma tela de listagem de usuários
# TODO: 6. Uma tela de bloqueio e desbloqueio de usuários
# TODO: 7. Uma tela de listagem de grupos

# TODO: 9. Uma tela de alteração de grupos
# TODO: 10. Uma tela para inclusão de um usuário em um grupo
# TODO: 11. Uma tela para exclusão de um usuário de um grupo com mensagem de confirmação da exclusão
# TODO: 12. Uma tela para listagem dos documentos cadastrados no sistema com mensagem de confirmação para exclusão
# TODO: 13. Uma tela para upload de múltiplos documentos no sistema


def cadastro(tipo_usuario):
    clear_terminal()

    sair_do_sistema = False
    while not sair_do_sistema:
        # Verificando se o tipo do cliente tem permissão antes do cadastro
        if tipo_usuario == "U":
            titulo_principal(10, "Tela de cadastro de Usuário.")
            print("Usuário sem permissão!")
            continuar = input("\nDeseja voltar para o menu inicial? S/N: ")
            match continuar.casefold():
                case 's':
                    clear_terminal()
                    menu_opcao()
                    break
                case 'n':
                    sair_sistema()
                case _:
                    print("Entrada inválida. Por favor, digite 's' para continuar ou 'n' para sair.")
        else:
            titulo_principal(10, "Tela de cadastro de Usuário.")
            nome_user()
            while True:
                # Leia a entrada do usuário
                login_usuario = input('Digite o nome do usuário: ')
                email_usuario = input('Digite o email do usuário: ')
                senha_usuario = cadastro_password()
                status_usuario = "A"
                tipo = "U"

                # Gere um hash seguro da senha usando o método 'scrypt'
                senha_hash = generate_password_hash(senha_usuario, method='scrypt')

                # Inicia a sessão do banco de dados
                session = Session()

                # Crie um objeto User e adicione-o ao banco de dados
                new_user = Usuarios(login_usuario=login_usuario, email_usuario=email_usuario, senha_usuario=senha_hash,
                                    status_usuario=status_usuario, tipo=tipo)
                session.add(new_user)
                session.commit()

                # Feche a sessão quando terminar de usá-la
                session.close()

                # Pergunte ao usuário se ele deseja continuar adicionando usuários
                while True:
                    choice = input("Deseja adicionar outro usuário (S/N), retornar ao menu (M) ou sair (X)? ")
                    if choice.lower() == 's':
                        break
                    elif choice.lower() == 'n' or choice.lower() == 'x':
                        sair_sistema()
                    elif choice.lower() == 'm':
                        clear_terminal()
                        menu_opcao()


# Uma tela de cadastro no sistema
def cadastro_login():
    clear_terminal()

    while True:
        titulo_principal(10, "Tela de cadastro de Usuário.")
        # Leia a entrada do usuário
        login_usuario = input('Digite o nome do usuário: ')
        email_usuario = input('Digite o email do usuário: ')
        senha_usuario = cadastro_password()
        status_usuario = "A"
        tipo = "U"

        # Gere um hash seguro da senha usando o método 'scrypt'
        senha_hash = generate_password_hash(senha_usuario, method='scrypt')

        # Inicia a sessão do banco de dados
        session = Session()

        # Crie um objeto User e adicione-o ao banco de dados
        new_user = Usuarios(login_usuario=login_usuario, email_usuario=email_usuario, senha_usuario=senha_hash,
                            status_usuario=status_usuario, tipo=tipo)
        session.add(new_user)
        session.commit()

        # Feche a sessão quando terminar de usá-la
        session.close()

        # Pergunte ao usuário se ele deseja continuar adicionando usuários
        while True:
            choice = input("Deseja retornar ao menu (M) ou sair (X)? ")
            if choice.lower() == 'n' or choice.lower() == 'x':
                sair_sistema()
                clear_terminal()
            elif choice.lower() == 'm':
                clear_terminal()
                menu_opcao()


# TODO: 4. Uma tela de alteração de senha
def alterar_senha():
    global logged_in_user_id
    while True:
        titulo_principal(10, "Tela de Alteração de Senhas.")
        session = Session()

        # Verifique se a senha está correta
        user = session.query(Usuarios).get(logged_in_user_id)
        if user:
            # Obtenha a senha antiga do usuário
            print(f"Usuário: {user.login_usuario.upper()}")
            senha_antiga = getpass("Senha antiga: ")
            if check_password_hash(user.senha_usuario, senha_antiga):
                new_password = cadastro_password()
                user.senha_usuario = generate_password_hash(new_password)
                session.commit()
                choice = input("Deseja retornar ao menu (M) ou sair (X)? ")
                if choice.lower() == 'n' or choice.lower() == 'x':
                    sair_sistema()
                    clear_terminal()
                elif choice.lower() == 'm':
                    clear_terminal()
                    menu_navegacao(tipo_usuario)
        else:
            print("Erro: usuário não encontrado.")

        # Feche a sessão quando terminar de usá-la
        session.close()


# 8. Uma tela de inclusão de grupos
def cadastrar_grupo():
    titulo_principal(10, "Tela de cadastro de Grupo.")
    nome_user()
    while True:
        # Leia a entrada do usuário
        descricao = input("Informe Nome/Descrição Novo Grupo: ")

        # Inicia a sessão do banco de dados
        session = Session()

        # Crie um objeto User e adicione-o ao banco de dados
        new_doc = Grupos(descricao=descricao)
        session.add(new_doc)
        session.commit()

        # Feche a sessão quando terminar de usá-la
        session.close()

        # Pergunte ao usuário se ele deseja continuar adicionando usuários
        while True:
            choice = input("Deseja adicionar outro documento (S/N), retornar ao menu (M) ou sair (X)? ")
            if choice.lower() == 's':
                break
            elif choice.lower() == 'n' or choice.lower() == 'x':
                clear_terminal()
                titulo_principal(10, "Tela de cadastro de Grupo.")
                sair_sistema()
            elif choice.lower() == 'm':
                clear_terminal()
                menu_opcao()


tipo_usuario = None


# Uma tela de login no sistema
def login():
    global tipo_usuario
    global logged_in_user_id
    while True:
        titulo_principal(17, "Tela de login.")
        # Get the username and password from the user
        username = input("Usuário: ")
        password = getpass("Senha: ")
        session = Session()

        # Check if the username and password are correct
        user = session.query(Usuarios).filter(func.lower(Usuarios.login_usuario) == username.lower()).first()

        if user and check_password_hash(user.senha_usuario, password):
            # Display success message
            print(f"\nBem vindo {username.upper()}!\n")

            linha(50)
            print(f'{"":6}Entrando no sistema por favor aguarde!')
            linha(50)

            # Wait for a few seconds
            print()
            tempo_sleep(50)

            # Clear the terminal
            clear_terminal()
            tipo_usuario = user.tipo
            logged_in_user_id = user.idusuario
            menu_navegacao(tipo_usuario)

        else:
            # Display error message
            print("Nome de usuário ou senha incorretos!\n")

            # Check if the Esc key was pressed
            titulo_sistema("Pressione Esc para sair ou qualquer outra tecla para continuar.")
            ch = getch()
            clear_terminal()
            if ch == '\x1b' or ch == '\033' or ch == '\u001b':
                titulo_principal(17, "Tela de login")
                print("\nA tecla Esc foi pressionada, saindo aguarde!")
                tempo_sleep(50)
                clear_terminal()
                break

        # Fechar a sessão quando terminar de usá-la
        session.close()


# Uma tela principal para ser mostrada para o usuário quando ele realizar login no sistema
def menu_opcao():
    """Função criada para ser menu"""
    continuar = "s"
    while continuar == 's' or continuar == 'S':
        titulo_principal(17, "Menu de Opção.")
        print("\nEscolha uma das opções abaixo:")
        print('''
        1 – Login no Sistema;\n
        2 – Cadastro para novos Usuários;\n
        3 - Sair.''')
        opcao = int(input("\nDigite uma opção para interagir: "))
        match opcao:
            case 1:
                clear_terminal()
                login()
            case 2:
                clear_terminal()
                cadastro_login()
            case 3:
                titulo_principal(17, "Menu de Opção.")
                sair_sistema()
        continuar = input("\nDeseja voltar para o menu inicial? S/N: ")
        while continuar.casefold() not in ['s', 'n']:
            print("Entrada inválida. Por favor, digite 's' para continuar ou 'n' para sair.")
            continuar = input("\nDeseja voltar para o menu inicial? S/N: ")


def menu_navegacao(tipo_user):
    """Função criada para ser menu"""
    continuar = "s"
    while continuar == 's' or continuar == 'S':
        titulo_principal(15, "Menu de Navegação.")
        print("\nEscolha uma das opções abaixo:")
        print('''
        1 – Cadastro de Usuários;\n
        2 – Cadastro de Grupos;\n
        3 – Alteração de Senha de usuário;\n
        4 - Sair.''')
        opcao = int(input("\nDigite uma opção para interagir: "))
        match opcao:
            case 1:
                clear_terminal()
                cadastro(tipo_user)
            case 2:
                clear_terminal()
                cadastrar_grupo()
            case 3:
                clear_terminal()
                alterar_senha()
            case 4:
                clear_terminal()
                titulo_principal(15, "Menu de Navegação.")
                sair_sistema()
        continuar = input("\nDeseja voltar para o menu inicial? S/N: ")
        while continuar.casefold() not in ['s', 'n']:
            print("Entrada inválida. Por favor, digite 's' para continuar ou 'n' para sair.")
            continuar = input("\nDeseja voltar para o menu inicial? S/N: ")

from getpass import getpass

from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash

from database import Session
from helpers import cadastro_password, getch, clear_terminal, logo, tempo_sleep, titulo_sistema, linha, sair_sistema
from models import Usuarios


def cadastro(tipo_usuario):
    clear_terminal()

    # session = Session()

    sair_do_sistema = False
    while not sair_do_sistema:
        # Verificando se o tipo do cliente tem permissão antes do cadastro
        if tipo_usuario == "U":
            logo()
            linha(50)
            print(f'{"":10}Tela de cadastro de Usuário.')
            linha(50)
            print()
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
            logo()
            linha(50)
            print(f'{"":10}Tela de cadastro de Usuário.')
            linha(50)
            print()
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


tipo_usuario = None


def login():
    global tipo_usuario
    while True:
        logo()
        linha(50)
        print(f'{"":17}Tela de Login')
        linha(50)
        print()
        # Get the username and password from the user
        username = input("Usuário: ")
        password = getpass("Senha: ")
        session = Session()

        # Check if the username and password are correct
        user = session.query(Usuarios).filter(func.lower(Usuarios.login_usuario) == username.lower()).first()

        if user and check_password_hash(user.senha_usuario, password):
            # Display success message
            print(f"\nBem vindo {username}!\n")

            linha(50)
            print(f'{"":6}Entrando no sistema por favor aguarde!')
            linha(50)

            # Wait for a few seconds
            print()
            tempo_sleep(50)

            # Clear the terminal
            clear_terminal()
            tipo_usuario = user.tipo
            menu_opcao()

        else:
            # Display error message
            print("Nome de usuário ou senha incorretos!\n")

            # Check if the Esc key was pressed
            titulo_sistema("Pressione Esc para sair ou qualquer outra tecla para continuar.")
            ch = getch()
            clear_terminal()
            if ch == '\x1b' or ch == '\033' or ch == '\u001b':
                logo()
                linha(50)
                print(f'{"":17}Tela de Login')
                linha(50)
                print()
                print("\nA tecla Esc foi pressionada, saindo aguarde!")
                tempo_sleep(50)
                clear_terminal()
                break

        # Fechar a sessão quando terminar de usá-la
        session.close()


def menu_opcao():
    """Função criada para ser menu"""
    continuar = "s"
    while continuar == 's' or continuar == 'S':
        logo()
        linha(50)
        print(f'{"":17}Menu de Opção')
        linha(50)
        print()
        print("\nEscolha uma das opções abaixo:")
        print('''
        1 – Cadastro ;\n
        2 – Atualizar ;\n
        3 - Excluir;\n
        4 – Relatorio; \n
        5 - Sair.''')
        opcao = int(input("\nDigite uma opção para interagir: "))
        match opcao:
            case 1:
                cadastro(tipo_usuario)

            # case 2:
            #     atualizar(dados_cadastrados)
            # case 3:
            #     excluir_cadastro(dados_cadastrados)
            # case 4:
            #     if not dados_cadastrados:
            #         print("Nenhum usuário cadastrado.")
            #     else:
            #         gera_relatorio(dados_cadastrados)
            case 5:
                sair_sistema()
        continuar = input("\nDeseja voltar para o menu inicial? S/N: ")
        while continuar.casefold() not in ['s', 'n']:
            print("Entrada inválida. Por favor, digite 's' para continuar ou 'n' para sair.")
            continuar = input("\nDeseja voltar para o menu inicial? S/N: ")

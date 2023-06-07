from getpass import getpass

from sqlalchemy import func
from werkzeug.security import check_password_hash, generate_password_hash

from database import Session
from helpers import getch, clear_terminal, tempo_sleep, titulo_sistema, linha, sair_sistema, \
    titulo_principal, cadastro_password
from models import Usuarios, Grupos
from ultis import listagem_usuario, pesquisa_usuario, listagem_grupo, pesquisa_grupo


# TODO: 6. Uma tela de bloqueio e desbloqueio de usuários
# TODO: 10. Uma tela para inclusão de um usuário em um grupo
# TODO: 11. Uma tela para exclusão de um usuário de um grupo com mensagem de confirmação da exclusão
# TODO: 12. Uma tela para listagem dos documentos cadastrados no sistema com mensagem de confirmação para exclusão
# TODO: 13. Uma tela para upload de múltiplos documentos no sistema


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


# INICIO DE FUNÇÕES DE CADASTRO
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


def cadastro(tipo_user):
    clear_terminal()

    sair_do_sistema = False
    while not sair_do_sistema:
        # Verificando se o tipo do cliente tem permissão antes do cadastro
        if tipo_user == "U":
            titulo_principal(10, "Tela de cadastro de Usuário.")
            print("Usuário sem permissão!")
            continuar = input("\nDeseja voltar para o menu inicial? S/N: ")
            match continuar.casefold():
                case 's':
                    clear_terminal()
                    menu_navegacao(tipo_user)
                    break
                case 'n':
                    sair_sistema()
                case _:
                    print("Entrada inválida. Por favor, digite 's' para continuar ou 'n' para sair.")
        else:
            titulo_principal(10, "Tela de cadastro de Usuário.")
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
                        menu_cadastro(tipo_user)


def cadastrar_grupo(tipo_user):
    titulo_principal(10, "Tela de cadastro de Grupo.")
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
                menu_cadastro(tipo_user)


# FIM DE FUNÇÕES DE CADASTRO

# INICIO DE FUNÇÕES DE ATUALIZAÇÃO

def alterar_senha(tipo_user):
    global logged_in_user_id
    while True:
        titulo_principal(8, "Tela de Atualização de Senhas.")
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
                    menu_navegacao(tipo_user)
        else:
            print("Erro: usuário não encontrado.")

        # Feche a sessão quando terminar de usá-la
        session.close()


def alterar_grupo(tipo_user):
    while True:
        titulo_principal(8, "Tela de Atualização de GRUPO.")

        # Pede ao usuário para digitar o nome do grupo que deseja buscar
        descricao = input("Digite o nome do grupo que deseja buscar: ")
        print()
        linha(50)
        print()
        session = Session()

        # Verifique se a senha está correta
        grupo = session.query(Grupos).filter(Grupos.descricao == descricao).first()
        if grupo:
            grupo.descricao = input("Digite o novo nome do grupo: ")
            session.commit()
            choice = input("Deseja retornar ao menu (M) ou sair (X)? ")
            if choice.lower() == 'n' or choice.lower() == 'x':
                sair_sistema()
                clear_terminal()
            elif choice.lower() == 'm':
                clear_terminal()
                menu_navegacao(tipo_user)
        else:
            print("Erro: usuário não encontrado.")

        # Feche a sessão quando terminar de usá-la
        session.close()


# FIM DE FUNÇÕES DE ATUALIZAÇÃO

tipo_usuario = None


# INICIO DE FUNÇÕES DE MENU
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
        2 – Atualização de dados;\n
        3 – Relatórios do Sistema;\n
        4 - Sair.''')
        opcao = int(input("\nDigite uma opção para interagir: "))
        match opcao:
            case 1:
                clear_terminal()
                menu_cadastro(tipo_user)
            case 2:
                clear_terminal()
                menu_alterar(tipo_user)
            case 3:
                clear_terminal()
                relatorios(tipo_user)
                sair_sistema()
            case 4:
                clear_terminal()
                titulo_principal(15, "Menu de Navegação.")
                sair_sistema()
        continuar = input("\nDeseja voltar para o menu navegação? S/N: ")
        while continuar.casefold() not in ['s', 'n']:
            print("Entrada inválida. Por favor, digite 's' para continuar ou 'n' para sair.")
            continuar = input("\nDeseja voltar para o menu navegação? S/N: ")


def menu_alterar(tipo_user):
    """Função criada para ser menu"""
    continuar = "s"
    while continuar == 's' or continuar == 'S':
        titulo_principal(8, "Menu de Atualização de dados.")
        print("\nEscolha uma das opções abaixo:")
        print('''
        1 – Atualizar Senha de Usuário;\n
        2 – Atualizar Nome de Grupo;\n
        3 – Menu de Navegação;\n
        4 - Sair.''')
        opcao = int(input("\nDigite uma opção para interagir: "))
        match opcao:
            case 1:
                clear_terminal()
                alterar_senha(tipo_user)
            case 2:
                clear_terminal()
                alterar_grupo(tipo_user)
            case 3:
                clear_terminal()
                menu_navegacao(tipo_user)
            case 4:
                clear_terminal()
                titulo_principal(8, "Menu de Atualização de dados.")
                sair_sistema()
        continuar = input("\nDeseja voltar para o menu navegação? S/N: ")
        while continuar.casefold() not in ['s', 'n']:
            print("Entrada inválida. Por favor, digite 's' para continuar ou 'n' para sair.")
            continuar = input("\nDeseja voltar para o menu navegação? S/N: ")


def menu_cadastro(tipo_user):
    """Função criada para ser menu"""
    continuar = "s"
    while continuar == 's' or continuar == 'S':
        titulo_principal(10, "Menu de Cadastro.")
        print("\nEscolha uma das opções abaixo:")
        print('''
        1 – Cadastro de Usuários;\n
        2 – Cadastro de Grupos;\n
        3 – Menu de Navegação;\n
        4 - Sair.''')
        opcao = int(input("\nDigite uma opção para interagir: "))
        match opcao:
            case 1:
                clear_terminal()
                cadastro(tipo_user)
            case 2:
                clear_terminal()
                cadastrar_grupo(tipo_user)
            case 3:
                clear_terminal()
                menu_navegacao(tipo_user)
            case 4:
                clear_terminal()
                titulo_principal(10, "Menu de Cadastro.")
                sair_sistema()
        continuar = input("\nDeseja voltar para o menu navegação? S/N: ")
        while continuar.casefold() not in ['s', 'n']:
            print("Entrada inválida. Por favor, digite 's' para continuar ou 'n' para sair.")
            continuar = input("\nDeseja voltar para o menu navegação? S/N: ")


def relatorios(tipo_user):
    cont = "s"
    while cont == 's' or cont == 'S':
        titulo_principal(15, "Menu de Relatórios.")
        print("\nEscolha uma das opções abaixo:")
        print('''
           1 – Listagem de Usuários;\n
           2 – Pesquisa de Usuários;\n
           3 – Listagem de Grupos;\n
           4 – Pesquisa de Grupos;\n
           5 – Menu de Navegação;\n
           6 - Sair.''')
        opcao = int(input("\nDigite uma opção para interagir: "))
        match opcao:
            case 1:
                clear_terminal()
                listagem_usuario()
            case 2:
                clear_terminal()
                pesquisa_usuario()

            case 3:
                clear_terminal()
                listagem_grupo()

            case 4:
                clear_terminal()
                pesquisa_grupo()

            case 5:
                clear_terminal()
                menu_navegacao(tipo_user)

            case 6:
                clear_terminal()
                titulo_principal(15, "Menu de Relatórios.")
                sair_sistema()
        cont = input("\nDeseja voltar para o menu relatório? S/N: ")
        while cont.casefold() not in ['s', 'n']:
            print("Entrada inválida. Por favor, digite 's' para continuar ou 'n' para sair.")
            cont = input("\nDeseja voltar para o menu relatório? S/N: ")

# FIM DE FUNÇÕES DE MENU

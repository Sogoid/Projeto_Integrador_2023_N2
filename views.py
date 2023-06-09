import os
import shutil
from getpass import getpass
from tkinter import Tk
from tkinter.filedialog import askopenfilename

from sqlalchemy import func
from werkzeug.security import check_password_hash, generate_password_hash

from database import Session, UPLOAD_PATH
from helpers import getch, clear_terminal, tempo_sleep, titulo_sistema, linha, sair_sistema, \
    titulo_principal, cadastro_password
from models import Usuarios, Grupos, Documentos, Pertence, Contem
from ultis import listagem_usuario, pesquisa_usuario, listagem_grupo, pesquisa_grupo, allowed_file, tabela_relatorio

# TODO: 11. Uma tela para exclusão de um usuário de um grupo com mensagem de confirmação da exclusão
# TODO: 12. Uma tela para listagem dos documentos cadastrados no sistema com mensagem de confirmação para exclusão


logged_in_user_id = None


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
        if user is None or not check_password_hash(user.senha_usuario, password):
            print("\nNome de usuário ou senha incorretos!\n")

            # Check if the Esc key was pressed
            titulo_sistema("Pressione Esc para sair ou qualquer outra tecla para continuar.")
            ch = getch()
            clear_terminal()
            if ch == '\x1b' or ch == '\033' or ch == '\u001b':
                titulo_principal(17, "Tela de login")
                print("\nA tecla Esc foi pressionada, saindo aguarde!")
                sair_sistema()
                clear_terminal()
            else:
                menu_opcao()

        # Check if the user is blocked
        if user.status_usuario != 'A':
            print(f"Usuário {user.login_usuario.upper()} bloqueado."
                  f"\nPor favor entre em contato com o administrador!")

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

        # Fechar a sessão quando terminar de usá-la
        session.close()


def user_logado():
    global logged_in_user_id
    session = Session()
    try:
        # Pede ao usuário para digitar o nome do grupo que deseja buscar
        user = session.query(Usuarios).get(logged_in_user_id)
        if user:
            # Obtenha a senha antiga do usuário
            print(f"Usuário: {user.login_usuario.upper()}")
        else:
            print("Erro: Usuário não encontrado.")
    except Exception as e:
        print(f"Erro ao acessar o banco de dados: {e}")

    # Feche a sessão quando terminar de usá-la
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
            user_logado()
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
    user_logado()
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
            choice = input("Deseja adicionar outro grupo (S/N), retornar ao menu (M) ou sair (X)? ")
            if choice.lower() == 's':
                break
            elif choice.lower() == 'n' or choice.lower() == 'x':
                clear_terminal()
                titulo_principal(10, "Tela de cadastro de Grupo.")
                sair_sistema()
            elif choice.lower() == 'm':
                clear_terminal()
                menu_cadastro(tipo_user)


def cadastro_documento(tipo_user):
    while True:
        titulo_principal(15, "Cadastro de Documentos.")
        user_logado()
        resposta = input('Você gostaria de cadastrar um documento? (s/n) ')
        if resposta.lower() == 's':
            # Seleciona o arquivo
            Tk().withdraw()
            filepath = askopenfilename()

            if not filepath:
                print('Nenhum arquivo selecionado.')
                return
            name = os.path.basename(filepath)

            # Verifica se o tipo de arquivo é permitido
            if not allowed_file(name):
                print(f'Tipo de arquivo não permitido: {name}')
                return

            # Cria a pasta uploads se ela não existir
            if not os.path.exists(UPLOAD_PATH):
                os.makedirs(UPLOAD_PATH)

            # Copia o arquivo para a pasta uploads
            path = f'{UPLOAD_PATH}/{name}'
            shutil.copyfile(filepath, path)

            # Salva o nome e o caminho do arquivo no banco de dados
            session = Session()
            file = Documentos(nome_documento=name, endereco_documento=path)
            session.add(file)
            session.commit()
            # Fecha a sessão quando terminar de usá-la
            session.close()

        elif resposta.lower() == 'n':
            print('Ok, não vamos cadastrar um documento.')
            tempo_sleep(50)
            menu_cadastro(tipo_user)

        else:
            print('Opção inválida. Por favor, digite "s" ou "n".')


def adicionar_usuario_grupo():
    titulo_principal(10, "Adicionar Usuário ao Grupo.")
    user_logado()

    # Cria a lista com os títulos das colunas
    cabecalho = ["ID USUÁRIO", "NOME USUÁRIO", "ID GRUPO", "DESCRIÇÃO"]

    session = Session()

    user = None
    while not user:
        # Pede ao usuário para digitar o nome do usuário que deseja buscar
        login_usuario = input("Digite o nome do usuário que deseja buscar: ")
        descricao = input("Digite o nome do grupo que deseja buscar: ")
        print()
        linha(50)
        print()

        # Busca informações sobre o usuário especificado
        user = session.query(Usuarios).filter(Usuarios.login_usuario == login_usuario).first()
        grupo = session.query(Grupos).filter(Grupos.descricao == descricao).first()
        if user:
            dados = [[user.idusuario, user.login_usuario, grupo.idgrupos, grupo.descricao]]
            tabela_relatorio(cabecalho, dados)
            linha(50)
            print()
        else:
            print("Usuário ou Grupo não encontrado.")

    id_usuario = input("Digite o ID do Usuário: ")
    id_grupo = input("Digite o ID do Grupo: ")
    linha(50)

    # Verifica se já existe um relacionamento entre o usuário e o grupo especificados
    new_pertence = session.query(Pertence).filter_by(idusuario=id_usuario, idgrupos=id_grupo).first()
    if new_pertence is not None:
        print('Já existe um relacionamento entre o usuário e o grupo especificados.')
    else:
        usuario_grupo = Pertence(idusuario=id_usuario, idgrupos=id_grupo)
        session.add(usuario_grupo)
        session.commit()
        print("Operação efetuada com sucesso!!")

    # Fechar a sessão quando terminar de usá-la
    session.close()


def adicionar_grupo_documento():
    titulo_principal(10, "Adicionar Grupo ao Documento.")
    user_logado()

    # Cria a lista com os títulos das colunas
    cabecalho = ["ID DOCUMENTO", "DESCRIÇÃO", "ID GRUPO", "DESCRIÇÃO"]

    session = Session()

    user = None
    while not user:
        # Pede ao usuário para digitar o nome do usuário que deseja buscar
        nome_documento = input("Digite o nome do documento que deseja buscar: ")
        descricao = input("Digite o nome do grupo que deseja buscar: ")
        print()
        linha(50)
        print()

        # Busca informações sobre o usuário especificado
        user = session.query(Documentos).filter(Documentos.nome_documento == nome_documento).first()
        grupo = session.query(Grupos).filter(Grupos.descricao == descricao).first()
        if user:
            dados = [[user.iddocumento, user.nome_documento, grupo.idgrupos, grupo.descricao]]
            tabela_relatorio(cabecalho, dados)
            linha(50)
            print()
        else:
            print("Documento ou Grupo não encontrado.")

    id_documento = input("Digite o ID do Documento: ")
    id_grupo = input("Digite o ID do Grupo: ")
    linha(50)

    # Verifica se já existe um relacionamento entre o usuário e o grupo especificados
    new_contem = session.query(Contem).filter_by(iddocumento=id_documento, idgrupos=id_grupo).first()
    if new_contem is not None:
        print('Já existe um relacionamento entre o usuário e o grupo especificados.')
    else:
        documento_grupo = Contem(iddocumento=id_documento, idgrupos=id_grupo)
        session.add(documento_grupo)
        session.commit()
        print("Operação efetuada com sucesso!!")

    # Fechar a sessão quando terminar de usá-la
    session.close()


# FIM DE FUNÇÕES DE CADASTRO

# INICIO DE FUNÇÕES DE ATUALIZAÇÃO

def alterar_senha_user(tipo_user):
    global logged_in_user_id
    while True:
        clear_terminal()
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
        user_logado()
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
            print("Erro: Grupo não encontrado.")

        # Feche a sessão quando terminar de usá-la
        session.close()


def alterar_status_user(tipo_user):
    titulo_principal(8, "Tela de Atualização de Status.")
    user_logado()
    if tipo_user != 'A':
        print("Erro: Apenas usuários com tipo 'A' (administrador) podem utilizar esta função.")
        return

    while True:
        titulo_principal(8, "Tela de Atualização de Status.")
        user_logado()

        id_user = input("Digite o ID do Usuário que deseja buscar: ")
        print()
        session = Session()

        # Verifique se a senha está correta
        user = session.query(Usuarios).filter(Usuarios.idusuario == id_user).first()
        if user:
            linha(50)
            print(f"Usuário: {user.login_usuario.upper()}")
            linha(50)
            print("\nLegenda: A-Ativo, B-Bloqueado\n")
            status_usuario = input("Digite o seu novo Status: ")
            while status_usuario.upper() not in ['A', 'B']:
                print("\nEntrada inválida. Por favor, digite 'A' para Ativo ou 'B' para Bloqueado.\n")
                status_usuario = input("Digite o seu novo Status: ")
            user.status_usuario = status_usuario.upper()
            session.commit()
            print()
            linha(50)
            print("Atualização do Status efetuada com sucesso!!")
            linha(50)
            print()
            choice = input("Deseja retornar ao menu (M) ou sair (X)? ")
            if choice.lower() == 'n' or choice.lower() == 'x':
                sair_sistema()
                clear_terminal()
            elif choice.lower() == 'm':
                clear_terminal()
                menu_update_user(tipo_user)
        else:
            print("Erro: Status não encontrado.")

        # Feche a sessão quando terminar de usá-la
        session.close()


def alterar_tipo_user(tipo_user):
    if tipo_user != 'A':
        titulo_principal(6, "Tela de Atualização de Tipo de Usuário.")
        user_logado()
        print("Erro: Apenas usuários com tipo 'A' (administrador) podem utilizar esta função.")
        return

    while True:
        titulo_principal(6, "Tela de Atualização de Tipo de Usuário.")
        user_logado()

        id_user = input("Digite o ID do Usuário que deseja buscar: ")
        print()
        session = Session()

        # Verifique se a senha está correta
        user = session.query(Usuarios).filter(Usuarios.idusuario == id_user).first()
        if user:
            linha(50)
            print(f"Usuário: {user.login_usuario.upper()}")
            linha(50)
            print("\nLegenda: A-Administrador, U-Usuário\n")
            new_tipo = input("Digite o seu novo Tipo de Usuário: ")
            while new_tipo.upper() not in ['A', 'U']:
                print("\nEntrada inválida. Por favor, digite 'A' para Administrador ou 'U' para Usuário.\n")
                new_tipo = input("Digite o seu novo Tipo de Usuário: ")
            user.tipo = new_tipo.upper()
            session.commit()
            print()
            linha(50)
            print("Atualização do Tipo de Usuário efetuada com sucesso!!")
            linha(50)
            print()
            choice = input("Deseja retornar ao menu (M) ou sair (X)? ")
            if choice.lower() == 'n' or choice.lower() == 'x':
                sair_sistema()
                clear_terminal()
            elif choice.lower() == 'm':
                clear_terminal()
                menu_update_user(tipo_user)
        else:
            print("Erro: Status não encontrado.")

        # Feche a sessão quando terminar de usá-la
        session.close()


def alterar_email_user(tipo_user):
    while True:
        titulo_principal(8, "Tela de Atualização de E-mail.")
        user_logado()

        old_email_user = input("Digite o E-mail que deseja buscar: ")
        print()
        linha(50)
        print()
        session = Session()

        # Verifique se a senha está correta
        new_email_user = session.query(Usuarios).filter(Usuarios.email_usuario == old_email_user).first()
        if new_email_user:
            new_email_user.email_usuario = input("Digite o seu novo E-mail: ")
            session.commit()
            print()
            linha(50)
            print("Atualização do E-mail efetuada com sucesso!!")
            linha(50)
            print()
            choice = input("Deseja retornar ao menu (M) ou sair (X)? ")
            if choice.lower() == 'n' or choice.lower() == 'x':
                sair_sistema()
                clear_terminal()
            elif choice.lower() == 'm':
                clear_terminal()
                menu_update_user(tipo_user)
        else:
            print("Erro: E-mail não encontrado.")

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
                clear_terminal()
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
        user_logado()
        print("\nEscolha uma das opções abaixo:")
        print('''
        1 – Cadastro em Geral;\n
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
        user_logado()
        print("\nEscolha uma das opções abaixo:")
        print('''
        1 – Atualizar Dados do Usuário;\n
        2 – Atualizar Nome de Grupo;\n
        3 – Menu de Navegação;\n
        4 - Sair.''')
        opcao = int(input("\nDigite uma opção para interagir: "))
        match opcao:
            case 1:
                clear_terminal()
                menu_update_user(tipo_user)
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
        continuar = input("\nDeseja voltar para o menu Atualização de Dados? S/N: ")
        while continuar.casefold() not in ['s', 'n']:
            print("Entrada inválida. Por favor, digite 's' para continuar ou 'n' para sair.")
            continuar = input("\nDeseja voltar para o menu Atualização de Dados? S/N: ")


def menu_cadastro(tipo_user):
    """Função criada para ser menu"""
    continuar = "s"
    while continuar == 's' or continuar == 'S':
        titulo_principal(15, "Menu de Cadastro.")
        user_logado()
        print("\nEscolha uma das opções abaixo:")
        print('''
        1 – Cadastro de Usuários;\n
        2 – Cadastro de Grupos;\n
        3 – Cadastro de Documentos;\n
        4 – Adicionar o Usuário ao Grupo;\n
        5 – Associação de Grupo ao Documento;\n
        6 – Menu de Navegação;\n
        7 - Sair.''')
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
                cadastro_documento(tipo_user)
            case 4:
                clear_terminal()
                adicionar_usuario_grupo()
            case 5:
                clear_terminal()
                adicionar_grupo_documento()
            case 6:
                clear_terminal()
                menu_navegacao(tipo_user)
            case 7:
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
        user_logado()
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


def menu_update_user(tipo_user):
    cont = "s"
    while cont == 's' or cont == 'S':
        titulo_principal(7, "Menu de Atualização Dados Usuário.")
        user_logado()
        print("\nEscolha uma das opções abaixo:")
        # Alterar Status e Tipo de usuário somente o Administrador pode fazer.
        print('''
               1 – Atualização de E-mail Usuários;\n
               2 – Alterar Senha de Usuários;\n
               3 – Alterar Status de Usuários;\n
               4 – Alterar Tipo de Usuários;\n
               5 – Menu de Atualização de dados;\n
               6 - Sair.''')
        opcao = int(input("\nDigite uma opção para interagir: "))
        match opcao:
            case 1:
                clear_terminal()
                alterar_email_user(tipo_user)
            case 2:
                clear_terminal()
                alterar_senha_user(tipo_user)
            case 3:
                clear_terminal()
                alterar_status_user(tipo_user)
            case 4:
                clear_terminal()
                alterar_tipo_user(tipo_user)
            case 5:
                clear_terminal()
                menu_alterar(tipo_user)

            case 6:
                clear_terminal()
                titulo_principal(7, "Menu de Atualização Dados Usuário.")
                sair_sistema()
        cont = input("\nDeseja voltar para o menu Atualização Dados Usuário? S/N: ")
        while cont.casefold() not in ['s', 'n']:
            print("Entrada inválida. Por favor, digite 's' para continuar ou 'n' para sair.")
            cont = input("\nDeseja voltar para o menu Atualização Dados Usuário? S/N: ")

# FIM DE FUNÇÕES DE MENU

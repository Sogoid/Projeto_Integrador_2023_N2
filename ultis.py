from database import Session
from helpers import titulo_principal, linha
from models import Usuarios, Grupos, Documentos


def list_user():
    titulo_principal(15, "Listagem de Usuários.")
    print("""Legenda da tabela\nSTATUS: A-Ativo, B-Bloqueado\nTIPO: A-Administrador, U-Usuário.\n""")
    # Cria a lista com os títulos das colunas
    header = ["MATRICULA", "NOME USUÁRIO", "E-MAIL", "STATUS", "TIPO"]

    session = Session()

    # Check if the username and password are correct
    user = session.query(Usuarios).all()
    dados = [[user.idusuario, user.login_usuario, user.email_usuario, user.status_usuario, user.tipo]
             for user in user]
    # Fechar a sessão quando terminar de usá-la
    session.close()
    table_report(header, dados)


def search_user():
    titulo_principal(15, "Pesquisa de Usuários.")

    # Cria a lista com os títulos das colunas
    header = ["MATRICULA", "NOME USUÁRIO", "E-MAIL", "STATUS", "TIPO"]

    # Pede ao usuário para digitar o nome do usuário que deseja buscar
    login_user = input("Digite o nome do usuário que deseja buscar: ")
    print()
    linha(50)
    print()
    print("""Legenda da tabela\nSTATUS: A-Ativo, B-Bloqueado\nTIPO: A-Administrador, U-Usuário.\n""")
    session = Session()

    # Busca informações sobre o usuário especificado
    user = session.query(Usuarios).filter(Usuarios.login_usuario == login_user).first()
    if user:
        dados = [[user.idusuario, user.login_usuario, user.email_usuario, user.status_usuario, user.tipo]]
        table_report(header, dados)
    else:
        print("Usuário não encontrado.")

    # Fechar a sessão quando terminar de usá-la
    session.close()


def list_user_deleted():
    titulo_principal(10, "Listagem de Usuários Excluídos.")
    print("""Legenda da tabela\nSTATUS: A-Ativo, B-Bloqueado\nTIPO: A-Administrador, U-Usuário.\n""")
    # Cria a lista com os títulos das colunas
    header = ["MATRICULA", "NOME USUÁRIO", "E-MAIL", "STATUS", "TIPO", "DELETADO"]

    session = Session()

    # Consulta a tabela 'Usuarios' para obter todos os usuários excluídos
    users = session.query(Usuarios).filter(Usuarios.deleted == True).all()

    # Prepara os dados para exibir na tabela
    dados = [[user.idusuario, user.login_usuario, user.email_usuario, user.status_usuario, user.tipo, user.deleted]
             for user in users]

    # Exibe a tabela com os usuários excluídos
    table_report(header, dados)

    # Fecha a sessão quando terminar de usá-la
    session.close()


def list_group():
    titulo_principal(15, "Listagem de Grupos.")
    # Cria a lista com os títulos das colunas
    header = ["MATRICULA", "DESCRIÇÃO DO GRUPO"]

    session = Session()

    # Check if the username and password are correct
    grupo = session.query(Grupos).all()
    dados = [[grupo.idgrupos, grupo.descricao]
             for grupo in grupo]
    # Fechar a sessão quando terminar de usá-la
    session.close()
    table_report(header, dados)


def search_group():
    titulo_principal(15, "Pesquisa de Grupo.")

    # Cria a lista com os títulos das colunas
    header = ["ID", "DESCRIÇÃO DO GRUPO"]

    # Pede ao usuário para digitar o nome do grupo que deseja buscar
    description = input("Digite o nome do grupo que deseja buscar: ")
    print()
    linha(50)
    print()

    session = Session()

    # Busca informações sobre o usuário especificado
    grupo = session.query(Grupos).filter(Grupos.descricao == description).first()
    if grupo:
        dados = [[grupo.idgrupos, grupo.descricao]]
        table_report(header, dados)
    else:
        print("Grupo não encontrado.")

    # Fechar a sessão quando terminar de usá-la
    session.close()


def list_document():
    titulo_principal(15, "Listagem de Documentos.")
    # Cria a lista com os títulos das colunas
    header = ["ID", "NOME DOCUMENTO", "LOCAL DE SALVAMENTO"]

    session = Session()

    # Check if the username and password are correct
    document = session.query(Documentos).all()
    dados = [[document.iddocumento, document.nome_documento, document.endereco_documento]
             for document in document]
    # Fechar a sessão quando terminar de usá-la
    session.close()
    table_report(header, dados)


def table_report(header, dados):
    # Verifica se a lista dados está vazia
    if len(dados) == 0:
        print("A lista dados está vazia")
        return

    # Verifica se todas as linhas têm o mesmo número de colunas que a lista cabeçalho
    for line in dados:
        if len(line) != len(header):
            # Adiciona elementos vazios à linha
            line.extend([""] * (len(header) - len(line)))

    # Calcula a largura máxima de cada coluna
    largura_colunas = [max(len(str(dado)) for dado in coluna) for coluna in zip(header, *dados)]

    # Imprime o cabeçalho da tabela
    for i, titulo in enumerate(header):
        print(f"{titulo:{largura_colunas[i]}}", end=" | ")
    print()

    # Imprime uma linha separadora
    for largura in largura_colunas:
        print("-" * largura, end="-+-")
    print()

    # Verifica se a lista largura_colunas tem o mesmo comprimento que a lista cabeçalho
    if len(largura_colunas) != len(header):
        print(
            f"Erro: A lista largura_colunas tem comprimento {len(largura_colunas)}, "
            f"mas deveria ter o mesmo comprimento que a lista cabeçalho ({len(header)})")

    else:
        # Imprime os dados da tabela
        for line in dados:
            for dado, largura in zip(line, largura_colunas):
                print(f"{dado:{largura}}", end=" | ")
            print()


# Extensão de arquivos permitidos para salvar
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

from database import Session
from helpers import titulo_principal, linha
from models import Usuarios, Grupos


def listagem_usuario():
    titulo_principal(15, "Listagem de Usuários.")
    print("""Legenda da tabela\nSTATUS: A-Ativo, B-Bloqueado\nTIPO: A-Administrador, U-Usuário.\n""")
    # Cria a lista com os títulos das colunas
    cabecalho = ["MATRICULA", "NOME USUÁRIO", "E-MAIL", "STATUS", "TIPO"]

    session = Session()

    # Check if the username and password are correct
    user = session.query(Usuarios).all()
    dados = [[user.idusuario, user.login_usuario, user.email_usuario, user.status_usuario, user.tipo]
             for user in user]
    # Fechar a sessão quando terminar de usá-la
    session.close()
    tabela_relatorio(cabecalho, dados)


def pesquisa_usuario():
    titulo_principal(15, "Pesquisa de Usuários.")

    # Cria a lista com os títulos das colunas
    cabecalho = ["MATRICULA", "NOME USUÁRIO", "E-MAIL", "STATUS", "TIPO"]

    # Pede ao usuário para digitar o nome do usuário que deseja buscar
    login_usuario = input("Digite o nome do usuário que deseja buscar: ")
    print()
    linha(50)
    print()
    print("""Legenda da tabela\nSTATUS: A-Ativo, B-Bloqueado\nTIPO: A-Administrador, U-Usuário.\n""")
    session = Session()

    # Busca informações sobre o usuário especificado
    user = session.query(Usuarios).filter(Usuarios.login_usuario == login_usuario).first()
    if user:
        dados = [[user.idusuario, user.login_usuario, user.email_usuario, user.status_usuario, user.tipo]]
        tabela_relatorio(cabecalho, dados)
    else:
        print("Usuário não encontrado.")

    # Fechar a sessão quando terminar de usá-la
    session.close()


def listagem_grupo():
    titulo_principal(15, "Listagem de Grupos.")
    # Cria a lista com os títulos das colunas
    cabecalho = ["MATRICULA", "DESCRIÇÃO DO GRUPO"]

    session = Session()

    # Check if the username and password are correct
    grupo = session.query(Grupos).all()
    dados = [[grupo.idgrupos, grupo.descricao]
             for grupo in grupo]
    # Fechar a sessão quando terminar de usá-la
    session.close()
    tabela_relatorio(cabecalho, dados)


def pesquisa_grupo():
    titulo_principal(15, "Pesquisa de Grupo.")

    # Cria a lista com os títulos das colunas
    cabecalho = ["MATRICULA", "DESCRIÇÃO DO GRUPO"]

    # Pede ao usuário para digitar o nome do grupo que deseja buscar
    descricao = input("Digite o nome do grupo que deseja buscar: ")
    print()
    linha(50)
    print()

    session = Session()

    # Busca informações sobre o usuário especificado
    grupo = session.query(Grupos).filter(Grupos.descricao == descricao).first()
    if grupo:
        dados = [[grupo.idgrupos, grupo.descricao]]
        tabela_relatorio(cabecalho, dados)
    else:
        print("Grupo não encontrado.")

    # Fechar a sessão quando terminar de usá-la
    session.close()


def tabela_relatorio(cabecalho, dados):
    # Verifica se a lista dados está vazia
    if len(dados) == 0:
        print("A lista dados está vazia")
        return

    # Verifica se todas as linhas têm o mesmo número de colunas que a lista cabeçalho
    for linha in dados:
        if len(linha) != len(cabecalho):
            # Adiciona elementos vazios à linha
            linha.extend([""] * (len(cabecalho) - len(linha)))

    # Calcula a largura máxima de cada coluna
    largura_colunas = [max(len(str(dado)) for dado in coluna) for coluna in zip(cabecalho, *dados)]

    # Imprime o cabeçalho da tabela
    for i, titulo in enumerate(cabecalho):
        print(f"{titulo:{largura_colunas[i]}}", end=" | ")
    print()

    # Imprime uma linha separadora
    for largura in largura_colunas:
        print("-" * largura, end="-+-")
    print()

    # Verifica se a lista largura_colunas tem o mesmo comprimento que a lista cabeçalho
    if len(largura_colunas) != len(cabecalho):
        print(
            f"Erro: A lista largura_colunas tem comprimento {len(largura_colunas)}, "
            f"mas deveria ter o mesmo comprimento que a lista cabeçalho ({len(cabecalho)})")

    else:
        # Imprime os dados da tabela
        for linha in dados:
            for dado, largura in zip(linha, largura_colunas):
                print(f"{dado:{largura}}", end=" | ")
            print()

import getpass
import os
import platform
import sys
import time


def logo():
    print("""
    
░█████╗░███╗░░██╗███████╗░██████╗░███████╗██████╗░
██╔══██╗████╗░██║██╔════╝██╔════╝░██╔════╝██╔══██╗
██║░░██║██╔██╗██║█████╗░░██║░░██╗░█████╗░░██║░░██║
██║░░██║██║╚████║██╔══╝░░██║░░╚██╗██╔══╝░░██║░░██║
╚█████╔╝██║░╚███║███████╗╚██████╔╝███████╗██████╔╝
░╚════╝░╚═╝░░╚══╝╚══════╝░╚═════╝░╚══════╝╚═════╝░
    """)


def titulo_principal(num, tmsg):
    logo()
    linha(50)
    print(f'{"":{num}}{tmsg}')
    linha(50)
    print()


def clear_terminal():
    """Função para verificar o sistema operacional e limpar o terminal
    Obs.: Esta função não funciona no terminal do pycharm somente no terminal do
    integrado.
    """
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        print("\033[H\033[J")


def getch():
    if platform.system() == 'Windows':
        import msvcrt
        return msvcrt.getch().decode()
    else:
        import termios
        import tty

        # Save terminal attributes
        old_settings = termios.tcgetattr(sys.stdin)

        try:
            # Set terminal to raw mode
            tty.setraw(sys.stdin.fileno())

            # Read a character from the keyboard
            ch = sys.stdin.read(1)
        finally:
            # Restore terminal attributes
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

        return ch


def cadastro_password():
    """Função para cadastrar senha!
    Obs: No Pycharm a função getpass da o seguinte erro:
    GetPassWarning: Can not control echo on the terminal.
    passwd = fallback_getpass(prompt, stream)
    Warning: Password input may be echoed.
    Executar o arquivo fora do Pycharm ele roda normal sem erro."""
    while True:
        senhas = getpass.getpass("Digite o Password: ")
        rep_senhas = getpass.getpass("Digite novamente : ")

        if senhas == rep_senhas:
            print(
                "\nSenha cadastrada com sucesso!\n"
                "Cadastro realizado com Sucesso!!\n"
            )
            return senhas
        print("\nSenhas diferentes. Tente novamente.\n")


def tempo_sleep(total):
    """Este código define uma função chamada tempo_sleep que recebe um
    argumento total. A função cria uma barra de progresso simples, atualizada
    a cada iteração do loop for.
    Dentro do loop for, a função faz o seguinte:
    Faz uma pausa de 0,1 segundo usando a função sleep do módulo time.
    Move o cursor para o início da linha atual usando o caractere de escape \r.
    Usa uma f-string para formatar a barra de progresso e a porcentagem de
    conclusão. A barra de progresso é criada repetindo o caractere = um número
    de vezes proporcional à porcentagem de conclusão. A porcentagem de
    conclusão é calculada dividindo o índice atual do loop pelo valor total e
    multiplicando por 100.
    Usa a função flush do objeto sys.stdout para forçar a atualização da saída.
    Depois que o loop for é concluído, a função move o cursor para o início da
    linha atual novamente e exibe a barra de progresso completa (100%) usando
    outra f-string. Por fim, a função chama a função print para mover o cursor
    para a próxima linha.
    Quando você chama a função progress_bar com um argumento numérico, ela
    exibe uma barra de progresso que é atualizada ao longo do tempo até
    atingir 100%. 😊"""

    for i in range(total):
        time.sleep(0.1)
        sys.stdout.write('\r')
        sys.stdout.write(' ' * 12 + f"[{'=' * int(20 * i / total):<20}]"
                                    f"{int(100 * i / total)}%")
        sys.stdout.flush()
    sys.stdout.write('\r')
    sys.stdout.write(' ' * 12 + f"[{'=' * 20:<20}] 100%")
    sys.stdout.flush()
    print()


def len_titulo(titulo):
    """A função len_titulo recebe um argumento titulo, sendo uma string
    representando uma mensagem de título. A função simplesmente retorna
    o comprimento da string titulo usando a função embutida len.
    Isso significa que, quando a função linha_titulo chama a função
    len_titulo e armazena o valor retornado na variável __nun_letras__,
    ela está armazenando o comprimento da string titulo. Portanto, a função
    linha_titulo imprime uma linha de asteriscos com o mesmo comprimento
    que a string titulo."""
    return len(titulo)


def linha_titulo(titulo):
    """A função linha_titulo recebe um argumento titulo, sendo uma
    string representando uma mensagem de título. A função começa chamando
    outra função chamada len_titulo e passando titulo como argumento.
    O valor retornado por len_titulo é armazenado na variável __nun_letras__.
    Em seguida, a função imprime um caractere "*" repetido __nun_letras__
    vezes.
    Isso cria uma linha de asteriscos com o mesmo comprimento que o valor
    retornado por len_titulo."""
    __nun_letras__ = len_titulo(titulo)
    print("*" * __nun_letras__)


def titulo_sistema(tmsg):
    """A função titulo_sistema recebe um argumento tmsg,
    sendo uma string representando uma mensagem de título.
    A função chama outra função chamada linha_titulo e passa
    tmsg como argumento. Em seguida, a função imprime a mensagem
    de título tmsg com uma quebra de linha antes e depois. Por fim,
    a função chama novamente a função linha_titulo com tmsg como argumento.
    Assim função serve para mostrar o título através da função."""
    linha_titulo(tmsg)
    print(f"\n{tmsg}\n")
    linha_titulo(tmsg)


def linha(numlinha):
    """A função linha cria uma linha de asteriscos com o mesmo comprimento que o valor
    retornado por numlinha."""
    print("*" * numlinha)


def sair_sistema():
    """Função para sair do sistema."""
    global logged_in_user_id
    logged_in_user_id = None
    print("\nSaindo do sistema...")
    tempo_sleep(50)
    clear_terminal()
    exit()

import mysql.connector
from mysql.connector import errorcode
from werkzeug.security import generate_password_hash

print("Conectando...")


def connect_to_database():
    try:
        db_ipog = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="root"
        )
        return db_ipog.cursor(), db_ipog
    except mysql.connector.Error as erro:
        if erro.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Existe algo errado no nome de usuário ou senha')
        else:
            print(erro)
        return None


cursor_ipog, ipog = connect_to_database()
if cursor_ipog is None:
    print("Não foi possível conectar ao banco de dados")
else:
    cursor_ipog.execute("DROP DATABASE IF EXISTS `ProjetoPI`;")
    cursor_ipog.execute("CREATE DATABASE `ProjetoPI`;")
    cursor_ipog.execute("USE `ProjetoPI`;")

# criando tabelas
TABLES = {'Usuarios': ('''
                         CREATE TABLE `usuarios` (
                         `idusuario` INT NOT NULL AUTO_INCREMENT,
                         `login_usuario` VARCHAR(255) NOT NULL ,
                         `email_usuario` VARCHAR(255) NOT NULL,
                         `senha_usuario` VARCHAR(255) NOT NULL,
                         `status_usuario` VARCHAR(1) NOT NULL,
                         `tipo` VARCHAR(1) NOT NULL, 
                         PRIMARY KEY (`idusuario`)
                         ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;'''), 'Grupos': ('''
                         CREATE TABLE `grupos` (
                         `idgrupos` INT NOT NULL AUTO_INCREMENT,
                         `descricao` VARCHAR(255) NOT NULL UNIQUE ,
                         PRIMARY KEY (`idgrupos`)
                         ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;'''), 'Documentos': ('''
                         CREATE TABLE `documentos` (
                         `iddocumento` INT NOT NULL AUTO_INCREMENT,
                         `nome_documento` VARCHAR(255) NOT NULL,
                         `endereco_documento` VARCHAR(255) NOT NULL,
                         `idusuario` INT NOT NULL, 
                         PRIMARY KEY (`iddocumento`)
                         )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;'''), 'Pertence': ('''
                         CREATE TABLE `pertence` (
                         `idusuario` INT NOT NULL, 
                         `idgrupos` INT NOT NULL,
                          PRIMARY KEY (`idusuario`,`idgrupos`),
                          FOREIGN KEY (`idusuario`) REFERENCES usuarios (`idusuario`)
                          ON UPDATE CASCADE
                          ON DELETE RESTRICT,
                          FOREIGN KEY (`idgrupos`) REFERENCES grupos (`idgrupos`)
                          ON UPDATE CASCADE
                          ON DELETE RESTRICT                          
                          ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;'''), 'Contem': ('''
                           CREATE TABLE `contem` (
                           `idgrupos` INT NOT NULL,
                           `iddocumento` INT NOT NULL,
                           PRIMARY KEY (idgrupos, iddocumento),
                           FOREIGN KEY (idgrupos) REFERENCES grupos(idgrupos)
                           ON UPDATE  CASCADE
                           ON DELETE  RESTRICT,
                           FOREIGN KEY (iddocumento) REFERENCES documentos(iddocumento)
                           ON UPDATE CASCADE
                           ON DELETE RESTRICT)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;'''),
          'Cadastra': ('''
                           CREATE TABLE `cadastra` (
                           `idusuario` INT NOT NULL,
                            `iddocumento` INT NOT NULL,
                            PRIMARY KEY (idusuario, iddocumento),
                            FOREIGN KEY (idusuario) REFERENCES usuarios(idusuario)
                            ON UPDATE CASCADE
                            ON DELETE RESTRICT,
                            FOREIGN KEY (iddocumento) REFERENCES documentos(iddocumento)
                            ON UPDATE CASCADE
                            ON DELETE RESTRICT
                           )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')}

for tabela_nome in TABLES:
    tabela_sql = TABLES[tabela_nome]
    try:
        print('Criando tabela {}:'.format(tabela_nome), end=' ')
        cursor_ipog.execute(tabela_sql)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print('Já existe')
        else:
            print(err.msg)
    else:
        print('OK')

# inserindo usuarios
usuario_sql = 'INSERT INTO usuarios (login_usuario, email_usuario, \
            senha_usuario, status_usuario, tipo) VALUES (%s, %s, %s, %s, %s)'
usuarios = ("Administrador", "admin", generate_password_hash("py2356", method='scrypt'), "A", "A"),

cursor_ipog.executemany(usuario_sql, usuarios)

cursor_ipog.execute('select * from ProjetoPI.usuarios')
print(' -------------  Usuários:  -------------')
for user in cursor_ipog.fetchall():
    print(user[1])

# commitando se não nada tem efeito
ipog.commit()

cursor_ipog.close()
ipog.close()

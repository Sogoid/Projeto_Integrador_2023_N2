from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Usuarios(Base):
    __tablename__ = 'usuarios'

    idusuario = Column(Integer, primary_key=True, autoincrement=True)
    login_usuario = Column(String(50), nullable=False)
    email_usuario = Column(String(8), nullable=False)
    senha_usuario = Column(String(20), nullable=False)
    status_usuario = Column(String(2), nullable=False)
    tipo = Column(String(2), nullable=False)

    def __repr__(self):
        return '<Name%r>' % self.login_usuario


class Contem(Base):
    __tablename__ = 'contem'
    idgrupos = Column(Integer, ForeignKey('grupos.idgrupos'), primary_key=True)
    iddocumento = Column(Integer, ForeignKey('documentos.iddocumento'), primary_key=True)


class Grupos(Base):
    __tablename__ = 'grupos'

    idgrupos = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(50), nullable=False)
    documentos = relationship('Documentos', secondary='contem', back_populates='grupos')

    def __repr__(self):
        return '<Name%r>' % self.descricao


class Documentos(Base):
    __tablename__ = 'documentos'

    iddocumento = Column(Integer, primary_key=True)
    nome_documento = Column(String(255), nullable=False)
    endereco_documento = Column(String(255), nullable=False)
    grupos = relationship('Grupos', secondary='contem', back_populates='documentos')

    def __repr__(self):
        return '<Name%r>' % self.nome_documento


class Pertence(Base):
    __tablename__ = 'pertence'
    idusuario = Column(Integer, ForeignKey('usuarios.idusuario'), primary_key=True)
    idgrupos = Column(Integer, ForeignKey('grupos.idgrupos'), primary_key=True)
    usuario = relationship('Usuarios', back_populates='grupos')
    grupo = relationship('Grupos', back_populates='usuarios')


Usuarios.grupos = relationship('Pertence', back_populates='usuario')
Grupos.usuarios = relationship('Pertence', back_populates='grupo')

from database import Base, Column, Integer, String


class Usuarios(Base):
    __tablename__ = 'usuarios'

    idusuario = Column(Integer, primary_key=True, autoincrement=True)
    login_usuario = Column(String(50), nullable=False)
    email_usuario = Column(String(8), nullable=False)
    senha_usuario = Column(String(20), nullable=False)
    status_usuario = Column(String(2), nullable=False)
    tipo = Column(String(2), nullable=False)

    def __repr__(self):
        return '<Name%r>' % self.nome

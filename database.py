import os

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Substitua os valores apropriados para o seu banco de dados
SQLALCHEMY_DATABASE_URI = '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
    SGBD='mysql+mysqlconnector',
    usuario='root',
    senha="root",
    servidor='127.0.0.1',
    database='ProjetoPI'
)

engine = create_engine(SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)
Base = declarative_base()


UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/static/uploads'



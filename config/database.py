import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# directorio donde se encuentra el archivo (config/database.py)
sqlite_file_name = "../database.sqlite"
base_dir = os.path.dirname(os.path.realpath(__file__))

#forma de conectarse a una base de datos
database_url = f"sqlite:///{os.path.join(base_dir, sqlite_file_name)}"

# echo = True, muestra en consola las consultas que se hacen a la base de datos
engine = create_engine(database_url, echo=True)

# crea una sesion para hacer consultas a la base de datos
Session = sessionmaker(bind=engine)

# Sirve para manipular las tablas de la base de datos
Base = declarative_base()
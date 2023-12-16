import os
from sqlalchemy import create_engine #create_engine : con esto creamos la conexion con la base de datos
from sqlalchemy.orm.session import sessionmaker #Esto es para crear secciones???
from sqlalchemy.ext.declarative import declarative_base #Nos ayuda a comunicarnos

#Nota: Este archivo es para configurar la base de datos.

#Vamos a darle un nombre a nuestra base de datos :
db_file_name = "database.sqlite"

#Vamos a crear la ruta del archivo de la base de datos:

#1. Preguntamos en donde está nuestro archivo database:
base_dir = os.path.dirname(os.path.realpath(__file__))

# Esto es para decirle en donde la queremos crear
path_file_database = os.path.join(
    base_dir, #
    "..", #Esto es para devolvernos, como en cmd cuando queremos salir de una carpeta
    db_file_name
)

#Creamos la url:
data_base_url = f"sqlite:///{path_file_database}"
#Creamos el motor : El motor sirve para ejecutar todas las funciones de sql (añadir, modificar, eliminar)
engine = create_engine(data_base_url, echo=True) 
#Creamos la session:
session = sessionmaker(bind=engine) #bin=engine es para decirle cual es el motor
#Creamos la base:
Base = declarative_base()
from config.database import Base
#from sqlalchemy import Column, Integer, string
from sqlalchemy import Column, Integer, String

#LA CARPETA MODELS CONTIENE EL ARCHIVO PARA CREAR COMO TAL LA BASE DE DATOS CON LOS REQUERIMIENTOS DEL PROYECTO

#Nota : Las bases de datos guardan unicamente texto/URL de donde se almacenan las cosas. SI YO QUISIERA CREAR UNA APLICACION DE DESCARGAR MUSICA ME TOCARIA CREAR UN DIRECTORIO DONDE GUARDAR LA MUSICA Y EN LA BASE DE DATOS LO QUE VA A HACER ES GUARDAR LA UBICACION DE ARCHIVO


#1. Con esto vamos a crear la tabla, si hacemos el simil con excel, esta class Movie seria una tabla. 
class Password_custom(Base):
    __tablename__ = "passwords_customs"

    id = Column(Integer, primary_key=True, index=True)
    length = Column(Integer)
    capital_letter = Column(Integer)
    numbers = Column(Integer)
    simbols = Column(Integer)

#2. 
class Password(Base):
    __tablename__ = "passwords" #Si hacemos el simil con excel, esto seria el nombre de la hoja.

    #2. Vamos a definir nuestras columnas:

    # a) Column(Integer, primary_key=True, index=True) -> Con esto decimos que la columna va a contener numeros enteros, irrepetibles, el index es pa que lo tenga como un indice por si lo queremos consultar.
    id = Column(Integer, primary_key=True, index=True) 

    # b) Column(String) -> La columna passwords va a almacenar elementos de tipo string
    password = Column(String)
    

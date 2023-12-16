Nombre: Jhonatan Orlando Garcia Aguilar
Codigo: 1.077.997.902


Saberes previos:

- El archivo llamado __init__.py,  sirve para indicar que ese directorio debe considerarse un paquete de Python, un paquete no es mas que una forma de organizar y estructurar código en módulos relacionados.


Explicacion de la base de datos: Para montar la base de datos tuve que seguir los siguientes pasos.

1. Crear la carpeta config: Este directorio contiene el archivo (database.py) que tiene las configuraciones de la base de datos.         

    1.1 Librerias: 

        - import os : Utilizo este modulo para manipular la ruta del archivo donde se almacena la bases de datos SQLite.
        - from sqlalchemy : SQLAlchemy es una libreria de Python que me permite trabajar con bases de datos relacionales.
            - import create_engine : Se utiliza para establecer la conexión y la comunicación entre la API y la base de datos. Gracias a esta funcion puedo hacer modificaciones en la DB.
        - from sqlalchemy.orm.session import sessionmaker : Sirve para crear session() dentro de mi API.
        - from sqlalchemy.ext.declarative import declarative_base : Sirve para la base de datos, donde crearemos las tablas.

    1.2 Codigo :

        - db_file_name = "database.sqlite" : Con esto le estoy dando un nombre a nuestra base de datos al archivo de nuestra base de datos.
        - base_dir = os.path.dirname(os.path.realpath(__file__)) : Aqui estoy guardando en <base_dir> la direccion (URL) del archivo <database.py>
        - path_file_database = os.path.join(base_dir, 
                                        "..", #Esto es para devolvernos, como en cmd cuando queremos salir de una carpeta
                                        db_file_name) 
          Basicamente os.path.join() recibe tres parametros, 1. la ubicacion actual, 2. navegador de carpetas (".."), 3. El nombre del archivo que contiene la base de datos. Todo esto nos sirve para decirle a Python en donde queremos crear nuestra Base de datos.
        - data_base_url = f"sqlite:///{path_file_database}" : Sirve para crear la URL
        - engine = create_engine(data_base_url, echo=True) : Creamos el motor, el motor sirve para ejecutar todas las funciones de sql (añadir, modificar, eliminar)
        - session = sessionmaker(bind=engine) : Creamos la session(), bind=engine es para decirle cual es el motor que usamos.
        - Base = declarative_base() : Sirve para crear la clase base para definir modelos de tablas. 
     
2. Creamos la carpeta models : Aqui basicamente va el modelo de las tablas de nuestra DB.

    2.1 Librerias:
        - from config.database import Base 
        - from sqlalchemy import Column, Integer, String : Column(columnas), Integer(Numeros enteros), String(Texto)
    
    2.2 Codigo:
        - Las clases que creo en este archivo, son basicamente las tablas con los mismos campos que deben llenar los usuarios para crear las contraseñas aleatorias.
    

3. Dentro del main.py : Aqui dare breves explicaciones de los cambios que hubo debido a la DB.

    3.1 Librerias :
        - from config.database import session, engine, Base 
        - from models.psword import Password_custom as psw_custom : Importamos la hoja 1 donde está la tabla Password_custom
        - from models.psword import Password as Pssw : Importamos la hoja 2 donde está la tabla Password
        - from fastapi.encoders import jsonable_encoder : Sirve para convertir un objeto en una lista de directorios.
    
    3.2 Codigo:
        - Base.metadata.create_all(bind=engine) : Creamos la base de datos en el proyecto.
        - db = session() : Sirve para crear una session para hacer busqueda y/o modificaciones.
        - result = db.query(Pssw).all() : En base a la session que hemos creado vamos hacer una consulta (query) en la tabla Pssw que se encuentra en la hoja 2, .all() es para que traiga todos los elementos en la tabla.
        - result = db.query(Pssw).filter(len(Pssw.password) == length).all() : Aqui estamos haciendo una consulta pero con un filtro(condicion), es muy eficaz a la hora de buscar elementos.
        - new_custom = psw_custom(**data.model_dump()) : Aqui estoy creando una nuevo dato en la DB
        - db.add(new_custom) : Con esto lo termino por añadir
        - db.commit() : Sirve para decirle que guarde los cambios.
        - db.delete(result) : Sirve para borrar un dato de la DB.
        - jsonable_encoder(result) : Es necesario porque en <result> está almacenando objetos dificiles de leer.

        Nota 1: Cada vez que haga un commit, debo iniciar otra session para hacer consultas y/o cambios.
        Nota 2: Yo puedo hacer varias consultas en una misma session, pero si llego a modificar algo, debo hacer el commit de una vez.

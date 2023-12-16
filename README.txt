Nombre: Jhonatan Orlando Garcia Aguilar
Código: 1.077.997.902

Proyecto de Gestión de Contraseñas 

    Crear una API para gestionar un sistema de almacenamiento de contraseñas. La API  permitir al usuario añadir nuevas 
    contraseñas (la contraseña debe ser generada aleatoriamente) , visualizar las contraseñas  guardadas, actualizar detalles de contraseñas existentes y 
    eliminar contraseñas.

    CRUD : create, read, update, delete

Requisitos Técnicos

    Utilizar FastAPI para la construcción de la API.
    Integrar una base de datos para el almacenamiento y gestión de datos se recomienda SQLite.
    Implementar autenticación y autorización seguras.
    Garantizar que la API tenga documentación adecuada.
    Escribir código claro y bien organizado con comentarios cuando sea necesario.


Saberes previos: 

- status_code : Este es un código numérico que indica el resultado de la solicitud HTTP. Algunos ejemplos comunes son:

    200 OK: La solicitud fue exitosa.
    201 Created: Se ha creado un nuevo recurso.
    400 Bad Request: La solicitud no fue válida.
    404 Not Found: El recurso solicitado no se encuentra.
    500 Internal Server Error: Hubo un error en el servidor.


- filter(funcion, estructura de datos) : Es como un bucle <for> que recibe dos parametros, una funcion y una estructura de datos (lista, tupla, 
diccionario) que podamos recorrer.
        a. lambda parametro: expresion/condicion : Cuando no tenemos una funcion y solo tenemos una condicion para recorrer la estructura de datos, 
        podemos usar lambda para hacerle creer a python que la condicion es una "funcion". IMAGINA QUE ESTAS CREANDO UNA FUNCION, NECESITAS UNOS PARAMETROS 
        Y UNA EXPRESION, ESO MISMO PASA CON LAMBDA, LA DIFERENCIA ES QUE TODO VA EN UNA LINEA.
            
Ejemplos con filter:
# Con una funcion
def es_par(num):
    return num % 2 == 0

numeros = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
pares = filter(es_par, numeros)

# Con lambda
numeros = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
pares = filter(lambda num: num % 2 == 0, numeros) -> Es parecido a un for porque asi seria con uno: for num in numeros





Documentación:

1. Importacion de librerias

    - from fastapi 
        a. import FastAPI  
            app = FastAPI() -> Aqui crearia la API
        b. Path : Se puede usar para definir y validar parámetros de la ruta (un parametro de ruta es aquel que aparece en la URL o link). 
            Puede recibir como parametros: ge y le, min_lenght y max_lenght, etc.
        

    - from fastapi.responses:
        a. import HTMLResponse : Genera una respuesta de tipo HTML, la utilizo para ponerle un titulo a la pagina. Es util porque ayuda a que la documentación automatica sea mas clara.
        b. JSONResponse : Es util para hacer retornos de tipo JSON. Estructura : JSONResponse(status_code=, content=). Un JSON no es mas que un diccionario.
            content : Este es el cuerpo de la respuesta que contiene los datos solicitados.

    - from pydantic 
        a. import BaseModel : Tiene funciones interesantes para validar datos. La heredo a mi class (clase Base).
        b. import Field : Me permite elegir cuales son los campos obligatorios. Estructura: Field(default="", min_lenght (or ge= ) =, max_lenght (le= ) =)
            default : Es el valor predeterminado que tendrá el campo.
            min_lenght y max_lenght : Se utiliza unicamente en el tipo de dato <STR>, sirve para determinar la longitud minima y maxima del texto.
            ge y le : Se utiliza unicamente en tipos de dato númerico, sirve para determinar el rango numerico que podemos elegir. ge<=x<=le -> Estructura matematica.

    - from typing 
        a. import Optional : Me permite elegir cuales campos son opcionales. Estructura: Opcional[tipo_dato] = Valor_predeterminado
        b. List : Lo utilizo para indicar que la funcion debe retornar una lista de objetos de tipo Movie. Estructura: -> List[class]

    - from random 
        a. import randint : Esta funcion me permite generar un número aleatoriamente dentro de un rango predeterminado. Estructura: randint(a, b) -> [a, b]
        b. shuffle : Esta funcion sirve para barajar/revolver los elementos de una lista. Estructura: shuffle(lista)
    
    - from math 
        a. import ceil : La funcion ceil me permite redondear para arriba los numeros flotantes. si tengo 2.5 me lo sube a 3. cosa que round no hace.

    

2. Plantilla Base : Esta plantilla contiene las caracteristicas que se pueden customizar de la contraseña.

Tener en cuenta: Los valores solo pueden ser 0 o 1, debido a que quise hacer el simil del False (0) y True (1). No lo hise con los booleanos porque me generaron muchos conflictos. Voy a mejorar el programa en futuras versiones. 

id : Este atributo/campo representa el identificador de la contraseña, lo voy a usar como uno de los metodos de busqueda.
length : Este atributo/campo representa la longitud de la contraseña, por default tiene un valor de 8.
capital_letter : Este atributo/campo representa las letras mayusculas, si el usuario digita 0 quiere decir que no quiere letras mayusculas, caso contrario si digita 1.
numbers : Este atributo/campo representa los numeros, si el usuario digita 0 quiere decir que no quiere números en la contraseña, caso contrario si digita 1.
simbols : Este atributo/campo representa los simbolos, si el usuario digita 0 quiere decir que no quiere simbolos en la contraseña, caso contrario si digita 1.

******CORREGIR***** password : Este atributo/campo representa la contraseña generada aleatoriamente. Si consigo que el usuario ignore este campo por completo sigo haciendo las cosas tal cual, pero sino, me toca crear otra clase donde guarde unicamente el id y la constraseña generada.


Nota: Estoy obviando las letras minusculas porque quiero cumplir con los estandares de contraseñas seguras. Quizas me contradiga poniendo libertad con las mayusculas pero quiero hacerlo mas interactivo.



3. Peticiones tipo Get: @app.get()

    3.1 Mostrar todas las contraseñas: 
        a. Ruta:
            - Primero, creo el endpoint : "/passwords"
            - Segundo, creo la etiqueta/sección de la funcionalidad get : "Get Passwords"
            - Tercero, aplico la buena practica de response_model, porque esto hace la documentación mas legible debido a que los desarrolladores sabrán que tipo de respuesta tiene la ruta : List[Password] -> Una lista que contiene objetos de tipo Password.
            - Cuarto, se espera que la ruta tenga una respuesta <ok>, por ello el status_code es 200.
        b. get_passwords() :
            - La funcion retornar un JSON (es un formato de texto estructurado y legible)
            - El JSON contiene el diccionario donde estan todas las contraseñas
            - El status_code es 200, porque se espera que la respuesta sea <<ok>>
    

    3.2 Mostrar todas las contraseñas dada su longitud:
        a. Ruta:
            - Primero, creo el endpoint : "/passwords/length/{length}"
            - Segundo, Lo guardo en la etiqueta/sección : "Get Passwords"
            - Tercero, aplico la buena practica de response_model=List[Password] -> Una lista que contiene objetos de tipo Password.
            - Cuarto, se espera que la ruta tenga una respuesta <ok>, por ello el status_code es 200.
        b.  get_passwords_length() :
            - Pregunta para el profesor sobre el retorno ->List[Password] y el return JSONResponse 
            - Dentro de la función defino una variable <password> de tipo lista, en esa variable voy a guardar las contraseñas con la longitud ingresada por el usuario.
            - filter(lambda i: len(i['password']) == length, dict_passwords) : Voy a recorrer la estructura <dict_passwords> con el iterador <i>; si en cada 
            posicion que se encuentre <i> con la clave 'password' tiene una longitud igual a la longitud dada por el usuario, entonces guardo todos los datos 
            que se encuentran en la posicion <i> en la variable password.
            - Terminado el filtro, voy a verificar que la lista <password> tiene datos o se encuentra vacia. Para cada caso hago el retorno correspondiende con el JSONResponse.
            
    3.3 Mostrar una contraseña dado su identificador:
        a. Ruta:
            - Primero, creo el endpoint : "/passwords/{id}"
            - Segundo, Lo guardo en la etiqueta/sección : "Get Passwords"
            - Tercero, aplico la buena practica de response_model=Password -> La respuesta de la URL es de tipo Password.
            - Cuarto, se espera que la ruta tenga una respuesta <ok>, por ello el status_code es 200.
        b. get_password() :
            - Pregunta para el profesor: si en la definicion de la funcion pongo ->Password, se supone que debe retornar un objeto de tipo Password, entonces porque retornamos otra cosa mas abajo?? return JSONResponse
            - filter(lambda i: i['id'] == id, dict_passwords) : Este trozo de codigo compara cada <id> registrado en <dict_passwords> con el --id-- dado como parametro de ruta.
            - Si hay algun <id> igual al que pasó el usuario, entonces, devuelvo todos los datos en esa posicion y la guardo como una lista dentro de la variable <password>, al final creo una variable result que contiene el JSON con el contenido de <password>
            - Si no hay coincidencias en una variable <result> guardo el JSON con el respectivo mensaje y el status_code 404.
    

4. Peticiones tipo Post : @app.post()

    4.1 Crear una nueva contraseña:
        a. Ruta:
            - Primero, creo el endpoint : "/passwords"
            - Segundo, Lo guardo en la etiqueta/sección : "Post Passwords"
            - Tercero, aplico la buena practica de response_model=dict -> La respuesta de la URL es de tipo diccionario porque la contraseña que se genera esta almacenada en un diccionario??? PREGUNTARLE AL profesor.
            - Cuarto, se espera que la ruta tenga una respuesta <ok>, por ello el status_code es 200.
        b. post_password() :
            - Por que retorna un dict?? -> dict???
            - La funcion recibe como parametro una variable <data> de tipo Password_custom, porque en esa clase se especifican las caracteristicas de la contraseña.
            - La primera acción dentro de la funcion, es guardar el objeto/variable <data> dentro de la lista <dict_password_custom> : dict_password_custom.append(data)
            - Las variables <letras_M>, <letras_m>, <numeros>, <especial>, contienen los caracteres que se pueden usar en una contraseña.
            - La variable <new_password> es la encargada de ir almacenando cada caracter que se genera aleatoriamente para componer la contraseña.
            - Logica para generar la constraseña :
                caso 1: Este caso es para cuando el usuario quiera letras mayusculas, numeros y simbolos en su contraseña. En este caso para generar contraseñas seguras lo que hago es mantener un proporción de 50% Letras, 25% numero y 25% simbolos.
                caso 2: Este caso es para cuando el usuario quiera letras minusculas, numeros y simbolos en su contraseña. Este caso tambien mantiene la proporcionalidad de 50-25-25.
                caso 3: Este caso es para cuando el usuario quiera letras mayusculas y simbolos, pero no quiere numeros en su contraseña. Este caso maneja la proporcionalidad de 65-35.
                caso 4: Este caso es para cuando el usuario quiera letras mayusculas y numeros, pero no quiere simbolos en su contraseña. Este caso maneja la proporcionalidad de 65-35.
                caso 5: Este caso es para cuando el usuario quiera letras minusculas y simbolos, pero no quiere numeros en su contraseña. Este caso maneja la proporcionalidad de 65-35.
                caso 6: Este caso es para cuando el usuario quiera letras minusculas y numeros, pero no quiere simbolos en su contraseña. Este caso maneja la proporcionalidad de 65-35.
                cualquier otro caso: retorna un mensaje advirtiendo que la forma que desea combinar las caracteristicas no es la adecuada.
                acomodando la contraseña al tamaño establecido: Es necesario este punto, porque utilicé la funcion <ceil> y en la mayoria de casos la contraseña tiene una longitud mayor.
                Revolviendo/Barajando la contraseña: Aqui utilicé la funcion <shuffle> para que la contraseña fuera aun mas segura.
                Reuniendo y almacenando los datos: Creé una funcion llamada <gether> donde le asignaria la plantilla <Password> con los datos <id> y <new_password>, acto seguido transformé la variable en un diccionario y lo almacene con el metodo <append> a la lista <dict_passwords>.


5. Peticiones tipo Put: @app.put()

    5.1 Actualizar contraseña dado su id:
        a. Ruta:
            - Primero, creo el endpoint : "/passwords/put-id/{id}"
            - Segundo, Lo guardo en la etiqueta/sección : "Put Passwords"
            - Tercero, aplico la buena practica de response_model=dict -> La respuesta de la URL es de tipo diccionario porque la contraseña que se genera esta almacenada en un diccionario??? PREGUNTARLE AL profesor.
            - Cuarto, se espera que la ruta tenga una respuesta <ok>, por ello el status_code es 200.
        b. put_password() : 
            - Por que retorna un dict?? -> dict???
            - La funcion recibe dos parametros:
                1. id:int, Este parametro es el id de la contraseña que el usuario quiere actualizar, nos ayudará a localizarla.
                2. data:Password_custom, Este parametro le servirá al usuario para customizar la nueva contraseña.
            - La primera accion dentro de la funcion es verificar si el <id> se encuentra en la Estructura <dict_passwords>, para ello usé un filter acompañado de un lambda y un list al final.
            - Luego verifico con la longitud de la lista, si el <id> se encuentra o no.
                1. Si el <id> se encuentra, hago lo mismo que en el --post--, la unica diferencia es que no voy agregar contenido nuevo, sino que voy a sobreescribir el que ya se encuentra.
                2. Si el <id> no se encuentra, entonces retorno un JSON con el contenido correspondiende.
    
    5.2 Actualizar alguna contraseña dada la contraseña:
        a. Ruta:
            - Primero, creo el endpoint : "/passwords/put-psw/{psw}"
            - Segundo, Lo guardo en la etiqueta/sección : "Put Passwords"
            - Tercero, aplico la buena practica de response_model=dict -> La respuesta de la URL es de tipo diccionario porque la contraseña que se genera esta almacenada en un diccionario??? PREGUNTARLE AL profesor.
            - Cuarto, se espera que la ruta tenga una respuesta <ok>, por ello el status_code es 200.

        b. put_password() : 
            - Por que retorna un dict?? -> dict???
            - La funcion recibe dos parametros:
                1. psw:str, Este parametro es la contraseña que el usuario quiere actualizar, nos ayudará a localizarla dentro de <dict_passwords>
                2. data:Password_custom, Este parametro le servirá al usuario para customizar la nueva contraseña.
            - La primera accion dentro de la funcion es verificar si la <psw> se encuentra en la Estructura <dict_passwords>, para ello usé un filter acompañado de un lambda y un list al final.
            - Luego verifico con la longitud de la lista, si el <psw> se encuentra o no.
                1. Si el <psw> se encuentra, hago lo mismo que en el --post--, la unica diferencia es que no voy agregar contenido nuevo, sino que voy a sobreescribir el que ya se encuentra. El metodo de busqueda se basa en guardar el <id> de la constraseña en una variable para poder localizarla en el <dict_password_custom> y poder sobreescribir. 
                2. Si el <psw> no se encuentra, entonces retorno un JSON con el contenido correspondiende.
        
6. Peticiones de tipo Delete: @app.delete()

    6.1 Borrar una contraseña dado su identificador :
        a. Ruta:
            - Primero, creo el endpoint : "/passwords/delete-id/{id}"
            - Segundo, Lo guardo en la etiqueta/sección : "Delete Passwords"
            - Tercero, aplico la buena practica de response_model=dict 
            - Cuarto, se espera que la ruta tenga una respuesta <ok>, por ello el status_code es 200.

        b. delete_password() : 
            - Por que retorna un dict?? -> dict???
            - La funcion recibe 1 parametro:
                1. id:int, Este parametro es el id de la contraseña que el usuario quiere borrar, nos ayudará a localizarla.                
            - La primera accion dentro de la funcion es verificar si el <id> se encuentra en la Estructura <dict_passwords>, para ello usé un filter acompañado de un lambda y un list al final.
            - Luego verifico con la longitud de la lista, si el <id> se encuentra o no.
                1. Si el <id> se encuentra, recorro por separado tanto el <dict_password_custom> como el <dict_passwords> y con una condicion verifico que el iterador se encuentre en la posicion correcta para poder hacer un <remove>. Al final devuelvo un JSON con el contenido correspondiende.                
                2. Si el <id> no se encuentra, entonces retorno un JSON con el contenido correspondiende.

    6.2 Borrar una contraseña dada la contraseña:
        a. Ruta:
            - Primero, creo el endpoint : "/passwords/delete-psw/{psw}"
            - Segundo, Lo guardo en la etiqueta/sección : "Delete Passwords"
            - Tercero, aplico la buena practica de response_model=dict -> La respuesta de la URL es de tipo diccionario porque la contraseña que se genera esta almacenada en un diccionario??? PREGUNTARLE AL profesor.
            - Cuarto, se espera que la ruta tenga una respuesta <ok>, por ello el status_code es 200.
        
        b. delete_password_() : 
            - Por que retorna un dict?? -> dict???
            - La funcion recibe 1 parametro:
                1. psw:str, Este parametro es la contraseña que el usuario quiere borrar, nos ayudará a localizarla dentro del <dict_passwords>.                
            - La primera accion dentro de la funcion es verificar si la <psw> se encuentra en la Estructura <dict_passwords>, para ello usé un filter acompañado de un lambda y un list al final.
            - Luego verifico con la longitud de la lista <validando>, si el <psw> se encuentra o no.
                1. Si la <psw> se encuentra, recorro la lista <validando> para guardar el <id>, lo hago porque es util para ubicar los datos de customizacion que le pertenecen a la contraseña. Luego recorro por separado tanto el <dict_password_custom> como el <dict_passwords> y con una condicion verifico que el iterador se encuentre en la posicion correcta para poder hacer un <remove>. Al final devuelvo un JSON con el contenido correspondiente.                
                2. Si el <id> no se encuentra, entonces retorno un JSON con el contenido correspondiende.


7. Encriptado :
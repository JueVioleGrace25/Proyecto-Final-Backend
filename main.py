from fastapi import FastAPI, Path
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from random import randint, shuffle
from math import ceil
from config.database import session, engine, Base 
from models.psword import Password_custom as psw_custom #as es para cambiarle el nombre en el archivo donde lo importé
from models.psword import Password as Pssw
from fastapi.encoders import jsonable_encoder #jsonable_encode : sirve para convertir un objeto en una lista de diccionarios



app = FastAPI()
app.version = '6.6.6'

#Creamos la base de datos:
Base.metadata.create_all(bind=engine)

#Plantilla Base:
class Password_custom(BaseModel):
    id : Optional[int] = None
    length : int = Field(default=8, ge=8, le=16)
    capital_letter : int = Field(default=1, ge=0, le=1)
    numbers : int = Field(default=1, ge=0, le=1)
    simbols : int = Field(default=1, ge=0, le=1)

    # Configuracion de la documentacion
    class Config:
        model_config = {
        "json_schema_extra": {
                "examples": [
                    {
                        "id": 1,
                        "length": 10,
                        "capital_letter": 1,
                        "numbers": 1,
                        "simbols": 0,                    
                    }
                ]
            }
        }

#Falta por documentar: Basicamente esta clase es para guardar las contraseñas con todas las personalizaciones del usuario. La idea es comunicar estas dos clases.
class Password(BaseModel):
    id : Optional[int] 
    password : str 

#Titulo:
@app.get("/", tags=["Home"])
def title():
    HTMLResponse(content="<h1>Generador de contraseñas seguras</h1>")



#1. Mostrar todas las contraseñas:
@app.get("/passwords", tags=["Get Passwords"], response_model=List[Password], status_code=200)
def get_passwords() -> List[Password]:
    db = session()
    result = db.query(Pssw).all() #Pssw es donde va unicamente el id y la contraseña
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


#2. Muestro todas las contraseñas dada su longitud:
@app.get("/passwords/length/{length}", tags=['Get Passwords'], response_model=List[Password], status_code=200)
def get_passwords_length(length:int=Path(ge=8,le=16)) -> List[Password]:    
    db = session()
    result = db.query(Pssw).filter(len(Pssw.password) == length).all()    
    if result:
        return JSONResponse(content=jsonable_encoder(result), status_code=200)
    else:
        return JSONResponse(content={"message": "Length not found"}, status_code=404)

        

#3. Muestro una pelicula dado su identificador:
@app.get("/passwords/get-id/{id}", tags=["Get Passwords"], response_model=Password, status_code=200)
def get_password(id:int=Path(ge=1, le=2000)) -> Password:
    db = session()
    result = db.query(Pssw).filter(Pssw.id == id).first()
    if result:
        return JSONResponse(content=jsonable_encoder(result), status_code=200)
    else:
        return JSONResponse(content={"message": "ID not found"}, status_code=404)

#4. Crear una nueva contraseña
@app.post("/passwords", tags=['Post Password'], response_model=dict, status_code=200) 
def post_password(data:Password_custom) -> dict:

    #Esta session es para guardar los datos dentro del pssword_custom(la personalizacion de la contraseña)
    db = session()
    new_custom = psw_custom(**data.model_dump())
    db.add(new_custom)
    db.commit()

    letras_M = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    letras_m = 'abcdefghijklmnopqrstuvwxyz'
    numeros = '0123456789'
    especial = '#$%&()*+,-./:;<=>@' 
    new_password = "" 

    #Caso 1: True True True    
    if (data.capital_letter and data.numbers and data.simbols) == 1:
        #Asignarle letras mayusculas:
        for i in range(ceil(data.length*0.5)): #50% de letras          
            new_password += letras_M[randint(0,25)]
            
        #Asignarle numeros:
        for i in range(ceil(data.length*0.25)): #25% de numeros                
            new_password += numeros[randint(0, 9)]
            
        #Asignarle caracteres especiales:
        for i in range(ceil(data.length*0.25)): #25% de numeros                        
            new_password += especial[randint(0, 17)]
            

    #Caso 2: F T T
    elif ((data.numbers and data.simbols) == 1) and (data.capital_letter == 0):
        #Asignarle letras minusculas:
        for i in range(ceil(data.length*0.5)): #50% de letras                        
            new_password += letras_m[randint(0, 25)]
    
        #Asignarle numeros:
        for i in range(ceil(data.length*0.25)): #25% de numeros                    
            new_password += numeros[randint(0, 9)]
        
        #Asignarle caracteres especiales:
        for i in range(ceil(data.length*0.25)): #25% de numeros                    
            new_password += especial[randint(0, 17)]
            

    #Caso 3: T F T
    elif (data.capital_letter and data.simbols) == 1 and data.numbers == 0:
        #Asignarle letras mayusculas:
        for i in range(ceil(data.length*0.65)): #65% de letras        
            new_password += letras_M[randint(0, 25)]

        #Asignarle caracteres especiales:
        for i in range(ceil(data.length*0.35)): #35% de numeros                        
            new_password += especial[randint(0, 17)]                    

    #Caso 4: T T F
    elif (data.capital_letter and data.numbers) == 1 and data.simbols == 0:
        #Asignarle letras mayusculas:
        for i in range(ceil(data.length*0.65)): #65% de letras                        
            new_password += letras_M[randint(0, 25)]
            
        #Asignarle numeros:
        for i in range(ceil(data.length*0.35)): #35% de numeros                        
            new_password += numeros[randint(0, 9)]
            
    #Caso 5: F F T
    elif (data.capital_letter and data.numbers) == 0 and data.simbols==1:
        #Asignarle letras minusculas:
        for i in range(ceil(data.length*0.65)):                    
            new_password += letras_m[randint(0, 25)]

        #Asignarle caracteres especiales:
        for i in range(ceil(data.length*0.35)): #35% de numeros                        
            new_password += especial[randint(0, 17)]            
    
    #Caso 6: F T F
    elif (data.capital_letter and data.simbols) == 0 and data.numbers == 1:
        #Asignarle letras minusculas:
        for i in range(ceil(data.length*0.65)):                    
            new_password += letras_m[randint(0, 25)]
        
        #Asignarle numeros:
        for i in range(ceil(data.length*0.35)): #35% de numeros                        
            new_password += numeros[randint(0, 9)]
        

    #Cualquier otro caso:
    else : 
        return JSONResponse(content={"message" : "La contraseña debe de tener al menos un número o simbolo"}, status_code=400)

    #Acomodando la contraseña al tamaño establecido:       
    new_password = new_password[:data.length]     

    #Revolviendo/Barajando la contraseña:
    new_password = list(new_password)
    shuffle(new_password) #barajando 
    new_password = "".join(new_password)

    #Reuniendo y almacenando los datos:    
    gether = Password(id=data.id, password=new_password)
    #Esta session es para guardar la contraseña como su id en la otra hoja:
    db = session() #Cada vez que cierre con un commit y deba seguir modificando debo volver a abrir session()
    new_data = Pssw(**gether.model_dump())
    db.add(new_data)    
    db.commit()   
    return JSONResponse(content={"message": "Password created successfully"}, 
                        status_code=201)



#5. Actualizar alguna contraseña dado su id
@app.put("/passwords/put-id/{id}", tags=['Put Password'], response_model=dict, status_code=200)
def put_password(id:int, data:Password_custom) ->dict:
    db = session()
    result = db.query(psw_custom).filter(psw_custom.id == id).first() #Verifico que el Id exista    
    if result: 
        result.id = data.id
        result.length = data.length
        result.capital_letter = data.capital_letter
        result.numbers = data.numbers        
        result.simbols = data.simbols
        db.commit()      

        letras_M = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        letras_m = 'abcdefghijklmnopqrstuvwxyz'
        numeros = '0123456789'
        especial = '#$%&()*+,-./:;<=>@' 
        new_password = "" 
        
        #Caso 1: True True True    
        if (data.capital_letter and data.numbers and data.simbols) == 1:
            #Asignarle letras mayusculas:
            for i in range(ceil(data.length*0.5)): #50% de letras          
                new_password += letras_M[randint(0,25)]
                
            #Asignarle numeros:
            for i in range(ceil(data.length*0.25)): #25% de numeros                
                new_password += numeros[randint(0, 9)]
                
            #Asignarle caracteres especiales:
            for i in range(ceil(data.length*0.25)): #25% de numeros                        
                new_password += especial[randint(0, 17)]
        
        #Caso 2: F T T
        elif ((data.numbers and data.simbols) == 1) and (data.capital_letter == 0):
            #Asignarle letras minusculas:
            for i in range(ceil(data.length*0.5)): #50% de letras                        
                new_password += letras_m[randint(0, 25)]
        
            #Asignarle numeros:
            for i in range(ceil(data.length*0.25)): #25% de numeros                    
                new_password += numeros[randint(0, 9)]
            
            #Asignarle caracteres especiales:
            for i in range(ceil(data.length*0.25)): #25% de numeros                    
                new_password += especial[randint(0, 17)]
                

        #Caso 3: T F T
        elif (data.capital_letter and data.simbols) == 1 and data.numbers == 0:
            #Asignarle letras mayusculas:
            for i in range(ceil(data.length*0.65)): #65% de letras        
                new_password += letras_M[randint(0, 25)]

            #Asignarle caracteres especiales:
            for i in range(ceil(data.length*0.35)): #35% de numeros                        
                new_password += especial[randint(0, 17)]                    

        #Caso 4: T T F
        elif (data.capital_letter and data.numbers) == 1 and data.simbols == 0:
            #Asignarle letras mayusculas:
            for i in range(ceil(data.length*0.65)): #65% de letras                        
                new_password += letras_M[randint(0, 25)]
                
            #Asignarle numeros:
            for i in range(ceil(data.length*0.35)): #35% de numeros                        
                new_password += numeros[randint(0, 9)]
                
        #Caso 5: F F T
        elif (data.capital_letter and data.numbers) == 0 and data.simbols==1:
            #Asignarle letras minusculas:
            for i in range(ceil(data.length*0.65)):                    
                new_password += letras_m[randint(0, 25)]

            #Asignarle caracteres especiales:
            for i in range(ceil(data.length*0.35)): #35% de numeros                        
                new_password += especial[randint(0, 17)]            
        
        #Caso 6: F T F
        elif (data.capital_letter and data.simbols) == 0 and data.numbers == 1:
            #Asignarle letras minusculas:
            for i in range(ceil(data.length*0.65)):                    
                new_password += letras_m[randint(0, 25)]
            
            #Asignarle numeros:
            for i in range(ceil(data.length*0.35)): #35% de numeros                        
                new_password += numeros[randint(0, 9)]
            

        #Cualquier otro caso:
        else : 
            return JSONResponse(content={"message" : "La contraseña debe de tener al menos un número o simbolo"}, status_code=400)

        #Acomodando la contraseña al tamaño establecido:       
        new_password = new_password[:data.length]     

        #Revolviendo/Barajando la contraseña:
        new_password = list(new_password)
        shuffle(new_password) #barajando 
        new_password = "".join(new_password)
        
        #Esta session es para guardar la contraseña como su id en la otra hoja:
        db = session() #Cada vez que cierre con un commit y deba seguir modificando debo volver a abrir session()
        result_2 = db.query(Pssw).filter(Pssw.id == id).first()                
        result_2.password = new_password
        db.commit() 

        final = JSONResponse(content={"message": "Password updated successfully"}, status_code=201)

    else:
        final = JSONResponse(content={"message": "ID not found"}, status_code=404)
    
    return final



#6. Actualizar alguna contraseña dada la contraseña
@app.put("/passwords/put-psw/{psw}", tags=['Put Password'], response_model=dict, status_code=200)
def put_password_(psw:str, data:Password_custom) -> dict:
    db = session()
    result = db.query(Pssw).filter(Pssw.password == psw).first()
    if result :
        id = result.id
        result_2 = db.query(psw_custom).filter(psw_custom.id == id).first()
        result_2.id = data.id
        result_2.length = data.length
        result_2.capital_letter = data.capital_letter
        result_2.numbers = data.numbers        
        result_2.simbols = data.simbols
        db.commit()

        letras_M = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        letras_m = 'abcdefghijklmnopqrstuvwxyz'
        numeros = '0123456789'
        especial = '#$%&()*+,-./:;<=>@' 
        new_password = ""

        
        #Caso 1: True True True    
        if (data.capital_letter and data.numbers and data.simbols) == 1:
            #Asignarle letras mayusculas:
            for i in range(ceil(data.length*0.5)): #50% de letras          
                new_password += letras_M[randint(0,25)]
                
            #Asignarle numeros:
            for i in range(ceil(data.length*0.25)): #25% de numeros                
                new_password += numeros[randint(0, 9)]
                
            #Asignarle caracteres especiales:
            for i in range(ceil(data.length*0.25)): #25% de numeros                        
                new_password += especial[randint(0, 17)]
        
        #Caso 2: F T T
        elif ((data.numbers and data.simbols) == 1) and (data.capital_letter == 0):
            #Asignarle letras minusculas:
            for i in range(ceil(data.length*0.5)): #50% de letras                        
                new_password += letras_m[randint(0, 25)]
        
            #Asignarle numeros:
            for i in range(ceil(data.length*0.25)): #25% de numeros                    
                new_password += numeros[randint(0, 9)]
            
            #Asignarle caracteres especiales:
            for i in range(ceil(data.length*0.25)): #25% de numeros                    
                new_password += especial[randint(0, 17)]
                

        #Caso 3: T F T
        elif (data.capital_letter and data.simbols) == 1 and data.numbers == 0:
            #Asignarle letras mayusculas:
            for i in range(ceil(data.length*0.65)): #65% de letras        
                new_password += letras_M[randint(0, 25)]

            #Asignarle caracteres especiales:
            for i in range(ceil(data.length*0.35)): #35% de numeros                        
                new_password += especial[randint(0, 17)]                    

        #Caso 4: T T F
        elif (data.capital_letter and data.numbers) == 1 and data.simbols == 0:
            #Asignarle letras mayusculas:
            for i in range(ceil(data.length*0.65)): #65% de letras                        
                new_password += letras_M[randint(0, 25)]
                
            #Asignarle numeros:
            for i in range(ceil(data.length*0.35)): #35% de numeros                        
                new_password += numeros[randint(0, 9)]
                
        #Caso 5: F F T
        elif (data.capital_letter and data.numbers) == 0 and data.simbols==1:
            #Asignarle letras minusculas:
            for i in range(ceil(data.length*0.65)):                    
                new_password += letras_m[randint(0, 25)]

            #Asignarle caracteres especiales:
            for i in range(ceil(data.length*0.35)): #35% de numeros                        
                new_password += especial[randint(0, 17)]            
        
        #Caso 6: F T F
        elif (data.capital_letter and data.simbols) == 0 and data.numbers == 1:
            #Asignarle letras minusculas:
            for i in range(ceil(data.length*0.65)):                    
                new_password += letras_m[randint(0, 25)]
            
            #Asignarle numeros:
            for i in range(ceil(data.length*0.35)): #35% de numeros                        
                new_password += numeros[randint(0, 9)]
            

        #Cualquier otro caso:
        else : 
            return JSONResponse(content={"message" : "La contraseña debe de tener al menos un número o simbolo"}, status_code=400)

        #Acomodando la contraseña al tamaño establecido:       
        new_password = new_password[:data.length]     

        #Revolviendo/Barajando la contraseña:
        new_password = list(new_password)
        shuffle(new_password) #barajando 
        new_password = "".join(new_password)

        #Esta session es para guardar la contraseña como su id en la otra hoja:
        db = session() #Cada vez que cierre con un commit y deba seguir modificando debo volver a abrir session()
        result = db.query(Pssw).filter(Pssw.password == psw).first()                
        result.password = new_password
        db.commit() 

        final = JSONResponse(content={"message": "Password updated successfully"}, status_code=201)

    else:
        final = JSONResponse(content={"message": "Password not found"}, status_code=404)
    
    return final


#7. Borrar una contraseña dado su identificador
@app.delete("/passwords/delete-id/{id}", tags=['Delete Password'], response_model=dict, status_code=200)
def delete_password(id:int) -> dict:
    db = session()
    result =db.query(psw_custom).filter(psw_custom.id==id).first()
    if result:
        #Eliminando los datos del password_custom:
        db.delete(result)
        db.commit()
        
        #Eliminando los datos del Passwords:
        db = session()
        result_2 = db.query(Pssw).filter(Pssw.id == id).first()
        db.delete(result_2)
        db.commit()

    
        final = JSONResponse(content={"message": "Password deleted successfully"}, status_code=201)

    else:
        final = JSONResponse(content={"message": "ID not found"}, status_code=404)
    return final


#8. Borrar una contraseña dada la contraseña:
@app.delete("/password/delete-psw/{psw}", tags=['Delete Password'], response_model=dict, status_code=200)
def delete_password_(psw:str) -> dict:
    db = session()
    result = db.query(Pssw).filter(Pssw.password == psw).first()    
    if result:        
        #Consiguiendo id:
        id = result.id        
        #Eliminando los datos del password_custom:
        result_2 = db.query(psw_custom).filter(psw_custom.id==id).first()
        db.delete(result_2)
        db.commit()
        #Eliminando los datos del Passwords:
        db = session()
        result = db.query(Pssw).filter(Pssw.id == id).first()
        db.delete(result)
        db.commit()
    
        final = JSONResponse(content={"message": "Password deleted successfully"}, status_code=201)

    else:
        final = JSONResponse(content={"message": "Password not found"}, status_code=404)
    return final

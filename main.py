from fastapi import FastAPI, Path
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from random import randint, shuffle
from math import ceil


app = FastAPI()
app.version = '6.6.6'

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

dict_password_custom = [
    {
        "id": 1,
        "length": 10,
        "capital_letter": 1,
        "numbers": 1,
        "simbols": 0,        
    },

    {
        "id": 2,
        "length": 8,
        "capital_letter": 0,
        "numbers": 1,
        "simbols": 1,        
    },
    
    {
        "id": 3,
        "length": 10,
        "capital_letter": 0,
        "numbers": 1,
        "simbols": 1,        
    }

]

dict_passwords = [
    {
        "id" : 1,
        "password" : "HDGFjsk123"
    },
    {
        "id" : 2,
        "password" : "dksl12##"
    },
    {
        "id": 3,
        "password" : "HDGFjsk213"
    }

]

#Titulo:
@app.get("/", tags=["Home"])
def title():
    HTMLResponse(content="<h1>Generador de contraseñas seguras</h1>")



#1. Mostrar todas las contraseñas:
@app.get("/passwords", tags=["Get Passwords"], response_model=List[Password], status_code=200)
def get_passwords() -> List[Password]:
    return JSONResponse(status_code=200, content=dict_passwords)


#2. Muestro todas las contraseñas dada su longitud:
@app.get("/passwords/length/{length}", tags=['Get Passwords'], response_model=List[Password], status_code=200)
def get_passwords_length(length:int=Path(ge=8,le=16)) -> List[Password]:    
    password=list(filter (lambda i: len(i['password'])==length, dict_passwords))
    if len(password)>0:
        result = JSONResponse(content=password, status_code=200)      
    else: 
        result = JSONResponse(content={"message": "Length not found"}, status_code=404)
    return result
        

#3. Muestro una pelicula dado su identificador:
@app.get("/passwords/get-id/{id}", tags=["Get Passwords"], response_model=Password, status_code=200)
def get_password(id:int=Path(ge=1, le=2000)) -> Password:
    password = list(filter(lambda i: i['id'] == id, dict_passwords))
    if len(password)>0:
        result = JSONResponse(content=password, status_code=200)
    else:
        result = JSONResponse(content={"message": "ID not found"}, status_code=404)
    return result


#4. Crear una nueva contraseña
@app.post("/passwords", tags=['Post Password'], response_model=dict, status_code=200) #response_model=Password_custom o Password????
def post_password(data:Password_custom) -> dict:
    dict_password_custom.append(data) 
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
    gether = dict(Password(id=data.id, password=new_password))
    dict_passwords.append(gether) #agregando la nueva contraseña con su id en la lista    
    return JSONResponse(content={"message": "Password created successfully"}, status_code=201)



#5. Actualizar alguna contraseña dado su id
@app.put("/passwords/put-id/{id}", tags=['Put Password'], response_model=dict, status_code=200)
def put_password(id:int, data:Password_custom) ->dict:
    validacion = list(filter(lambda i: i['id'] == id, dict_passwords)) #Corroboro que el id se encuentre en la estructura.
    if len(validacion)>0: #Si esto es verdad es porque encontró un id identico en la estructura        
        letras_M = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        letras_m = 'abcdefghijklmnopqrstuvwxyz'
        numeros = '0123456789'
        especial = '#$%&()*+,-./:;<=>@' 
        new_password = "" 

        #Actualizando el dict_password_custom:
        for i in dict_password_custom:
            if i['id'] == id:
                i['length'] = data.length                
                i["capital_letter"] = data.capital_letter
                i["numbers"] = data.numbers
                i["simbols"] = data.simbols
                break

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

        #Actualizando la contraseña:    
        for i in dict_passwords:
            if i['id'] == id:
                i['password'] = new_password            
                break

        result = JSONResponse(content={"message": "Password updated successfully"}, status_code=201)

    else:
        result = JSONResponse(content={"message": "ID not found"}, status_code=404)
    
    return result



#6. Actualizar alguna contraseña dada la contraseña
@app.put("/passwords/put-psw/{psw}", tags=['Put Password'], response_model=dict, status_code=200)
def put_password_(psw:str, data:Password_custom) -> dict:
    validacion = list(filter(lambda i: i['password'] == psw, dict_passwords))
    if len(validacion)>0:
        letras_M = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        letras_m = 'abcdefghijklmnopqrstuvwxyz'
        numeros = '0123456789'
        especial = '#$%&()*+,-./:;<=>@' 
        new_password = ""

        #Sacando el id :
        for i in dict_passwords:
            if i['password'] == psw:
                id = i['id']
                break
        
        #Actualizando el dict_password_custom:
        for i in dict_password_custom:
            if i['id'] == id :                
                i['length'] = data.length                
                i["capital_letter"] = data.capital_letter
                i["numbers"] = data.numbers
                i["simbols"] = data.simbols
                break

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

        #Actualizando la contraseña:    
        for i in dict_passwords:
            if i['id'] == id:                
                i['password'] = new_password   
                break         

        result = JSONResponse(content={"message": "Password updated successfully"}, status_code=201)

    else:
        result = JSONResponse(content={"message": "Password not found"}, status_code=404)
    
    return result


#7. Borrar una contraseña dado su identificador
@app.delete("/passwords/delete-id/{id}", tags=['Delete Password'], response_model=dict, status_code=200)
def delete_password(id:int) -> dict:
    validando = list(filter(lambda i: i['id']==id, dict_passwords))
    if len(validando)>0:
        #Eliminando los datos del dict_password_custom:
        for i in dict_password_custom:
            if i['id'] == id:            
                dict_password_custom.remove(i)
                break
        
        #Eliminando los datos del dict_passwords:
        for i in dict_passwords:
            if i['id'] == id:
                dict_passwords.remove(i)
                break
    
        result = JSONResponse(content={"message": "Password deleted successfully"}, status_code=201)

    else:
        result = JSONResponse(content={"message": "ID not found"}, status_code=404)
    return result


#8. Borrar una contraseña dada la contraseña:
@app.delete("/password/delete-psw/{psw}", tags=['Delete Password'], response_model=dict, status_code=200)
def delete_password_(psw:str) -> dict:
    validando = list(filter(lambda i: i['password']==psw, dict_passwords)) #Aqui guardo el diccionario con el id y password
    if len(validando)>0:
        #Consiguiendo id:
        for i in validando:
            if i['password'] == psw:                
                ide = i['id']        
                
        #Eliminando los datos del dict_password_custom:
        for i in dict_password_custom:
            if i['id'] == ide:            
                dict_password_custom.remove(i)
                break
        
        #Eliminando los datos del dict_passwords:
        for i in dict_passwords:
            if i['id'] == ide:
                dict_passwords.remove(i)
                break
    
        result = JSONResponse(content={"message": "Password deleted successfully"}, status_code=201)

    else:
        result = JSONResponse(content={"message": "Password not found"}, status_code=404)
    return result

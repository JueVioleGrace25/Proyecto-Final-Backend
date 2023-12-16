from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from random import randint




class Password_custom(BaseModel):
    id : Optional[int] 
    length : int 
    capital_letter : int
    numbers : int 
    simbols : int

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


#data = dict(Password(id=8, password="jdkks"))
#print(data.id)
#data['id'] = 3
#dict_passwords.append(data)
#print(dict_passwords[-1])

#print(letras_M[25])

def post_password(data:Password_custom) -> dict:
    dict_password_custom.append(data) #Agregando la nueva customizacion de password
    new_password = ""    

#Caso 1: True True True    
    if (data.capital_letter and data.numbers and data.simbols) == 1:
        #Asignarle letras mayusculas:
        for i in range(round(data.length*0.5)): #50% de letras
            rand = randint(0,25)
            letras_M = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            new_password += letras_M[rand]
            #dict_passwords.append(letras_M[rand])
        #Asignarle numeros:
        for i in range(round(data.length*0.25)): #25% de numeros
            rand = randint(0, 9)
            numeros = '0123456789'
            new_password += numeros[rand]
            #password.append(numeros[rand])
        #Asignarle caracteres especiales:
        for i in range(round(data.length*0.25)): #25% de numeros
            rand = randint(0, 17)
            especial = '#$%&()*+,-./:;<=>@' 
            new_password += especial[rand]
            #password.append(especial[rand])

    #Caso 2: F T T
    elif ((data.numbers and data.simbols) == 1) and (data.capital_letter == 0):
        #Asignarle letras minusculas:
        for i in range(round(data.length*0.5)): #50% de letras
            rand = randint(0, 25)
            letras_M = 'abcdefghijklmnopqrstuvwxyz'
            new_password += letras_M[rand]
            #password.append(letras_M[rand])
        #Asignarle numeros:
        for i in range(round(data.length*0.25)): #25% de numeros
            rand = randint(0, 9)
            numeros = '0123456789'
            new_password += numeros[rand]
            #password.append(numeros[rand])
        #Asignarle caracteres especiales:
        for i in range(round(data.length*0.25)): #25% de numeros
            rand = randint(0, 17)
            especial = '#$%&()*+,-./:;<=>@'
            new_password += especial[rand]
            #password.append(especial[rand])

    #Caso 3: T F T
    elif (data.capital_letter and data.simbols) == 1 and data.numbers == 0:
        #Asignarle letras mayusculas:
        for i in range(round(data.length*0.65)): #65% de letras
            rand = randint(0, 25)
            letras_M = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            new_password += letras_M[rand]
            #password.append(letras_M[rand])

        #Asignarle caracteres especiales:
        for i in range(round(data.length*0.35)): #35% de numeros
            rand = randint(0, 17)
            especial = '#$%&()*+,-./:;<=>@' 
            new_password += especial[rand]
            #password.append(especial[rand])
        

    #Caso 4: T T F
    elif (data.capital_letter and data.numbers) == 1 and data.simbols == 0:
        #Asignarle letras mayusculas:
        for i in range(round(data.length*0.65)): #65% de letras
            rand = randint(0, 25)
            letras_M = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            new_password += letras_M[rand]
            #password.append(letras_M[rand])

        #Asignarle numeros:
        for i in range(round(data.length*0.35)): #35% de numeros
            rand = randint(0, 9)
            numeros = '0123456789'
            new_password += numeros[rand]
            #password.append(numeros[rand])        

    #Caso 5: F F F
    else :
        #Asignarle letras minusculas:
        for i in range(round(data.length)):
            rand = randint(0, 25)
            letras_M = 'abcdefghijklmnopqrstuvwxyz'
            new_password += letras_M[rand]
            #password.append(letras_M[rand])    

    gether = Password(id=data.id, password=new_password)
    #gether = dict(Password(id=data.id, password=new_password))
    dict_passwords.append(gether) #agregando la nueva contraseña con su id en la lista
    
    return dict_passwords    
    #return JSONResponse(content={"message": "Movie created successfully"}, status_code=201)

data = Password_custom(id=4, length=8, capital_letter=1, numbers=0, simbols=1)
post_password(data)
print(dict_passwords[-1])
print(type(dict_passwords[2]))
#print(data.id)


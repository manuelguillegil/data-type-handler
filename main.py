## MANUEL GUILLERMO GIL 14-10397

from handler import *
from Atomic import *

def is_valid(option):
    option = option.strip()
    option = option.split(" ")
    if option[0].lower() == "salir":
        return True
    if len(option) < 2:
        return False    
    if option[0].lower() != "atomico" and option[0].lower() != "struct" and option[0].lower() != "describir" and option[0].lower() != "union": 
        return False
    if option[0].lower() == "atomico":
        if(len(option) > 4):            
            return False
        if option[2].isdigit() and option[3].isdigit():
            return True
    if option[0].lower() == "struct" or option[0].lower() == "union":
        if len(option) < 3:
            return False
        return True
    if option[0].lower() == "describir":
        return True

def main():
    
    print("Bienvenido, por favor introduzca una de las optiones")
    option = ""
    while True:
        print("Introduzca ATOMICO <nombre> <representacion> <alineacion> para crear un nuevo tipo atomico")
        print("Introduzca STRUCT <nombre> [<tipo>] para crear un nuevo struct")
        print("Introduzca UNION <nombre> [<tipo>] para crear un nuevo struct")
        print("Introduzca DESCRIBIR <nombre> para describir un registro ya existente")
        print("Introduzca SALIR para salir del programa")
        print()
        option = input()
        if(is_valid(option)):
            option = option.split(" ")

            if(option[0].lower() == "atomico"):                
                create_atomic(option)
                
            elif(option[0].lower() == "struct"):
                create_register(option, "struct")
           
            elif(option[0].lower() == "union"):
                create_register(option, "union")
            elif(option[0].lower() == "describir"):
                describe(option[1])
              
            elif(option[0].lower() == "salir"):
                break
        else:
            print("Por favor introduzca una option valida")
        print()
            

if __name__ == '__main__':
    main()
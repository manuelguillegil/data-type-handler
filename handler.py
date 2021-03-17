## MANUEL GUILLERMO GIL 14-10397
import copy
import functools
from itertools import permutations

from handler import *
from Atomic import *
from Union import *
from Struct import *

atomics  = []
unions = []
structs = [] 

# Funcion que busca un elemento en alguna de las listas
# @param name - Nombre a buscar
# @param type - Indica si es para la lista de atómicos, o registros struct o de tipo union
def search_element(name, type):
    if(name):
        if (type == 'atomic'):
            return [atomic for atomic in atomics if atomic.name == name].pop() if [atomic for atomic in atomics if atomic.name == name] else False
        elif (type == 'struct'):
            return [struct for struct in structs if struct.name == name].pop() if [struct for struct in structs if struct.name == name] else False
        else:
            return [union for union in unions if union.name == name].pop() if [union for union in unions if union.name == name] else False
    return ''

# Funcion que verifica si existe el nombre en algún tipo
# @param name - Nombre a chequear
def exists(name):
    if(name):
        if ([atomic for atomic in atomics if atomic.name == name] or [struct for struct in structs if struct.name == name] or [union for union in unions if union.name == name]):
            print("Nombre ya existente") 
            return True
    else:
        print("Ingrese un nombre") 
        return True

# Crea un atomico y lo añade a la lista correspondiente
# @param option - Arreglo con el nombre, representación y alineación
def create_atomic(option):
    if(not(exists(option[1]))):          
        atomics.append(Atomic(option[1],option[2], option[3]))

# Crea un registro y lo añade a la lista correspondiente
# @param option - Arreglo con el nombre de la estructura a crear y con los tipos atomicos
# @param type - Indica si se desea crear una estructura o una union
def create_register(option, type):
    if not(exists(option[1])): 
        for elem in option[2:]: 
            if (not [atomic for atomic in atomics if atomic.name == elem]):
                print("Ha introducido un tipo que no existe")
                return

        elements = [] 
        for elem in option[2:]:
            elements.append(search_element(elem, 'atomic'))
        if(type == "struct"):
            structs.append(Struct(option[1], elements))
        else:
            unions.append(Union(option[1], elements))

#Funcion utilizada para crear el espacio sin ninguna regla
# @param elements - Lista de elementos que se almacenarán en el espacio para el caso de no respetar la alineación
def create_space_packed(elements):
    result = []
    elements = elements[::-1]
    while elements:
        element = elements.pop()
        counter = int(element.representation)
        name = element.name
        while counter:
            result.append(element)
            counter -= 1

    return result
  
#Funcion utilizada para crear espacio respetando reglas de alineamiento
# @param elements - Lista de elementos que se almacenarán en el espacio para el caso de respetar la alineación
def create_space_unpacked(elements, resultado):
    elements = elements[::-1]
    while elements:
        element = elements.pop()
        counter = int(element.representation)
        alignment = int(element.alignment)
        name = element.name 
        if len(resultado) % alignment == 0:
            if [atomic for atomic in atomics if atomic.name == name]:
                while counter:
                    resultado.append(element)
                    counter -= 1
        else:
            while len(resultado) % alignment != 0:
                resultado.append(' ')
            if [atomic for atomic in atomics if atomic.name == name]:
                while counter:
                    resultado.append(element)
                    counter -= 1            
    return resultado

#Funcion utilizada para buscar el mejor caso que respete la alineacion y pierda la menor cantidad de bytes posible
# @param name - Nombre de la estructura donde queremos que sus elementos se almacenen en un espacio para el caso de optimización
def optimization(name):
    permu_list = []
    struct_element = [struct for struct in structs if struct.name == name]
    if struct_element:
        array = copy.deepcopy(search_element(name, 'struct').elements)
        for permu_element in list(permutations(array)):              
            permu_list.append(create_space_unpacked(list(permu_element), []))
            
        minimo = permu_list[0].count(' ')
        list_optimized = permu_list[0]

        for permu_list_element in permu_list:        
            lost = permu_list_element.count(' ')
            if(lost < minimo):
                minimo = lost
                list_optimized = permu_list_element
        return list_optimized

#Funcion utilizada para imprimir un array como una matriz, diviendolo de 4 en 4
# @param elements - Elementos
def print_like_matriz(elements):
    print(elements)
    for i in range(len(elements)):
        if i % 4 == 0 : print()
        try:
            print(elements[i].name + " |", end=" ")
        except:
            print(str(elements[i]) + " |", end =" ")

#Funcion utilizada para imprimir los elementos de un struct
# @param elements - Elementos de un struct
def print_struct(elements):
    indice = 0
    while indice < len(elements):
        if (elements[indice] == ' '):
            indice +=1
            continue

        print("Me encuentro en la posicion {}, {}".format(indice, elements[indice]))
        indice += int(elements[indice].representation)
  
    print_like_matriz(elements)

#Funcion para determinar el maximo comun divisor de dos numeros
def gcd(a,b):
    while b:
        a,b = b, a%b
    return a
#Funcion para determinar el minimo comun multimo entre dos numeros
def lcm(a,b):
    return a*b // gcd(a,b)

#Funcion utilizada por los union, basicamente busca entre todas las representaciones de sus posibles elementos
# y selecciona aquella que sea mayor
def union_size(array):
    result = []
    for elem in array:
        result.append(int(elem.representation))
    return max(result)

#Funcion utilizada por los union, basicamente busca entre las alineaciones de todos sus posibles elementos y retorna el minimo comun multiplo entre todos ellos
def union_alignment(array):
    result = []
    for elem in array:
        result.append(int(elem.alignment))
    return functools.reduce(lambda x, y: lcm(x, y), result)

#Funcion utilizada para imprimir registros variantes
# @param union - Union
def print_union(union):
    print("Soy un registro union, mi tamano es de: {} bytes, y mi alineacion en caso de estar en un struct seria {}".format(union.representation, union.alignment))
    print("Mis posibles opciones son:")
    for elem in union.elements:
        print("\n")
        print("\t"+str(elem), end="")

#Funcion utilizada para describir un elemento
# @name - Nombre del elemento. Puede ser un atómico, struct o union
def describe(name):
    atomic_element = search_element(name, 'atomic')
    struct_element = search_element(name, 'struct')
    union_element = search_element(name, 'union')
    if atomic_element:
        print(atomic_element.name)
        return str(atomic_element)
    elif struct_element:
        print("----------- STRUCT EMPAQUETADO ------------------")
        to_evaluate = struct_element.elements  
        struct_element.elements_packed = create_space_packed(to_evaluate)
        print_struct(struct_element.elements_packed)
        struct_element.waste = struct_element.elements_packed.count(' ')
        struct_element.representation = len(struct_element.elements_packed)
        print("\nCaso Empaquetado: Total de {} bytes ocupados, y una perdida de 0 bytes".format(struct_element.representation))
        print()

        print("-------------STRUCT NO EMPAQUETADO--------")

        struct_element.elements_unpacked = create_space_unpacked(to_evaluate, [])
        struct_element.representation = len(struct_element.elements_unpacked)
        print_struct(struct_element.elements_unpacked)
        struct_element.waste = struct_element.elements_unpacked.count(' ')
        print("\nCaso no Empaquetado: Total de {} bytes ocupados, y una perdida total de {} bytes".format(struct_element.representation, struct_element.waste))
        print()
        
        print("------------- STRUCT OPTIMIZACION--------")
        struct_element.elements_optimized = optimization(name)
        struct_element.representation = len(struct_element.elements_optimized)
        print_struct(struct_element.elements_optimized)
        struct_element.waste = struct_element.elements_optimized.count(' ')
        print("\nCaso Optimizado: Total de {} bytes ocupados, y una perdida total de {} bytes".format(struct_element.representation,struct_element.waste))
        print()
    
    elif union_element:
        to_evaluate = union_element.elements       
        union_element.representation = union_size(union_element.elements)
        union_element.alignment = union_alignment(union_element.elements)
        print_union(union_element)
    else:
        print("No es válido")

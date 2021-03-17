from handler import *
import unittest
from collections import Counter
from io import StringIO
from unittest.mock import patch

class TestRegistrosMethods(unittest.TestCase):
    #Verificamos instancia de atomico
    def test_1(self):
        new_input = "ATOMICO int 4 4"
        new_input = new_input.split(" ")
        create_atomic(new_input)
        self.assertIsInstance(search_element('int', 'atomic'), Atomic)

    #Verificamos instancia de struct
    def test_2(self):
        new_input = "STRUCT prueba int"
        new_input = new_input.split(" ")
        create_register(new_input, "struct")
        self.assertIsInstance(search_element('prueba', 'struct'), Struct)

    #Verificamos instancia de union
    def test_3(self):
        new_input = "UNION prueba2 int"
        new_input = new_input.split(" ")
        create_register(new_input, "union")
        print(new_input)
        self.assertIsInstance(search_element('prueba2', 'union'), Union)

    #Crearemos ahora un struct mas complejo que tenga int 4 4 y char 2 2. Ver output en consola para corroborar
    def test_4(self):
        create_atomic("ATOMICO char 2 2".split(" "))
        create_register("STRUCT prueba3 char int".split(" "), "struct")
        with patch('sys.stdout', new=StringIO()) as mocked_stdout:
            describe("prueba3")
            output = mocked_stdout.getvalue()
        empaquetado = "Caso Empaquetado: Total de 6 bytes ocupados, y una perdida de 0 bytes"
        no_empaquetado =  "Caso no Empaquetado: Total de 8 bytes ocupados, y una perdida total de 2 bytes"
        optimizado = "Caso Optimizado: Total de 6 bytes ocupados, y una perdida total de 0 bytes"
        print(output)
        #Verificamos que el output contenga los strings de los resultados esperados
        self.assertTrue(empaquetado in output and no_empaquetado in output and optimizado in output)  
    
if __name__ == '__main__':
    unittest.main()
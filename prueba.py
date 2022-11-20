from itertools import permutations

cedula = "6880"
division = len(cedula)//2
print(division)

def is_numero_vampiro(cedula):
    cont = 0
    for permutaciones in permutations(cedula):
        digitos_separados = "".join(permutaciones)
        primera_parte = digitos_separados[:int(len(digitos_separados)//2)]
        segunda_parte = digitos_separados[int(len(digitos_separados)//2):]
        primera_parte = int(primera_parte)
        segunda_parte = int(segunda_parte)
        if primera_parte * segunda_parte == int(cedula):
            cont+=1
    if cont != 0:
        return True
    else:
        return False

boolean = is_numero_vampiro(cedula)
print(boolean)
class Equipo():
    def __init__(self, nombre, bandera, codigo_fifa, grupo, id):
        self.nombre = nombre
        self.bandera = bandera
        self.codigo_fifa = codigo_fifa
        self.grupo = grupo
        self.id = id
    
    def show(self):
        print(f"-----{(self.nombre).upper()}-----")
        print(f"Codigo FIFA -> {self.codigo_fifa}")
        print(f"Grupo -> {self.grupo}")
        
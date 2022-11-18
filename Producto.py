class Producto():
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio
    
class Comida(Producto):
    def __init__(self, nombre, precio):
        super().__init__(nombre, precio)
        self.type = "Comida"
    
    def show(self):
        print(f"Nombre -> {self.nombre}")
        print(f"Precio -> {self.precio}$")
        print(f"Tipo -> Comida")
    
    
class Bebida(Producto):
    def __init__(self, nombre, precio):
        super().__init__(nombre, precio)
        self.type = "Bebida"
    
    def show(self):
        print(f"Nombre -> {self.nombre}")
        print(f"Precio -> {self.precio}$")
        print(f"Tipo -> Bebida")

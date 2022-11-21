class Producto():
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio
        self.IVA = precio * 0.16
        self.total = self.IVA + precio
    
class Alimento(Producto):
    def __init__(self, nombre, precio):
        super().__init__(nombre, precio)
        self.type = "Alimento"
    
    def show(self):
        print(f"Nombre -> {self.nombre}")
        print(f"Precio -> {self.precio}$")
        print(f"IVA -> {self.IVA}$")
        print(f"Total -> {self.total}$")
        print(f"Tipo -> Alimento")
    
class Bebida(Producto):
    def __init__(self, nombre, precio):
        super().__init__(nombre, precio)
        self.type = "Bebida"
    
    def show(self):
        print(f"Nombre -> {self.nombre}")
        print(f"Precio -> {self.precio}$")
        print(f"IVA -> {self.IVA}$")
        print(f"Total -> {self.total}$")
        print(f"Tipo -> Bebida")
    

class Producto():
    def __init__(self, nombre, precio, adicional):
        self.nombre = nombre
        self.precio = precio
        self.adicional = adicional
        self.IVA = precio * 0.16
        self.total = self.IVA + precio
    
class Alimento(Producto):
    def __init__(self, nombre, precio, adicional):
        super().__init__(nombre, precio, adicional)
        self.type = "Alimento"

    def show_sin_iva(self):
        print(f"Nombre -> {self.nombre}")
        print(f"Precio -> {self.precio}$")
        print(f"Adicional -> {self.adicional}")
        print(f"Tipo -> Alimento")

    def show(self):
        print(f"Nombre -> {self.nombre}")
        print(f"Precio -> {self.precio}$")
        print(f"Adicional -> {self.adicional}")
        print(f"IVA -> {self.IVA}$")
        print(f"Total -> {self.total}$")
        print(f"Tipo -> Alimento")
    
class Bebida(Producto):
    def __init__(self, nombre, precio, adicional):
        super().__init__(nombre, precio, adicional)
        self.type = "Bebida"
    
    def show_sin_iva(self):
        print(f"Nombre -> {self.nombre}")
        print(f"Precio -> {self.precio}$")
        print(f"Adicional -> {self.adicional}")
        print(f"Tipo -> Bebida")

    def show(self):
        print(f"Nombre -> {self.nombre}")
        print(f"Precio -> {self.precio}$")
        print(f"Adicional -> {self.adicional}")
        print(f"IVA -> {self.IVA}$")
        print(f"Total -> {self.total}$")
        print(f"Tipo -> Bebida")
    

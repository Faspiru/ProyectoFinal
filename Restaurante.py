class Restaurante():
    def __init__(self, nombre, productos):
        self.nombre = nombre
        self.productos = productos
    
    def show(self):
        print(f"-----Restaurante -> {self.nombre}-----")
        print()
        print(f"Productos -> ")
        print()
        for producto in self.productos:
            producto.show()
            print()
        

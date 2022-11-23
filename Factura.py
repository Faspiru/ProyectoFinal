class Factura():
    def __init__(self, nombre, cedula, edad):
        self.nombre = nombre
        self.cedula = cedula
        self.edad = edad

class FacturaTicket(Factura):
    def __init__(self, nombre, cedula, edad, tickets_comprados, subtotal, descuento, IVA, total):
        super().__init__(nombre, cedula, edad)
        self.tickets_comprados = tickets_comprados
        self.subtotal = subtotal
        self.descuento = descuento
        self.IVA = IVA
        self.total = total

    def show(self):
        print("-------------FACTURA-------------")
        print(f"Nombre Cliente -> {self.nombre}")
        print(f"Cedula Cliente -> {self.cedula}")
        print(f"Edad Cliente -> {self.edad}")
        print(f"Tickets Comprados -> ")
        for ticket in self.tickets_comprados:
            ticket.show()
        print("----------------------------------")
        print(f"Subtotal -> {self.subtotal}$")
        print(f"IVA -> {self.IVA}$")
        print(f"Descuento -> {self.descuento}$")
        print(f"Total a pagar -> {self.total}$")

class FacturaRestaurante(Factura):
    def __init__(self, nombre, cedula, edad, cuenta_dict, cuenta_productos):
        super().__init__(nombre, cedula, edad)
        self.cuenta_dict = cuenta_dict
        self.cuenta_productos = cuenta_productos
        self.subtotal = 0
        self.descuento = 0
        for producto in self.cuenta_productos:
            for dict in cuenta_dict:
                for key, value in dict.items():
                    if producto.nombre == key:
                        self.subtotal += producto.precio * value
        self.IVA = round(self.subtotal * 0.16, 2)
        self.total = self.subtotal + self.IVA
        divisores = [1]
        aux = 0
        for x in range(2, cedula):
            if cedula%x == 0:
                divisores.append(x)
        for y in divisores:
            aux += y
        if aux == cedula:
            self.descuento = round(self.total * 0.15, 2)
        self.total = self.total - self.descuento
    
    def show(self):
        print("-------------FACTURA-------------")
        print(f"Nombre Cliente -> {self.nombre}")
        print(f"Cedula Cliente -> {self.cedula}")
        print(f"Edad Cliente -> {self.edad}")
        print(f"Productos Comprados -> ")
        for producto in self.cuenta_dict:
            for key, value in producto.items():
                print(f"{key} --> Cantidad: {value}")
        print("----------------------------------")
        print(f"Subtotal -> {self.subtotal}$")
        print(f"IVA -> {self.IVA}$")
        print(f"Descuento -> {self.descuento}$")
        print(f"Total a pagar -> {self.total}$")




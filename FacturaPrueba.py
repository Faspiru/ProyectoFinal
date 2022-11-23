class Factura():
    def __init__(self, nombre, cedula, edad, tickets_comprados, subtotal, descuento, IVA, total):
        self.nombre = nombre
        self.cedula = cedula
        self.edad = edad
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
        print(f"Tickets Comprados-> ")
        for ticket in self.tickets_comprados:
            ticket.show()
        print("----------------------------------")
        print(f"Subtotal -> {self.subtotal}")
        print(f"IVA -> {self.IVA}")
        print(f"Descuento -> {self.descuento}")
        print(f"Total a pagar -> {self.total}")
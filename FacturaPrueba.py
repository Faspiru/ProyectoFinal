class Factura():
    def __init__(self, nombre, cedula, edad, ticket, subtotal, descuento, IVA, total):
        self.nombre = nombre
        self.cedula = cedula
        self.edad = edad
        self.ticket = ticket
        self.subtotal = subtotal
        self.descuento = descuento
        self.IVA = IVA
        self.total = total
    
    def show(self):
        print("-------------FACTURA-------------")
        print(f"Nombre Cliente -> {self.nombre}")
        print(f"Cedula Cliente -> {self.cedula}")
        print(f"Edad Cliente -> {self.edad}")
        print(f"Ticket -> {self.ticket.tipo_entrada}")
        print(f"Numero de Asiento -> {self.ticket.id_asiento}")
        print(f"Asistencia del cliente -> {self.ticket.asistencia}")
        print(f"Codigo Autentico -> {self.ticket.ticket_code}")
        print("Partido Comprado -> ")
        print()
        self.ticket.partido_cliente.show()
        print("----------------------------------")
        print(f"Subtotal -> {self.subtotal}")
        print(f"IVA -> {self.IVA}")
        print(f"Descuento -> {self.descuento}")
        print(f"Total a pagar -> {self.total}")
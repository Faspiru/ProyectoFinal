class Ticket():
    def __init__(self, partido_cliente, id_asiento, ticket_code):
        self.partido_cliente = partido_cliente
        self.id_asiento = id_asiento
        self.asistencia = "No asistio"
        self.ticket_code = ticket_code

class General(Ticket):
    def __init__(self, partido_cliente, id_asiento, ticket_code):
        super().__init__(partido_cliente, id_asiento, ticket_code)
        self.tipo_entrada = "General"
        self.precio = 50
    
    def show(self):
        print()
        self.partido_cliente.show()
        print(f"Id Asiento -> {self.id_asiento}")
        print(f"Tipo de Entrada -> {self.tipo_entrada}")
        print(f"Codigo Autentico -> {self.ticket_code}")
        print(f"Precio entrada -> {self.precio}")

class Vip(Ticket):
    def __init__(self, partido_cliente, id_asiento, ticket_code):
        super().__init__(partido_cliente, id_asiento, ticket_code)
        self.tipo_entrada = "VIP"
        self.precio = 120
    
    def show(self):
        print()
        self.partido_cliente.show()
        print(f"Id Asiento -> {self.id_asiento}")
        print(f"Tipo de Entrada -> {self.tipo_entrada}")
        print(f"Codigo Autentico -> {self.ticket_code}")
        print(f"Precio entrada -> {self.precio}")
        
        


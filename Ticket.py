class Ticket():
    def __init__(self, partido_cliente, id_asiento):
        self.partido_cliente = partido_cliente
        self.id_asiento = id_asiento
        self.asistencia = "No asistio"
class General(Ticket):
    def __init__(self, partido_cliente, id_asiento, asistencia):
        super().__init__(partido_cliente, id_asiento, asistencia)
        self.tipo_entrada = "General"
        self.precio = 50

class Vip(Ticket):
    def __init__(self, partido_cliente, id_asiento, asistencia):
        super().__init__(partido_cliente, id_asiento, asistencia)
        self.tipo_entrada = "VIP"
        self.precio = 120
        
        


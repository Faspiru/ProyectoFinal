class Cliente():
    def __init__(self, nombre, cedula, edad, partidos_comprados, tickets_comprados, factura_tickets):
        self.nombre = nombre
        self.cedula = cedula
        self.edad = edad
        self.partidos_comprados = partidos_comprados
        self.tickets_comprados = tickets_comprados
        self.factura_tickets = factura_tickets
        self.factura_restaurante = []
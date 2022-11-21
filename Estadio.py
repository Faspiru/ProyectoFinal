class Estadio():
    def __init__(self, id, nombre, capacidad, location, restaurantes):
        self.id = id
        self.nombre = nombre
        self.capacidad = capacidad
        self.location = location
        self.restaurantes = restaurantes
    
    def show(self):
        print(f"-----{self.nombre}-----")
        print(f"Id -> {self.id}")
        print(f"Capacidad -> {self.capacidad}")
        print(f"Location -> {self.location}")
        print(f"Restaurantes -> ")
        print()
        for restaurante in self.restaurantes:
            restaurante.show()
    
    def show_without_restaurant(self):
        print(f"-----{self.nombre}-----")
        print(f"Id -> {self.id}")
        print(f"Capacidad -> {self.capacidad}")
        print(f"Location -> {self.location}")

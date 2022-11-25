class Partido():
    def __init__(self, home_team, away_team, date, stadium_id, id):
        self.home_team = home_team
        self.away_team = away_team
        self.date = date
        self.stadium_id = stadium_id
        self.id = id
        self.asistencias = 0
        self.ventas = 0
    
    def show(self):
        print(f"--DATOS DEL PARTIDO #{self.id}--")
        print()
        print(f"Equipo Local -> {(self.home_team).nombre}")
        print(f"Equipo Visitante -> {(self.away_team).nombre}")
        print(f"Fecha y hora del partido -> {self.date}")
        print(f"Estadio -> {(self.stadium_id).nombre}")
        print()

    def show_stadistics(self):
        print()
        print(f"{(self.home_team.nombre).upper()}--{(self.away_team.nombre).upper()}")
        print(f"Fecha y hora del partido -> {self.date}")
        print(f"Estadio -> {(self.stadium_id).nombre}")
        print(f"Boletos Vendidos -> {self.ventas}")
        print(f"Personas Asistidas -> {self.asistencias}")
        if self.ventas == 0 :
            print(f"Relacion Asistencia/Venta -> 0")
        else:
            print(f"Relacion Asistencia/Venta -> {round(self.asistencias/self.ventas, 2)}")
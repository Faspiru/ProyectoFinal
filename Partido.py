class Partido():
    def __init__(self, home_team, away_team, date, stadium_id, id) -> None:
        self.home_team = home_team
        self.away_team = away_team
        self.date = date
        self.stadium_id = stadium_id
        self.id = id
    
    def show(self):
        print(f"--DATOS DEL PARTIDO #{self.id}--")
        print()
        print(f"Equipo Local -> {(self.home_team).nombre}")
        print(f"Equipo Visitante -> {(self.away_team).nombre}")
        print(f"Fecha y hora del partido -> {self.date}")
        print(f"Estadio -> {(self.stadium_id).nombre}")
        print()

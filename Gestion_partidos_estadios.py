import requests
from Equipo import Equipo
from Estadio import Estadio
from Producto import Comida, Bebida
from Restaurante import Restaurante
from Partido import Partido

## Con el siguiente codigo se busca transferir la estructura de datos 
## proporcionada en la api, a nuestro programa para poder utilizarla
urlEq = "https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-1/api-proyecto/main/teams.json"
rEq = requests.get(urlEq)
equipos_edd = rEq.json()

## A continuacion, se procede a crear los objetos de equipos
equipos = []
for equipo_dict in equipos_edd:
    equipo = Equipo(equipo_dict.get("name"), equipo_dict.get("flag"), equipo_dict.get("fifa_code"), equipo_dict.get("group"), equipo_dict.get("id"))
    equipos.append(equipo)

## Se procede a extraer los datos de los estadios
## a traves de la api
urlEs = "https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-1/api-proyecto/main/stadiums.json"
rEs = requests.get(urlEs)
estadios_edd = rEs.json()

## Con el siguiente codigo se crean los objetos estadios, restaurantes y sus respectivas ofertas
estadios = []
for estadios_dict in estadios_edd:
    for key, value in estadios_dict.items():
        if key == "restaurants":
            restaurantes = []
            for restaurantes_dict in value:
                for keyR, valueR in restaurantes_dict.items():
                    if keyR == "products":
                        productos = []
                        for products_dict in valueR:
                            if products_dict.get("type") == "beverages":
                                bebida = Bebida(products_dict.get("name"), products_dict.get("price"))
                                productos.append(bebida)
                            elif products_dict.get("type") == "food":
                                comida = Comida(products_dict.get("name"), products_dict.get("price"))
                                productos.append(comida)
                restaurante = Restaurante(restaurantes_dict.get("name"), productos)
                restaurantes.append(restaurante)
    estadio = Estadio(estadios_dict.get("id"), estadios_dict.get("name"), estadios_dict.get("capacity"), estadios_dict.get("location"), restaurantes)
    estadios.append(estadio)

## Se procede a extraer los datos de los partidos
## a traves de la api
urlPa = "https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-1/api-proyecto/main/matches.json"
rPa = requests.get(urlPa)
partidos_edd = rPa.json()

## Con el siguiente codigo se crean los objetos partido
partidos = []
for partidos_dict in partidos_edd:
    cont = 0
    for equipo in equipos:
        if equipo.nombre == partidos_dict.get("home_team"):
            home_team = equipo
            cont += 1
        if equipo.nombre == partidos_dict.get("away_team"):
            away_team = equipo
            cont += 1
        if cont == 2:
            break
    for estadio in estadios:
        if estadio.id == partidos_dict.get("stadium_id"):
            stadium_id = estadio
            break
    partido = Partido(home_team, away_team, partidos_dict.get("date"), stadium_id, partidos_dict.get("id"))
    partidos.append(partido)











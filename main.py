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

## La siguiente funcion realiza una busqueda de partidos segun el pais
def get_matches_equipos(partidos):
    pais = input("Escriba el nombre del pais que desea buscar sus partidos \n -> ").title()
    while not pais.isalpha():
        pais = input("Porfavor ingrese un pais valido. Escriba el nombre del pais que desea buscar sus partidos \n -> ").title()
    filtro_partidos_pais = []
    aux = False
    for partido in partidos:
        if partido.home_team.nombre == pais or partido.away_team.nombre == pais:
            filtro_partidos_pais.append(partido)
            aux = True
    if aux == False:
        if pais == "Italia":
            print()
            print("Tranquilo hermano, todos sabemos que italia es la mejor del mundo, lamentable lo de su ausencia este mundial \U0001F614\N{raised fist}")
            print()
        else:
            print()
            print("El pais seleccionado no forma parte del mundial de futbol 2022. Intente buscar nuevamente con otro pais")
            print()
    return filtro_partidos_pais

## La siguiente funcion realiza una busqueda de partidos segun el estadio
def get_matches_estadio(partidos):
    estadio_selection = input("Escoga el estadio del que desea filtrar los partidos \n 1. Al Bayt Stadium \n 2. Lusail Stadium \n 3. Ahmad Bin Ali Stadium \n 4. Al Janoub Stadium \n 5. Al Thumama Stadium \n 6. Education City Stadium \n 7. Khalifa International Stadium \n 8. Stadium 974 \n --> ")
    while not estadio_selection.isnumeric() or not int(estadio_selection) in range(1, 9):
        estadio_selection = input("Porfavor ingrese una opcion valida. Escoga el estadio del que desea filtrar los partidos \n 1. Al Bayt Stadium \n 2. Lusail Stadium \n 3. Ahmad Bin Ali Stadium \n 4. Al Janoub Stadium \n 5. Al Thumama Stadium \n 6. Education City Stadium \n 7. Khalifa International Stadium \n 8. Stadium 974 \n --> ")
    estadio_selection = int(estadio_selection)
    filtro_partidos_estadio = []
    for partido in partidos:
        if partido.stadium_id.id == estadio_selection:
            filtro_partidos_estadio.append(partido)
    return filtro_partidos_estadio

## Funcion para obtener el mapa del estadio con id 1
def get_stadium_id1():
    pass

## La siguiente funcion realiza una busqueda de partidos segun la fecha y hora
def get_matches_fecha(partidos):
    fecha = input("Ingrese la fecha y hora de los partidos que desea visualizar \n --> ")
    while fecha.isalpha() or not fecha.count("/") == 2 or not fecha.count(" ") == 1 or not fecha.count(":") == 1 or not len(fecha) in range(15, 17):
        fecha = input("Porfavor ingrese una hora y fecha valida. Ingrese la fecha y hora de los partidos que desea visualizar \n --> ")
    filtro_partidos_fecha = []
    aux2 = False
    for partido in partidos:
        if partido.date == fecha:
            filtro_partidos_fecha.append(partido)
            aux2 = True
    if aux2 == False:
        print()
        print("No se pudieron encontrar partidos debido a un error desconocido, intente nuevamente colocando una fecha valida")
        print()
    return filtro_partidos_fecha

## La siguiente funcion recolecta datos del cliente
def get_client_data(partidos):
    nombre_cliente = input("Porfavor ingrese su nombre completo \n --> ") 
    while not nombre_cliente.isalpha or nombre_cliente.count(" ") > 4:
        nombre_cliente = input("Porfavor ingrese un nombre valido. Ingrese su nombre completo \n --> ")
    
    cedula_cliente = input("Porfavor ingrese su cedula de identidad \n --> ")
    while not cedula_cliente.isnumeric():
        cedula_cliente = input("Porfavor ingrese una cedula valida. Ingrese su cedula de identidad \n --> ")
    cedula_cliente = int(cedula_cliente)
    
    edad_cliente = input("Porfavor ingrese su edad \n --> ")
    while not int(edad_cliente) in range(1, 105):
        edad_cliente = input("Porfavor ingrese una edad valida. Ingrese su edad \n --> ")
    edad_cliente = int(edad_cliente)

    for partido in partidos:
        partido.show()
    id_partido = input("Porfavor ingrese el id del partido que desea comprar el ticket \n --> ")
    while not id_partido.isnumeric() or not int(id_partido) in range (1, 49):
        id_partido = input("Porfavor ingrese un partido valido. Ingrese el id del partido que desea comprar \n --> ")
    for partido in partidos:
        if partido.id == id_partido:
            partido_cliente = partido
            break
    
    option_entrada_cliente = input("Porfavor esocga el tipo de entrada que desea \n 1. General 50$ \n 2. VIP 120$ \n --> ")
    while not option_entrada_cliente.isnumeric() or not int(entrada_cliente) in range(1, 3):
        entrada_cliente = "General" if option_entrada_cliente == "1" else "VIP"
    if entrada_cliente == "General":
        precio_cliente = 50
    else:
        precio_cliente = 120
    



## A continuacion se encuentra la funcion main, que la funcionalidad a todo el programa
def main():
    while True:
        print("\N{soccer ball} BIENVENIDO AL SISTEMA DEL MUNDIAL DE FUTBOL QATAR 2022 \N{soccer ball}")
        print()
        option = input("A que modulo desea acceder? \n 1. Gestion de partidos y estadios \N{stadium} \n 2. Gestion de venta de entradas \N{ticket} \n 3. Gestion de asistencia de partidos \N{telephone receiver} \n 4. Gestion de restaurantes \N{fork and knife with plate} \n 5. Gestion de venta de restaurantes \N{money with wings} \n 6. Indicadores de gestion (estadisticas) \N{bar chart} \n 7. Salir \n --> ")
        while not option.isnumeric() or not int(option) in range(1, 8):
            option = input("Porfavor ingrese una opcion valida. A que modulo desea acceder? \n 1. Gestion de partidos y estadios \N{stadium} \n Gestion de venta de entradas \N{ticket} \n 3. Gestion de asistencia de partidos \N{telephone receiver} \n 4. Gestion de restaurantes \N{fork and knife with plate} \n 5. Gestion de venta de restaurantes \N{money with wings} \n 6. Indicadores de gestion (estadisticas) \N{bar chart} \n 7. Salir \n -->  ")
        if option == "1":
            while True:
                print("\U0001F50D BUSQUEDA DE PARTIDOS \U0001F50D")
                print()
                option1 = input("Que desea realizar? \n 1. Buscar todos los partidos de un pais \n 2. Buscar todos los partidos que se jugaran en un estadio especifico \n 3. Buscar todos los partidos que se jugaran en una fecha determinada \n 4. Salir \n --> ")
                while not option1.isnumeric() or not int(option1) in range(1, 5):
                    option1 = input("Porfavor ingrese una opcion valida. Que desea realizar? \n 1. Buscar todos los partidos de un pais \n 2. Buscar todos los partidos que se jugaran en un estadio especifico \n 3. Buscar todos los partidos que se jugaran en una fecha determinada \n 4. Salir \n --> ")
                if option1 == "1":
                    filtro_partidos_pais = get_matches_equipos(partidos)
                    if filtro_partidos_pais != []:
                        for partidos_encontrados in filtro_partidos_pais:
                            partidos_encontrados.show()
                if option1 == "2":
                    filtro_partidos_estadio = get_matches_estadio(partidos)
                    if filtro_partidos_estadio != []:
                        for partidos_encontrados_estadio in filtro_partidos_estadio:
                            partidos_encontrados_estadio.show()
                if option1 == "3":
                    filtro_partidos_fecha = get_matches_fecha(partidos)
                    if filtro_partidos_fecha != []:
                        for partidos_encontrados_fecha in filtro_partidos_fecha:
                            partidos_encontrados_fecha.show()
                if option1 == "4":
                    break
        if option == "2":
            pass
        if option == "3":
            pass
        if option == "4":
            pass
        if option == "5":
            pass
        if option == "6":
            pass
        if option == "7":
            break
main()
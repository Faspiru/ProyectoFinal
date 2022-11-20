import requests
from colorama import *
from Equipo import Equipo
from Estadio import Estadio
from Producto import Comida, Bebida
from Restaurante import Restaurante
from Partido import Partido
from Ticket import General, Vip
from Cliente import Cliente
from Factura import Factura

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


def get_mapa_estadio(x, tickets_ocupados, partido_cliente):
    taken = []
    for ticket in tickets_ocupados:
        if ticket.partido_comprado == partido_cliente:
            taken.append(ticket.id_asiento)

    for a in range(x[0]):
        fila = []
        for b in range(x[1]):
            if f"{a}{b}" not in taken:
                changed_color = (f"{Fore.GREEN} {a}{b}")
                fila.append(changed_color)
            else:
                changed_color = (f"{Fore.RED} X ")
                fila.append(changed_color)       
        print(" ".join(fila))
        print()
    print(Style.RESET_ALL)  


def get_IVA(ticket):
    IVA = ticket.precio * 0.16
    return IVA

    
def get_discount(cedula, ticket):
    if cedula == 1:
        discount = ticket.precio * 0.50
    else: 
        discount = 0

    return discount    
        
def get_total(subtotal, discount, IVA):
    total = subtotal + IVA - discount
    return total


def get_client_data(partidos, clientes):
    nombre_cliente = input("Porfavor ingrese su nombre completo \n --> ") 
    while not nombre_cliente.isalpha or nombre_cliente.count(" ") > 4:
        nombre_cliente = input("Porfavor ingrese un nombre valido. Ingrese su nombre completo \n --> ")

    if clientes != []:
        for cliente in clientes:
            if cliente.nombre == nombre_cliente:
                print(f"---BIENVENIDO de nuevo {nombre_cliente}---")
                print()
                for partido in partidos:
                    partido.show()
                id_partido = input("Porfavor ingrese el id del partido que desea comprar el ticket \n --> ")
                while not id_partido.isnumeric() or not int(id_partido) in range (1, 49):
                    id_partido = input("Porfavor ingrese un partido valido. Ingrese el id del partido que desea comprar \n --> ")
                for partido in partidos:
                    if partido.id == id_partido:
                        partido_cliente = partido
                        break 

                option_ticket_cliente = input("Porfavor esocga el tipo de entrada que desea \n 1. General 50$ \n 2. VIP 120$ \n --> ")
                while not option_ticket_cliente.isnumeric() or not int(option_ticket_cliente) in range(1, 3):
                    option_ticket_cliente = input("Porfavor ingrese un tipo de entrada valido. Esocga el tipo de entrada que desea \n 1. General 50$ \n 2. VIP 120$ \n --> ")
                
                for partido in partidos:
                    if partido.id == id_partido:
                        estadio_selected = partido.stadium_id
                        get_mapa_estadio(estadio_selected.capacidad, tickets_comprados, partido_cliente)
                    
                id_asiento = input("Anteriormente se mostro un mapa del estadio, porfavor ingrese el asiento que desea comprar \n --> ")
                while not id_asiento.isnumeric():
                    id_asiento = input("Anteriormente se mostro un mapa del estadio, porfavor ingrese el asiento que desea comprar \n --> ")
                
                if option_ticket_cliente == "1":
                    ticket = General(partido_cliente, id_asiento)
                else:
                    ticket = Vip(partido_cliente, id_asiento)
                
                subtotal = ticket.precio
                descuento = get_discount(cedula_cliente, ticket)
                IVA = get_IVA(ticket)
                total = get_total(subtotal, descuento, IVA)

                factura = Factura(nombre_cliente, cedula_cliente, edad_cliente, ticket, subtotal, descuento, IVA, total)
                factura.show()
                final_option = input("Desea continuar con su pago y generar el ticket? \n 1. SI \n 2. NO \n --> ")
                while not final_option.isnumeric() or not int(final_option) in range(1, 3):
                    final_option = input("Porfavor ingrese una opcion valida. Desea continuar con su pago y generar el ticket? \n 1. SI \n 2. NO \n --> ")
                if final_option == "1":
                    print(f"{Fore.GREEN} Compra realizada exitosamente")
                    print(Style.RESET_ALL)
                    cliente.tickets_comprados.append(ticket)
                    cliente.partidos_comprados.append(partido_cliente)
                    return ticket
                else:
                    print(f"{Fore.RED} Se ha cancelado su compra") 
                    print(Style.RESET_ALL)
            else:
                cedula_cliente = input("Porfavor ingrese su cedula de identidad \n --> ")
                while not cedula_cliente.isnumeric():
                    cedula_cliente = input("Porfavor ingrese una cedula valida. Ingrese su cedula de identidad \n --> ")
                cedula_cliente = int(cedula_cliente)
                
                edad_cliente = input("Porfavor ingrese su edad \n --> ")
                while not int(edad_cliente) in range(1, 105):
                    edad_cliente = input("Porfavor ingrese una edad valida. Ingrese su edad \n --> ")
                edad_cliente = int(edad_cliente)

                partidos_comprados = []
                for partido in partidos:
                    partido.show()
                id_partido = input("Porfavor ingrese el id del partido que desea comprar el ticket \n --> ")
                while not id_partido.isnumeric() or not int(id_partido) in range (1, 49):
                    id_partido = input("Porfavor ingrese un partido valido. Ingrese el id del partido que desea comprar \n --> ")
                for partido in partidos:
                    if partido.id == id_partido:
                        partido_cliente = partido
                        break 

                option_ticket_cliente = input("Porfavor esocga el tipo de entrada que desea \n 1. General 50$ \n 2. VIP 120$ \n --> ")
                while not option_ticket_cliente.isnumeric() or not int(option_ticket_cliente) in range(1, 3):
                    option_ticket_cliente = input("Porfavor ingrese un tipo de entrada valido. Esocga el tipo de entrada que desea \n 1. General 50$ \n 2. VIP 120$ \n --> ") 
                
                for partido in partidos:
                    if partido.id == id_partido:
                        estadio_selected = partido.stadium_id
                        get_mapa_estadio(estadio_selected.capacidad, tickets_comprados, partido_cliente)
                        
                id_asiento = input("Anteriormente se mostro un mapa del estadio, porfavor ingrese el asiento que desea comprar \n --> ")
                while not id_asiento.isnumeric():
                    id_asiento = input("Anteriormente se mostro un mapa del estadio, porfavor ingrese el asiento que desea comprar \n --> ")
                
                tickets_comprados = []
                if option_ticket_cliente == "1":
                    ticket = General(partido_cliente, id_asiento)
                else:
                    ticket = Vip(partido_cliente, id_asiento)

                subtotal = ticket.precio
                descuento = get_discount(cedula_cliente, ticket)
                IVA = get_IVA(ticket)
                total = get_total(subtotal, descuento, IVA)

                factura = Factura(nombre_cliente, cedula_cliente, edad_cliente, ticket, subtotal, descuento, IVA, total)
                factura.show()
                final_option = input("Desea continuar con su pago y generar el ticket? \n 1. SI \n 2. NO \n --> ")
                while not final_option.isnumeric() or not int(final_option) in range(1, 3):
                    final_option = input("Porfavor ingrese una opcion valida. Desea continuar con su pago y generar el ticket? \n 1. SI \n 2. NO \n --> ")
                if final_option == "1":
                    print(f"{Fore.GREEN} Compra realizada exitosamente")
                    print(Style.RESET_ALL)
                    tickets_comprados.append(ticket)
                    partidos_comprados.append(partido_cliente)
                    cliente = Cliente(nombre_cliente, cedula_cliente, edad_cliente, partidos_comprados, tickets_comprados)
                    return cliente, ticket
                else:
                    print(f"{Fore.RED} Se ha cancelado su compra") 
                    print(Style.RESET_ALL)
    else:
        cedula_cliente = input("Porfavor ingrese su cedula de identidad \n --> ")
        while not cedula_cliente.isnumeric():
            cedula_cliente = input("Porfavor ingrese una cedula valida. Ingrese su cedula de identidad \n --> ")
        cedula_cliente = int(cedula_cliente)
        
        edad_cliente = input("Porfavor ingrese su edad \n --> ")
        while not int(edad_cliente) in range(1, 105):
            edad_cliente = input("Porfavor ingrese una edad valida. Ingrese su edad \n --> ")
        edad_cliente = int(edad_cliente)

        partidos_comprados = []
        for partido in partidos:
            partido.show()
        id_partido = input("Porfavor ingrese el id del partido que desea comprar el ticket \n --> ")
        while not id_partido.isnumeric() or not int(id_partido) in range (1, 49):
            id_partido = input("Porfavor ingrese un partido valido. Ingrese el id del partido que desea comprar \n --> ")
        for partido in partidos:
            if partido.id == id_partido:
                partido_cliente = partido
                break 

        option_ticket_cliente = input("Porfavor esocga el tipo de entrada que desea \n 1. General 50$ \n 2. VIP 120$ \n --> ")
        while not option_ticket_cliente.isnumeric() or not int(option_ticket_cliente) in range(1, 3):
            option_ticket_cliente = input("Porfavor ingrese un tipo de entrada valido. Esocga el tipo de entrada que desea \n 1. General 50$ \n 2. VIP 120$ \n --> ") 
        
        for partido in partidos:
            if partido.id == id_partido:
                estadio_selected = partido.stadium_id
                get_mapa_estadio(estadio_selected.capacidad, tickets_ocupados, partido_cliente)
                
        id_asiento = input("Anteriormente se mostro un mapa del estadio, porfavor ingrese el asiento que desea comprar \n --> ")
        while not id_asiento.isnumeric():
            id_asiento = input("Anteriormente se mostro un mapa del estadio, porfavor ingrese el asiento que desea comprar \n --> ")
        
        tickets_comprados = []
        if option_ticket_cliente == "1":
            ticket = General(partido_cliente, id_asiento)
        else:
            ticket = Vip(partido_cliente, id_asiento)

        subtotal = ticket.precio
        descuento = get_discount(cedula_cliente, ticket)
        IVA = get_IVA(ticket)
        total = get_total(subtotal, descuento, IVA)

        factura = Factura(nombre_cliente, cedula_cliente, edad_cliente, ticket, subtotal, descuento, IVA, total)
        factura.show()
        final_option = input("Desea continuar con su pago y generar el ticket? \n 1. SI \n 2. NO \n --> ")
        while not final_option.isnumeric() or not int(final_option) in range(1, 3):
            final_option = input("Porfavor ingrese una opcion valida. Desea continuar con su pago y generar el ticket? \n 1. SI \n 2. NO \n --> ")
        if final_option == "1":
            print(f"{Fore.GREEN} Compra realizada exitosamente")
            print(Style.RESET_ALL)
            tickets_comprados.append(ticket)
            partidos_comprados.append(partido_cliente)
            cliente = Cliente(nombre_cliente, cedula_cliente, edad_cliente, partidos_comprados, tickets_comprados)
            return cliente, ticket
        else:
            print(f"{Fore.RED} Se ha cancelado su compra") 
            print(Style.RESET_ALL)
            cliente = None
            ticket = None
            return cliente, ticket

tickets_ocupados = []
clientes = []
cliente, ticket = get_client_data(partidos, clientes)   
clientes.append(cliente)
tickets_ocupados.append(ticket)




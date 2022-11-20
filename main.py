import requests
from itertools import permutations
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

## La siguiente funcion realiza una busqueda de partidos segun la fecha y hora
def get_matches_fecha(partidos):
    fecha = input("Ingrese la fecha y hora de los partidos que desea visualizar \n --> ")
    while fecha.isalpha() or not fecha.count("/") == 2 or not fecha.count(" ") in range(0,2) or not fecha.count(":") in range(0,2) or not len(fecha) in range(15, 17) and not len(fecha) in range(9,11):
        fecha = input("Porfavor ingrese una hora y fecha valida. Ingrese la fecha y hora de los partidos que desea visualizar \n --> ")
    filtro_partidos_fecha = []
    aux2 = False
    for partido in partidos:
        if fecha in partido.date:
            filtro_partidos_fecha.append(partido)
            aux2 = True
    if aux2 == False:
        print()
        print("No se pudieron encontrar partidos debido a un error desconocido, intente nuevamente colocando una fecha valida")
        print()
    return filtro_partidos_fecha

## Funcion para obtener el mapa del estadio con id 1
def get_mapa_estadio(x, tickets_ocupados, partido_cliente):
    taken = []
    for ticket in tickets_ocupados:
        if ticket.partido_cliente == partido_cliente:
            taken.append(ticket.id_asiento)

    asientos_libres = []
    for a in range(x[0]):
        fila = []
        for b in range(x[1]):
            if f"{a}{b}" not in taken:
                changed_color = (f"{Fore.GREEN} {a}{b}")
                fila.append(changed_color)
                asientos_libres.append(f"{a}{b}")
            else:
                changed_color = (f"{Fore.RED} X ")
                fila.append(changed_color)       
        print(" ".join(fila))
        print()
    print(Style.RESET_ALL)
    return asientos_libres

## Funcion para verificar si un numero es vampiro
def is_numero_vampiro(cedula):
    cedula = str(cedula)
    cont = 0
    for permutaciones in permutations(cedula):
        digitos_separados = "".join(permutaciones)
        primera_parte = digitos_separados[:int(len(digitos_separados)//2)]
        segunda_parte = digitos_separados[int(len(digitos_separados)//2):]
        primera_parte = int(primera_parte)
        segunda_parte = int(segunda_parte)
        if primera_parte * segunda_parte == int(cedula):
            cont+=1
    if cont != 0:
        return True
    else:
        return False

## Funcion para obtener el IVA
def get_IVA(ticket):
    IVA = ticket.precio * 0.16
    return IVA

## Funcion para obtener el descuento (si aplica)
def get_discount(cedula, ticket):
    if is_numero_vampiro(cedula):
        discount = ticket.precio * 0.50
    else: 
        discount = 0

    return discount    

## Funcion para obtener el total de la compra
def get_total(subtotal, discount, IVA):
    total = subtotal + IVA - discount
    return total

## La siguiente funcion recolecta datos del cliente
def get_client_data(partidos, clientes, tickets_ocupados):
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
                        asientos_libre = get_mapa_estadio(estadio_selected.capacidad, tickets_ocupados, partido_cliente)
                    
                id_asiento = input("Anteriormente se mostro un mapa del estadio, porfavor ingrese el asiento que desea comprar \n --> ")
                while not id_asiento.isnumeric() or not id_asiento in asientos_libre:
                    id_asiento = input("Porfavor ingrese un asiento libre y disponible. Ingrese nuevamente el asiento que desea comprar \n --> ")
                
                if option_ticket_cliente == "1":
                    ticket = General(partido_cliente, id_asiento)
                else:
                    ticket = Vip(partido_cliente, id_asiento)
                
                subtotal = ticket.precio
                descuento = get_discount(cliente.cedula, ticket)
                IVA = get_IVA(ticket)
                total = get_total(subtotal, descuento, IVA)

                factura = Factura(cliente.nombre, cliente.cedula, cliente.edad, ticket, subtotal, descuento, IVA, total)
                factura.show()
                final_option = input("Desea continuar con su pago y generar el ticket? \n 1. SI \n 2. NO \n --> ")
                while not final_option.isnumeric() or not int(final_option) in range(1, 3):
                    final_option = input("Porfavor ingrese una opcion valida. Desea continuar con su pago y generar el ticket? \n 1. SI \n 2. NO \n --> ")
                if final_option == "1":
                    print(f"{Fore.GREEN} Compra realizada exitosamente")
                    print(Style.RESET_ALL)
                    cliente.tickets_comprados.append(ticket)
                    cliente.partidos_comprados.append(partido_cliente)
                    cliente.facturas.append(factura)
                    cliente = None
                    return cliente, ticket
                else:
                    print(f"{Fore.RED} Se ha cancelado su compra") 
                    print(Style.RESET_ALL)
                    cliente = None
                    ticket = None
                    return cliente, ticket
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
                        asientos_libre = get_mapa_estadio(estadio_selected.capacidad, tickets_ocupados, partido_cliente)
                        break
                        
                id_asiento = input("Anteriormente se mostro un mapa del estadio, porfavor ingrese el asiento que desea comprar \n --> ")
                while not id_asiento.isnumeric() or not id_asiento in asientos_libre:
                    id_asiento = input("Porfavor ingrese un asiento libre y disponible. Ingrese nuevamente el asiento que desea comprar \n --> ")
                
                tickets_comprados = []
                if option_ticket_cliente == "1":
                    ticket = General(partido_cliente, id_asiento)
                else:
                    ticket = Vip(partido_cliente, id_asiento)

                subtotal = ticket.precio
                descuento = get_discount(cedula_cliente, ticket)
                IVA = get_IVA(ticket)
                total = get_total(subtotal, descuento, IVA)

                facturas = []
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
                    facturas.append(factura)
                    cliente = Cliente(nombre_cliente, cedula_cliente, edad_cliente, partidos_comprados, tickets_comprados, facturas)
                    return cliente, ticket
                else:
                    print(f"{Fore.RED} Se ha cancelado su compra") 
                    print(Style.RESET_ALL)
                    cliente = None
                    ticket = None
                    return cliente, ticket
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
                asientos_libre = get_mapa_estadio(estadio_selected.capacidad, tickets_ocupados, partido_cliente)
                break
                
        id_asiento = input("Anteriormente se mostro un mapa del estadio, porfavor ingrese el asiento que desea comprar \n --> ")
        while not id_asiento.isnumeric() or not id_asiento in asientos_libre:
            id_asiento = input("Porfavor ingrese un asiento libre. Ingrese nuevamente el asiento que desea comprar \n --> ")
        
        tickets_comprados = []
        if option_ticket_cliente == "1":
            ticket = General(partido_cliente, id_asiento)
        else:
            ticket = Vip(partido_cliente, id_asiento)

        subtotal = ticket.precio
        descuento = get_discount(cedula_cliente, ticket)
        IVA = get_IVA(ticket)
        total = get_total(subtotal, descuento, IVA)

        facturas = []
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
            facturas.append(factura)
            cliente = Cliente(nombre_cliente, cedula_cliente, edad_cliente, partidos_comprados, tickets_comprados, facturas)
            return cliente, ticket
        else:
            print(f"{Fore.RED} Se ha cancelado su compra") 
            print(Style.RESET_ALL)
            cliente = None
            ticket = None
            return cliente, ticket
    
## A continuacion se encuentra la funcion main, que la funcionalidad a todo el programa
def main():
    clientes = []
    tickets_ocupados = []
    while True:
        print()
        print("\N{soccer ball} BIENVENIDO AL SISTEMA DEL MUNDIAL DE FUTBOL QATAR 2022 \N{soccer ball}")
        print()
        option = input("A que modulo desea acceder? \n 1. Gestion de partidos y estadios \N{stadium} \n 2. Gestion de venta de entradas \N{ticket} \n 3. Gestion de asistencia de partidos \N{telephone receiver} \n 4. Gestion de restaurantes \N{fork and knife with plate} \n 5. Gestion de venta de restaurantes \N{money with wings} \n 6. Indicadores de gestion (estadisticas) \N{bar chart} \n 7. Salir \n --> ")
        while not option.isnumeric() or not int(option) in range(1, 8):
            option = input("Porfavor ingrese una opcion valida. A que modulo desea acceder? \n 1. Gestion de partidos y estadios \N{stadium} \n Gestion de venta de entradas \N{ticket} \n 3. Gestion de asistencia de partidos \N{telephone receiver} \n 4. Gestion de restaurantes \N{fork and knife with plate} \n 5. Gestion de venta de restaurantes \N{money with wings} \n 6. Indicadores de gestion (estadisticas) \N{bar chart} \n 7. Salir \n -->  ")

        ## MODULO 1     
        if option == "1":
            while True:
                print("\U0001F50D BUSQUEDA DE PARTIDOS \U0001F50D")
                print()
                option1 = input("Que desea realizar? \n 1. Buscar todos los partidos de un pais \n 2. Buscar todos los partidos que se jugaran en un estadio especifico \n 3. Buscar todos los partidos que se jugaran en una fecha determinada \n 4. Salir del modulo \n --> ")
                while not option1.isnumeric() or not int(option1) in range(1, 5):
                    option1 = input("Porfavor ingrese una opcion valida. Que desea realizar? \n 1. Buscar todos los partidos de un pais \n 2. Buscar todos los partidos que se jugaran en un estadio especifico \n 3. Buscar todos los partidos que se jugaran en una fecha determinada \n 4. Salir del modulo \n --> ")
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

        ## MODULO 2        
        if option == "2":
            while True:
                print()
                print("\U0001F4B5 VENTA DE ENTRADAS \U0001F4B5")
                print()
                option2 = input("Que desea realizar? \n 1. Comprar entradas \n 2. Salir del modulo \n --> ")
                while not option2.isnumeric() or not int(option2) in range(1, 3):
                     option2 = input("Porfavor seleccione una opcion valida. Que desea realizar? \n 1. Comprar ebtradas \n 2. Salir \n --> ")
                if option2 == "1":
                    cliente, ticket = get_client_data(partidos, clientes, tickets_ocupados)
                    if cliente != None:   
                        clientes.append(cliente)
                    if ticket != None:
                        tickets_ocupados.append(ticket)   
                else:
                    break   
        if option == "3":
            while True:
                print()
                print("\U0001F64B BIENVENIDO AL MODULO DE ASISTENCIA DE PARTIDOS \U0001F64B")
                print()
                option3 = input("Que desea realizar? \n 1. Ingresar a un partido validando su boleto \n 2. Salir del modulo \n --> ")
                

        if option == "4":
            pass
        if option == "5":
            pass
        if option == "6":
            pass
        if option == "7":
            break
main()
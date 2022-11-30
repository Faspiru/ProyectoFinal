import requests
import matplotlib.pyplot as plt
import pickle5 as pickle
from itertools import permutations
from colorama import *
from Equipo import Equipo
from Estadio import Estadio
from Producto import Alimento, Bebida
from Restaurante import Restaurante
from Partido import Partido
from Ticket import General, Vip
from Cliente import Cliente
from Factura import FacturaTicket, FacturaRestaurante

## Con el siguiente codigo se busca transferir la estructura de datos proporcionada en la api, a nuestro programa para poder utilizarla
def get_equipos():
    urlEq = "https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-1/api-proyecto/main/teams.json"
    rEq = requests.get(urlEq)
    equipos_edd = rEq.json()

    equipos = []
    for equipo_dict in equipos_edd:
        equipo = Equipo(equipo_dict.get("name"), equipo_dict.get("flag"), equipo_dict.get("fifa_code"), equipo_dict.get("group"), equipo_dict.get("id"))
        equipos.append(equipo)
    return equipos

## Se procede a extraer los datos de los estadios a traves de la api
def get_estadios():
    urlEs = "https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-1/api-proyecto/main/stadiums.json"
    rEs = requests.get(urlEs)
    estadios_edd = rEs.json()

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
                                    bebida = Bebida(products_dict.get("name"), products_dict.get("price"), products_dict.get("adicional"), products_dict.get("quantity"))
                                    productos.append(bebida)
                                elif products_dict.get("type") == "food":
                                    alimento = Alimento(products_dict.get("name"), products_dict.get("price"), products_dict.get("adicional"), products_dict.get("quantity"))
                                    productos.append(alimento)
                    restaurante = Restaurante(restaurantes_dict.get("name"), productos)
                    restaurantes.append(restaurante)
        estadio = Estadio(estadios_dict.get("id"), estadios_dict.get("name"), estadios_dict.get("capacity"), estadios_dict.get("location"), restaurantes)
        estadios.append(estadio)
    return estadios

## Se procede a extraer los datos de los partidos  a traves de la api
def get_partidos(equipos, estadios):
    urlPa = "https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-1/api-proyecto/main/matches.json"
    rPa = requests.get(urlPa)
    partidos_edd = rPa.json()

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
    return partidos

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
        if pais == "Italia" or pais == "Italy":
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
        if ticket.partido_cliente.id == partido_cliente.id:
            taken.append(ticket.id_asiento)

    asientos_libres = []
    for a in range(int(x/10)):
        fila = []
        for b in range(10):
            if f"{a}{b}" not in taken:
                changed_color = (f"{Fore.BLUE}|{Fore.GREEN} {a}{b}")
                fila.append(changed_color)
                asientos_libres.append(f"{a}{b}")
            else:
                changed_color = (f"{Fore.BLUE}|{Fore.RED} XX")
                fila.append(changed_color)       
        print(" ".join(fila))
        print()
    print(Style.RESET_ALL)
    return asientos_libres

## Funcion para verificar si un numero es vampiro
def is_numero_vampiro(cedula):
    cedula = str(cedula)
    cont = 0
    if len(cedula) != 1:
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

## Funcion para obtener el subtotal 
def get_subtotal(tickets_comprados):
    subtotal = 0
    for ticket in tickets_comprados:
        subtotal += ticket.precio
    return subtotal

## Funcion para obtener el IVA
def get_IVA(subtotal):
    IVA = subtotal * 0.16
    return IVA

## Funcion para obtener el descuento (si aplica)
def get_discount(cedula, subtotal, IVA):
    if is_numero_vampiro(cedula):
        discount = (subtotal+IVA) * 0.50
    else: 
        discount = 0
    return discount     

## Funcion para obtener el total de la compra
def get_total(subtotal, discount, IVA):
    total = subtotal + IVA - discount
    return total

## La siguiente funcion recolecta datos del cliente
def get_client_data(partidos, tickets_ocupados, tickets_ocupados_general, tickets_ocupados_VIP, clientes):
    lista_cedulas_registradas = []

    if clientes != []:
        for cliente in clientes:
            lista_cedulas_registradas.append(cliente.cedula)

    nombre_cliente = input("Porfavor ingrese su nombre completo \n --> ").title()
    cliente_list = nombre_cliente.split(" ")
    nombre_junto = "".join(cliente_list)
    while not nombre_junto.isalpha() or nombre_cliente.count(" ") > 4:
        nombre_cliente = input("Porfavor ingrese un nombre valido. Ingrese su nombre completo \n --> ").title()
        cliente_list = nombre_cliente.split(" ")
        nombre_junto = "".join(cliente_list)

    cedula_cliente = input("Porfavor ingrese su cedula de identidad \n --> ")
    while not cedula_cliente.isnumeric() or int(cedula_cliente) in lista_cedulas_registradas:
        cedula_cliente = input("Porfavor ingrese una cedula valida y que no haya sido registrada. Ingrese su cedula de identidad \n --> ")
    cedula_cliente = int(cedula_cliente)
    
    edad_cliente = input("Porfavor ingrese su edad \n --> ")
    while not edad_cliente.isnumeric() or not int(edad_cliente) in range(1, 119):
        edad_cliente = input("Porfavor ingrese una edad valida. Ingrese su edad \n --> ")
    edad_cliente = int(edad_cliente)

    partidos_comprados = []
    tickets_comprados = []
    tickets_general_comprados = []
    tickets_VIP_comprados = []

    while True:
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
                if option_ticket_cliente == "1":
                    asientos_libres_general = get_mapa_estadio(estadio_selected.capacidad[0], tickets_ocupados_general, partido_cliente)
                else:
                    asientos_libres_VIP = get_mapa_estadio(estadio_selected.capacidad[1], tickets_ocupados_VIP, partido_cliente)
                break
        
        if option_ticket_cliente == "1": 
            if asientos_libres_general != []:      
                id_asiento = input("Anteriormente se mostro un mapa del estadio, porfavor ingrese el asiento que desea comprar \n --> ")
                while not id_asiento.isnumeric() or not id_asiento in asientos_libres_general:
                    id_asiento = input("Porfavor ingrese un asiento libre. Ingrese nuevamente el asiento que desea comprar \n --> ")
            else:
                print("No hay asientos disponibles, todos estan ocupados")
                print()
        else:
            if asientos_libres_VIP != []:
                id_asiento = input("Anteriormente se mostro un mapa del estadio, porfavor ingrese el asiento que desea comprar \n --> ")
                while not id_asiento.isnumeric() or not id_asiento in asientos_libres_VIP:
                    id_asiento = input("Porfavor ingrese un asiento libre. Ingrese nuevamente el asiento que desea comprar \n --> ")
            else:
                print("No hay asientos disponibles, todos estan ocupados")
                print()

        partidos_comprados.append(partido_cliente)

        if option_ticket_cliente == "1": 
            ticket_code = (f"{partido_cliente.home_team.codigo_fifa}-{partido_cliente.away_team.codigo_fifa}-G-{id_partido}{id_asiento}") 
        else:
            ticket_code = (f"{partido_cliente.home_team.codigo_fifa}-{partido_cliente.away_team.codigo_fifa}-V-{id_partido}{id_asiento}")

        if option_ticket_cliente == "1":
            ticket = General(partido_cliente, id_asiento, ticket_code)
        else:
            ticket = Vip(partido_cliente, id_asiento, ticket_code)

        if option_ticket_cliente == "1":  
            tickets_ocupados.append(ticket)
            tickets_comprados.append(ticket)
            tickets_ocupados_general.append(ticket)
            tickets_general_comprados.append(ticket)
        else:
            tickets_ocupados.append(ticket)
            tickets_comprados.append(ticket)
            tickets_ocupados_VIP.append(ticket)
            tickets_VIP_comprados.append(ticket)
        
        keep_adding = input("Que desea realizar? \n 1. Comprar otro ticket \n 2. Salir \n --> ")
        while not keep_adding.isnumeric() or not int(keep_adding) in range(1, 3):
            keep_adding = input("Ingreso Invalido. Que desea realizar? \n 1. Comprar otro ticket \n 2. Salir \n --> ")
                
        if keep_adding == "2":
            subtotal = get_subtotal(tickets_comprados)
            IVA = get_IVA(subtotal)
            descuento = get_discount(cedula_cliente, subtotal, IVA)
            total = get_total(subtotal, descuento, IVA)

            factura_ticket = FacturaTicket(nombre_cliente, cedula_cliente, edad_cliente, tickets_comprados, subtotal, descuento, IVA, total)
            factura_ticket.show()

            final_option = input("Desea continuar con su pago y generar el ticket? \n 1. SI \n 2. NO \n --> ")
            while not final_option.isnumeric() or not int(final_option) in range(1, 3):
                final_option = input("Porfavor ingrese una opcion valida. Desea continuar con su pago y generar el ticket? \n 1. SI \n 2. NO \n --> ")
            if final_option == "1":
                print(f"{Fore.GREEN} Compra realizada exitosamente")
                print(Style.RESET_ALL)
                cliente = Cliente(nombre_cliente, cedula_cliente, edad_cliente, partidos_comprados, tickets_comprados, factura_ticket)
                for ticket in cliente.tickets_comprados:
                    ticket.partido_cliente.ventas += 1
                return cliente
            else:
                for ticket_in_for in tickets_comprados:
                    tickets_ocupados.remove(ticket_in_for)
                for ticketV in tickets_VIP_comprados:
                    tickets_ocupados_VIP.remove(ticketV)
                for ticketG in tickets_general_comprados:
                    tickets_ocupados_general.remove(ticketG)
                print(f"{Fore.RED} Se ha cancelado su compra") 
                print(Style.RESET_ALL)
            break

## A continuacion se encuentra la funcion para validar la autenticidad de los boletos comprados
def get_validation_ticket(clientes, tickets_validados, partidos):
    codigos_validados = []
    if clientes != []: 
        nombre_cliente_validation = input("Porfavor ingrese el nombre al que esta asociado el boleto comprado \n --> ").title()
        while nombre_cliente_validation.isnumeric():
            nombre_cliente_validation = input("Ingreso Invalido. Porfavor ingrese el nombre al que esta asociado el boleto comprado \ n --> ").title()
        
        aux1 = False
        for cliente in clientes:
            if cliente.nombre == nombre_cliente_validation:
                aux1 = True
                print(f"-----BIENVENIDO {cliente.nombre}-----")
                print()
                print("A continucacion se muestran los tickets comprados a su nombre")
                print()
                cliente.factura_tickets.show()
                print()
                ticket_code_input = input("Ingrese el codigo de su boleto exactamente como aparece en su factura -> CodigoFifaEquipoLocal-CodigoFifaEquipoVisitante-TipoDeEntrada-IdPartidoIdDeSuAsiento --> Ejemplo: BRA-CMR-G-4811 \n --> ").upper()
                while not len(ticket_code_input) in range(11, 15) or not ticket_code_input.count("-") == 3:
                    ticket_code_input = input("Ingreso Invalido. Porfavor ingrese el codigo de su boleto exactamente como aparece en su factura -> CodigoFifaEquipoLocal-CodigoFifaEquipoVisitante-TipoDeEntrada-IdPartidoIdDeSuAsiento --> Ejemplo: BRA-CMR-G-4811 \n --> ").upper()
                
                if tickets_validados != []:
                    for ticket_validado in tickets_validados:
                        codigos_validados.append(ticket_validado.ticket_code)
                
                if tickets_validados != []:
                    for ticket in cliente.tickets_comprados:
                        if ticket.ticket_code == ticket_code_input:
                            if ticket.ticket_code in codigos_validados:
                                print()
                                print(f"{Fore.RED} EL ticket ya fue validado anteriormente")
                                print(Style.RESET_ALL)
                                return None, None
                        else:
                            aux2 = False
                            if ticket.ticket_code == ticket_code_input:
                                aux2 = True
                                ticket.asistencia = "Si Asistio"
                                print()
                                print(f"{Fore.GREEN} BOLETO VALIDADO CON EXITO, BIENVENIDO A SU PARTIDO")
                                print(Style.RESET_ALL)
                                for partido in partidos:
                                    if partido.id == ticket.partido_cliente.id:
                                        partido.asistencias += 1
                                return cliente, ticket
                            if aux2 == False:
                                print()
                                print(f"{Fore.RED} NO SE HA PODIDO VALIDAR SU BOLETO DEBIDO A UN ERROR DESCONOCIDO. PORFAVOR INTENTE NUEVAMENTE")
                                print(Style.RESET_ALL)
                                return None, None
                else:
                    aux2 = False
                    for ticket in cliente.tickets_comprados:
                        if ticket.ticket_code == ticket_code_input:
                            aux2 = True
                            ticket.asistencia = "Si Asistio"
                            print()
                            print(f"{Fore.GREEN} BOLETO VALIDADO CON EXITO, BIENVENIDO A SU PARTIDO")
                            print(Style.RESET_ALL)
                            for partido in partidos:
                                if partido.id == ticket.partido_cliente.id:
                                    partido.asistencias += 1
                            return cliente, ticket
                    if aux2 == False:
                        print()
                        print(f"{Fore.RED} NO SE HA PODIDO VALIDAR SU BOLETO DEBIDO A UN ERROR DESCONOCIDO. PORFAVOR INTENTE NUEVAMENTE")
                        print(Style.RESET_ALL)
                        return None, None
        if aux1 == False:
            print(f"{Fore.RED} No hay clientes asociados al nombre indicado anteriormente")
            print(Style.RESET_ALL)
            return None, None
    else:
        print("No hay clientes registrados en el sistema")
        return None, None

## A continuacion se encuentra la funcion para validar la autenticidad de los boletos comprados manualmente
def get_manual_validation_ticket(clientes, tickets_validados, partidos):
    codigos_validados = []
    if clientes != []:
        nombre_cliente_validation = input("Porfavor ingrese el nombre al que esta asociado el boleto comprado \n --> ").title()
        while nombre_cliente_validation.isnumeric():
            nombre_cliente_validation = input("Ingreso Invalido. Porfavor ingrese el nombre al que esta asociado el boleto comprado \n --> ").title()
        
        aux1 = False
        for cliente in clientes:
            if cliente.nombre == nombre_cliente_validation:
                aux1 = True
                print(f"-----BIENVENIDO {cliente.nombre}-----")
                print()
                print("A continucacion se muestran los tickets comprados a su nombre")
                print()

                cliente.factura_tickets.show()
                print()
                id_partido_manual_validation = input("Ingrese el id del partido que compro el ticket \n --> ")
                while not id_partido_manual_validation.isnumeric() or not int(id_partido_manual_validation) in range(1, 49):
                    id_partido_manual_validation = input("Porfavor ingrese un partido valido. Ingrese el id del partido que compro el ticket \n --> ")
                
                id_asiento_validation = input("Ingrese el id del asiento que compro \n --> ")
                while not id_asiento_validation.isnumeric() and not int(id_asiento_validation) in range(1, 5):
                    id_asiento_validation = input("Ingreso Invalido. Ingrese el id del asiento que compro \n --> ")
                
                if tickets_validados != []:
                    for ticket_validado in tickets_validados:
                        codigos_validados.append(ticket_validado.ticket_code)
                
                aux2 = False
                for ticket in cliente.tickets_comprados:
                    if ticket.partido_cliente.id == id_partido_manual_validation and ticket.id_asiento == id_asiento_validation:
                        if tickets_validados != []:
                            if ticket.ticket_code not in codigos_validados:
                                aux2 = True
                                ticket.asistencia = "Si asistio"
                                print()
                                print(f"{Fore.GREEN} BOLETO VALIDADO CON EXITO, BIENVENIDO A SU PARTIDO")
                                print(Style.RESET_ALL)
                                for partido in partidos:
                                    if partido.id == ticket.partido_cliente.id:
                                        partido.asistencias += 1
                                return cliente, ticket
                            else:
                                print()
                                print(f"{Fore.RED} EL ticket ya fue validado anteriormente")
                                print(Style.RESET_ALL)
                                return None, None
                        else:
                            aux2 = True
                            ticket.asistencia = "Si asistio"
                            print()
                            print(f"{Fore.GREEN} BOLETO VALIDADO CON EXITO, BIENVENIDO A SU PARTIDO")
                            print(Style.RESET_ALL)
                            for partido in partidos:
                                if partido.id == ticket.partido_cliente.id:
                                    partido.asistencias += 1
                            return cliente, ticket
                if aux2 == False:
                    print()
                    print(f"{Fore.RED} NO SE HA PODIDO VALIDAR SU BOLETO DEBIDO A UN ERROR DESCONOCIDO. PORFAVOR INTENTE NUEVAMENTE")
                    print(Style.RESET_ALL)
                    return None, None
        if aux1 == False:
            print(f"{Fore.RED} No hay clientes asociados al nombre indicado anteriormente")
            print(Style.RESET_ALL)
            return None, None
    else:
        print("No hay clientes registrados en el sistema")
        return None, None

## A continuacion se encuentra la funcion para observar los menus de los distintos restaurantes
def get_restaurantes_segun_estadio(estadios):
    print()
    print("\N{stadium} SELECCIONE EL ESTADIO DONDE SE ENCUENTRA EL RESTAURANTE \N{stadium}")
    print()
    for estadio in estadios:
        print()
        estadio.show_without_restaurant()

    print()
    id_estadio_option = input("Porfavor seleccione el id del estadio que desea visualizar sus restaurantes disponibles \n --> ")
    while not id_estadio_option.isnumeric() or not int(id_estadio_option) in range(1, 9):
        id_estadio_option = input("Ingreso Invalido. Porfavor seleccione el id del estadio que desea visualizar sus restaurantes disponibles \n --> ")
    id_estadio_option = int(id_estadio_option)
    
    lista_nombres_restaurantes_for_validation = []
    lista_productos_for_validation = []
    for estadio in estadios:
        if estadio.id == id_estadio_option:
            for restaurante in estadio.restaurantes:
                print(f"Nombre --> {restaurante.nombre}")
                lista_nombres_restaurantes_for_validation.append(restaurante.nombre)
            print()
            name_restaurante_option = input("Porfavor coloque el nombre del restaurante que desea ver el menu \n --> ")
            while not name_restaurante_option in lista_nombres_restaurantes_for_validation:
                name_restaurante_option = input("Ingreso Invalido. Porfavor coloque el nombre del restaurante tal cual como se muestra por pantalla \n --> ")
            
            for restaurante in estadio.restaurantes:
                if restaurante.nombre == name_restaurante_option:
                    print()
                    print(f"---BIENVENIDO AL RESTURANTE {restaurante.nombre}---")
                    print()
                    suboption = input("Como desearia ver el menu? \n 1. Completo \n 2. Por nombre \n 3. Por tipo \n 4. Por rango de precios \n --> ")
                    while not suboption.isnumeric() or not int(suboption) in range(1, 5):
                        suboption = input("Ingreso Invalido. Como desearia ver el menu? \n 1. Completo \n 2. Por nombre \n 3. Por tipo \n 4. Por rango de precios \n --> ")

                    for producto in restaurante.productos:
                        lista_productos_for_validation.append(producto.nombre)

                    if suboption == "1":
                        print()
                        print("\U0001F377 --MENU-- \U0001F377")
                        print()
                        for producto in restaurante.productos:
                            producto.show() 
                            lista_productos_for_validation.append(producto.nombre)
                            print()  
                    if suboption == "2":
                        nombre_option = input("Ingrese el nombre del alimento o bebida que desea comprar \n --> ")
                        nombre_list = nombre_option.split(" ")
                        nombre_junto = "".join(nombre_list)
                        while not nombre_junto.isalpha() or not nombre_junto in lista_productos_for_validation:
                            nombre_option = input("Lo sentimos, no se ha podido encontrar el alimento anterior, porfavor ingrese un alimento del menu \n --> ")
                            nombre_list = nombre_option.split(" ")
                            nombre_junto = "".join(nombre_list)
                        print()
                        print("\U0001F377 --MENU-- \U0001F377")
                        print()
                        aux2 = False
                        for producto in restaurante.productos:
                            if producto.nombre == nombre_option:
                                aux2 = True
                                producto.show()
                                print()
                        if aux2 == False:
                            print()
                            print("No se ha encontrado el alimento seleccionado en el menu. Intente nuevamente")
                    if suboption == "3":
                        tipo_option = input("Ingrese la clasificacion de lo que desea visualizar \n 1. Bebidas \n 2. Alimentos \n --> ")
                        while not tipo_option.isnumeric() or not int(tipo_option) in range(1, 3):
                            tipo_option = input("Porfavor seleccione una opcion valida. Ingrese la clasificacion de lo que desea visualizar \n 1. Bebidas \n 2. Alimentos \n --> ")
                        if tipo_option == "1":
                            tipo_option_nombre = "Bebida"
                        else:
                            tipo_option_nombre = "Alimento"
                        print()
                        print("\U0001F377 --MENU-- \U0001F377")
                        print()
                        aux3 = False
                        for producto in restaurante.productos:
                            if producto.type == tipo_option_nombre:
                                aux3 = True
                                producto.show()
                                print()
                        if aux3 == False:
                            print("No se ha encontrado el alimento seleccionado en el menu. Intente nuevamente")
                    if suboption == "4":
                        limite_menor = input("Ingrese el limite menor del rango de precios que desea filtrar (numero entero) \n --> ")
                        while not limite_menor.isnumeric() and int(limite_menor) < 35:
                            limite_menor = input("Porfavor ingrese un limite menor valido. Ingrese el limite menor del rango de precios que desea filtrar (numero entero) \n --> ")
                        limite_mayor = input("Ingrese el limite mayor del rango de precios que desea filtrar (numero entero) \n --> ")
                        while not limite_mayor.isnumeric():
                            limite_menor = input("Porfavor ingrese un limite mayor valido. Ingrese el limite menor del rango de precios que desea filtrar (numero entero) \n --> ")
                        limite_menor = int(limite_menor)
                        limite_mayor = int(limite_mayor) 
                        print()
                        print("\U0001F377 --MENU-- \U0001F377")
                        print()
                        aux4 = False
                        for producto in restaurante.productos:
                            if producto.total <= limite_mayor and producto.total >= limite_menor:
                                aux4 = True
                                producto.show()
                                print()
                        if aux4 == False:
                            print("No se ha encontrado el alimento seleccionado en el menu. Intente nuevamente")

## A continuacion se encuentra la funcion para detectar si un cliente tiene acceso al restaurante, y que desea comprar
def get_factura_productos(clientes, partidos):
    cedula = input("Porfavor ingrese la cedula registrada en el sistema al comprar los tickets \n --> ")
    while not cedula.isnumeric():
        cedula = input("Ingreso Invalido. Porfavor ingrese la cedula registrada en el sistema al comprar los tickets \n --> ")
    cedula = int(cedula)

    for cliente in clientes:
        if cliente.cedula == cedula:
            if cliente.tickets_VIP_detectados == []:
                print()
                print(f"{Fore.RED} Lo sentimos, usted no tiene acceso al restaurante debido a que ninguna de sus entradas compradas es VIP o la cedula introducida no pertenece a ningun cliente")
                print(Style.RESET_ALL)
            else:
                while True:
                    lista_id_partidos_for_validation = []
                    lista_nombre_productos = []
                    carrito_dict = {}
                    cuenta_productos = []
                    cuenta_dict = []
                    print()
                    print(f"Usted tiene a su disposicion tickets VIP para {len(cliente.tickets_VIP_detectados)} partidos difrentes")

                    option = input("Que desea realizar? \n 1. Registrar compra en un restaurante \n 2. Salir \n --> ")
                    while not option.isnumeric() or not int(option) in range (1, 3):
                        option = input("Ingreso Invalido. Que desea realizar? \n --> 1. Registrar compra en un restaurante \n 2. Salir \n --> ")
                    if option == "1":
                        if cliente.tickets_VIP_detectados == []:
                            print()
                            print(f"{Fore.RED} Usted ya no posee acceso para el restaurante de algun partido, debido a que ya realizo las compras disponibles")
                            print(Style.RESET_ALL)
                        else:
                            for ticketVIP in cliente.tickets_VIP_detectados:
                                lista_id_partidos_for_validation.append(ticketVIP.partido_cliente.id)
                                ticketVIP.partido_cliente.show()
                                print()
                            suboption = input("Ingrese el id del partido que desea realizar alguna compra en su restaurante \n --> ")
                            while not suboption.isnumeric() or not suboption in lista_id_partidos_for_validation:
                                suboption = input("Porfavor seleccione uno de sus partidos comprados con ticket VIP para acceder al menu de su restaurante \n --> ")
                            
                            for ticketVIP in cliente.tickets_VIP_detectados:
                                if ticketVIP.partido_cliente.id == suboption:
                                    print("--- RESTAURANTES DISPONIBLES ---")
                                    print()
                                    for i, restaurante in enumerate(ticketVIP.partido_cliente.stadium_id.restaurantes):
                                        print(f"{i+1} -> {restaurante.nombre}")
                                    print()
                                    restaurant_selection = input("Porfavor seleccione el id del restaurante al cual desea acceder \n --> ")
                                    while not restaurant_selection.isnumeric() or not int(restaurant_selection) in range(1, len(ticketVIP.partido_cliente.stadium_id.restaurantes) + 1):
                                        restaurant_selection = input("Ingreso Invalido. Porfavor seleccione el id del restaurante al cual desea acceder \n --> ")
                                    restaurant_selection = int(restaurant_selection)
                                    restaurante_selected = (ticketVIP.partido_cliente.stadium_id.restaurantes)[restaurant_selection - 1]

                                    while True:
                                        option_para_comprar = input("Que desea realizar? \n 1. Agregar productos a la cuenta \n 2. Salir \n --> ")
                                        while not option_para_comprar.isnumeric() or not int(option_para_comprar) in range(1, 3):
                                            option_para_comprar = input("Ingreso Invalido. Que desea realizar? \n 1. Agregar productos a la cuenta \n 2. Salir \n --> ")
                                        if option_para_comprar == "1":
                                            print()
                                            print(f"--- MENU {restaurante_selected.nombre} ---")
                                            print()
                                            for producto in restaurante_selected.productos:
                                                producto.show_sin_iva()
                                                lista_nombre_productos.append(producto.nombre)
                                                print()
                                            while True:
                                                agregar_producto = input("Ingrese el nombre del producto que desea comprar, tal cual como aparece en el menu \n --> ")
                                                agregar_producto_list = agregar_producto.split(" ")
                                                agregar_producto_junto = "".join(agregar_producto_list)
                                                while not agregar_producto_junto.isalpha() or not agregar_producto in lista_nombre_productos:
                                                    agregar_producto = input("Lo sentimos, no se ha podido encontrar el producto seleccionado, porfavor ingrese un alimento del menu \n --> ")
                                                    agregar_producto_list = agregar_producto.split(" ")
                                                    agregar_producto_junto = "".join(agregar_producto_list)
                                                aux = False
                                                for producto in restaurante_selected.productos:
                                                    if producto.nombre == agregar_producto and producto.adicional == "alcoholic" and cliente.edad < 18:
                                                        aux = True
                                                        print("Usted no puede comprar dicho producto debido a que es menor de edad")
                                                if aux == False:
                                                    break
                                            agregar_producto_cantidad = input("Ingrese la cantidad de productos que desea comprar \n --> ")
                                            while not agregar_producto_cantidad.isnumeric() or not int(agregar_producto_cantidad) <= 25:
                                                agregar_producto_cantidad = input("Ingreso Invalido. Ingrese la cantidad de productos que desea comprar \n --> ")
                                            agregar_producto_cantidad = int(agregar_producto_cantidad)

                                            for partido in partidos:
                                                if partido.id == suboption:
                                                    for restaurante in partido.stadium_id.restaurantes:
                                                        if restaurante.nombre == restaurante_selected.nombre:
                                                            for producto in restaurante_selected.productos:
                                                                if producto.nombre == agregar_producto:
                                                                    if producto.inventario == 0:
                                                                        print()
                                                                        print("Lo sentimos, ya no quedan mas cantidades del producto seleccionado")
                                                                        print()
                                                                    else:
                                                                        producto.inventario -= agregar_producto_cantidad
                                                                        if carrito_dict == {}:
                                                                            carrito_dict[producto.nombre] = agregar_producto_cantidad
                                                                        else:
                                                                            explotar = False
                                                                            for key, value in carrito_dict.items():
                                                                                if key == producto.nombre:
                                                                                    explotar = True
                                                                                    carrito_dict[producto.nombre] += agregar_producto_cantidad
                                                                            if explotar == False:
                                                                                carrito_dict[producto.nombre] = agregar_producto_cantidad
                                                                        cuenta_productos.append(producto)
                                                                        break
                                            if cuenta_dict == []:
                                                cuenta_dict.append(carrito_dict)
                                        else:
                                            if cuenta_dict == []:
                                                print()
                                                print("La cuenta esta vacia")
                                                print()
                                            else:
                                                factura_restaurante = FacturaRestaurante(cliente.nombre, cliente.cedula, cliente.edad, cuenta_dict, cuenta_productos)   
                                                print() 
                                                factura_restaurante.show()
                                                print()
                                                confirm_purschase = input("Desea proceder y continuar con el pago? \n 1. SI \n 2. NO \n --> ")
                                                while not confirm_purschase.isnumeric() or not int(confirm_purschase) in range (1, 3):
                                                    confirm_purschase = input("Ingreso Invalido. Desea proceder y continuar con el pago? \n 1. SI \n 2. NO \n --> ")
                                                if confirm_purschase == "1":
                                                    print()
                                                    print(f"{Fore.GREEN} PAGO EXITOSO. SE HA REGISTRADO SU COMPRA")
                                                    print(Style.RESET_ALL)
                                                    cliente.tickets_VIP_detectados.remove(ticketVIP)
                                                    cliente.factura_restaurante.append(factura_restaurante)
                                                else:
                                                    for producto in restaurante_selected.productos:
                                                        for key, value in carrito_dict.items():
                                                            if producto.nombre == key:
                                                                producto.inventario += value
                                                    print()
                                                    print(f"{Fore.RED} SE HA CANCELADO SU PAGO")
                                                    print(Style.RESET_ALL)
                                            break     
                    elif option == "2":     
                        break

## A continuacion se encuentra la funcion para sacar el promedio de gasto de un cliente VIP en un partido
def get_promedio_gasto_VIP(clientes):
    clientes_VIP = []
    monto_total = 0
    for cliente in clientes:
        for ticket in cliente.tickets_comprados:
            if ticket.tipo_entrada == "VIP":
                clientes_VIP.append(cliente)
                break
    
    for cliente in clientes_VIP:
        monto_total += cliente.factura_tickets.total
        if cliente.factura_restaurante == []:
            monto_total += 0 
        else:
            for factura in cliente.factura_restaurante:
                monto_total += factura.total
    if clientes_VIP != []:
        promedio_de_gasto = round(monto_total / len(clientes_VIP), 2)
        return promedio_de_gasto
    else:
        print("No hay clientes VIP registrados en el sistema")

## A continuacion se encuentra la funcion para desplegar la asistencia de los partidos
def get_asistencia_partidos(partidos):
    partidos_ordenados = sorted(partidos, key = lambda x: x.asistencias, reverse=True)
    for partido in partidos_ordenados:
        partido.show_stadistics()

## A continuacion se encuentra la funcion para seleccionar el partido con mayor asistencia
def get_partido_mayor_asistencia(partidos):
    partidos_ordenados = sorted(partidos, key=lambda x: x.asistencias, reverse= True)
    return partidos_ordenados[0]

## A continuacion se encuentra la funcion para seleccionar el partido con mayor ventas
def get_partido_mayor_ventas(partidos):
    partidos_ordenados = sorted(partidos, key=lambda x: x.ventas, reverse=True)
    return partidos_ordenados[0]

## A continuacion se encuentra la funcion para conocer el top 3 de los productos mas vendidos en cada restaurante
def get_top_restaurant_products(partidos):
    option = input("Ingrese el id del restaurante sobre el cual desea conocer el top de productos mas vendidos \n 1. Al Bayt Restaurant \n 2. Lusail Restaurant \n 3. The emir Restaurant \n 4. Ahmad Bin Ali Restaurant \n 5. Al Janoub Restaurant \n 6. Al Thumama Restaurant \n 7. Education City Restaurant \n 8. Khalifa International Restaurant \n 9. 974 Restaurant \n --> ")
    while not option.isnumeric() or not int(option) in range(1, 9):
        option = option = input("Ingreso Invalido. Ingrese el id del restaurante sobre el cual desea conocer el top de productos mas vendidos \n 1. Al Bayt Restaurant \n 2. Lusail Restaurant \n 3. The emir Restaurant \n 4. Ahmad Bin Ali Restaurant \n 5. Al Janoub Restaurant \n 6. Al Thumama Restaurant \n 7. Education City Restaurant \n 8. Khalifa International Restaurant \n 9. 974 Restaurant \n --> ")
    if option == "1":
        option = "Al Bayt Restaurant"
    elif option == "2":
        option = "Lusail Restaurant"
    elif option == "3":
        option = "The emir Restaurant"
    elif option == "4":
        option = "Ahmad Bin Ali Restaurant"
    elif option == "5":
        option = "Al Janoub Restaurant"
    elif option == "6":
        option = "Al Thumama Restaurant"
    elif option == "7":
        option = "Education City Restaurant"
    elif option == "8":
        option = "Khalifa International Restaurant"
    elif option == "9":
        option = "974 Restaurant"
    
    for partido in partidos:
        for restaurante in partido.stadium_id.restaurantes:
            if restaurante.nombre == option:
                productos_ordenados = sorted(restaurante.productos, key = lambda x: x.inventario)
                break
    print()
    print(f"---RESTAURANTE {option}---")
    print()
    productos_ordenados[0].show_stadistics()
    print()
    productos_ordenados[1].show_stadistics()
    print()
    productos_ordenados[2].show_stadistics()
    print()
    
## A continuacion se encuentra la funcion para conocer el top 3 de los clientes que mas compraron entradas
def get_most_tickets_clients(clientes):
    clientes_ordenados = sorted(clientes, key = lambda x: len(x.tickets_comprados), reverse=True)
    if len(clientes) >= 3:
        top1_cliente = clientes_ordenados[0]
        top2_cliente = clientes_ordenados[1]
        top3_cliente = clientes_ordenados[2]
        top1_cliente.show()
        top2_cliente.show()
        top3_cliente.show()
    else:
        for cliente in clientes_ordenados:
            cliente.show()

## A continuacion se muestra la funcion para obtener el grafico de la estadistica numero 1 en el apartado de estadisticas
def get_grafico_asistencia(partidos):
    ejeX = []
    ejeY = []
    for partido in partidos:
        ejeX.append(partido.id)
        ejeY.append(partido.asistencias)

    fig, ax = plt.subplots() 
    ax.plot(ejeX, ejeY, color = "tab:olive", marker = "o")
    ax.set_title("ASISTENCIA DE PARTIDOS", loc = "center", fontdict= {"fontsize": 18, "fontweight":"bold", "color" : "tab:olive"})
    ax.set_xlabel("Id Del Partido", fontdict = {'fontsize':12, 'fontweight':'bold', 'color':'tab:olive'})
    ax.set_ylabel("Asistencia", fontdict = {'fontsize':12, 'fontweight':'bold', 'color':'tab:olive'})
    fig.set_size_inches(16, 5)
    plt.show()

## A continuacion se muestra la funcion para obtener el grafico de la estadistica numero 2 en el apartado de estadisticas
def get_grafico_ventas(partidos):
    ejeX = []
    ejeY = []
    for partido in partidos:
        ejeX.append(partido.id)
        ejeY.append(partido.ventas)

    fig, ax = plt.subplots()
    ax.plot(ejeX, ejeY, color = "tab:olive", marker = "o")
    ax.set_title("VENTAS DE LOS PARTIDOS", loc = "center", fontdict= {"fontsize": 18, "fontweight":"bold", "color" : "tab:olive"})
    ax.set_xlabel("Id Del Partido", fontdict = {'fontsize':12, 'fontweight':'bold', 'color':'tab:olive'})
    ax.set_ylabel("Ventas", fontdict = {'fontsize':12, 'fontweight':'bold', 'color':'tab:olive'})
    fig.set_size_inches(16, 5)
    plt.show()

## A continuacion se encuentra la funcion para generar el grafico de la estadistica numero 3 en el apartado de las estadisticas
def get_grafico_top_productos(partidos):
    option = input("Ingrese el id del restaurante sobre el cual desea conocer el top de productos mas vendidos \n 1. Al Bayt Restaurant \n 2. Lusail Restaurant \n 3. The emir Restaurant \n 4. Ahmad Bin Ali Restaurant \n 5. Al Janoub Restaurant \n 6. Al Thumama Restaurant \n 7. Education City Restaurant \n 8. Khalifa International Restaurant \n 9. 974 Restaurant \n --> ")
    while not option.isnumeric() or not int(option) in range(1, 9):
        option = option = input("Ingreso Invalido. Ingrese el id del restaurante sobre el cual desea conocer el top de productos mas vendidos \n 1. Al Bayt Restaurant \n 2. Lusail Restaurant \n 3. The emir Restaurant \n 4. Ahmad Bin Ali Restaurant \n 5. Al Janoub Restaurant \n 6. Al Thumama Restaurant \n 7. Education City Restaurant \n 8. Khalifa International Restaurant \n 9. 974 Restaurant \n --> ")
    if option == "1":
        option = "Al Bayt Restaurant"
    elif option == "2":
        option = "Lusail Restaurant"
    elif option == "3":
        option = "The emir Restaurant"
    elif option == "4":
        option = "Ahmad Bin Ali Restaurant"
    elif option == "5":
        option = "Al Janoub Restaurant"
    elif option == "6":
        option = "Al Thumama Restaurant"
    elif option == "7":
        option = "Education City Restaurant"
    elif option == "8":
        option = "Khalifa International Restaurant"
    elif option == "9":
        option = "974 Restaurant"
    
    for partido in partidos:
        for restaurante in partido.stadium_id.restaurantes:
            if restaurante.nombre == option:
                productos_ordenados = sorted(restaurante.productos, key = lambda x: x.inventario)
                break

    fig, ax = plt.subplots()
    ejeX = [productos_ordenados[0].nombre, productos_ordenados[1].nombre, productos_ordenados[2].nombre]
    ejeY = [25-(productos_ordenados[0].inventario), 25-(productos_ordenados[1].inventario), 25-(productos_ordenados[2].inventario)]
    ax.plot(ejeX, ejeY, color = "tab:olive", marker = "o")
    ax.set_title(f"TOP 3 PRODUCTOS MAS VENDIDOS EN {option.upper()}", loc = "center", fontdict= {"fontsize": 18, "fontweight":"bold", "color" : "tab:olive"})
    ax.set_xlabel("Id Del Partido", fontdict = {'fontsize':12, 'fontweight':'bold', 'color':'tab:olive'})
    ax.set_ylabel("Ventas", fontdict = {'fontsize':12, 'fontweight':'bold', 'color':'tab:olive'})
    fig.set_size_inches(10, 5)
    plt.show()

## A continuacion se muestra la funcion para obtener el grafico de la estadistica numero 4 en el apartado de estadisticas
def get_grafico_top_clientes(clientes):
    clientes_ordenados = sorted(clientes, key = lambda x: len(x.tickets_comprados), reverse=True)
    ejeX = []
    ejeY = []
    if len(clientes) >= 3:
        ejeX = [clientes_ordenados[0].nombre, clientes_ordenados[1].nombre, clientes_ordenados[2].nombre]
        ejeY = [len(clientes_ordenados[0].tickets_comprados), len(clientes_ordenados[1].tickets_comprados), len(clientes_ordenados[2].tickets_comprados)]
    else:
        for cliente in clientes_ordenados:
            ejeX.append(cliente.nombre)
        for cliente in clientes_ordenados:
            ejeY.append(len(cliente.tickets_comprados))

    fig, ax = plt.subplots()
    ax.plot(ejeX, ejeY, color = "tab:olive", marker = "o")
    ax.set_title(f"TOP 3 CLIENTES CON MAS TICKETS COMPRADOS", loc = "center", fontdict= {"fontsize": 18, "fontweight":"bold", "color" : "tab:olive"})
    ax.set_xlabel("Clientes", fontdict = {'fontsize':12, 'fontweight':'bold', 'color':'tab:olive'})
    ax.set_ylabel("Ventas", fontdict = {'fontsize':12, 'fontweight':'bold', 'color':'tab:olive'})
    fig.set_size_inches(10, 5)
    plt.show()
    
## A continuacion se encuentra la funcion main, que la funcionalidad a todo el programa
def main():
    while True:
        reset = input("Desea correr el programa tomando en cuenta los datos ya cargados en el sistema? \n 1. Utilizar datos cargados \n 2. Comenzar el programa desde cero \n --> ")
        while not reset.isnumeric() or not int(reset) in range(1, 3):
            reset = input("Ingreso Invalido. Desea correr el programa tomando en cuenta los datos ya cargados en el sistema? \n 1. Utilizar datos cargados \n 2. Comenzar el programa desde cero \n --> ")
        if reset == "1":
            try:
                with open("equipos.txt", "rb") as r:
                    equipos = pickle.load(r)
                with open("estadios.txt", "rb") as r:
                    estadios = pickle.load(r)
                with open("partidos.txt", "rb") as r:
                    partidos = pickle.load(r)
                with open("clientes.txt", "rb") as r:
                    clientes = pickle.load(r)
                with open("tickets_ocupados.txt", "rb") as r:
                    tickets_ocupados = pickle.load(r)
                with open("tickets_ocupados_general.txt", "rb") as r:
                    tickets_ocupados_general = pickle.load(r)
                with open("tickets_ocupados_VIP.txt", "rb") as r:
                    tickets_ocupados_VIP = pickle.load(r)
                with open("clientes_con_tickets_validados.txt", "rb") as r:
                    clientes_con_tickets_validados = pickle.load(r)
                with open("tickets_validados.txt", "rb") as r:
                    tickets_validados = pickle.load(r)
                break
            except EOFError:
                equipos = get_equipos()
                estadios = get_estadios()
                partidos = get_partidos(equipos, estadios)
                clientes = []
                tickets_ocupados = []
                tickets_ocupados_general = []
                tickets_ocupados_VIP = []
                clientes_con_tickets_validados = []
                tickets_validados = []
                break
        else:
            clave = input("Ingrese la clave para borrar los datos guardados \n --> ")
            while not clave.isnumeric():
                clave = input("Ingreso Invalido. Ingrese la clave para borrar los datos guardados \n --> ")
            if clave != "1107":
                print()
                print(f"{Fore.RED} LA CLAVE INTRODUCIDA ES INCORRECTA")
                print(Style.RESET_ALL)
            else:
                print()
                print(f"{Fore.GREEN} LA CLAVE INTRODUCIDA ES CORRECTA")
                print(Style.RESET_ALL)
                equipos = get_equipos()
                estadios = get_estadios()
                partidos = get_partidos(equipos, estadios)
                clientes = []
                tickets_ocupados = []
                tickets_ocupados_general = []
                tickets_ocupados_VIP = []
                clientes_con_tickets_validados = []
                tickets_validados = []
                break
    
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
                     option2 = input("Porfavor seleccione una opcion valida. Que desea realizar? \n 1. Comprar ebtradas \n 2. Salir del modulo \n --> ")
                if option2 == "1":
                    cliente = get_client_data(partidos, tickets_ocupados, tickets_ocupados_general, tickets_ocupados_VIP, clientes)
                    if cliente != None:   
                        clientes.append(cliente)
                        for ticket in cliente.tickets_comprados:
                            if ticket.tipo_entrada == "VIP":
                                if cliente.tickets_VIP_detectados == []:    
                                    cliente.tickets_VIP_detectados.append(ticket)
                                else:
                                    for ticketVIP in cliente.tickets_VIP_detectados:
                                        if ticketVIP.partido_cliente != ticket.partido_cliente:
                                            cliente.tickets_VIP_detectados.append(ticket)    
                else:
                    break   
        
        ## MODULO 3 
        if option == "3":
            while True:
                print()
                print("\U0001F64B ASISTENCIA DE PARTIDOS \U0001F64B")
                print()
                option3 = input("Que desea realizar? \n 1. Ingresar a un partido validando su boleto \n 2. Salir del modulo \n --> ")
                if option3 == "1":
                    sub_option3 = input("Como desea validar su boleto? \n 1. Utilizando el codigo unico \n 2. Realizarlo manualmente \n --> ")
                    if sub_option3 == "1":
                        cliente_validado, ticket_validado = get_validation_ticket(clientes, tickets_validados, partidos)
                        if cliente_validado != None and ticket_validado != None:
                            clientes_con_tickets_validados.append(cliente_validado)
                            tickets_validados.append(ticket_validado)
                    elif sub_option3 == "2":
                        cliente_validado_manual, ticket_validado = get_manual_validation_ticket(clientes, tickets_validados, partidos)
                        if cliente_validado_manual != None and ticket_validado != None:
                            clientes_con_tickets_validados.append(cliente_validado_manual)
                            tickets_validados.append(ticket_validado)
                if option3 == "2":
                    break
        
        ## MODULO 4 
        if option == "4":
            while True:
                print()
                print("\N{fork and knife with plate} GESTION DE RESTAURANTES \N{fork and knife with plate}") 
                print()
                option4 = input("Que desea realizar? \n 1. Ver las ofertas de los restaurantes disponibles \n 2. Salir del modulo \n --> ")
                while not option4.isnumeric() or not int(option4) in range(1, 3):
                    option4 = input("Ingreso Invalido. Que desea realizar? \n 1. Ver las ofertas de los restaurantes disponibles \n 2. Salir del modulo \n --> ")
                if option4 == "1":
                    get_restaurantes_segun_estadio(estadios)
                if option4 == "2":
                    break
        
        ## MODULO 5
        if option == "5":
            while True:
                print()
                print("\N{money with wings} GESTION DE VENTA DE RESTAURANTE \N{money with wings}")
                print()
                option5 = input("Que desea realizar? \n 1. Registrar compra de restaurante (solo para clientes con tickets VIP) \n 2. Salir del modulo \n --> ")
                while not option5.isnumeric() or not int(option5) in range(1, 3):
                    option5 = input("Ingreso Invalido. Que desea realizar? \n 1. Registrar compra de restaurante (solo para clientes con tickets VIP) \n 2. Salir del modulo \n --> ")
                if option5 == "1":
                    if clientes != []:
                        get_factura_productos(clientes, partidos)
                    else:
                        print()
                        print("No hay clientes registrados")
                if option5 == "2":
                    break
        
        ## MODULO 6
        if option == "6":
            while True:
                print()
                print("\N{bar chart} INDICADORES DE GESTION (ESTADISTICAS) \N{bar chart}")
                print()
                option7 = input("Que estadistica desea visualizar? \n 1. Promedio de gasto de un cliente VIP \n 2. Asistencia a los partidos \n 3. Partido con mayor asistencia \n 4. Partido con mayor boletos vendidos \n 5. Top 3 de productos mas vendidos en el restaurante \n 6. Top 3 de clientes que mas compraron boletos \n 7. Mostrar graficos \n 8. Salir del modulo \n --> ")
                while not option.isnumeric() or not int(option7) in range(1, 9):
                    option7 = input("Ingreso Invalido. Que estadistica desea visualizar? \n 1. Promedio de gasto de un cliente VIP \n 2. Asistencia a los partidos \n 3. Partido con mayor asistencia \n 4. Partido con mayor boletos vendidos \n 5. Top 3 de productos mas vendidos en el restaurante \n 6. Top 3 de clientes que mas compraron boletos \n 7. Mostrar graficos \n 8. Salir del modulo \n --> ")
                if option7 == "1":
                    promedio_gasto = get_promedio_gasto_VIP(clientes)
                    if promedio_gasto != None:
                        print()
                        print(f"El promedio de gasto de un cliente VIP es --> {promedio_gasto}$")
                        print()
                elif option7 == "2":
                    print("--- TABLA DE ASISTENCIA DE PARTIDOS ---")
                    print()
                    get_asistencia_partidos(partidos)
                elif option7 == "3":
                    print("--- PARTIDO CON MAYOR ASISTENCIA ---")
                    print()
                    partido_mas_asistido = get_partido_mayor_asistencia(partidos)
                    partido_mas_asistido.show_stadistics()
                elif option7 == "4":
                    print("--- PARTIDO CON MAYOR VENTAS ---")
                    partido_mas_vendido = get_partido_mayor_ventas(partidos)
                    partido_mas_vendido.show_stadistics()
                elif option7 == "5":
                    print("---TOP 3 PRODUCTOS MAS VENDIDOS EN ALGUN RESTAURANTE---")
                    print()
                    get_top_restaurant_products(partidos)
                elif option7 == "6":
                    print("---TOP 3 CLIENTES CON MAS TICKETS COMPRADOS---")
                    get_most_tickets_clients(clientes)
                elif option7 == "7":
                    while True:
                        print()
                        print("\N{bar chart} GRAFICOS DE LAS ESTADISTICAS \N{bar chart}")
                        print()
                        suboption7 = input("Que grafico desea visualizar? \n 1. Asistencia de partidos \n 2. Tickets vendidos \n 3. Top 3 productos mas vendidos en cada restaurante \n 4. Top 3 clientes que mas compraron tickets \n 5. Salir del modulo \n --> ")
                        while not suboption7.isnumeric() or not int(suboption7) in range (1, 6):
                            suboption7 = input("Ingreso Invalido. Que grafico desea visualizar? \n 1. Asistencia de partidos \n 2. Tickets vendidos \n 3. Top 3 productos mas vendidos en cada restaurante \n 4, Top 3 clientes que mas compraron tickets \n 5. Salir del modulo \n --> ")
                        if suboption7 == "1":
                            get_grafico_asistencia(partidos)
                        elif suboption7 == "2":
                            get_grafico_ventas(partidos)
                        elif suboption7 == "3":
                            get_grafico_top_productos(partidos)
                        elif suboption7 == "4":
                            get_grafico_top_clientes(clientes)
                        elif suboption7 == "5":
                            break
                elif option7 == "8":
                    break
        if option == "7":
            with open("equipos.txt", "wb") as w:
                equipos = pickle.dump(equipos, w)
            with open("estadios.txt", "wb") as w:
                estadios = pickle.dump(estadios, w)
            with open("partidos.txt", "wb") as w:
                partidos = pickle.dump(partidos, w)
            with open("clientes.txt", "wb") as w:
                clientes = pickle.dump(clientes, w)
            with open("tickets_ocupados.txt", "wb") as w:
                tickets_ocupados = pickle.dump(tickets_ocupados, w)
            with open("tickets_ocupados_general.txt", "wb") as w:
                tickets_ocupados_general = pickle.dump(tickets_ocupados_general, w)
            with open("tickets_ocupados_VIP.txt", "wb") as w:
                tickets_ocupados_VIP = pickle.dump(tickets_ocupados_VIP, w)
            with open("clientes_con_tickets_validados.txt", "wb") as w:
                clientes_con_tickets_validados = pickle.dump(clientes_con_tickets_validados, w)
            with open("tickets_validados.txt", "wb") as w:
                tickets_validados = pickle.dump(tickets_validados, w)
            break
try:
    main()
except:
    print(f"{Fore.RED} LO SENTIMOS, HA OCURRIDO UN ERROR DESCONOCIDO")
    print(Style.RESET_ALL)
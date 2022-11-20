def get_client_data(partidos, clientes, tickets_ocupados):
    tickets_ocupados = []
    nombre_cliente = input("Porfavor ingrese su nombre completo \n --> ") 
    while not nombre_cliente.isalpha or nombre_cliente.count(" ") > 4:
        nombre_cliente = input("Porfavor ingrese un nombre valido. Ingrese su nombre completo \n --> ")

    if clientes != []:
        for cliente in clientes:
            if nombre_cliente == cliente.nombre:
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
                cliente.partidos_comprados.append(partido_cliente)
                
                option_ticket_cliente = input("Porfavor esocga el tipo de entrada que desea \n 1. General 50$ \n 2. VIP 120$ \n --> ")
                while not option_ticket_cliente.isnumeric() or not int(option_ticket_cliente) in range(1, 3):
                    option_ticket_cliente = input("Porfavor ingrese un tipo de entrada valido. Esocga el tipo de entrada que desea \n 1. General 50$ \n 2. VIP 120$ \n --> ") 
                
                for partido in partidos:
                    if partido.id == id_partido:
                        estadio_selected = partido.stadium_id
                        get_mapa_estadio(estadio_selected.capacidad, tickets_ocupados)
                        
                id_asiento = input("Anteriormente se mostro un mapa del estadio, porfavor ingrese el asiento que desea comprar \n --> ")
                while not id_asiento.isnumeric():
                    id_asiento = input("Anteriormente se mostro un mapa del estadio, porfavor ingrese el asiento que desea comprar \n --> ")
                
                if option_ticket_cliente == "1":
                    ticket_general = General(id_partido, id_asiento)
                else:
                    ticket_vip = Vip(id_partido, id_asiento)    
                
                         
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
                        partidos_comprados.append(partido)
                        break 

                ticket_list_cliente = []
                option_ticket_cliente = input("Porfavor esocga el tipo de entrada que desea \n 1. General 50$ \n 2. VIP 120$ \n --> ")
                while not option_ticket_cliente.isnumeric() or not int(option_ticket_cliente) in range(1, 3):
                    option_ticket_cliente = input("Porfavor ingrese un tipo de entrada valido. Esocga el tipo de entrada que desea \n 1. General 50$ \n 2. VIP 120$ \n --> ") 
                if option_ticket_cliente == "1":
                    ticket_general = General(id_partido)
                    ticket_list_cliente.append(ticket_general)
                else:
                    ticket_vip = Vip(id_partido)
                    ticket_list_cliente.append(ticket_vip)
                
                cliente = Cliente(nombre_cliente, cedula_cliente, edad_cliente, partidos_comprados, ticket_list_cliente)
                return cliente
    else:
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

        ticket_list_cliente = []
        option_ticket_cliente = input("Porfavor esocga el tipo de entrada que desea \n 1. General 50$ \n 2. VIP 120$ \n --> ")
        while not option_ticket_cliente.isnumeric() or not int(option_ticket_cliente) in range(1, 3):
            option_ticket_cliente = input("Porfavor ingrese un tipo de entrada valido. Esocga el tipo de entrada que desea \n 1. General 50$ \n 2. VIP 120$ \n --> ") 
        if option_ticket_cliente == "1":
            ticket_general = General()
            ticket_list_cliente.append(ticket_general)
        else:
            ticket_vip = Vip()
            ticket_list_cliente.append(ticket_vip)
        
        cliente = Cliente(nombre_cliente, cedula_cliente, edad_cliente, partido_cliente, ticket_list_cliente)
        return cliente
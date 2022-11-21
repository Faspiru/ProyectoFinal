from colorama import *

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

get_mapa_estadio([3, 3], [], )

        
    
    
            
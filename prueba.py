from colorama import *

def get_mapa_estadio(x):
    taken = []
    #for ticket in tickets_ocupados:
       # if ticket.partido_cliente == partido_cliente:
            #taken.append(ticket.id_asiento)

    asientos_libres = []
    for a in range(x[0]):
        fila = []
        for b in range(x[1]):
            if f"{a}{b}" not in taken:
                changed_color = (f"{Fore.GREEN}{a}{b}")
                if len(changed_color) == 7:
                    fila.append(f"|  {changed_color}")
                    asientos_libres.append(f"{a}{b}")
                elif len(changed_color) == 8:
                    fila.append(f"| {changed_color}")
                    asientos_libres.append(f"{a}{b}")
                else:
                    fila.append(f"| {changed_color}")
                    asientos_libres.append(f"{a}{b}")
            else:
                changed_color = (f"{Fore.RED} X ")
                fila.append(f"{changed_color}")       
        print(" ".join(fila))
        print()
    print(Style.RESET_ALL)
    return asientos_libres

get_mapa_estadio([60, 20])

        
    
    
            
import ipaddress
def calcular_subneteo_ipv6(ip_str, prefixo):
    try:
        # Convertir la dirección IPv6 ingresada en un objeto IPv6Address
        ip = ipaddress.IPv6Address(ip_str)

        # Verificar si el prefijo proporcionado es válido
        if prefixo < 0 or prefixo > 128:
            print("Error: El prefijo debe estar entre 0 y 128.")
            return

        # Obtener la red a partir de la dirección IP y el prefijo
        red = ipaddress.IPv6Network(f"{ip}/{prefixo}", strict=False)

        # Imprimir información sobre la red y la dirección IP
        print("Dirección IPv6:", ip)
        print("Máscara de prefijo:", prefixo)
        print("Red:", red.network_address)
        print("Dirección de broadcast:", red.broadcast_address)
        print("Primera IP:", red.network_address + 1)
        print("Última IP:", red.broadcast_address - 1)
        print("Cantidad de direcciones en la red:", red.num_addresses)
    except ipaddress.AddressValueError:
        print("Error: La dirección IPv6 ingresada no es válida.")



# Definir función para convertir IP a binario
def ip_a_binario(ip_segments):
    ip_binaria = "".join([bin(segment)[2:].zfill(8) for segment in ip_segments])
    return ip_binaria

# Definir función para calcular la máscara de red
def calcular_mascara_red(numero_mascara):
    if numero_mascara < 0 or numero_mascara > 32:
        print("Error: El número para calcular la máscara personalizada debe estar entre 0 y 32.")
        return None

    mascara_binaria = "1" * numero_mascara + "0" * (32 - numero_mascara)
    mascara_segmentos = [
        int(mascara_binaria[i:i + 8], 2) for i in range(0, 32, 8)
    ]
    mascara_personalizada = ".".join(map(str, mascara_segmentos))
    return mascara_personalizada

# Definir función para determinar la dirección de broadcast
def calcular_broadcast(direccion_red_binaria, mascara_binaria):
    if len(direccion_red_binaria) != 32 or len(mascara_binaria) != 32:
        print("Error: La longitud de la dirección de red o la máscara de red no es válida.")
        return None

    direccion_broadcast_binaria = ""
    for i in range(32):
        if mascara_binaria[i] == "1":
            direccion_broadcast_binaria += direccion_red_binaria[i]
        else:
            direccion_broadcast_binaria += "1"

    direccion_broadcast_segmentos = [int(direccion_broadcast_binaria[i:i + 8], 2) for i in range(0, 32, 8)]
    direccion_broadcast = ".".join(map(str, direccion_broadcast_segmentos))
    return direccion_broadcast

# Definir función para calcular la primera IP
def calcular_primera_ip(ip_segments):
    ip_segments[-1] += 1  # Sumar 1 al último segmento de la dirección de red
    primera_ip = ".".join(map(str, ip_segments))
    return primera_ip

# Definir función para calcular la última IP
def calcular_ultima_ip(direccion_broadcast):
    direccion_broadcast_segmentos = list(map(int, direccion_broadcast.split(".")))
    direccion_broadcast_segmentos[-1] -= 1  # Restar 1 al último segmento de la dirección de broadcast
    ultima_ip = ".".join(map(str, direccion_broadcast_segmentos))
    return ultima_ip

# Definir función para determinar la clase y máscara de red predeterminada
def determinar_clase_mascara(ip_segments):
    if 0 <= ip_segments[0] <= 127:
        clase = "A"
        mascara_predeterminada = "255.0.0.0"
    elif 128 <= ip_segments[0] <= 191:
        clase = "B"
        mascara_predeterminada = "255.255.0.0"
    elif 192 <= ip_segments[0] <= 223:
        clase = "C"
        mascara_predeterminada = "255.255.255.0"
    elif 224 <= ip_segments[0] <= 239:
        clase = "D"
        mascara_predeterminada = None  # No hay máscara de red predeterminada para clase D
    elif 240 <= ip_segments[0] <= 254:
        clase = "E"
        mascara_predeterminada = None  # No hay máscara de red predeterminada para clase E

    return clase, mascara_predeterminada

# Definir función para calcular la dirección de red
def calcular_direccion_red(ip_binaria, mascara_binaria):
    direccion_red_binaria = ip_binaria[:mascara_binaria.count("1")] + "0" * (32 - mascara_binaria.count("1"))
    direccion_red_segmentos = [int(direccion_red_binaria[i:i + 8], 2) for i in range(0, 32, 8)]
    direccion_red = ".".join(map(str, direccion_red_segmentos))
    return direccion_red

def sumar_rango_a_direccion(direccion_red, rango):
    direccion_red_segmentos = list(map(int, direccion_red.split(".")))  # Convertir dirección de red a lista de segmentos

    # Sumar el rango al último segmento de la dirección IP, dependiendo de la clase
    if clase == "A":
        direccion_red_segmentos[-1] += rango
    elif clase == "B":
        direccion_red_segmentos[-2] += rango
    elif clase == "C":
        direccion_red_segmentos[-3] += rango

    # Convertir los segmentos nuevamente a cadena de texto
    direccion_red_actualizada = ".".join(map(str, direccion_red_segmentos))
    return direccion_red_actualizada


# Definir función principal para calcular una sola red
def calcular_red_unica(direccion_red, ip_segments, clase, mascara_predeterminada):

    # Solicitar al usuario si desea ingresar un número para calcular la máscara de red personalizada
    opcion_mascara = input("Desea ingresar un número para calcular la máscara de red personalizada? (S/N): ")

    if opcion_mascara.lower() == "s":
        numero_mascara = int(input("Ingrese el número para calcular la máscara de red personalizada (0-32): "))
        mascara_personalizada = calcular_mascara_red(numero_mascara)
    else:
        mascara_personalizada = mascara_predeterminada

    if mascara_personalizada is not None:
        # Calcular la dirección de broadcast
        mascara_binaria = ip_a_binario(list(map(int, mascara_personalizada.split("."))))
        direccion_broadcast = calcular_broadcast(ip_a_binario(ip_segments), mascara_binaria)

        # Calcular la primera y última IP
        primera_ip = calcular_primera_ip(ip_segments)
        ultima_ip = calcular_ultima_ip(direccion_broadcast)

        # Imprimir los resultados adicionales
        print("Máscara de red:", mascara_personalizada)
        print("Dirección de red:", direccion_red)  # Utilizar la dirección de red recibida como parámetro
        print("Dirección de broadcast:", direccion_broadcast)
        print("Primera IP:", primera_ip)
        print("Última IP:", ultima_ip)

    else:
        print("No hay máscara de red predeterminada para la clase", clase)

# Solicitar al usuario que elija una opción
opcion = int(input("Ingrese 1 para calcular una sola red, o 2 para realizar subneteo,3 para ipv6 "))

if opcion == 1:
    ip_segments = []
    for i in range(4):
        if i == 0:
            segment = int(input(f"Ingrese el segmento {i + 1} de la IP (0-254): "))
            while segment < 0 or segment > 254:
                print("Fuera de los límites, ingrese nuevamente el segmento.")
                segment = int(input(f"Ingrese nuevamente el segmento {i + 1} de la IP (0-254): "))
        else:
            segment = int(input(f"Ingrese el segmento {i + 1} de la IP: "))
        ip_segments.append(segment)

    # Convertir la IP a binario
    ip_binaria = ip_a_binario(ip_segments)

    # Determinar la clase y máscara de red predeterminada
    clase, mascara_predeterminada = determinar_clase_mascara(ip_segments)

    # Calcular la dirección de red
    direccion_red = calcular_direccion_red(ip_binaria, ip_a_binario(list(map(int, mascara_predeterminada.split(".")))))

    calcular_red_unica(direccion_red, ip_segments, clase, mascara_predeterminada)

elif opcion == 2:
    # Solicitar al usuario la cantidad de redes (máximo 16)
    cantidad_redes = int(input("Ingrese la cantidad de redes (máximo 16): "))
    while cantidad_redes < 1 or cantidad_redes > 16:
        print("Cantidad inválida. Ingrese nuevamente.")
        cantidad_redes = int(input("Ingrese la cantidad de redes (máximo 16): "))

    # Pedir al usuario que ingrese la dirección IP
    ip_segments = []
    for i in range(4):
        if i == 0:
            while True:
                segment = input(f"Ingrese el segmento {i + 1} de la IP (0-254): ")
                if segment.isdigit() and 0 <= int(segment) <= 254:
                    break
                print("Valor inválido. Ingrese nuevamente.")
        else:
            while True:
                segment = input(f"Ingrese el segmento {i + 1} de la IP: ")
                if segment.isdigit() and 0 <= int(segment) <= 255:
                    break
                print("Valor inválido. Ingrese nuevamente.")
        ip_segments.append(int(segment))

    # Convertir la IP a binario
    ip_binaria = ip_a_binario(ip_segments)

    # Determinar la clase y máscara de red predeterminada
    clase, mascara_predeterminada = determinar_clase_mascara(ip_segments)

    # Imprimir la máscara de red predeterminada
    print("Máscara de red:", mascara_predeterminada)

    if clase != "D" and clase != "E":
        # Calcular la dirección de red
        direccion_red = calcular_direccion_red(ip_binaria,
                                               ip_a_binario(list(map(int, mascara_predeterminada.split(".")))))

        # Imprimir la dirección de red

        print("Subneteo:")

        # Realizar el subneteo
        n = 0
        while 2 ** n < cantidad_redes:
            n += 1

        cantidad_host = 2 ** n - 2
        numerorestar = 0
        if n == 1:
            numerorestar = 128
        if n == 2:
            numerorestar = 192
        if n == 3:
            numerorestar = 224
        if n == 4:
            numerorestar = 240
        if n == 5:
            numerorestar = 248

        # Calcular Rango
        Rango = numerorestar - 256

        rango_ip = cantidad_host + 2  # Calcular el rango de IP por subred

        print("Rango de IP por subred:", rango_ip)
        for i in range(cantidad_redes):
            calcular_red_unica(direccion_red, ip_segments, clase, mascara_predeterminada)
            # Sumar el rango a la dirección de red para la siguiente subred
            direccion_red = sumar_rango_a_direccion(direccion_red, rango_ip)
elif opcion == 3:
    # Pedir al usuario que ingrese una dirección IPv6 y el prefijo
    ip_ipv6 = input("Ingrese la dirección IPv6: ")
    prefixo_ipv6 = int(input("Ingrese el prefijo (0-128): "))

    calcular_subneteo_ipv6(ip_ipv6, prefixo_ipv6)
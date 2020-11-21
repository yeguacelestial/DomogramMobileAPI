def handle_temp_hum(board, shelf, identificador):
    # Fetch temperatura
    board.write(b'O')
    # temperatura = float(board.readline().decode()[:5])
    temperatura = board.readline().decode()

    if '°C' in temperatura:
        print(f"TEMPERATURA => {temperatura}")
        # Replace temperatura and humedad fields
        shelf[identificador]['parametros']['temperatura'] = float(
            temperatura[:5])

    # Fetch humedad
    board.write(b'X')
    # humedad = float(board.readline().decode()[:5])
    humedad = board.readline().decode()
    if '%' in humedad:
        print(f"HUMEDAD => {humedad}")
        shelf[identificador]['parametros']['humedad'] = float(humedad[:5])

    return shelf[identificador]


def handle_ultrasonico(board, shelf, identificador):
    # Fetch movimiento
    board.write(b'V')
    movimiento = board.readline().decode()
    if 'cm' in movimiento:
        print(f"MOVIMIENTO => {movimiento}")
        # Replace movimiento field
        shelf[identificador]['parametros']['distancia'] = float(movimiento[:5])

    return shelf[identificador]

def handle_temp_hum(board, shelf, identificador):
    # Fetch temperatura
    board.write(b'O')
    temperatura = float(board.readline().decode()[:5])
    print(f"TEMPERATURA => {temperatura}°C")

    # Fetch humedad
    board.write(b'X')
    humedad = float(board.readline().decode()[:5])
    print("HUMEDAD => {humedad}%")

    # Replace temperatura and humedad fields
    shelf[identificador]['parametros']['temperatura'] = temperatura
    shelf[identificador]['parametros']['humedad'] = humedad

    return shelf[identificador]

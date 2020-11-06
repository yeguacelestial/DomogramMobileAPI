def send_serial(board, args, shelf, identificador, dato_serial):
    print("DATO SERIAL => ", dato_serial)
    board.write(dato_serial)

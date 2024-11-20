import os

# Función para limpiar la pantalla
def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

# Función para imprimir el tablero
def mostrar_tablero(tablero):
    limpiar_pantalla()
    for fila in tablero:
        print(" | ".join(fila))
        print("-" * 9)

# Función para verificar si hay un ganador
def verificar_ganador(tablero):
    # Verificar filas, columnas y diagonales
    for i in range(3):
        if tablero[i][0] == tablero[i][1] == tablero[i][2] != "-":
            return tablero[i][0]  # Ganador en fila
        if tablero[0][i] == tablero[1][i] == tablero[2][i] != "-":
            return tablero[0][i]  # Ganador en columna
    if tablero[0][0] == tablero[1][1] == tablero[2][2] != "-":
        return tablero[0][0]  # Ganador en diagonal principal
    if tablero[0][2] == tablero[1][1] == tablero[2][0] != "-":
        return tablero[0][2]  # Ganador en diagonal secundaria
    return None

# Función principal del juego
def juego_gato():
    # Inicializar tablero y turno
    tablero = [["-" for _ in range(3)] for _ in range(3)]
    turno = "X"
    movimientos_restantes = 9

    while movimientos_restantes > 0:
        mostrar_tablero(tablero)
        print(f"Turno de {turno}. Elija una posición (1-9):")

        try:
            posicion = int(input()) - 1  # Convertir a índice base 0
            fila, columna = divmod(posicion, 3)  # Obtener fila y columna

            if tablero[fila][columna] == "-":
                tablero[fila][columna] = turno
                movimientos_restantes -= 1

                # Verificar si hay un ganador
                ganador = verificar_ganador(tablero)
                if ganador:
                    mostrar_tablero(tablero)
                    print(f"¡{ganador} ha ganado el juego!")
                    break

                # Cambiar turno
                turno = "O" if turno == "X" else "X"
            else:
                print("La posición ya está ocupada. Intenta de nuevo.")
        except (ValueError, IndexError):
            print("Entrada no válida. Introduce un número entre 1 y 9.")

    else:
        mostrar_tablero(tablero)
        print("¡Es un empate!")

# Ejecutar el juego
if __name__ == "__main__":
    while True:
        juego_gato()
        respuesta = input("¿Quieres jugar otra vez? (S/N): ").strip().upper()
        if respuesta != "S":
            print("¡Gracias por jugar!")
            break

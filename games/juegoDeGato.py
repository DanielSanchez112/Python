import os
tablero = [["-","-","-"],["-","-","-"],["-","-","-"]]
diccionarioX = { 7:0, 8:0, 9:0, 4:1, 5:1, 6:1, 1:2, 2:2, 3:2}
diccionarioY = { 7:0, 8:1, 9:2, 4:0, 5:1, 6:2, 1:0, 2:1, 3:2} 

def nadieGana():
    i = 0        
    for x in range(3):
        vic = tablero[x][0]
        vic1 = tablero[x][1]
        vic2 = tablero[x][2]

        if vic != "-" and vic1 != "-" and vic2 != "-":
            i = i + 1
        if i == 3:
            print("nadie gana jaja")
            return True
    i = 0
    

def victorias(turno):
    # victoria horizontal
    for x in range(3):
        vic = tablero[x][0]
        vic1 = tablero[x][1]
        vic2 = tablero[x][2]

        if vic == turno and vic1 == turno and vic2 == turno:
            print("ganador son: " + turno)
            return True

    # victoria vertical
    for x in range(3):
        vic = tablero[0][x]
        vic1 = tablero[1][x]
        vic2 = tablero[2][x]

        if vic == turno and vic1 == turno and vic2 == turno:
            print("ganador son: " + turno)
            return True

    # victoria en diagonal
    vic = tablero[0][0]
    vic1 = tablero[1][1]
    vic2 = tablero[2][2]
    if vic == turno and vic1 == turno and vic2 == turno:
        print("ganador son: " + turno)
        return True
    vic = tablero[0][2]
    vic1 = tablero[1][1]
    vic2 = tablero[2][0]
    if vic == turno and vic1 == turno and vic2 == turno:
        print("ganador son: " + turno)
        return True

   

def imprimirTablero():
    for fila in tablero:
        print(fila)

def seleccionarPosicion(posicion,turno):
    y = diccionarioX[posicion]
    x = diccionarioY[posicion]
    if tablero[y][x] == "-":
        tablero[y][x] = turno
        return True
    else:
        return False

def jugarGato():
    turno = "X"
    while True:
        imprimirTablero()

        #ejecuta la seleccion de posicion
        posiciones = input("turno de " + turno + ": ")
        posicion = int(posiciones)
        if posicion < 10 and posicion > 0:
            if seleccionarPosicion(posicion,turno) == False:
                os.system('cls')
                print("posicion ya usada")  
                continue
        else:
            os.system('cls')
            print(" solo se pueden jugar posiciones del 1 al 9")   
            continue
        os.system('cls')

        # decide al ganador
        if victorias(turno) == True:
            imprimirTablero()
            break
        elif nadieGana():
            imprimirTablero()
            break

        # asigna el turno a las X y O
        if turno == "X":
            turno = "O"
        else:
            turno = "X"

if __name__ == "__main__":
    while True:
        jugarGato()
        respuesta = input("¿Quieres jugar otra vez? (S/N): ").strip().upper()
        os.system('cls')
        tablero = [["-","-","-"],["-","-","-"],["-","-","-"]]
        if respuesta != "S":
            print("¡Gracias por jugar!")
            break

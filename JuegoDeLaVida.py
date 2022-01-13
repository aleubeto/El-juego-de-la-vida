#0.Importar librerías
import pygame
import numpy as np
import time

#1.Crear canvas (500 x 500)
pygame.init()
width, height = 500, 500
screen = pygame.display.set_mode((height,width))
bg = 25, 25, 25 #intensidad de 25 en cada canal de color
screen.fill(bg)

#2. Creación de celdas
nxC, nyC = 50, 50   #25 celdas en ambos ejes
dimCW = width/nxC   #ancho de celdas
dimCH = height/nyC  #alto de celdas

#3. Estructura de estados de celdas
gameState = np.zeros((nxC,nyC)) #matriz vacia de 25x25

#4. Control de pausa del juego
pauseExect = True

#5. Bucle de ejecución
while True:

    #Copia del estado actual del juego
    newGameState = np.copy(gameState)

    #Limpieza de pantalla
    screen.fill(bg)
    time.sleep(0.25)

    #Registro de eventos de teclado y ratón
    ev = pygame.event.get()
    for event in ev:

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        elif event.type == pygame.KEYDOWN:
            pauseExect = not pauseExect

        #Detección de ratón
        mouseClick = pygame.mouse.get_pressed()
        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX/dimCW)), int(np.floor(posY/dimCH))
            newGameState[celX,celY] = not mouseClick[2]

    for y in range (0, nxC):
        for x in range (0, nyC):

            if not pauseExect:

                #Cálculo de el número de vecinos cercanos
                n_neigh =   gameState[(x - 1) % nxC, (y - 1) % nyC] + \
                            gameState[(x) % nxC, (y - 1) % nyC] + \
                            gameState[(x + 1) % nxC, (y - 1) % nyC] + \
                            gameState[(x - 1) % nxC, (y) % nyC] + \
                            gameState[(x + 1) % nxC, (y) % nyC] + \
                            gameState[(x - 1) % nxC, ( y + 1) % nyC] + \
                            gameState[(x) % nxC, (y + 1) % nyC] + \
                            gameState[(x + 1) % nxC, (y + 1) % nyC]

                #Regla 1: Una celda apagada con exactamente 3 vecinas encendidas, se enciende
                if gameState[x,y] == 0 and n_neigh == 3:
                    newGameState[x,y] = 1

                #Regla 2: Una celda encendida con menos de 2 o más de 3 vecinas encendidas, se apaga
                elif gameState[x,y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newGameState[x,y] = 0

            #Creación del polígono de cada celda a dibujar
            poly = [((x) * dimCW, y * dimCH),
                    ((x+1) * dimCW, y * dimCH),
                    ((x+1) * dimCW, (y+1) * dimCH),
                    ((x) * dimCW, (y+1) * dimCH)]

            #Dibujo de celda para cada par de X e Y
            if newGameState[x,y] == 0:
                pygame.draw.polygon(screen, (128,128,128),poly,1)
            else:
                pygame.draw.polygon(screen, (255,255,255),poly,0)
    
    #Actualización del estado del juego
    gameState = np.copy(newGameState)

    #Actualización de pantalla
    pygame.display.flip()
#!/usr/bin/env python
# la siguiente línea no es necesaria en python 3
# -*- coding: utf-8 -*-

# Módulos
import os
import sys
import pygame
from pygame.locals import *  # para QUIT, teclas etc.

# Constantes
WIDTH = 640
HEIGHT = 480


# Clases
# ---------------------------------------------------------------------

class Bola(pygame.sprite.Sprite):
    """
    La línea 1 crea la clase Bola que hereda los métodos de la clase pygame.sprite.Sprite, esto es muy importante
    debido a que contiene métodos necesarios para el manejo de Sprites.

    La línea 2 crea el método __init__ que inicializa la clase.

    La línea 3 invoca al método init de la clase heredada, muy importante también y difícil de explicar para comenzar.

    La línea 4 ya nos suena más y lo que hace es cargar con nuestra función load_image() la imagen de la pelota,
    como vemos tenemos puesto True porque la pelota si tiene zonas transparentes.

    La línea 5 es de las cosas más útiles de pygame la función self.image.get_rect() obtiene un rectangulo con las
    dimensiones y posición de la imagen (en este caso self.image) y se lo asignamos a self.rect

    Aquí hago un inciso para comentar que get_rect() tiene unos parámetros muy útiles que podemos modificar para
    posicionar y redimensionar nuestra imagen, son los siguientes:

        top, left, bottom, right
        topleft, bottomleft, topright, bottomright
        midtop, midleft, midbottom, midright
        center, centerx, centery
        size, width, height
        w, h

    Así que podemos acceder a los diferentes valores como self.rect.centerx que nos devuelve la posición central de
    la pelota respecto al ancho de la pantalla, y así con todos es cuestión de probarlos, pero más o menos se
    entiende lo que devuelve cada uno. Lo mejor de todos ellos es que si cambias el valor de alguno el resto se
    actualiza. Aquí lo tenéis mejor expliado.

    En la línea 6 y 7 usamos las propiedades de rect y con centerx y centery definimos el centro de la pelota en el
    centro de la pantalla. (aquí vemos porque pusimos WIDTH y HEIGHT como constantes globales).

    La línea 8 define la velocidad que queremos para la pelota, separamos la velocidad en dos, la velocidad en el eje
    x y la velocidad en el eje y, luego veremos porqué.
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("images/ball.png", True)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.centery = HEIGHT // 2
        self.speed = [0.5, -0.5]

    def actualizar(self, time):
        """[summary] La linea 1 define el método, recibe el parámetro self (como siempre) y el parámetro time que es
        el tiempo transcurrido, más adelante lo explicamos.

        La línea 2 y 3 usa la física básica de espacio es igual a la velocidad por el tiempo (e = v*t), por tanto
        establecemos que el centro de nuestro rectangulo en x es el valor que tenía (self.rect.centerx) más (+=) la
        valocidad a la que se mueve en el eje x (self.speed[0]) por (*) el tiempo transcurrido (time). Lo mismo se
        aplica al eje y en la línea 3.

        La linea 4, 5 y 6 establece que si la parte izquierda del rectángulo de la bola es menor o igual a 0 ó mayor
        o igual a el ancho de la pantalla (WIDTH), es decir,  que este en el extremo izquierdo o derecho,
        la velocidad de x (self.speed[0]) cambie de signo (-self.speed[0]) con esto conseguiremos que vaya hacia el
        otro lado.

        Las líneas 7, 8 y 9 es lo mismo pero en el eje y como se puede ver.

        Args:
            time ([type]): [description]
        """
        self.rect.centerx += int(self.speed[0] * time)
        self.rect.centery += int(self.speed[1] * time)
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed[0] = -self.speed[0]
            self.rect.centerx += int(self.speed[0] * time)
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed[1] = -self.speed[1]
            self.rect.centery += self.speed[1] * time

# ---------------------------------------------------------------------

# Funciones
# ---------------------------------------------------------------------


def load_image(filename, transparent=False):
    try:
        image = pygame.image.load(filename)
    except pygame.error as message:
        raise SystemExit(message)
    image = image.convert()
    if transparent:
        colour = image.get_at((0, 0))
        image.set_colorkey(colour, pygame.RLEACCEL)
    return image


# ---------------------------------------------------------------------


def main():
    # establecer el modo de la pantalla de juego
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pruebas Pygame")  # crear y abrir la ventana
    background_image = load_image('images/fondo_pong.png')  # cargar imagen
    bola = Bola()

    # Ahora vamos a crear un reloj que controle el tiempo del juego, esto es
    # importante para el movimiento, pues sabemos cuanto tiempo a pasado desde
    # la ultima actualización de la pelota y con ello poder situarla en el espacio.
    clock = pygame.time.Clock()

    while True:  # bucle de juego Game Loop
        # Ahora necesitamos saber cuanto tiempo pasa cada vez que se ejecuta
        # una interección del bucle, para ello dentro del bucle ponemos como primera línea:
        #60 nos da el "framerate"
        time=clock.tick(60)
        for eventos in pygame.event.get():  # manejo de eventos
            if eventos.type == QUIT:  # pygame.locals.QUIT
                pygame.quit()
                sys.exit(0)


        bola.actualizar(time) #actualizar la posición de la bola antes de repintar
        screen.blit(background_image, (0, 0)) # ponerla en la ventana, en la posición x=0,y=0
        screen.blit(bola.image, bola.rect)
        pygame.display.flip()  # actualiza la pantalla para que se muestre la imagen
    return 0


if __name__ == '__main__':
    # establecer variable de entorno para centrar la venta Linux, ¿Windows?
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()  # habla por sí sola
    main()

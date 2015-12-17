# Program: Superpong !
# Date: 12-10-2015
# Edited by: Cody Huzarski


import pygame, sys, math, time
from pygame.locals import *
from rotating_rectangle import RotatingRect
from controllers import *
from util import LifeCycles
from game import Game


def exitCheck():
    for event in pygame.event.get():
        if event.type == QUIT:
            print("Exited by user")
            exitGame()

def exitGame():
    pygame.quit()
    sys.exit()

def main():

    surface_width = 1280
    surface_height = 720

    pygame.init()
    surface = pygame.display.set_mode((surface_width, surface_height))
    pygame.display.set_caption("Super Pong!")
    clock = pygame.time.Clock()
    FPS = 60
    lifecycles = LifeCycles()
    curr_lifecycle = None

    # register all lifecycles
    lifecycles.register_lifecycle("game", Game(surface))

    curr_lifecycle = lifecycles.get_lifecycle("game")

    while True:
        # First thing to do is check for exit
        exitCheck()


        # Lifecycle cycle method is called here

        curr_lifecycle.cycle()


        # End of loop
        pygame.display.flip()
        clock.tick(FPS)


main()
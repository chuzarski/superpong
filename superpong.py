# Program: Superpong !
# Date: 12-10-2015
# Edited by: Cody Huzarski


import pygame, sys, math, time
from pygame.locals import *
from rotating_rectangle import RotatingRect
from controllers import *
from util import LifeCycles
from game import Game
from start_screen import StartScreen


def exitCheck():
    for event in pygame.event.get():
        if event.type == QUIT:
            print("Exited by user")
            exitGame()

def exitGame():
    pygame.quit()
    sys.exit()

def main():

    surface_width = 960
    surface_height = 540

    pygame.init()
    surface = pygame.display.set_mode((surface_width, surface_height))
    pygame.display.set_caption("Super Pong!")
    clock = pygame.time.Clock()
    FPS = 60
    lifecycles = LifeCycles()
    curr_lifecycle = None

    result = 0

    # register all lifecycles
    lifecycles.register_lifecycle("game", Game(surface))
    lifecycles.register_lifecycle("start", StartScreen(surface))

    curr_lifecycle = lifecycles.get_lifecycle("start")

    while True:
        # First thing to do is check for exit
        exitCheck()

        if result == 100:
            curr_lifecycle = lifecycles.get_lifecycle("game")
        elif result == 200:
            lifecycles.get_lifecycle("game").__init__(surface)
            curr_lifecycle = lifecycles.get_lifecycle("game")
        elif result == 1:
            lifecycles.get_lifecycle("start").set_winning_player(1)
            curr_lifecycle = lifecycles.get_lifecycle("start")
        elif result == 2:
            lifecycles.get_lifecycle("start").set_winning_player(2)
            curr_lifecycle = lifecycles.get_lifecycle("start")

        # Lifecycle cycle method is called here
        result = curr_lifecycle.cycle()


        # End of loop
        pygame.display.flip()
        clock.tick(FPS)


main()
from util import LifeCycle
import pygame
from pygame.locals import *
from colors import *
class StartScreen(LifeCycle):

    def __init__(self, surface, win_player=0):
        LifeCycle.__init__(self, surface)

        self.player = win_player

        self.normal_font = pygame.font.Font("airstrike.ttf", 48)
        self.small_font = pygame.font.Font("airstrike.ttf", 32)

    def draw_first_play(self):
        stringBlit = self.normal_font.render("Hit spacebar to play", 1, (255, 255, 255))
        self.surface.blit(stringBlit, (self.surface_size[1] / 2, 200))

    def draw_play_again(self):
        p = "Player 3"

        if self.player == 1:
            p = "Player 1"
        elif self.player == 2:
            p = "Player 2"

        stringBlit = self.normal_font.render(p + " has won the game!", 1, (255, 255, 255))
        self.surface.blit(stringBlit, (self.surface_size[1] / 2, 200))

        second_stringBlit = self.small_font.render("Press the spacebar to play again", 1, (255, 255, 255))
        self.surface.blit(second_stringBlit, (self.surface_size[1] / 2, 250))

    def set_winning_player(self, p):
        self.player = p

    def cycle(self):
        keys = pygame.key.get_pressed()
        self.surface.fill(COLOR_BLACK)

        if keys[K_SPACE]:
            if self.player == 0:
                return 100
            else:
                return 200

        if self.player == 0:
            self.draw_first_play()
        else:
            self.draw_play_again()
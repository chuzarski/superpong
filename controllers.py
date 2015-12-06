import pygame
from pygame.locals import *

class Controller():
    # Basic controller class
    def __init__(self):

        # Control types
        self.CONTROL_UP = 'u'
        self.CONTROL_DOWN = 'd'
        self.CONTROL_ROT_FORWARD = 'f'
        self.CONTROL_ROT_BACKWARD = 'b'

    def poll(self):
        return dict()

class KeyboardController(Controller):
    def __init__(self, up, down, rotf, rotb):
        Controller.__init__(self) # call base class

        self.__bind_up = up
        self.__bind_down = down
        self.__bind_rotate_forward = rotf
        self.__bind_rotate_back = rotb

    def poll(self):
        events = {}

        # poll pygame for keyboard
        keys = pygame.key.get_pressed()

        # up
        if keys[self.__bind_up]:
            events[self.CONTROL_UP] = True
        else:
            events[self.CONTROL_UP] = False

        # down
        if keys[self.__bind_down]:
            events[self.CONTROL_DOWN] = True
        else:
            events[self.CONTROL_DOWN] = False

        # rotb
        if keys[self.__bind_rotate_back]:
            events[self.CONTROL_ROT_BACKWARD] = True
        else:
            events[self.CONTROL_ROT_BACKWARD] = False

        # rotf
        if keys[self.__bind_rotate_forward]:
            events[self.CONTROL_ROT_FORWARD] = True
        else:
            events[self.CONTROL_ROT_FORWARD] = False

        return events
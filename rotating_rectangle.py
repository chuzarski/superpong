import pygame, math
from pygame.locals import *


class RotatingRect():

    def __init__(self, x, y, width, height, rotation=0):
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        self.__rotation = rotation
        self.__rect = None

        self.__calculate_verticies()


    def __calculate_verticies(self):

        rads = math.radians(self.__rotation)

        UL  =  self.__x + ( self.__width / 2 ) * math.cos(rads) - ( self.__height / 2 ) * math.sin(rads),  self.__y + ( self.__height / 2 ) * math.cos(rads)  + ( self.__width / 2 ) * math.sin(rads)
        UR  =  self.__x - ( self.__width / 2 ) * math.cos(rads) - ( self.__height / 2 ) * math.sin(rads),  self.__y + ( self.__height / 2 ) * math.cos(rads)  - ( self.__width / 2 ) * math.sin(rads)
        LL =   self.__x + ( self.__width / 2 ) * math.cos(rads) + ( self.__height / 2 ) * math.sin(rads),  self.__y - ( self.__height / 2 ) * math.cos(rads)  + ( self.__width / 2 ) * math.sin(rads)
        LR  =  self.__x - ( self.__width / 2 ) * math.cos(rads) + ( self.__height / 2 ) * math.sin(rads),  self.__y - ( self.__height / 2 ) * math.cos(rads)  - ( self.__width / 2 ) * math.sin(rads)

        self.__verticies = [UL, UR, LR, LL]


    def setX(self, x):
        self.__x = x
        self.__calculate_verticies()

    def setY(self, y):
        self.__y = y
        self.__calculate_verticies()

    def set_width(self, width):
        self.__width = width
        self.__calculate_verticies()

    def set_height(self, height):
        self.__height = height
        self.__calculate_verticies()

    def set_rotation(self, deg):
        self.__rotation = deg
        self.__calculate_verticies()

    def get_rotation(self):
        return self.__rotation

    def get_height(self):
        return self.__height

    def get_width(self):
        return self.__width

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

    def get_rect(self):
        return self.__rect

    def draw(self, surface, color=(255, 255, 255)):
        self.__rect = pygame.draw.polygon(surface, color, self.__verticies)
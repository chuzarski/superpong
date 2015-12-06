# Program: Pong
# Date: 11-12-2015
# Edited by: Cody Huzarski

SURFACE_WIDTH = 800
SURFACE_HEIGHT = 600

import pygame, sys, math
from pygame.locals import *
from rotating_rectangle import RotatingRect
from controllers import *



class Player():

    def __init__(self, name, pos):
        self.__paddle = None
        self.__name = name
        self.__controller = Controller() # default controller. Does nothing when polled

        self.__move_rate = 4
        self.__rotate_rate = 1
        self.__rotate_max = 10
        self.__rotate_min = -10

        # init
        try:
            self.set_player_pos(pos)
        except ValueError():
            print("Incorrect position passed to the player")
            exitGame()


    def set_player_pos(self, pos):

        paddle_height = 80
        paddle_width = 10
        paddle_margin = 20
        paddle_center = (SURFACE_HEIGHT / 2) - (paddle_height / 2)

        if pos == 'l':
            # position rectangle on left side
            self.__paddle = RotatingRect(paddle_margin, paddle_center, paddle_width, paddle_height)
        elif pos == 'r':
            xpos = SURFACE_WIDTH - paddle_margin
            self.__paddle = RotatingRect(xpos, paddle_center, paddle_width, paddle_height)
        else:
            raise ValueError

    def get_paddle(self):
        return self.__paddle

    def get_name(self):
        return self.__name

    def set_controller(self, con):
        self.__controller = con

    def update_movement(self):
        e = self.__controller.poll()

        # eval up/down
        if e[self.__controller.CONTROL_UP]:
            self.__move('u')
        elif e[self.__controller.CONTROL_DOWN]:
            self.__move('d')

        # eval rotation forward/backward

        if e[self.__controller.CONTROL_ROT_FORWARD]:
            self.__rotate('f')
        elif e[self.__controller.CONTROL_ROT_BACKWARD]:
            self.__rotate('b')
        elif e[self.__controller.CONTROL_ROT_FORWARD] == False and e[self.__controller.CONTROL_ROT_BACKWARD] == False:
            self.__rotate('n')

    def get_relative_angle(self):

        return 90 - self.__paddle.get_rotation()

    def __move(self, flag):

        if flag == 'u':
            top = self.get_paddle().getY() - (self.__paddle.get_height() / 2)
            if top > 0:
                self.__paddle.setY(self.__paddle.getY() - self.__move_rate) # UP
        elif flag == 'd':
            bottom = self.get_paddle().getY() + (self.__paddle.get_height() / 2)
            if bottom < SURFACE_HEIGHT:
                self.__paddle.setY(self.__paddle.getY() + self.__move_rate) # DOWN

    def __rotate(self, flag):

        if flag == 'f':
            if self.__paddle.get_rotation() < self.__rotate_max:
                self.__paddle.set_rotation(self.__paddle.get_rotation() + self.__rotate_rate)

        elif flag == 'b':
            if self.__paddle.get_rotation() > self.__rotate_min:
                self.__paddle.set_rotation(self.__paddle.get_rotation() - self.__rotate_rate)

        elif flag == 'n':
            if self.__paddle.get_rotation() > 0:
                self.__paddle.set_rotation(self.__paddle.get_rotation() - self.__rotate_rate)
            elif self.__paddle.get_rotation() < 0:
                self.__paddle.set_rotation(self.__paddle.get_rotation() + self.__rotate_rate)

    def did_collide(self, ball):

        #For now simple bounding box collision will work but will not look right
        # TODO IMPLEMENT SAT COLLISION

        paddle_rect = self.__paddle.get_rect()
        bX = ball.getX()
        bY = ball.getY()

        return paddle_rect.collidepoint(bX, bY)


class Ball():

    def __init__(self):
        self.__rect = None
        self.__move_rate = 3
        self.__x = SURFACE_WIDTH / 2
        self.__y = SURFACE_HEIGHT / 2
        self.__move_rate = 3
        self.__radius = 7


        self.__vx = self.__x
        self.__vy = self.__y
        self.__m = 1

    def get_rect(self):
        return self.__rect

    def update_movement(self):

        # keep ref of last point
        self.__vx = self.__x
        self.__vy = self.__y

        self.__x = self.__x - self.__move_rate
        self.__y = self.__y + self.__m


    def draw(self, surface, color=(255, 255, 255)):
        self.__rect = pygame.draw.circle(surface, color, (int(self.__x), int(self.__y)), self.__radius)

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

    def recalculateY(self, normal):

        incoming = self.calculateIncomingAngle()
        diff = 0
        bA = 0

        # Find angle that we bounce off surface
        diff = (180 + incoming) - normal
        bA = 180 - diff
        bA = math.radians(bA)
        # find new slope
        self.__m = math.sin(bA) / math.cos(bA)

    def calculateIncomingAngle(self):

        sA = math.fabs(self.__vx - self.__x)
        sB = self.__vy - self.__y
        return math.degrees(math.atan(sB / sA))

    def flipX(self):
        self.__move_rate = self.__move_rate * -1

    def flipM(self):
        self.__m = self.__m * -1

def exitCheck():
    for event in pygame.event.get():
        if event.type == QUIT:
            print("Exited by user")
            exitGame()
def exitGame():
    pygame.quit()
    sys.exit()

def main():
    pygame.init()
    surface = pygame.display.set_mode((SURFACE_WIDTH, SURFACE_HEIGHT))
    pygame.display.set_caption("Super Pong!")
    clock = pygame.time.Clock()
    FPS = 60

    # ball
    ball = Ball()

    # Players
    p1 = Player("Player 1", 'l')
    p2 = Player("Player 2", 'r')

    p1.set_controller(KeyboardController(K_w, K_s, K_a, K_d))
    p2.set_controller(KeyboardController(K_UP, K_DOWN, K_RIGHT, K_LEFT))


    while True:

        exitCheck()

        # take input, update movement
        p1.update_movement()
        p2.update_movement()
        ball.update_movement()

        # draw
        surface.fill((0, 0, 0))

        p1.get_paddle().draw(surface)
        p2.get_paddle().draw(surface)

        ball.draw(surface)

        # Test collisions
        # TODO collisions should only be tested if and only if they are possible (i.e. don't test paddle collision when ball is at center of screen)

        if p1.did_collide(ball):
            print("Ball collision with player 1")
            ball.recalculateY(p1.get_relative_angle())
            ball.flipX()
            ball.flipM()
        if p2.did_collide(ball):
            print("Ball collision with player 2")
            ball.recalculateY(p1.get_relative_angle())
            ball.flipX()
            ball.flipM()

        # test wall collisions
        if ball.getY() <= 0 or ball.getY() >= SURFACE_HEIGHT:
            ball.flipM()

        pygame.display.flip()
        clock.tick(FPS)


# Entry Point
main()

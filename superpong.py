# Program: Pong
# Date: 12-10-2015
# Edited by: Cody Huzarski

SURFACE_WIDTH = 800
SURFACE_HEIGHT = 600

import pygame, sys, math, time
from pygame.locals import *
from rotating_rectangle import RotatingRect
from controllers import *



def select_effect():
    effects = ["large_paddle", "flash_bg"]
class MessageBus():

    def __init__(self):
        self.__clients = dict()

    def register(self, type, obj):

        # check for exisitng message type
        if type in self.__clients:
            # Append the object to the type list
            self.__clients[type].append(obj)
        else:
            # Create the new message type and add the object
            self.__clients[type] = list()
            self.__clients[type].append(obj)

    def post(self, type):

        type = str(type)


        if type in self.__clients:
            for c in self.__clients.get(type):
                c.message_bus_recieve(type)
        else:
            return False

class Player():

    def __init__(self, name, pos):
        self.__paddle = None
        self.__name = name
        self.__controller = Controller() # default controller. Does nothing when polled

        self.__position = pos

        self.__move_rate = 6
        self.__rotate_rate = 1
        self.__rotate_max = 10
        self.__rotate_min = -10

        self.__scoring_font = pygame.font.Font("PROMETHEUS.ttf", 64)

        self.__score = 0

        # init
        self.set_initial_pos(self.__position)

    def __reset(self):
        self.set_initial_pos(self.__position)

    def set_initial_pos(self, pos):

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

    def get_rotation(self):
        return self.__paddle.get_rotation()

    def get_name(self):
        return self.__name

    def set_controller(self, con):
        self.__controller = con

    def get_score(self):
        return self.__score

    def draw_score(self, surface):

        x_margin = 25
        y_margin = 50

        if self.__position == "l":
            horiz_pos = self.__paddle.getX() + x_margin
        elif self.__position == "r":
            horiz_pos = SURFACE_WIDTH - 64 - x_margin
        else:
            horiz_pos = SURFACE_WIDTH / 2

        scoreBlit = self.__scoring_font.render(str(self.__score), 1, (255, 255, 255))
        surface.blit(scoreBlit, (horiz_pos, y_margin))

    def score(self):
        self.__score = self.__score + 1

    def message_bus_recieve(self, type):

        if type == "reset":
            self.__reset()

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

        # For now simple bounding box collision will work but will not look right
        paddle_rect = self.__paddle.get_rect()
        bX = ball.getX()
        bY = ball.getY()

        return paddle_rect.collidepoint(bX, bY)

    def draw(self, surface):
        self.__paddle.draw(surface)
        self.draw_score(surface)

class Ball():

    def __init__(self):
        self.__rect = None
        self.__set_initial_values()



    def __reset(self):
        self.__set_initial_values()

    def __set_initial_values(self):
        self.__move_rate = 3
        self.__x = SURFACE_WIDTH / 2
        self.__y = SURFACE_HEIGHT / 2
        self.__radius = 7
        self.__x_flip = -1
        self.__y_flip = 1
        self.__effect = False

    def get_effect(self):
        return self.__effect

    def set_effect(self, effect):
        effect = str(effect)
        self.__effect = effect

    def message_bus_recieve(self, type):

        if type is "reset":
            self.__reset()

    def get_rect(self):
        return self.__rect

    def update_movement(self):
        self.__x = self.__x + (self.__move_rate * self.__x_flip)
        self.__y = self.__y - (self.__move_rate * self.__y_flip)

    def draw(self, surface, color=(255, 255, 255)):
        self.__rect = pygame.draw.circle(surface, color, (int(self.__x), int(self.__y)), self.__radius)

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

    def getX_flip(self):
        return self.__x_flip

    def getY_flip(self):
        return self.__y_flip

    def flipX(self):
        self.__x_flip = self.__x_flip * -1

    def flipY(self):
        self.__y_flip = self.__y_flip * -1

def exitCheck():
    for event in pygame.event.get():
        if event.type == QUIT:
            print("Exited by user")
            exitGame()
def exitGame():
    pygame.quit()
    sys.exit()

def handle_paddle_collision(p, ball):

    if p.get_rotation() == 0:
        ball.flipX()

    elif p.get_rotation() < 0 and ball.getY_flip() == 1:
        # Paddle is rotated FORWARD and ball is headed UP
        ball.flipX()
        ball.flipY()
    elif p.get_rotation() > 0 and ball.getY_flip() == 1:
        # Paddle is rotated BACKWARD and ball is headed
        ball.flipX()
    elif p.get_rotation() < 0 and ball.getY_flip() == -1:
        # Paddle is rotated BACKWARD and ball is headed DOWN
        ball.flipX()
        ball.flipY()
    elif p.get_rotation() > 0 and ball.getY_flip() == -1:
        ball.flipX()


def main():
    pygame.init()
    surface = pygame.display.set_mode((SURFACE_WIDTH, SURFACE_HEIGHT))
    pygame.display.set_caption("Super Pong!")
    clock = pygame.time.Clock()
    FPS = 60
    last_collision = time.time()

    message_bus = MessageBus()

    # ball
    ball = Ball()

    # Players
    p1 = Player("Player 1", 'l')
    p2 = Player("Player 2", 'r')

    p1.set_controller(KeyboardController(K_w, K_s, K_a, K_d))
    p2.set_controller(KeyboardController(K_UP, K_DOWN, K_RIGHT, K_LEFT))

    # Register for event registration
    message_bus.register("reset", p1)
    message_bus.register("reset", p2)
    message_bus.register("reset", ball)


    while True:

        exitCheck()

        # take input, update movement
        p1.update_movement()
        p2.update_movement()
        ball.update_movement()

        # draw
        surface.fill((0, 0, 0))

        p1.draw(surface)
        p2.draw(surface)

        ball.draw(surface)

        if (time.time() - last_collision) > .5: # Fixes a glitch that causes the ball to collide with paddles infinitely
            # Test collisions
            if p1.did_collide(ball):
                handle_paddle_collision(p1, ball)

            if p2.did_collide(ball):
                handle_paddle_collision(p2, ball)


        # test wall collisions
        if ball.getY() <= 0 or ball.getY() >= SURFACE_HEIGHT:
            ball.flipY()

        if ball.getX() <= 0:
            p2.score()
            message_bus.post("reset")

        if ball.getX() >= SURFACE_WIDTH:
            p1.score()
            message_bus.post("reset")

        pygame.display.flip()
        clock.tick(FPS)


# Entry Point
main()

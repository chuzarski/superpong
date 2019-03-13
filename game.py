# Program: Superpong !
# Date: 12-10-2015
# Edited by: Cody Huzarski

import pygame, sys, math, time, random
from colors import *
from pygame.locals import *
from entities import *
from controllers import *
from util import LifeCycle

class Game(LifeCycle):
    def __init__(self, surface):
        LifeCycle.__init__(self, surface)

        self.player_1 = None
        self.player_2 = None
        self.ball = Ball(self.surface_size)

        self.last_collision = time.time()
        self.total_ball_hits = 0

        self.ball_charges = ["FAST_BALL", "COLOR_FLASH", "PAD_GROW"]
        self.active_charges = list()

        self.bg_color = COLOR_BLACK
        self.initial_setup()

    def initial_setup(self):
        self.player_1 = Player("Player 1", 'l', self.surface_size)
        self.player_2 = Player("Player 2", 'r', self.surface_size)
        self.player_1.set_controller(KeyboardController(K_w, K_s, K_a, K_d))
        self.player_2.set_controller(KeyboardController(K_UP, K_DOWN, K_RIGHT, K_LEFT))


    def handle_paddle_collision(self, p, ball):
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

    def reset_all(self):
        self.ball.reset()
        self.player_1.reset()
        self.player_2.reset()

        self.total_ball_hits = 0

        self.bg_color = COLOR_BLACK

        # clear active charge states
        self.active_charges.clear()

    def player_collision_event(self, player):
        player = int(player)

        if player is 1:
            self.handle_paddle_collision(self.player_1, self.ball)
            if self.ball.has_charge():
                self.register_charge(1)
                pass

        elif player is 2:
            self.handle_paddle_collision(self.player_2, self.ball)
            if self.ball.has_charge():
                self.register_charge(2)
                pass
        else:
            return False

        self.last_collision = time.time()
        self.total_ball_hits = self.total_ball_hits + 1

        if self.total_ball_hits > 2:
            self.charge_ball()


    def generate_charge(self):
        randIdx = random.randint(0, len(self.ball_charges) - 1)

        return self.ball_charges[randIdx]

    def charge_ball(self):
        # Heads or tails, charge the ball?
        if bool(random.getrandbits(1)):
            self.ball.set_charge(self.generate_charge())
        else:
            return False

    def register_charge(self, consumer):

        c = self.ball.get_charge()
        self.ball.clear_charge()

        if c is self.ball_charges[0]: # Fast Ball
            self.active_charges.append(ChargeType(self.ball_charges[0], "NUM_HITS", self.total_ball_hits))

        elif c is self.ball_charges[1]: # Color flash
            self.active_charges.append(ChargeType(self.ball_charges[1], "TIME", time.time()))
        elif c is self.ball_charges[2]: # paddle grow
            self.active_charges.append(ChargeType(self.ball_charges[2], "NUM_HITS",
                                                  self.total_ball_hits, consumer))

    def handle_active_charges(self):
        if len(self.active_charges) > 0:
            for c in self.active_charges:
                if c == self.ball_charges[0]: # fast ball
                    self.handle_fast_ball(c)
                elif c == self.ball_charges[1]: # color flash
                        self.handle_bg_flash(c)
                elif c == self.ball_charges[2]: # Paddle grow
                    self.handle_paddle_grow(c)

    def handle_fast_ball(self, charge):

        # check expiration policy
        if (self.total_ball_hits - charge.val) > 1:
            # remove from active
            self.active_charges.pop(self.active_charges.index(charge))
            # reset ball
            self.ball.set_speed(5)
            return True

        if self.ball.get_speed() < 9:
            self.ball.set_speed(9)

    def handle_bg_flash(self, charge):
        # check expiration policy
        if(time.time() - charge.val) > 3:
            # remove from active
            self.active_charges.pop(self.active_charges.index(charge))

            # reset bg and ball
            self.bg_color = COLOR_BLACK
            self.ball.set_color(COLOR_WHITE)

            return True

        color_list = [COLOR_BLACK, COLOR_WHITE, COLOR_BLUE,
                      COLOR_PURPLE, COLOR_GREEN, COLOR_RED, COLOR_CYAN, COLOR_YELLOW]
        rIdx = 0
        bIdx = 0
        bIdx = random.randint(1, len(color_list) - 2)
        while True:
            rIdx = random.randint(0, len(color_list) - 1)

            if self.bg_color is not color_list[rIdx]:
                break

        self.bg_color = color_list[rIdx]
        self.ball.set_color(color_list[bIdx])

    def handle_paddle_grow(self, charge):
        player = self.player_1
        # determine player
        if charge.consumer == 1:
            player = self.player_1
        elif charge.consumer == 2:
            player = self.player_2

        # check expiration policy
        if (self.total_ball_hits - charge.val) > 3:
            # remove charge from active
            self.active_charges.pop(self.active_charges.index(charge))
            # disable
            player.paddle_grow_active = False

        elif not player.paddle_grow_active:
            player.paddle_grow_active = True

    def cycle(self):

        # apply active charges
        self.handle_active_charges()

        # take input, update movement
        self.player_1.update_movement()
        self.player_2.update_movement()
        self.ball.update_movement()
        # draw
        self.surface.fill(self.bg_color)

        self.player_1.draw(self.surface)
        self.player_2.draw(self.surface)

        self.ball.draw(self.surface)

        if (time.time() - self.last_collision) > .5: # Fixes a glitch that causes the ball to collide with paddles infinitely
            # Test collisions
            if self.player_1.did_collide(self.ball):
                self.player_collision_event(1)
            if self.player_2.did_collide(self.ball):
                self.player_collision_event(2)


        # test wall collisions
        if self.ball.getY() <= 0 or self.ball.getY() >= self.surface_size[1]:
            self.ball.flipY()

        if self.ball.getX() <= 0:
            self.player_2.score()
            self.reset_all()

        if self.ball.getX() >= self.surface_size[0]:
            self.player_1.score()
            self.reset_all()

        if self.player_1.get_score() == 10:
            return 1
        if self.player_2.get_score() == 10:
            return 2
        return "None"

class ChargeType():
    def __init__(self, tag, expiration_policy, val, consumer=0):
        self.tag = str(tag)
        self.expiration_policy = str(expiration_policy)
        self.val = val
        self.consumer = int(consumer)

    def __eq__(self, other):

        # compare string to object
        if isinstance(other, str):
            if other == self.tag:
                return True
            else:
                return False

        # compare objet to object
        if other.tag == self.tag:
            return True
        else:
            return False

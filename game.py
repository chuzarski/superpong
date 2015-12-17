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

        self.ball_charges = ["FAST_BALL"]
        self.active_powerups = dict()

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
        self.active_powerups.clear()

    def player_collision_event(self, player):
        player = int(player)

        if player is 1:
            self.handle_paddle_collision(self.player_1, self.ball)
            if self.ball.has_charge():
                self.handle_charge(1)

        elif player is 2:
            self.handle_paddle_collision(self.player_2, self.ball)
            if self.ball.has_charge():
                self.handle_charge(2)
        else:
            return False

        self.last_collision = time.time()
        self.total_ball_hits = self.total_ball_hits + 1

        self.charge_ball()

    def handle_charge(self, consumer):
        consumer = int(consumer)

        c = self.ball.get_charge()
        self.ball.clear_charge()

        if c not in self.active_powerups:
            if c is "FAST_BALL":
                self.active_powerups[c] = self.total_ball_hits
        else:
            return False

    def handle_powerup(self):
        for p in self.active_powerups.keys():
            if p is "FAST_BALL":
                self.handle_fast_ball()

    def handle_fast_ball(self):
        # check expiration policy
        if self.total_ball_hits - self.active_powerups["FAST_BALL"] is 1:
            # remove set ball back and remove policy
            self.ball.set_speed(5)
            del self.active_powerups["FAST_BALL"]
        else:
            if self.ball.get_speed() < 7:
                self.ball.set_speed(7)
    def generate_charge(self):
        randIdx = random.randint(0, len(self.ball_charges) - 1)

        print("Charing with: ", self.ball_charges[randIdx])

        return self.ball_charges[randIdx]

    def charge_ball(self):
        # Heads or tails, charge the ball?
        if bool(random.getrandbits(1)):
            self.ball.set_charge(self.generate_charge())
        else:
            return False

    def cycle(self):
        # take input, update movement
        self.player_1.update_movement()
        self.player_2.update_movement()
        self.ball.update_movement()

        # draw
        self.surface.fill((0, 0, 0))

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

        self.handle_powerup()



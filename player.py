# -*- coding: utf-8; -*-

from OpenGL.GL import *
import game
import math

class Player(object):
    max_speed = 1.5

    def __init__(self):
        self.x = 0
        self.y = 1 # starts a bit in the air
        self.z = 0

        # speed
        self.vel = 0.0
        self.acc = 0.0
        
        # for jumps
        self.in_air = True
        self.jump_pow = 0.0

    def render(self):
        glPushMatrix()
        glTranslatef(player.x, player.y, player.z)
        glColor4f(1,1,1,1)
        glBegin(GL_QUADS)
        glVertex3f(-0.1, 1.5, 0)
        glVertex3f( 0.1, 1.5, 0)
        glVertex3f( 0.1,   0, 0)
        glVertex3f(-0.1,   0, 0)
        glEnd()
        glPopMatrix()

    def inc(self):
        self.acc = 0.01
        if self.vel > 0.0:
            self.acc *= 1.0 - (self.vel/Player.max_speed)

    def dec(self):
        self.acc = -0.1

    def jump(self):
        if self.in_air:
            return

        self.jump_pow += 2

        if self.jump_pow == 13:
            self.in_air = True

    def update(self):
        # get height
        mx = int(math.ceil(player.x-0.5) + 2)
        my =  int(player.z)
        height = -1
        try:
            height = map[my][mx]
        except IndexError:
            pass
        print
        print 'px:', player.x
        print player.x - 0.5
        print math.ceil(player.x-0.5)
        print mx, player.x, '    ',  my, height

        if self.jump_pow > 0:
            self.y += 0.2
            self.jump_pow -= 1

        if self.y < height:
            raise game.Lost, 'crashed'

        self.y -= 0.1
        if self.y < height:
            self.in_air = False
            self.y = height

        # fell down
        if self.y < -0.9:
            raise game.Lost, 'fell down'

        self.vel += self.acc
        self.z += self.vel
        self.acc = 0.0

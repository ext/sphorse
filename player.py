# -*- coding: utf-8; -*-

from OpenGL.GL import *

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
        glVertex3f(-0.5, 1.5, 0)
        glVertex3f( 0.5, 1.5, 0)
        glVertex3f( 0.5,   0, 0)
        glVertex3f(-0.5,   0, 0)
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

        if self.jump_pow == 10:
            self.in_air = True

    def update(self):
        if self.jump_pow > 0:
            self.y += 0.2
            self.jump_pow -= 1

        self.y -= 0.1

        if self.y < 0.0:
            self.in_air = False
            self.y = 0.0

        self.vel += self.acc
        self.z += self.vel
        self.acc = 0.0


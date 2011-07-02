# -*- coding: utf-8; -*-

from OpenGL.GL import *
import game
import math
from sprite import Sprite

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

        self.sprite = Sprite('player.png', 10)
        self.shadow = Sprite('shadow.png', 1)
        self.frame = 0

    def render(self):
        h = self.calc_height()
        
        if h > -0.1:
            glPushMatrix()
            glTranslatef(player.x, h + 0.01, player.z)
            
            self.shadow.bind()
            glBegin(GL_QUADS)
            glTexCoord2f(0,0)
            glVertex3f(-0.4, 0, -0.4)
            glTexCoord2f(1,0)
            glVertex3f( 0.4, 0, -0.4)
            glTexCoord2f(1,1)
            glVertex3f( 0.4, 0,  0.4)
            glTexCoord2f(0,1)
            glVertex3f(-0.4, 0,  0.4)
            glEnd()

            glPopMatrix()

        glPushMatrix()
        glTranslatef(player.x, player.y, player.z)
        glColor4f(1,1,1,1)
        self.sprite.bind()
      
        t = self.sprite.index((self.frame / 3) % 10)
        self.frame += 1

        glBegin(GL_QUADS)
        glTexCoord2f(*t[3])
        glVertex3f(-0.4, 1.5, 0)

        glTexCoord2f(*t[0])
        glVertex3f( 0.4, 1.5, 0)

        glTexCoord2f(*t[1])
        glVertex3f( 0.4,   0, 0)

        glTexCoord2f(*t[2])
        glVertex3f(-0.4,   0, 0)
        glEnd()

        glPopMatrix()

    def inc(self):
        self.acc = 0.01
        if self.vel > 0.0:
            self.acc *= 1.0 - (self.vel/Player.max_speed)

    def dec(self):
        self.acc = -0.1
        if self.vel < 0.0:
            self.acc *= 1.0 - (self.vel/(-Player.max_speed*0.3))

    def jump(self):
        if self.in_air:
            return

        self.jump_pow += 2

        if self.jump_pow == 13:
            self.in_air = True

    def update(self):
        height = self.calc_height()

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

    def calc_height(self):
        # get height (from two sample points)
        mx1 = int(math.ceil(player.x-0.8) + 2)
        mx2 = int(math.ceil(player.x-0.2) + 2)
        my =  int(player.z)
        height1 = -1
        height2 = -1
        try:
            height1 = map[my][mx1]
        except IndexError:
            pass
        try:
            height2 = map[my][mx2]
        except IndexError:
            pass
        return max(height1, height2)

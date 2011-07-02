# -*- coding: utf-8; -*-

from OpenGL.GL import *
import game
import math
from sprite import Sprite

class Player(object):
    max_speed = 1.8

    def __init__(self):
        self.x = 2
        self.y = 2 # starts a bit in the air
        self.z = 960

        # speed
        self.vel = 0.0
        self.acc = 0.0
        
        # for jumps
        self.in_air = True
        self.jump_pow = 0.0
        self.jumping = False

        self.sprite = Sprite('player.png', 10)
        self.shadow = Sprite('shadow.png', 1)
        self.frame = 0

    def render(self):
        h,_ = self.calc_height()
        
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
        glPushAttrib(GL_ENABLE_BIT)
        #glDisable(GL_DEPTH_TEST)
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

        glPopAttrib()
        glPopMatrix()

    def inc(self):
        self.acc = 0.01
        if self.vel > 0.0:
            self.acc *= 1.0 - (self.vel/Player.max_speed)

    def dec(self):
        self.acc = -0.03
        if self.vel < 0.0:
            self.acc *= 1.0 - (self.vel/(-Player.max_speed*0.3))
    
    def left(self):
        x = player.x + 0.1
        mx2 = int(math.ceil(x-0.2) + 2)
        my =  int(player.z)
        h1 = player.y
        h2 = -1
        try:
            h2 = map[my][mx2]
        except IndexError:
            pass

        lower = math.floor(h2) 
        upper = (h2 - math.floor(h2)) * 100

        if lower > 9:
            lower = int(lower) % 10 + int(lower)/10

        if lower <= h1 and (upper < 0.01 or upper > h1+1.5):
            player.x = x

    def right(self):
        x = player.x - 0.1
        mx2 = int(math.ceil(x-0.8) + 2)
        my =  int(player.z)
        h1 = player.y
        h2 = -1
        try:
            h2 = map[my][mx2]
        except IndexError:
            pass

        lower = math.floor(h2) 
        upper = (h2 - math.floor(h2)) * 100

        if lower > 9:
            lower = int(lower) % 10 + int(lower)/10

        if lower <= h1 and (upper < 0.01 or upper > h1+1.5):
            player.x = x


    def jump(self):
        if self.in_air:
            return

        self.jumping = True
        self.jump_pow += 1

        if self.jump_pow >= 20:
            self.in_air = True
            self.jumping = False

    def unjump(self):
        self.jump_pow = 0
        self.jumping = False
        self.in_air = True

    def update(self):
        lower, upper = self.calc_height()
        if self.jumping > 0:
            if self.y + 2.6 < upper:
                self.y += 0.2

        if self.y < lower or self.y+2.4 > upper:
            self.z -= self.vel
            self.acc = -0.1
            self.vel = 0.0
            return
            #raise game.Lost, 'crashed'

        self.vel *= 0.993

        self.y -= 0.1
        if self.y < lower:
            self.in_air = False
            self.y = lower

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
        
        tmp = max(height1, height2)
        lower = math.floor(tmp) 
        upper = (tmp - math.floor(tmp)) * 100

        if lower > 9:
            lower = int(lower) % 10 + int(lower)/10
        if upper < 0.001:
            upper = 9999999.0
        
        return lower, int(upper)/10

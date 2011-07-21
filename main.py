# /usr/bin/env python
# -*- coding: utf-8; -*-
import pygame, sys
from lib.game import Game
from lib.player import Player
from lib.vector import Vector2i
from level.party import map

if __name__ == '__main__':
    pygame.display.init()
	
    try:
        pygame.mixer.init()
    except Exception, e:
        print >> sys.stderr, e
    
    game = Game(size=Vector2i(800,600), fullscreen=False)

    __builtins__.game = game
    __builtins__.player = Player()
    __builtins__.map = map

    game.do_stuff()

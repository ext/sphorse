# -*- coding: utf-8; -*-
import pygame
from game import Game
from player import Player
from vector import Vector2i

if __name__ == '__main__':
    pygame.display.init()
    
    game = Game(size=Vector2i(800,600), fullscreen=False)

    __builtins__.game = game
    __builtins__.player = Player()

    game.do_stuff()

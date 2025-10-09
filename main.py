import pygame
from managers import GameManager
from settings import *

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Kingdom New Lands Clone")

    game = GameManager(screen)
    game.run()
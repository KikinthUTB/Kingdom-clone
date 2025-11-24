import pygame
import sys
from settings import *
from level import Level

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Kingdom Clone")
        self.clock = pygame.time.Clock()
        self.running = True
        self.level = Level()

    def run(self):
        while self.running:
            self.events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        self.level.run()

    def draw(self):
        self.screen.fill(BG_DAY_SKY)
        # Level draws itself in update currently, but we should separate logic and drawing
        # For now, level.run() handles drawing too
        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()

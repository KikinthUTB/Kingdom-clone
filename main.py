import pygame
import sys
from settings import *
from state_manager import StateManager, BaseState
from assets import get_assets
from world import World
from endgame import CaveState
from ui import UI

class MenuState(BaseState):
    def __init__(self, manager):
        super().__init__(manager)
        self.ui = UI(pygame.display.get_surface())

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.manager.push(GameState(self.manager))

    def draw(self, surface):
        self.ui.draw_menu()

# Game State
class GameState(BaseState):
    def __init__(self, manager):
        super().__init__(manager)
        self.world = World(self)
        self.ui = UI(pygame.display.get_surface())

    def update(self):
        self.world.update()

        # Check Win Condition / Cave Entry
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]:
             self.manager.push(CaveState(self.manager))

    def draw(self, surface):
        self.world.draw(surface)
        self.ui.draw_game_ui(self.world.player, self.world.day, self.world.is_night)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Kingdom Clone")
        self.clock = pygame.time.Clock()
        self.running = True

        # Init Assets (Pre-render)
        get_assets()

        self.state_manager = StateManager(self)
        self.state_manager.push(MenuState(self.state_manager))

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.state_manager.current().world.player.drop_coin()

    def update(self):
        self.state_manager.update()

    def draw(self):
        self.state_manager.draw(self.screen)
        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()

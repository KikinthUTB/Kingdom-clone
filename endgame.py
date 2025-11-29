import pygame
from settings import *
from assets import get_assets
from state_manager import BaseState

class Bomb(pygame.sprite.Sprite):
    def __init__(self, pos, groups, world):
        super().__init__(groups)
        self.image = pygame.Surface((30, 30))
        self.image.fill(BLACK)
        pygame.draw.circle(self.image, (255, 0, 0), (15, 15), 5) # Fuse

        self.rect = self.image.get_rect(bottomleft=pos)
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.world = world
        self.layer = L_ITEMS

        self.state = "idle" # idle, pushing, ignited
        self.target_portal = None

    def ignite(self):
        self.state = "ignited"
        print("BOMB IGNITED! RUN!")
        return True # Trigger transition to cave logic or simple explosion

class CaveState(BaseState):
    def __init__(self, manager):
        super().__init__(manager)
        self.assets = get_assets()
        # Simplified Cave: Just a boss fight or run to exit?
        # User said: "slays some greed and pay coin to ignite the bomb, then he needs to go to the entrance"
        self.bomb_ignited = False
        self.timer = 0
        self.win = False

    def update(self):
        if not self.bomb_ignited:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]: # Placeholder interaction
                self.bomb_ignited = True
                print("Ignited inside cave!")
        else:
            self.timer += 1
            if self.timer > 300: # 5 seconds to run
                print("BOOM! Victory.")
                self.win = True

    def draw(self, surface):
        surface.fill((20, 0, 20)) # Dark cave
        font = pygame.font.SysFont("Arial", 30)

        if self.win:
            text = font.render("VICTORY! The Greed are defeated.", True, YELLOW)
        elif self.bomb_ignited:
            text = font.render(f"RUN! Detonation in {5 - self.timer//60}", True, RED)
        else:
            text = font.render("Press SPACE to ignite the bomb!", True, WHITE)

        surface.blit(text, (SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2))

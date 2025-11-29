import pygame
from settings import *
from assets import get_assets
from units import Unit

class Camp(pygame.sprite.Sprite):
    def __init__(self, pos, groups, world):
        super().__init__(groups)
        self.assets = get_assets()
        # No camp asset yet, draw two sticks
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.line(self.image, BROWN, (10, 40), (20, 10), 3)
        pygame.draw.line(self.image, BROWN, (30, 40), (20, 10), 3)
        self.rect = self.image.get_rect(bottomleft=pos)
        self.layer = L_BUILDING_BG

        self.world = world
        self.spawn_timer = 0
        self.max_vagrants = 2

    def update(self):
        # Spawn vagrants slowly if below cap
        # Count vagrants nearby
        nearby_vagrants = [u for u in self.world.units if u.job == "vagrant" and abs(u.pos.x - self.rect.centerx) < 200]

        if len(nearby_vagrants) < self.max_vagrants:
            self.spawn_timer += 1
            if self.spawn_timer > 600: # 10 seconds
                self.spawn_vagrant()
                self.spawn_timer = 0

    def spawn_vagrant(self):
        Unit((self.rect.centerx, self.world.ground_y), [self.world.all_sprites, self.world.units], self.world, "vagrant")

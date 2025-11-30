import pygame
import random
from settings import *
from assets import get_assets

class Coin(pygame.sprite.Sprite):
    def __init__(self, pos, groups, ground_y, velocity=None):
        super().__init__(groups)
        self.assets = get_assets()
        self.image = self.assets['coin']
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(pos)
        self.layer = L_ITEMS

        # Physics
        # If velocity is provided, it's a "dropped" coin
        if velocity:
            self.velocity = velocity
        else:
            # Spawn logic (pop up slightly)
            self.velocity = pygame.math.Vector2(random.uniform(-2, 2), -4)

        self.gravity = 0.5
        self.ground_y = ground_y
        self.bounce_factor = -0.5
        self.on_ground = False

        self.life_timer = 0 # Can despawn if too many?

    def update(self):
        if not self.on_ground:
            self.velocity.y += self.gravity
            self.pos += self.velocity

            # Ground Collision
            if self.pos.y >= self.ground_y - 5: # Small offset for radius
                self.pos.y = self.ground_y - 5
                self.velocity.y *= self.bounce_factor
                self.velocity.x *= 0.8 # Friction

                # Stop if slow enough
                if abs(self.velocity.y) < 1:
                    self.velocity.y = 0
                    self.on_ground = True
                    self.velocity.x = 0

            self.rect.center = self.pos

import pygame
import random
from settings import *

class Coin(pygame.sprite.Sprite):
    def __init__(self, pos, groups, ground_y):
        super().__init__(groups)
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(self.image, GOLD_COLOR, (5, 5), 5)
        self.rect = self.image.get_rect(center=pos)

        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.velocity = pygame.math.Vector2(random.uniform(-2, 2), -5) # Initial pop up
        self.ground_y = ground_y
        self.restitution = 0.6 # Bounciness

        self.lifetime = 12000 # Frames? No, milliseconds? We'll tick it down or check time.
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        # Gravity
        self.velocity.y += GRAVITY

        # Move
        self.pos += self.velocity
        self.rect.topleft = self.pos

        # Ground collision
        if self.rect.bottom >= self.ground_y:
            self.rect.bottom = self.ground_y
            self.pos.y = self.rect.y
            self.velocity.y *= -self.restitution
            self.velocity.x *= 0.9 # Friction

            # Stop bouncing if too slow
            if abs(self.velocity.y) < 1:
                self.velocity.y = 0

        # Bounds check (simple)
        if self.rect.left < 0: self.rect.left = 0; self.velocity.x *= -1

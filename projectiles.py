import pygame
import math
from settings import *

class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, target, groups, ground_y, damage=1):
        super().__init__(groups)
        self.image = pygame.Surface((10, 4), pygame.SRCALPHA)
        pygame.draw.line(self.image, (255, 255, 255), (0, 2), (10, 2), 2)
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(pos)

        self.damage = damage
        self.speed = 8
        self.gravity = 0.2
        self.velocity = self.calculate_velocity(target)
        self.ground_y = ground_y

    def calculate_velocity(self, target):
        dx = target.rect.centerx - self.pos.x
        dy = target.rect.centery - self.pos.y
        angle = math.atan2(dy, dx)
        return pygame.math.Vector2(math.cos(angle), math.sin(angle)) * self.speed

    def update(self):
        self.velocity.y += self.gravity
        self.pos += self.velocity
        self.rect.center = self.pos

        # Kill if hits ground
        if self.rect.bottom > self.ground_y:
            self.kill()

        # Check off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH + 4000:
            self.kill()

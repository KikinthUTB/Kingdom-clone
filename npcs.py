import pygame
import random
from settings import *

class Vagrant(pygame.sprite.Sprite):
    def __init__(self, pos, groups, ground_y):
        super().__init__(groups)
        self.image = pygame.Surface((16, 24))
        self.image.fill((100, 100, 100)) # Grey rags
        self.rect = self.image.get_rect(bottomleft=(pos[0], ground_y))

        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.velocity = pygame.math.Vector2(0, 0)
        self.speed = 1
        self.direction = 1
        self.ground_y = ground_y

        # Behavior
        self.timer = 0
        self.is_recruited = False

    def update(self):
        if not self.is_recruited:
            self.wander()
        else:
            self.run_to_base()

        self.pos += self.velocity
        self.rect.topleft = self.pos

    def wander(self):
        self.timer += 1
        if self.timer > 100:
            self.timer = 0
            self.direction = random.choice([-1, 1, 0])

        self.velocity.x = self.direction * self.speed

        # Bounds within camp (simplified)

    def run_to_base(self):
        # Placeholder: Run to center of map
        target = 4000 // 2
        diff = target - self.pos.x
        if abs(diff) > 5:
            self.velocity.x = (diff / abs(diff)) * (self.speed * 2)
        else:
            self.velocity.x = 0
            # Change to peasant? Handled by Level or Manager?

class Camp(pygame.sprite.Sprite):
    def __init__(self, pos, groups, vagrant_groups, ground_y):
        super().__init__(groups)
        self.image = pygame.Surface((60, 40))
        self.image.fill((80, 50, 20)) # Tent color
        pygame.draw.polygon(self.image, (100, 70, 30), [(10, 40), (30, 0), (50, 40)])
        self.rect = self.image.get_rect(bottomleft=(pos[0], ground_y))
        self.vagrant_groups = vagrant_groups
        self.ground_y = ground_y

        self.spawn_timer = 0
        self.vagrants = []

    def update(self):
        self.spawn_timer += 1
        if self.spawn_timer > 600: # Spawn every 10 seconds
            self.spawn_timer = 0
            if len(self.vagrants) < 2:
                v = Vagrant((self.rect.centerx, self.rect.bottom), self.vagrant_groups, self.ground_y)
                self.vagrants.append(v)

        # Clean up vagrants list
        self.vagrants = [v for v in self.vagrants if v.alive()]

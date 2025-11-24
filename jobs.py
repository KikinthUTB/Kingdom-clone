import pygame
import random
from settings import *

class Tool(pygame.sprite.Sprite):
    def __init__(self, pos, groups, ground_y, tool_type):
        super().__init__(groups)
        self.tool_type = tool_type
        self.ground_y = ground_y

        self.image = pygame.Surface((12, 12), pygame.SRCALPHA)
        color = (255, 255, 0) if tool_type == "bow" else (150, 150, 150)
        pygame.draw.circle(self.image, color, (6, 6), 6)

        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.velocity = pygame.math.Vector2(random.uniform(-1, 1), -4)

    def update(self):
        # Gravity
        self.velocity.y += GRAVITY
        self.pos += self.velocity
        self.rect.topleft = self.pos

        # Ground
        if self.rect.bottom >= self.ground_y:
            self.rect.bottom = self.ground_y
            self.pos.y = self.rect.y
            self.velocity.y = 0
            self.velocity.x = 0

class Unit(pygame.sprite.Sprite):
    def __init__(self, vagrant_sprite, groups, job="peasant"):
        super().__init__(groups)
        # Inherit position from vagrant
        self.ground_y = vagrant_sprite.ground_y
        self.rect = vagrant_sprite.rect.copy()
        self.pos = pygame.math.Vector2(self.rect.topleft)

        self.job = job
        self.image = pygame.Surface((16, 24))
        self.update_graphics()

        self.velocity = pygame.math.Vector2(0, 0)
        self.speed = 1.5
        self.target = None # Target x position or object

        # Behavior
        self.state = "idle" # idle, move, work, hunt
        self.timer = 0

    def update_graphics(self):
        if self.job == "peasant":
            self.image.fill((100, 150, 100))
        elif self.job == "archer":
            self.image.fill((50, 200, 50))
            # Bow
            pygame.draw.arc(self.image, (139, 69, 19), (2, 5, 12, 14), -0.5, 3.5, 2)
        elif self.job == "builder":
            self.image.fill((200, 150, 100))
            # Hammer
            pygame.draw.rect(self.image, (100, 100, 100), (8, 2, 6, 4))

    def update(self):
        if self.job == "peasant":
            self.update_peasant()
        elif self.job == "archer":
            self.update_archer()
        elif self.job == "builder":
            self.update_builder()

        self.pos += self.velocity
        self.rect.topleft = self.pos

    def move_to(self, target_x):
        diff = target_x - self.pos.x
        if abs(diff) > 2:
            self.velocity.x = (diff / abs(diff)) * self.speed
        else:
            self.velocity.x = 0
            return True # Arrived
        return False

    def update_peasant(self):
        # Look for tools?
        # For now, just stand there or wander near center
        pass

    def update_archer(self):
        # Patrol or hunt
        # Simple patrol
        if self.state == "idle":
             self.timer += 1
             if self.timer > 200:
                 self.state = "patrol"
                 self.target = self.pos.x + random.randint(-100, 100)
        elif self.state == "patrol":
             if self.move_to(self.target):
                 self.state = "idle"
                 self.timer = 0

    def update_builder(self):
        # Move to construction sites (not fully implemented)
        pass

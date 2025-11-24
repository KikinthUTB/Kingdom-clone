import pygame
import random
from settings import *

class Greed(pygame.sprite.Sprite):
    def __init__(self, pos, groups, ground_y, target_func):
        super().__init__(groups)
        self.image = pygame.Surface((20, 20))
        self.image.fill((100, 0, 100)) # Purple
        pygame.draw.circle(self.image, (255, 0, 0), (5, 5), 2) # Eye

        self.rect = self.image.get_rect(bottomleft=(pos[0], ground_y))
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.velocity = pygame.math.Vector2(0, 0)
        self.speed = 2
        self.ground_y = ground_y
        self.target_func = target_func # Function to find target

        self.state = "seek" # seek, retreat
        self.item_stolen = None

    def update(self):
        if self.state == "seek":
            target = self.target_func(self.pos)
            if target:
                # Move towards target
                diff = target.rect.centerx - self.pos.x
                if abs(diff) > 5:
                    self.velocity.x = (diff / abs(diff)) * self.speed
                else:
                    self.velocity.x = 0
                    self.attack(target)
            else:
                # No target, roam?
                pass

        elif self.state == "retreat":
            # Run away to edges
            portal_x = 0 if self.pos.x < 2000 else 4000
            diff = portal_x - self.pos.x
            self.velocity.x = (diff / abs(diff)) * self.speed

            if abs(diff) < 10:
                self.kill() # Escaped

        self.pos += self.velocity
        self.rect.topleft = self.pos

    def attack(self, target):
        # Simplification: Hit target, steal item, retreat
        # Logic depends on target type

        # Player: Drop coins, if 0 coins -> drop crown
        if hasattr(target, 'coins'):
            if target.coins > 0:
                target.coins -= 1
                target.drop_coin() # Visual drop
                self.item_stolen = "coin"
                self.state = "retreat"
            else:
                 # Steal Crown
                 # We need to signal Game Over or drop crown item
                 # For now, let's say "stolen crown"
                 self.item_stolen = "crown"
                 self.state = "retreat"
                 print("CROWN STOLEN")
                 if hasattr(target, 'lose_crown'):
                     target.lose_crown()

        # Unit: Lose tool -> become peasant
        # Coin/Tool on ground: Pick up -> retreat
        # This logic is complex for collision, usually Greed overlaps item to pick up
        pass

class Portal(pygame.sprite.Sprite):
    def __init__(self, pos, groups, ground_y):
        super().__init__(groups)
        self.image = pygame.Surface((50, 80))
        self.image.fill((50, 0, 50))
        pygame.draw.circle(self.image, (150, 0, 150), (25, 40), 15)

        self.rect = self.image.get_rect(bottomleft=(pos[0], ground_y))
        self.health = 10

    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()
            print("PORTAL DESTROYED")

class DayNightCycle:
    def __init__(self):
        self.day_duration = 2000 # ticks
        self.timer = 0
        self.is_day = True
        self.day_count = 1

    def update(self):
        self.timer += 1
        if self.timer > self.day_duration:
            self.timer = 0
            self.is_day = not self.is_day
            if self.is_day:
                self.day_count += 1
                print(f"Day {self.day_count}")
            else:
                print("Night falls...")
                return True # Signal spawn wave
        return False

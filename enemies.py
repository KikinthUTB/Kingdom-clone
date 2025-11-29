import pygame
from settings import *
from assets import get_assets

class Greed(pygame.sprite.Sprite):
    def __init__(self, pos, groups, world):
        super().__init__(groups)
        self.assets = get_assets()
        self.image = self.assets['greed']
        self.rect = self.image.get_rect(bottomleft=pos)
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.velocity = pygame.math.Vector2(0, 0)
        self.world = world
        self.layer = L_UNITS

        # Stats
        self.speed = 2
        self.state = "seek" # seek, attack, retreat
        self.item_stolen = None
        self.target = None

    def update(self):
        # State Machine
        if self.state == "seek":
            self.seek_behavior()
        elif self.state == "retreat":
            self.retreat_behavior()

        # Physics
        self.pos += self.velocity
        self.rect.topleft = self.pos

        # Ground constraint
        if self.pos.y > self.world.ground_y - self.rect.height:
             self.pos.y = self.world.ground_y - self.rect.height

    def seek_behavior(self):
        # 1. Look for coins/tools on ground to steal
        # 2. Look for Player/Units/Walls to attack

        # Priority: Items > Player/Units > Walls

        # Check nearby items
        if not self.target:
            items = [i for i in self.world.items] + [c for c in self.world.coins]
            closest_item = None
            min_dist = 400

            for item in items:
                dist = abs(item.rect.centerx - self.rect.centerx)
                if dist < min_dist:
                    min_dist = dist
                    closest_item = item

            if closest_item:
                self.target = closest_item
            else:
                # Target Player
                self.target = self.world.player

        # Check Walls Blocking Path
        # Simple Raycast or Rect Check ahead
        look_ahead_rect = self.rect.move(5 if self.velocity.x > 0 else -5, 0)
        walls = [b for b in self.world.buildings if b.building_type == "wall" and b.rect.colliderect(look_ahead_rect)]

        if walls:
            self.velocity.x = 0
            self.attack(walls[0])
            return

        if self.target:
             # Move to target
             diff = self.target.rect.centerx - self.rect.centerx
             if abs(diff) > 5:
                 self.velocity.x = (diff / abs(diff)) * self.speed
             else:
                 self.velocity.x = 0
                 self.attack(self.target)

    def attack(self, target):
        # If item, pick up
        if target in self.world.coins or target in self.world.items:
            target.kill()
            self.item_stolen = "item"
            self.state = "retreat"
            self.target = None

        # If Player, hit
        elif target == self.world.player:
            # Cooldown?
            dropped = target.drop_coin()
            if not dropped:
                # Steal Crown if implemented or Game Over
                if target.coins <= 0:
                     print("GAME OVER - CROWN STOLEN")
                     # Actually steal crown logic
                     self.item_stolen = "crown"
                     self.state = "retreat"
            else:
                # Greed doesn't instantly pick up the dropped coin, it falls, then he targets it next frame
                # Force him to wait/re-target
                self.target = None

        # If Wall/Building
        elif hasattr(target, 'building_type') and target.building_type == "wall":
             # Attack logic (damage)
             # Should have cooldown
             if hasattr(target, 'take_damage'):
                 target.take_damage(1)
             else:
                 target.kill() # Instantly destroy if no HP logic yet

    def retreat_behavior(self):
        # Run to nearest edge
        portal_x = 0 if self.pos.x < self.world.width / 2 else self.world.width
        diff = portal_x - self.pos.x
        self.velocity.x = (diff / abs(diff)) * self.speed

        if abs(diff) < 10:
            self.kill() # Escaped with loot

class Portal(pygame.sprite.Sprite):
    def __init__(self, pos, groups, world, is_main=False):
        super().__init__(groups)
        self.image = pygame.Surface((60, 100))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect(bottomleft=pos)
        self.world = world
        self.is_main = is_main # The Cliff portal
        self.layer = L_BUILDING_BG

        self.health = 10 if not is_main else 50

    def spawn_wave(self, difficulty):
        for _ in range(difficulty):
            Greed((self.rect.centerx, self.world.ground_y), [self.world.all_sprites, self.world.enemies], self.world)

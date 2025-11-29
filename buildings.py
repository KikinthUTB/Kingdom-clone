import pygame
from settings import *
from assets import get_assets
from economy import Coin

class Building(pygame.sprite.Sprite):
    def __init__(self, pos, groups, world, building_type="mound"):
        super().__init__(groups)
        self.assets = get_assets()
        self.building_type = building_type # mound, wall, tower, farm, campfire
        self.world = world
        self.level = 0
        self.pos = pygame.math.Vector2(pos)
        self.layer = L_BUILDING_BG

        # Visuals
        self.image = pygame.Surface((40, 10))
        self.image.fill((100, 100, 100)) # Mound
        self.rect = self.image.get_rect(bottomleft=pos)

        # Interaction
        self.cost = 1
        self.coins_paid = 0
        self.hp = 100

        self.update_graphics()

    def update_graphics(self):
        if self.building_type == "mound":
            self.image = pygame.Surface((40, 20))
            self.image.fill((80, 80, 80))
            self.cost = 1
        elif self.building_type == "wall":
            self.image = self.assets[f'wall_{min(self.level, 2)}']
            self.cost = 3
            self.hp = 50 * self.level
        elif self.building_type == "campfire":
            self.image = self.assets['campfire']
            self.cost = 5 # Upgrade cost

        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    def take_damage(self, amount):
        if self.building_type == "wall":
            self.hp -= amount
            if self.hp <= 0:
                print("WALL DESTROYED")
                self.building_type = "mound" # Revert to mound
                self.level = 0
                self.update_graphics()

    def add_coin(self):
        self.coins_paid += 1
        print(f"Building {self.building_type} paid {self.coins_paid}/{self.cost}")
        if self.coins_paid >= self.cost:
            self.upgrade()
            self.coins_paid = 0

    def upgrade(self):
        if self.building_type == "mound":
            self.building_type = "wall"
            self.level = 1
        elif self.building_type == "wall":
            self.level += 1
        elif self.building_type == "campfire":
            self.level += 1
            # Unlocks features

        self.update_graphics()

class Shop(Building):
    def __init__(self, pos, groups, world, tool_type="bow"):
        super().__init__(pos, groups, world, "shop")
        self.tool_type = tool_type # bow, hammer, scythe
        self.image = pygame.Surface((60, 60))
        color = GREEN if tool_type == "bow" else (BROWN if tool_type == "hammer" else YELLOW)
        self.image.fill(color)
        self.rect = self.image.get_rect(bottomleft=pos)
        self.cost = 2 if tool_type == "bow" else 3

        # Shop logic
        self.tools_in_stock = 0

    def add_coin(self):
        self.coins_paid += 1
        if self.coins_paid >= self.cost:
            self.spawn_tool()
            self.coins_paid = 0

    def spawn_tool(self):
        # Spawn tool entity
        Tool(self.rect.center, [self.world.all_sprites, self.world.items], self.world, self.tool_type)

class Tool(pygame.sprite.Sprite):
    def __init__(self, pos, groups, world, tool_type):
        super().__init__(groups)
        self.tool_type = tool_type
        self.image = pygame.Surface((20, 20))
        if tool_type == "bow": self.image.fill(GREEN)
        elif tool_type == "hammer": self.image.fill(BROWN)
        elif tool_type == "scythe": self.image.fill(YELLOW)

        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(pos)
        self.velocity = pygame.math.Vector2(0, -4)
        self.world = world
        self.layer = L_ITEMS
        self.ground_y = world.ground_y

    def update(self):
        # Physics similar to coin
        self.velocity.y += GRAVITY
        self.pos += self.velocity

        if self.pos.y >= self.ground_y - 10:
            self.pos.y = self.ground_y - 10
            self.velocity.y = 0
            self.velocity.x = 0

        self.rect.center = self.pos

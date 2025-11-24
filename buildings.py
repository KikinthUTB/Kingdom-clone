import pygame
from settings import *

class Building(pygame.sprite.Sprite):
    def __init__(self, pos, groups, ground_y, building_type="mound"):
        super().__init__(groups)
        self.building_type = building_type
        self.ground_y = ground_y
        self.pos = pygame.math.Vector2(pos)

        self.level = 0
        self.image = pygame.Surface((40, 40))
        self.image.fill((100, 100, 100)) # Placeholder

        self.update_graphics()

        self.rect = self.image.get_rect(midbottom=(pos[0], ground_y))

        # Interaction
        self.cost = 1
        self.coins_stored = 0

    def update_graphics(self):
        self.image.fill((0,0,0,0)) # Clear
        if self.building_type == "mound": # For Walls
            if self.level == 0:
                pygame.draw.circle(self.image, (100, 80, 50), (20, 40), 10) # Dirt mound
                self.cost = 1
            elif self.level == 1:
                pygame.draw.rect(self.image, (139, 69, 19), (10, 20, 20, 20)) # Wood wall
                self.cost = 3

        elif self.building_type == "rock": # For Towers
            if self.level == 0:
                pygame.draw.polygon(self.image, (100, 100, 100), [(10, 40), (20, 25), (30, 40)])
                self.cost = 2

        elif self.building_type == "center": # Town Center
             if self.level == 0:
                 # Campfire
                 pygame.draw.circle(self.image, (50, 50, 50), (20, 38), 10)
                 pygame.draw.circle(self.image, (255, 100, 0), (20, 35), 5)
                 self.cost = 3
             elif self.level == 1:
                 # Tent
                 pygame.draw.polygon(self.image, (200, 200, 200), [(5, 40), (20, 10), (35, 40)])
                 self.cost = 5

    def add_coin(self):
        if self.level < 5: # Max level cap
            self.coins_stored += 1
            if self.coins_stored >= self.cost:
                self.upgrade()

    def upgrade(self):
        self.level += 1
        self.coins_stored = 0
        self.update_graphics()
        # Resize rect if image changed size (though we kept it 40x40 for now)
        self.rect = self.image.get_rect(midbottom=(self.pos.x, self.ground_y))

class Shop(Building):
    def __init__(self, pos, groups, ground_y, tool_type):
        self.tool_type = tool_type # "bow" or "hammer"
        super().__init__(pos, groups, ground_y, building_type="shop")
        # super calls update_graphics, which needs self.tool_type set first

    def update_graphics(self):
        self.image.fill((0,0,0,0))
        # Shop stand
        pygame.draw.rect(self.image, (150, 100, 50), (5, 20, 30, 20))
        # Icon
        color = (255, 255, 0) if self.tool_type == "bow" else (150, 150, 150)
        pygame.draw.circle(self.image, color, (20, 10), 5)
        self.cost = 2 if self.tool_type == "bow" else 3

    def add_coin(self):
        self.coins_stored += 1
        if self.coins_stored >= self.cost:
            self.produce_tool()
            self.coins_stored = 0

    def produce_tool(self):
        # Spawn a tool item (not implemented yet, just print for now)
        print(f"Produced {self.tool_type}")
        # Need to signal level to spawn tool
        if hasattr(self, 'spawn_tool_callback'):
            self.spawn_tool_callback(self.rect.center, self.tool_type)

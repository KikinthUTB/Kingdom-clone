import pygame
from settings import *

class AssetManager:
    """
    Generates placeholder pixel art assets procedurally.
    This avoids the need for external image files while keeping a consistent style.
    """
    def __init__(self):
        self.assets = {}
        self.generate_assets()

    def generate_assets(self):
        # Player (Crown, Cape)
        self.assets['player_idle'] = self.create_blocky_sprite(30, 50, BLUE, [(5, 0, 20, 10, YELLOW)]) # Body + Crown
        self.assets['player_run'] = self.create_blocky_sprite(30, 50, BLUE, [(5, 0, 20, 10, YELLOW), (0, 40, 10, 10, BLACK)]) # Leg moving

        # Mounts
        self.assets['horse'] = self.create_blocky_sprite(60, 40, BROWN, [(0, 30, 10, 10, BLACK), (50, 30, 10, 10, BLACK), (40, -10, 15, 20, BROWN)]) # Body + Legs + Head
        self.assets['stag'] = self.create_blocky_sprite(60, 45, (100, 80, 60), [(40, -15, 2, 10, WHITE), (50, -15, 2, 10, WHITE)]) # Antlers
        self.assets['bear'] = self.create_blocky_sprite(70, 50, (50, 30, 10), [])

        # Units
        self.assets['vagrant'] = self.create_blocky_sprite(20, 40, (100, 100, 100), [])
        self.assets['peasant'] = self.create_blocky_sprite(20, 40, (150, 150, 100), [(5, 10, 10, 30, BROWN)])
        self.assets['archer'] = self.create_blocky_sprite(20, 40, GREEN, [(15, 15, 5, 20, BROWN)]) # Bow
        self.assets['builder'] = self.create_blocky_sprite(20, 40, (200, 100, 50), [(15, 5, 10, 10, (100, 100, 100))]) # Hammer
        self.assets['farmer'] = self.create_blocky_sprite(20, 40, (200, 200, 50), [(0, 10, 30, 5, (150, 150, 150))]) # Scythe

        # Enemies
        self.assets['greed'] = self.create_blocky_sprite(20, 20, PURPLE, [(5, 5, 5, 5, RED)]) # Eye
        self.assets['floater'] = self.create_blocky_sprite(30, 30, (100, 0, 100), [(5, 5, 20, 5, WHITE)]) # Wings

        # Buildings
        self.assets['campfire'] = self.create_blocky_sprite(60, 30, (50, 50, 50), [(20, -10, 20, 20, (255, 100, 0))]) # Fire
        self.assets['wall_1'] = self.create_blocky_sprite(20, 60, BROWN, [])
        self.assets['wall_2'] = self.create_blocky_sprite(25, 80, (100, 100, 100), [])

        # Items
        self.assets['coin'] = self.create_circle_sprite(10, YELLOW)
        self.assets['gem'] = self.create_diamond_sprite(12, (0, 255, 255))

        # Environment
        self.assets['tree'] = self.create_tree(60, 150)
        self.assets['grass'] = self.create_blocky_sprite(64, 20, (50, 150, 50), [])

        # UI
        self.assets['ui_coin'] = self.create_circle_sprite(20, YELLOW)

    def create_blocky_sprite(self, width, height, color, additions):
        """
        additions: list of tuples (rel_x, rel_y, w, h, color)
        """
        # Determine bounds including additions (which might stick out)
        min_x, min_y = 0, 0
        max_x, max_y = width, height

        for add in additions:
            ax, ay, aw, ah, ac = add
            min_x = min(min_x, ax)
            min_y = min(min_y, ay)
            max_x = max(max_x, ax + aw)
            max_y = max(max_y, ay + ah)

        full_w = max_x - min_x
        full_h = max_y - min_y

        surface = pygame.Surface((full_w, full_h), pygame.SRCALPHA)

        # Offset everything by -min_x, -min_y to ensure drawing starts at 0,0
        # Draw Base
        base_rect = pygame.Rect(-min_x, -min_y, width, height)
        pygame.draw.rect(surface, color, base_rect)

        # Draw additions
        for add in additions:
            ax, ay, aw, ah, ac = add
            add_rect = pygame.Rect(ax - min_x, ay - min_y, aw, ah)
            pygame.draw.rect(surface, ac, add_rect)

        return surface

    def create_circle_sprite(self, radius, color):
        surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(surface, color, (radius, radius), radius)
        return surface

    def create_diamond_sprite(self, size, color):
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        pts = [(size//2, 0), (size, size//2), (size//2, size), (0, size//2)]
        pygame.draw.polygon(surface, color, pts)
        return surface

    def create_tree(self, width, height):
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        # Trunk
        pygame.draw.rect(surface, (100, 50, 0), (width//2 - 10, height//2, 20, height//2))
        # Leaves
        pygame.draw.circle(surface, (0, 100, 0), (width//2, height//3), width//2)
        return surface

asset_manager = None

def get_assets():
    global asset_manager
    if not asset_manager:
        asset_manager = AssetManager()
    return asset_manager.assets

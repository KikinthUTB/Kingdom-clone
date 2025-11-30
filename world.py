import pygame
import random
from settings import *
from assets import get_assets
from camera import Camera
from player import Player
from economy import Coin
from camp import Camp
from units import Unit
from buildings import Building, Shop
from enemies import Greed, Portal
from mounts_boat import Boat

class World:
    def __init__(self, state):
        self.state = state
        self.width = 6000 # Map size
        self.height = SCREEN_HEIGHT
        self.ground_y = SCREEN_HEIGHT - 80

        self.camera = Camera(self.width, self.height)
        self.assets = get_assets()

        # Groups
        self.all_sprites = pygame.sprite.Group()
        self.bg_sprites = pygame.sprite.Group() # Trees, etc
        self.coins = pygame.sprite.Group()
        self.units = pygame.sprite.Group()
        self.buildings = pygame.sprite.Group()
        self.items = pygame.sprite.Group() # Tools etc
        self.enemies = pygame.sprite.Group()
        self.portals = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()

        # Day Night
        self.time = 0
        self.day = 1
        self.is_night = False

        # Biomes Setup
        # 0-500: Ocean/Beach
        # 500-2500: Plains
        # 2500-4500: Forest
        # 4500-6000: Mountain/Cliff
        self.biomes = [
            (0, 500, 'beach'),
            (500, 2500, 'plains'),
            (2500, 4500, 'forest'),
            (4500, 6000, 'cliff')
        ]

        self.setup_world()

    def setup_world(self):
        # Generate Trees/Grass based on biomes
        for i in range(0, self.width, 100):
            biome = self.get_biome(i)

            # Trees
            if biome == 'forest':
                if random.random() < 0.8: # Dense forest
                     self.spawn_tree(i)
            elif biome == 'plains':
                if random.random() < 0.2: # Sparse
                     self.spawn_tree(i)

            # Grass
            if biome in ['plains', 'forest']:
                BackgroundObject((i, self.ground_y - 10), [self.all_sprites, self.bg_sprites], self.assets['grass'], L_BG)

        # Player
        self.player = Player((1000, self.ground_y - 40), [self.all_sprites], self)
        self.player.coins = 10 # Start with some coins

        # Camps
        Camp((600, self.ground_y), [self.all_sprites, self.buildings], self)
        Camp((2000, self.ground_y), [self.all_sprites, self.buildings], self)

        # Buildings
        Building((1000, self.ground_y), [self.all_sprites, self.buildings], self, "campfire")
        Building((800, self.ground_y), [self.all_sprites, self.buildings], self, "mound")
        Building((1200, self.ground_y), [self.all_sprites, self.buildings], self, "mound")

        # Shops
        Shop((900, self.ground_y), [self.all_sprites, self.buildings], self, "bow")
        Shop((1100, self.ground_y), [self.all_sprites, self.buildings], self, "hammer")

        # Boat
        Boat((1500, self.ground_y), [self.all_sprites, self.buildings], self)

        # Portals
        Portal((200, self.ground_y), [self.all_sprites, self.portals], self, is_main=False)
        Portal((5800, self.ground_y), [self.all_sprites, self.portals], self, is_main=True)

    def get_biome(self, x):
        for start, end, name in self.biomes:
            if start <= x < end:
                return name
        return 'plains'

    def spawn_tree(self, x):
        # Randomize x slightly
        x += random.randint(-40, 40)
        BackgroundObject((x, self.ground_y - 140), [self.all_sprites, self.bg_sprites], self.assets['tree'], L_BG)

    def update(self):
        self.update_day_cycle()
        self.all_sprites.update()
        self.camera.update(self.player)
        self.check_recruitment()
        self.check_payments()
        self.check_enemy_interactions()

    def update_day_cycle(self):
        self.time += 1
        if self.time >= DAY_LENGTH:
            self.time = 0
            self.day += 1
            print(f"Day {self.day} Begins")
            self.is_night = False

        if self.time > DAY_LENGTH * NIGHT_START_THRESHOLD and not self.is_night:
            self.is_night = True
            print("Night Falls")
            self.spawn_wave()

    def spawn_wave(self):
        for portal in self.portals:
            portal.spawn_wave(self.day)

    def check_enemy_interactions(self):
        # Projectile vs Enemy
        hits = pygame.sprite.groupcollide(self.enemies, self.projectiles, True, True)
        if hits:
            pass # Enemy dead

    def check_recruitment(self):
        # Coin vs Vagrant
        collisions = pygame.sprite.groupcollide(self.units, self.coins, False, True)
        for unit, coins in collisions.items():
            if unit.job == "vagrant":
                if unit.recruit():
                    pass

    def check_payments(self):
        # Coin vs Buildings
        collisions = pygame.sprite.groupcollide(self.buildings, self.coins, False, True)
        for building, coins in collisions.items():
            for _ in coins:
                building.add_coin()

    def draw(self, surface):
        # Draw Sky (Gradient or flat)
        surface.fill(SKY_BLUE)

        # Draw Parallax (Mountains) - Simplified as static rects for now
        # Ideally we shift them by camera.x * 0.5

        # Draw Ground
        ground_rect = pygame.Rect(0, self.ground_y, self.width, SCREEN_HEIGHT - self.ground_y)
        pygame.draw.rect(surface, GREEN, self.camera.apply_rect(ground_rect))

        # Draw Sprites
        # Sort by layer usually, but group ordering works if added correctly
        # We need custom draw loop for layers

        # Separate sprites by layers for manual Z-ordering
        for layer in range(0, 11):
            for sprite in self.all_sprites:
                if hasattr(sprite, 'layer') and sprite.layer == layer:
                     surface.blit(sprite.image, self.camera.apply(sprite))
                elif layer == L_PLAYER and sprite == self.player: # Player usually doesn't have layer attr yet
                     surface.blit(sprite.image, self.camera.apply(sprite))

class BackgroundObject(pygame.sprite.Sprite):
    def __init__(self, pos, groups, image, layer):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        self.layer = layer

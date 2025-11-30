import pygame
from settings import *
from assets import get_assets

class Mount:
    def __init__(self, name, speed, run_speed, stamina):
        self.name = name
        self.speed = speed
        self.run_speed = run_speed
        self.max_stamina = stamina
        self.stamina = stamina
        self.regen_rate = 0.5

class Boat(pygame.sprite.Sprite):
    def __init__(self, pos, groups, world):
        super().__init__(groups)
        self.assets = get_assets()
        self.world = world
        self.layer = L_BUILDING_BG

        self.phase = 0 # 0=Wreck, 1=Frame, 2=Hull, 3=Complete
        self.max_phases = 3
        self.parts_needed = 10 # per phase? Let's say 20 total parts
        self.parts_added = 0

        self.image = pygame.Surface((120, 60))
        self.image.fill((100, 50, 50)) # Wreck
        self.rect = self.image.get_rect(bottomleft=pos)
        self.pos = pygame.math.Vector2(self.rect.topleft)

        self.is_moving = False

    def add_part(self):
        self.parts_added += 1
        if self.parts_added >= self.parts_needed:
            self.advance_phase()

    def advance_phase(self):
        self.phase += 1
        if self.phase == 1:
            self.image.fill((150, 100, 50)) # Frame
        elif self.phase == 2:
            self.image.fill((200, 150, 50)) # Hull
        elif self.phase == 3:
            self.image.fill((255, 200, 50)) # Complete
            print("BOAT COMPLETED")

    def push(self, direction):
        if self.phase == 3:
            self.pos.x += direction * 0.5
            self.rect.x = round(self.pos.x)

            # Check if reached water (Biome 0)
            if self.world.get_biome(self.pos.x) == 'beach':
                print("BOAT LAUNCHED - VICTORY OPTION A")
                # Trigger end sequence or just show prompt

import pygame
from settings import *
from player import Player
from economy import Coin
from npcs import Camp, Vagrant
from buildings import Building, Shop
from jobs import Tool, Unit
from enemies import Greed, Portal, DayNightCycle
from logic import check_win_condition

class Camera:
    def __init__(self, width, height):
        self.camera_rect = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera_rect.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera_rect.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(SCREEN_WIDTH / 2)
        y = -target.rect.centery + int(SCREEN_HEIGHT / 2)

        # Limit scrolling (optional, but good for finite worlds)
        # x = min(0, x)  # left
        # x = max(-(self.width - SCREEN_WIDTH), x)  # right
        # y = max(-(self.height - SCREEN_HEIGHT), y) # bottom
        # y = min(0, y) # top

        # Lock Y axis for side scrolling
        y = 0

        self.camera_rect = pygame.Rect(x, y, self.width, self.height)

class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.world_width = 4000
        self.ground_y = SCREEN_HEIGHT - 100
        self.camera = Camera(self.world_width, SCREEN_HEIGHT)

        # Sprite Groups
        self.all_sprites = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.vagrants = pygame.sprite.Group()
        self.camps = pygame.sprite.Group()
        self.buildings = pygame.sprite.Group()
        self.tools = pygame.sprite.Group()
        self.units = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.portals = pygame.sprite.Group()

        self.day_night = DayNightCycle()

        # Setup
        self.setup_level()

    def setup_level(self):
        self.player = Player((self.world_width // 2, self.ground_y - 40), [self.all_sprites])
        self.player.lose_crown = self.game_over
        self.player.spawn_coin_callback = self.spawn_coin

        # Spawn Camps
        Camp((1000, 0), [self.all_sprites, self.camps], [self.all_sprites, self.vagrants], self.ground_y)
        Camp((3000, 0), [self.all_sprites, self.camps], [self.all_sprites, self.vagrants], self.ground_y)

        # Spawn Buildings
        # Center
        Building((self.world_width // 2, 0), [self.all_sprites, self.buildings], self.ground_y, "center")

        # Walls/Towers spots
        Building((self.world_width // 2 - 300, 0), [self.all_sprites, self.buildings], self.ground_y, "mound")
        Building((self.world_width // 2 + 300, 0), [self.all_sprites, self.buildings], self.ground_y, "mound")

        # Shops
        shop_bow = Shop((self.world_width // 2 - 150, 0), [self.all_sprites, self.buildings], self.ground_y, "bow")
        shop_bow.spawn_tool_callback = self.spawn_tool

        shop_hammer = Shop((self.world_width // 2 + 150, 0), [self.all_sprites, self.buildings], self.ground_y, "hammer")
        shop_hammer.spawn_tool_callback = self.spawn_tool

        # Portals
        Portal((100, 0), [self.all_sprites, self.portals], self.ground_y)
        Portal((3900, 0), [self.all_sprites, self.portals], self.ground_y)

    def game_over(self):
        print("GAME OVER")
        pygame.quit()
        import sys
        sys.exit()

    def spawn_coin(self, pos):
        Coin(pos, [self.all_sprites, self.coins], self.ground_y)

    def spawn_tool(self, pos, tool_type):
        Tool(pos, [self.all_sprites, self.tools], self.ground_y, tool_type)

    def draw_background(self):
        # Sky is cleared in main loop

        # Parallax placeholder (just a static rect for now or moving layers later)
        # Ground
        ground_rect = pygame.Rect(0, self.ground_y, self.world_width, SCREEN_HEIGHT - self.ground_y)
        camera_ground = self.camera.apply_rect(ground_rect)
        pygame.draw.rect(self.display_surface, GROUND_COLOR, camera_ground)

        # Water Reflection (just a darker rect below ground line)
        water_rect = pygame.Rect(0, self.ground_y + 20, self.world_width, SCREEN_HEIGHT - (self.ground_y + 20))
        camera_water = self.camera.apply_rect(water_rect)
        pygame.draw.rect(self.display_surface, WATER_COLOR, camera_water)

    def run(self):
        # Check Win
        if check_win_condition(self.portals):
             print("YOU WIN")
             # End game or keep playing?
             # For now, just print and maybe stop spawning
             self.day_night.is_day = True # Permanent day?

        # Day Night Cycle
        spawn_wave = self.day_night.update()
        if spawn_wave:
            self.spawn_greed_wave()

        # Update sprites
        self.all_sprites.update()

        # Check coin pickup
        self.check_coin_collisions()

        # Check recruitment
        self.check_recruitment()

        # Check building interaction
        self.check_building_payment()

        # Check unit job conversion
        self.check_job_conversion()

        # Check enemy collisions
        self.check_enemy_interactions()

        # Update camera
        self.camera.update(self.player)

        # Draw
        self.draw_background()
        for sprite in self.all_sprites:
            self.display_surface.blit(sprite.image, self.camera.apply(sprite))

        # UI (Simple coin counter)
        self.draw_ui()

    def check_coin_collisions(self):
        # Player pickup
        hit_coins = pygame.sprite.spritecollide(self.player, self.coins, True)
        for coin in hit_coins:
            self.player.coins += 1

    def check_recruitment(self):
        # Check if coin hits vagrant
        collisions = pygame.sprite.groupcollide(self.vagrants, self.coins, False, True)
        for vagrant, coins in collisions.items():
            if not vagrant.is_recruited:
                vagrant.is_recruited = True
                vagrant.image.fill((100, 150, 100)) # Change color to show recruited (Peasant-ish)

    def check_building_payment(self):
        collisions = pygame.sprite.groupcollide(self.buildings, self.coins, False, True)
        for building, coins in collisions.items():
            for _ in coins:
                building.add_coin()

    def check_job_conversion(self):
        # 1. Vagrant -> Peasant
        for vagrant in self.vagrants:
            if vagrant.is_recruited:
                Unit(vagrant, [self.all_sprites, self.units], job="peasant")
                vagrant.kill()

        # 2. Peasant + Tool -> Job Unit
        peasants = [u for u in self.units if u.job == "peasant"]
        for peasant in peasants:
             hit_tools = pygame.sprite.spritecollide(peasant, self.tools, True)
             for tool in hit_tools:
                 if tool.tool_type == "bow":
                     peasant.job = "archer"
                     peasant.update_graphics()
                     tool.kill() # Consume tool
                 elif tool.tool_type == "hammer":
                     peasant.job = "builder"
                     peasant.update_graphics()
                     tool.kill()

    def spawn_greed_wave(self):
        # Spawn greed at portals
        for portal in self.portals:
            count = self.day_night.day_count
            for i in range(count):
                Greed((portal.rect.centerx, 0), [self.all_sprites, self.enemies], self.ground_y, self.get_nearest_target)

    def get_nearest_target(self, pos):
        # Find nearest player or unit or interesting thing
        # Simplified: Just target Player
        return self.player

    def check_enemy_interactions(self):
        # Greed vs Player
        # We use a custom check because we want to trigger 'attack' method
        for enemy in self.enemies:
            if enemy.state == "seek":
                if enemy.rect.colliderect(self.player.rect):
                    enemy.attack(self.player)

            # Greed vs Coins (Stealing)
            hit_coins = pygame.sprite.spritecollide(enemy, self.coins, True)
            if hit_coins:
                enemy.item_stolen = "coin"
                enemy.state = "retreat"

            # Greed vs Tools
            hit_tools = pygame.sprite.spritecollide(enemy, self.tools, True)
            if hit_tools:
                enemy.item_stolen = "tool"
                enemy.state = "retreat"

    def draw_ui(self):
        # Debug font or simple rendering
        pass # Placeholder for now, maybe use pygame.font if initialized

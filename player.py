import pygame
from settings import *
from assets import get_assets
from economy import Coin

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, world):
        super().__init__(groups)
        self.assets = get_assets()
        self.image = self.assets['player_idle']
        self.rect = self.image.get_rect(topleft=pos)
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.velocity = pygame.math.Vector2(0, 0)
        self.world = world

        # Stats
        self.coins = 0
        self.gems = 0
        self.has_crown = True
        self.facing_right = True
        self.speed = PLAYER_SPEED
        self.run_speed = PLAYER_RUN_SPEED
        self.stamina = 100
        self.max_stamina = 100

        # State
        self.is_running = False
        self.is_mounted = True

        # Mounts
        self.mounts = {
            "horse": {"speed": 5, "run": 9, "stamina": 100},
            "stag": {"speed": 6, "run": 11, "stamina": 80}, # Fast but weak
            "warhorse": {"speed": 4, "run": 8, "stamina": 200}, # Tank
        }
        self.mount_type = "horse"
        self.update_mount_stats()

    def update_mount_stats(self):
        stats = self.mounts[self.mount_type]
        self.speed = stats['speed']
        self.run_speed = stats['run']
        self.max_stamina = stats['stamina']

    def swap_mount(self, new_mount):
        if new_mount in self.mounts:
            self.mount_type = new_mount
            self.update_mount_stats()
            # Visual update would happen in animate/assets

    def input(self):
        keys = pygame.key.get_pressed()

        # Movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity.x = -self.speed
            self.facing_right = False
            if keys[pygame.K_LSHIFT] and self.stamina > 0:
                self.velocity.x = -self.run_speed
                self.is_running = True
                self.stamina -= 1
            else:
                self.is_running = False
                self.stamina += 0.5
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity.x = self.speed
            self.facing_right = True
            if keys[pygame.K_LSHIFT] and self.stamina > 0:
                self.velocity.x = self.run_speed
                self.is_running = True
                self.stamina -= 1
            else:
                self.is_running = False
                self.stamina += 0.5
        else:
            self.velocity.x = 0
            self.is_running = False
            self.stamina += 1

        self.stamina = min(self.stamina, self.max_stamina)

        # Actions
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
             # We need a debounce or one-tap logic here, usually handled in event loop
             # But for continuous dropping (like Kingdom), holding it might work?
             # No, Kingdom is tap to drop.
             pass

    def update(self):
        self.input()
        self.move()
        self.animate()
        self.check_collisions()

    def check_collisions(self):
        # Pickup coins
        hit_coins = pygame.sprite.spritecollide(self, self.world.coins, True)
        for coin in hit_coins:
            self.coins += 1

    def move(self):
        self.pos.x += self.velocity.x

        # Bounds Check
        if self.pos.x < 0: self.pos.x = 0
        if self.pos.x > self.world.width - self.rect.width:
            self.pos.x = self.world.width - self.rect.width

        self.rect.x = round(self.pos.x)
        self.rect.y = round(self.pos.y) # Locked Y usually

    def animate(self):
        # Flip image based on direction
        img = self.assets['player_run'] if self.velocity.x != 0 else self.assets['player_idle']

        if not self.facing_right:
            img = pygame.transform.flip(img, True, False)

        self.image = img

    def drop_coin(self):
        if self.coins > 0:
            self.coins -= 1
            # Spawn coin with velocity
            vx = 3 if self.facing_right else -3
            vy = -5
            Coin(self.rect.center, [self.world.all_sprites, self.world.coins], self.world.ground_y, pygame.math.Vector2(vx, vy))
            return True
        return False

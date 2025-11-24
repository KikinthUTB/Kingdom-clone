import pygame
from settings import *
from assets import create_horse_sprite, create_monarch_sprite

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)

        # Graphics
        self.horse_surf = create_horse_sprite((139, 69, 19)) # Saddle Brown
        self.monarch_surf = create_monarch_sprite((255, 0, 0)) # Red Cape

        self.original_image = pygame.Surface((32, 40), pygame.SRCALPHA)
        self.original_image.blit(self.horse_surf, (0, 8))
        self.original_image.blit(self.monarch_surf, (10, 0))

        self.image = self.original_image
        self.rect = self.image.get_rect(topleft=pos)

        # Movement
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.speed = 3
        self.run_speed = 6
        self.velocity_x = 0
        self.acceleration = 0.5
        self.friction = 0.85

        # State
        self.facing_right = True
        self.coins = 10 # Start with some coins
        self.drop_cooldown = 0

    def input(self):
        keys = pygame.key.get_pressed()

        # Movement
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            self.current_speed = self.run_speed
        else:
            self.current_speed = self.speed

        # Actions
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if self.drop_cooldown <= 0 and self.coins > 0:
                self.drop_coin()
                self.drop_cooldown = 20 # Frames

    def drop_coin(self):
        self.coins -= 1
        # Signal level to spawn coin (handled via callback or return value, but for now we need a way)
        # We will add a callback to Player init
        if hasattr(self, 'spawn_coin_callback'):
            self.spawn_coin_callback(self.rect.center)

    def move(self):
        # Physics based movement
        if self.direction.x != 0:
            self.velocity_x += self.direction.x * self.acceleration
            if abs(self.velocity_x) > self.current_speed:
                 self.velocity_x = self.current_speed * self.direction.x
        else:
            self.velocity_x *= self.friction

        self.pos.x += self.velocity_x
        self.rect.x = round(self.pos.x)

        # Boundaries
        if self.pos.x < 0:
            self.pos.x = 0
            self.velocity_x = 0
            self.rect.x = 0

        # We need a reference to world width, but for now just hardcode or update later
        # if self.pos.x > world_width: ...

    def animate(self):
        if self.facing_right:
            self.image = self.original_image
        else:
            self.image = pygame.transform.flip(self.original_image, True, False)

    def update(self):
        if self.drop_cooldown > 0:
            self.drop_cooldown -= 1
        self.input()
        self.move()
        self.animate()

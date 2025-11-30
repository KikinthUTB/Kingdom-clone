import pygame
from settings import *
from assets import get_assets
from projectiles import Projectile

class Unit(pygame.sprite.Sprite):
    def __init__(self, pos, groups, world, job="vagrant"):
        super().__init__(groups)
        self.assets = get_assets()
        self.job = job
        self.update_graphics()

        self.rect = self.image.get_rect(bottomleft=pos)
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.velocity = pygame.math.Vector2(0, 0)
        self.world = world
        self.layer = L_UNITS

        # AI
        self.state = "idle" # idle, move, work, run
        self.target = None
        self.speed = 2
        self.cooldown = 0

    def update_graphics(self):
        if self.job == "vagrant":
            self.image = self.assets['vagrant']
        elif self.job == "peasant":
            self.image = self.assets['peasant']
        elif self.job == "archer":
            self.image = self.assets['archer']
        elif self.job == "builder":
            self.image = self.assets['builder']
        elif self.job == "farmer":
            self.image = self.assets['farmer']

    def update(self):
        # Basic gravity
        self.velocity.y += GRAVITY
        self.pos += self.velocity

        # Ground constraint
        if self.pos.y > self.world.ground_y - self.rect.height:
             self.pos.y = self.world.ground_y - self.rect.height
             self.velocity.y = 0

        self.rect.topleft = self.pos

        self.ai_behavior()

    def ai_behavior(self):
        # Override in subclasses or manage big switch here
        # For prototype, we keep it simple

        if self.job == "vagrant":
            # Wander logic
            pass
        elif self.job == "peasant":
            # Seek tools
            self.seek_tools()
        elif self.job == "archer":
            self.archer_logic()

    def archer_logic(self):
        # Attack nearby enemies
        if self.cooldown > 0:
            self.cooldown -= 1
            return

        # Find nearest enemy
        # Optimization: distance check
        target = None
        min_dist = 400

        for enemy in self.world.enemies:
            dist = abs(enemy.rect.centerx - self.rect.centerx)
            if dist < min_dist:
                min_dist = dist
                target = enemy

        if target:
            # Shoot
            Projectile(self.rect.center, target, [self.world.all_sprites, self.world.projectiles], self.world.ground_y)
            self.cooldown = 60 # 1 sec

    def seek_tools(self):
        # Find nearest tool
        # Optimization: Don't check every frame?
        if not self.target:
             # Find tools in world
             tools = [s for s in self.world.items if hasattr(s, 'tool_type')]
             if tools:
                 self.target = tools[0] # Pick first for now

        if self.target:
             # Move towards tool
             direction = self.target.pos.x - self.pos.x
             if abs(direction) > 5:
                 self.velocity.x = (direction / abs(direction)) * self.speed
             else:
                 self.velocity.x = 0
                 # Pickup
                 if self.rect.colliderect(self.target.rect):
                     self.equip_tool(self.target)
                     self.target = None

    def equip_tool(self, tool):
        if tool.tool_type == "bow":
            self.job = "archer"
        elif tool.tool_type == "hammer":
            self.job = "builder"
        elif tool.tool_type == "scythe":
            self.job = "farmer"

        tool.kill()
        self.update_graphics()

    def recruit(self):
        if self.job == "vagrant":
            self.job = "peasant"
            self.update_graphics()
            return True
        return False

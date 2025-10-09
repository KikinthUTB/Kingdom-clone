import pygame
import random
from settings import *

# --- Herní Entity ---

class Greed(pygame.sprite.Sprite):
    def __init__(self, x, y, home_portal):
        super().__init__()
        self.image = pygame.Surface((25, 40)); self.image.fill(GREED_COLOR)
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.base_speed, self.speed = 1.5, 1.5
        self.retreat_speed = 2.5
        self.state = 'ROAMING'
        self.home_portal = home_portal
        self.target = None
        self.last_attack = -1000

    def update(self, game_objects):
        current_time = pygame.time.get_ticks()
        if self.state == 'ATTACKING' and current_time - self.last_attack < 500: return
        elif self.state == 'ATTACKING': self.retreat()

        if self.state in ['CARRYING_COIN', 'CARRYING_CROWN', 'RETREATING']:
            self.move_towards(self.home_portal.rect.centerx)
        elif self.state == 'ROAMING':
            self.find_target(game_objects)
            self.move_towards(self.get_target_position(game_objects['town_center']))

    def find_target(self, game_objects):
        targets = []
        if game_objects['crown'].sprites(): targets.append((game_objects['crown'].sprite, 0))
        targets.extend([(c, 1) for c in game_objects['coins']])
        targets.extend([(n, 2) for n in game_objects['npcs'] if n.state != 'BEGGAR'])
        targets.append((game_objects['monarch'], 3))
        targets.sort(key=lambda t: (t[1], abs(self.rect.centerx - t[0].rect.centerx)))
        self.target = targets[0][0] if targets else None

    def get_target_position(self, town_center):
        return self.target.rect.centerx if self.target else town_center.rect.centerx

    def move_towards(self, target_x):
        if self.rect.centerx < target_x: self.rect.x += self.speed
        else: self.rect.x -= self.speed

    def attack(self):
        self.state = 'ATTACKING'; self.speed = 0; self.last_attack = pygame.time.get_ticks()

    def steal(self, item):
        self.attack()
        if isinstance(item, Coin): self.state = 'CARRYING_COIN'
        elif isinstance(item, Crown): self.state = 'CARRYING_CROWN'
        item.kill()

    def retreat(self):
        self.state = 'RETREATING'; self.speed = self.retreat_speed; self.target = None

class Crown(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(); self.image = pygame.Surface((20, 15)); self.image.fill(CROWN_GOLD)
        self.rect = self.image.get_rect(center=(x, y))

class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(); self.image = pygame.Surface((30, 80)); self.image.fill(PURPLE)
        self.rect = self.image.get_rect(midbottom=(x, y))

class Mount:
    def __init__(self): self.normal_speed, self.sprint_speed = 5, 8

class CoinSystem:
    def __init__(self, starting_coins=10): self.player_coins = starting_coins
    def spend_coins(self, amount):
        if self.player_coins >= amount: self.player_coins -= amount; return True
        return False
    def add_coins(self, amount): self.player_coins += amount

class Monarch(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(); self.image = pygame.Surface((40, 60)); self.image.fill(WHITE)
        self.rect = self.image.get_rect(midbottom=(WIDTH / 2, HEIGHT - 50))
        self.coin_system, self.mount = CoinSystem(), Mount()
        self.movementSpeed = self.mount.normal_speed
        self.can_drop_coins, self.has_crown, self.direction = True, True, 1

    def update(self, keys):
        self.movementSpeed = self.mount.sprint_speed if keys.get(pygame.K_LSHIFT) else self.mount.normal_speed
        if keys.get(pygame.K_LEFT): self.rect.x -= self.movementSpeed; self.direction = -1
        if keys.get(pygame.K_RIGHT): self.rect.x += self.movementSpeed; self.direction = 1

    def drop_coin(self):
        if self.can_drop_coins and self.coin_system.spend_coins(1):
            return Coin(self.rect.centerx + (self.direction * 30), self.rect.bottom - 10)

    def lose_coin_from_attack(self):
        if self.coin_system.spend_coins(1): return Coin(self.rect.centerx, self.rect.centery)

    def drop_crown(self):
        if self.has_crown: self.has_crown = False; return Crown(self.rect.centerx, self.rect.centery)

    def pickup_crown(self): self.has_crown = True

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(); self.image = pygame.Surface((15, 15), pygame.SRCALPHA)
        pygame.draw.circle(self.image, YELLOW, (7, 7), 7); self.rect = self.image.get_rect(center=(x, y))

class NPC(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(); self.state = 'BEGGAR'
        self.image = pygame.Surface((30, 50)); self.image.fill(GRAY)
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.speed, self.target_station, self.profession, self.target_position, self.held_coins = 2, None, None, None, 0

    def update(self, monarch, town_center, tool_stations):
        if self.state == 'VILLAGER_FOLLOWING':
            self.move_to_target(monarch.rect.centerx, 50)
            if self.rect.colliderect(town_center): self.state, self.image.fill(WHITE) = 'VILLAGER_IDLE',
        elif self.state == 'VILLAGER_IDLE':
            if not self.target_station: self.find_tool(tool_stations)
            if self.target_station:
                self.move_to_target(self.target_station.rect.centerx)
                if self.rect.colliderect(self.target_station.rect): self.take_tool(town_center)
        elif self.state in ['BUILDER', 'ARCHER', 'FARMER']:
            if self.target_position:
                self.move_to_target(self.target_position)
                if abs(self.rect.centerx - self.target_position) <= self.speed: self.target_position = None

    def move_to_target(self, target_x, buffer=0):
        if abs(self.rect.centerx - target_x) > buffer:
            if self.rect.centerx < target_x: self.rect.x += self.speed
            else: self.rect.x -= self.speed

    def find_tool(self, tool_stations):
        self.target_station = min([s for s in tool_stations if s.tools], key=lambda s: abs(self.rect.centerx - s.rect.centerx), default=None)

    def take_tool(self, town_center):
        if self.target_station and self.target_station.take_tool():
            self.profession = self.target_station.tool_type
            if self.profession == 'hammer': self.state = 'BUILDER'; self.image.fill(ORANGE)
            elif self.profession == 'bow': self.state = 'ARCHER'; self.image.fill(LIGHT_GREEN)
            elif self.profession == 'scythe': self.state = 'FARMER'; self.image.fill(LIGHT_BROWN)
            self.target_station, self.target_position = None, town_center.centerx

    def recruit(self): self.state, self.image.fill(WHITE) = 'VILLAGER_FOLLOWING',

class Tool(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__(); self.image = pygame.Surface((10,20)); self.image.fill(color)
        self.rect=self.image.get_rect(center=(x,y))

class ToolStation:
    def __init__(self, x, y, tool_type, cost, color):
        self.rect, self.tool_type, self.tool_cost, self.tool_color = pygame.Rect(x,y,60,60), tool_type, cost, color
        self.money_paid, self.max_tools, self.tools = 0, 4, pygame.sprite.Group()
    def add_coin(self):
        self.money_paid += 1
        if self.money_paid >= self.tool_cost and len(self.tools) < self.max_tools:
            self.money_paid = 0; self.create_tool()
    def create_tool(self): self.tools.add(Tool(self.rect.centerx, self.rect.top-(len(self.tools)*25)-15, self.tool_color))
    def take_tool(self):
        if self.tools: self.tools.sprites()[-1].kill(); return True
        return False
    def draw(self, screen, offset):
        scr_rect = self.rect.move(-offset, 0); pygame.draw.rect(screen, BROWN, scr_rect)
        for tool in self.tools: screen.blit(tool.image, tool.rect.move(-offset, 0))

class TreasureChest(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(); self.state = 'closed'
        self.image = pygame.Surface((50, 40)); self.image.fill(BROWN)
        self.rect = self.image.get_rect(midbottom=(x, y))
    def open(self):
        if self.state == 'closed': self.state = 'opened'; self.image.fill((80, 40, 10)); return 5
        return 0
import pygame
import sys
import random

# Inicializace Pygame
pygame.init()

# --- Nastavení a Konstanty ---
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kingdom New Lands Clone")

# Barvy
WHITE, BLACK, GREEN, BROWN, SKY_BLUE, GRAY, YELLOW = (255,255,255), (0,0,0), (0,128,0), (139,69,19), (135,206,235), (128,128,128), (255,255,0)
ORANGE, LIGHT_GREEN, LIGHT_BROWN = (255,165,0), (144,238,144), (210,180,140)
PURPLE, DARK_BLUE, GREED_COLOR, CROWN_GOLD = (128,0,128), (0,0,50), (220,20,60), (255,215,0)

# --- Herní Třídy ---

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
        self.attack_cooldown = 1000
        self.last_attack = -self.attack_cooldown

    def update(self, game_objects):
        current_time = pygame.time.get_ticks()
        if self.state == 'ATTACKING' and current_time - self.last_attack < 500:
            return
        elif self.state == 'ATTACKING':
            self.retreat()

        if self.state in ['CARRYING_COIN', 'CARRYING_CROWN', 'RETREATING']:
            self.move_towards(self.home_portal.rect.centerx)
        elif self.state == 'ROAMING':
            self.find_target(game_objects)
            target_pos = self.get_target_position(game_objects['town_center'])
            self.move_towards(target_pos)

    def find_target(self, game_objects):
        potential_targets = []
        if game_objects['crown'].sprites(): potential_targets.append((game_objects['crown'].sprite, 0))
        for coin in game_objects['coins']: potential_targets.append((coin, 1))
        for npc in game_objects['npcs']:
            if npc.state != 'BEGGAR': potential_targets.append((npc, 2))
        potential_targets.append((game_objects['monarch'], 3))

        potential_targets.sort(key=lambda t: (t[1], abs(self.rect.centerx - t[0].rect.centerx)))
        self.target = potential_targets[0][0] if potential_targets else None

    def get_target_position(self, town_center):
        return self.target.rect.centerx if self.target else town_center.centerx

    def move_towards(self, target_x):
        if self.rect.centerx < target_x: self.rect.x += self.speed
        else: self.rect.x -= self.speed

    def attack(self):
        self.state = 'ATTACKING'
        self.speed = 0
        self.last_attack = pygame.time.get_ticks()

    def steal(self, item):
        self.attack()
        if isinstance(item, Coin): self.state = 'CARRYING_COIN'
        elif isinstance(item, Crown): self.state = 'CARRYING_CROWN'
        item.kill()

    def retreat(self):
        self.state = 'RETREATING'
        self.speed = self.retreat_speed
        self.target = None

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
        self.movementSpeed = self.mount.sprint_speed if keys[pygame.K_LSHIFT] else self.mount.normal_speed
        if keys[pygame.K_LEFT]: self.rect.x -= self.movementSpeed; self.direction = -1
        if keys[pygame.K_RIGHT]: self.rect.x += self.movementSpeed; self.direction = 1
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

class SubjectManager:
    def __init__(self, all_sprites, beggar_camp):
        self.all_sprites, self.beggar_camp = all_sprites, beggar_camp
        self.all_npcs = pygame.sprite.Group()
    def spawn_beggar(self, initial=False):
        if initial or not any(n.state == 'BEGGAR' for n in self.all_npcs):
            beggar = NPC(self.beggar_camp.centerx, self.beggar_camp.bottom); self.all_npcs.add(beggar); self.all_sprites.add(beggar)
    def recruit_beggars(self, coins_on_ground):
        for beggar in [n for n in self.all_npcs if n.state == 'BEGGAR' and pygame.sprite.spritecollideany(n, coins_on_ground)]:
            pygame.sprite.spritecollideany(beggar, coins_on_ground).kill(); beggar.recruit()
    def collect_coins(self, coins_on_ground):
        for npc in [n for n in self.all_npcs if n.state != 'BEGGAR']:
            npc.held_coins += len(pygame.sprite.spritecollide(npc, coins_on_ground, True))
    def drop_coins_for_monarch(self, monarch, all_sprites, coins_on_ground):
        for npc in [n for n in self.all_npcs if n.held_coins > 0 and abs(n.rect.centerx - monarch.rect.centerx) < 70]:
            for _ in range(npc.held_coins):
                new_coin = Coin(npc.rect.centerx + random.randint(-20, 20), npc.rect.bottom - 10)
                all_sprites.add(new_coin); coins_on_ground.add(new_coin)
            npc.held_coins = 0
    def handle_attack(self, npc):
        if npc.state in ['BUILDER', 'ARCHER', 'FARMER']:
            npc.state, npc.profession, npc.image.fill(WHITE) = 'VILLAGER_IDLE', None,
        elif npc.state in ['VILLAGER_IDLE', 'VILLAGER_FOLLOWING']:
            npc.state, npc.held_coins, npc.image.fill(GRAY) = 'BEGGAR', 0,
    def update_all(self, monarch, town_center, tool_stations): self.all_npcs.update(monarch, town_center, tool_stations)

class EnemyManager:
    def __init__(self, all_sprites):
        self.all_sprites, self.enemies = all_sprites, pygame.sprite.Group()
    def spawn_greeds(self, portals):
        for portal in portals:
            for _ in range(random.randint(1, 3)):
                greed = Greed(portal.rect.centerx, portal.rect.bottom, portal)
                self.enemies.add(greed); self.all_sprites.add(greed)
    def update(self, game_objects):
        self.enemies.update(game_objects)
        for greed in self.enemies:
            if greed.state == 'ROAMING' and greed.target and greed.rect.colliderect(greed.target.rect):
                target = greed.target
                if isinstance(target, (Coin, Crown)): greed.steal(target)
                elif isinstance(target, NPC): game_objects['subjects'].handle_attack(target); greed.attack()
                elif isinstance(target, Monarch): self.attack_monarch(greed, game_objects)
            elif greed.rect.colliderect(greed.home_portal.rect): greed.kill()
    def attack_monarch(self, greed, game_objects):
        monarch = game_objects['monarch']
        greed.attack()
        if monarch.coin_system.player_coins > 0:
            new_coin = monarch.lose_coin_from_attack()
            if new_coin: game_objects['all_sprites'].add(new_coin); game_objects['coins'].add(new_coin)
        elif monarch.has_crown:
            new_crown = monarch.drop_crown()
            if new_crown: game_objects['all_sprites'].add(new_crown); game_objects['crown'].add(new_crown)

class TreasureChest(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(); self.state = 'closed'
        self.image = pygame.Surface((50, 40)); self.image.fill(BROWN)
        self.rect = self.image.get_rect(midbottom=(x, y))
    def open(self):
        if self.state == 'closed': self.state = 'opened'; self.image.fill((80, 40, 10)); return 5
        return 0

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

def main():
    clock, font = pygame.time.Clock(), pygame.font.Font(None, 36)
    monarch, all_sprites, coins, crown_group = Monarch(), pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group()
    all_sprites.add(monarch)

    WORLD_WIDTH = WIDTH * 3; ground_rect = pygame.Rect(0, HEIGHT - 50, WORLD_WIDTH, 50)
    town_center = pygame.Rect(WIDTH*1.5 - 50, HEIGHT-50, 100, 10); beggar_camp = pygame.Rect(300, HEIGHT-100, 80, 50)

    subject_manager = SubjectManager(all_sprites, beggar_camp); subject_manager.spawn_beggar(initial=True)
    enemy_manager = EnemyManager(all_sprites)

    tool_stations = [ToolStation(x, HEIGHT-110, t, c, cl) for x,t,c,cl in
                     [(town_center.left-80,'hammer',3,ORANGE), (town_center.right+20,'bow',2,LIGHT_GREEN), (town_center.left-160,'scythe',4,LIGHT_BROWN)]]

    chests = pygame.sprite.Group(TreasureChest(WORLD_WIDTH - 200, HEIGHT - 90)); all_sprites.add(chests)
    portals = [Portal(100, HEIGHT-90), Portal(WORLD_WIDTH-100, HEIGHT-90)]; all_sprites.add(portals)

    pygame.time.set_timer(pygame.USEREVENT + 1, 10000)
    DAY_LENGTH, NIGHT_LENGTH = 20000, 15000
    cycle_timer, is_night, game_over = pygame.time.get_ticks(), False, False

    bg_layers = [{'r':pygame.Rect(0,y,WIDTH,150),'c':c,'s':s} for y,c,s in [(HEIGHT-250,(100,150,200),0.2),(HEIGHT-200,(50,100,150),0.4),(HEIGHT-150,(20,50,80),0.6)]]

    while not game_over:
        current_time = pygame.time.get_ticks()
        # Day/Night Cycle
        if is_night and current_time - cycle_timer > NIGHT_LENGTH: is_night, cycle_timer = False, current_time
        elif not is_night and current_time - cycle_timer > DAY_LENGTH:
            is_night, cycle_timer = True, current_time
            enemy_manager.spawn_greeds(portals)

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT: game_over = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                new_coin = monarch.drop_coin()
                if new_coin: all_sprites.add(new_coin), coins.add(new_coin)
            if event.type == pygame.USEREVENT + 1: subject_manager.spawn_beggar()

        # --- Updates ---
        game_objects = {'monarch': monarch, 'coins': coins, 'crown': crown_group, 'npcs': subject_manager.all_npcs, 'subjects': subject_manager, 'town_center': town_center}
        monarch.update(pygame.key.get_pressed())
        subject_manager.update_all(monarch, town_center, tool_stations)
        enemy_manager.update(game_objects)

        # --- Interactions ---
        if not monarch.has_crown and pygame.sprite.spritecollide(monarch, crown_group, True): monarch.pickup_crown()
        monarch.coin_system.add_coins(len(pygame.sprite.spritecollide(monarch, coins, True)))
        subject_manager.collect_coins(coins); subject_manager.recruit_beggars(coins)
        subject_manager.drop_coins_for_monarch(monarch, all_sprites, coins)
        for station in tool_stations:
            for coin in [c for c in coins if station.rect.colliderect(c.rect)]: station.add_coin(), coin.kill()
        for chest in chests:
            if chest.state == 'closed' and monarch.rect.colliderect(chest.rect):
                for _ in range(chest.open()):
                    new_coin = Coin(chest.rect.centerx+random.randint(-40,40), chest.rect.bottom-10)
                    all_sprites.add(new_coin), coins.add(new_coin)

        # --- Game Over Checks ---
        if monarch.rect.left < 0: monarch.rect.left = 0
        if monarch.rect.right > WORLD_WIDTH: monarch.rect.right = WORLD_WIDTH
        if monarch.coin_system.player_coins <= 0 and not monarch.has_crown: game_over = True
        for greed in enemy_manager.enemies:
            if greed.state == 'CARRYING_CROWN' and not screen.get_rect().colliderect(greed.rect): game_over = True

        # --- Drawing ---
        camera_offset_x = monarch.rect.centerx - WIDTH / 2
        screen.fill(DARK_BLUE if is_night else SKY_BLUE)
        for l in bg_layers:
            for i in range(2): screen.fill(l['c'], pygame.Rect(((-camera_offset_x*l['s'])%WIDTH)+(i-1)*WIDTH, l['r'].y, WIDTH, l['r'].height))
        ground_rect.x = -camera_offset_x; screen.fill(GREEN, ground_rect)
        for loc in [beggar_camp, town_center]:
            loc_rect = loc.copy(); loc_rect.x -= camera_offset_x; pygame.draw.rect(screen, BROWN if loc==beggar_camp else GRAY, loc_rect)
        for station in tool_stations: station.draw(screen, camera_offset_x)
        for sprite in all_sprites: screen.blit(sprite.image, sprite.rect.move(-camera_offset_x, 0))

        screen.blit(font.render(f"Coins: {monarch.coin_system.player_coins}", True, WHITE), (10, 10))
        pygame.display.flip()
        clock.tick(60)

    print("Game Over!")
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
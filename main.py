import pygame
import sys
import random

# Inicializace Pygame
pygame.init()

# Nastavení obrazovky
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kingdom New Lands Clone")

# Barvy
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
BROWN = (139, 69, 19)
SKY_BLUE = (135, 206, 235)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)  # Stavař
LIGHT_GREEN = (144, 238, 144)  # Lučištník
LIGHT_BROWN = (210, 180, 140) # Farmář

# Jezdecké zvíře
class Mount:
    def __init__(self):
        self.normal_speed = 5
        self.sprint_speed = 8

# System mincí
class CoinSystem:
    def __init__(self, starting_coins=10):
        self.player_coins = starting_coins

    def spend_coins(self, amount):
        if self.player_coins >= amount:
            self.player_coins -= amount
            return True
        return False

    def add_coins(self, amount):
        self.player_coins += amount

# Monarcha (hráč)
class Monarch(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(midbottom=(WIDTH / 2, HEIGHT - 50))

        self.coin_system = CoinSystem()
        self.mount = Mount()
        self.movementSpeed = self.mount.normal_speed
        self.can_drop_coins = True
        self.crown = True
        self.direction = 1

    def update(self, keys):
        if keys[pygame.K_LSHIFT]:
            self.movementSpeed = self.mount.sprint_speed
        else:
            self.movementSpeed = self.mount.normal_speed

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.movementSpeed
            self.direction = -1
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.movementSpeed
            self.direction = 1

    def drop_coin(self):
        if self.can_drop_coins and self.coin_system.spend_coins(1):
            coin_x = self.rect.centerx + (self.direction * 30)
            coin_y = self.rect.bottom - 10
            return Coin(coin_x, coin_y)
        return None

# Mince
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((15, 15), pygame.SRCALPHA)
        pygame.draw.circle(self.image, YELLOW, (7, 7), 7)
        self.rect = self.image.get_rect(center=(x, y))

# NPC
class NPC(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.state = 'BEGGAR'
        self.image = pygame.Surface((30, 50))
        self.image.fill(GRAY)
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.speed = 2
        self.target_station = None
        self.profession = None
        self.target_position = None
        self.held_coins = 0

    def update(self, monarch, town_center, tool_stations):
        if self.state == 'VILLAGER_FOLLOWING':
            if abs(self.rect.centerx - monarch.rect.centerx) > 50:
                if self.rect.centerx < monarch.rect.centerx: self.rect.x += self.speed
                else: self.rect.x -= self.speed
            if self.rect.colliderect(town_center):
                self.state = 'VILLAGER_IDLE'
                self.image.fill(WHITE)

        elif self.state == 'VILLAGER_IDLE':
            if not self.target_station:
                self.find_tool(tool_stations)
            if self.target_station:
                self.move_to_target()
                if self.rect.colliderect(self.target_station.rect):
                    self.take_tool(town_center)

        elif self.state in ['BUILDER', 'ARCHER', 'FARMER']:
            if self.target_position:
                self.move_to_target()
                if abs(self.rect.centerx - self.target_position) <= self.speed:
                    self.target_position = None

    def find_tool(self, tool_stations):
        closest_station = None
        min_dist = float('inf')
        for station in tool_stations:
            if station.tools:
                dist = abs(self.rect.centerx - station.rect.centerx)
                if dist < min_dist:
                    min_dist = dist
                    closest_station = station
        self.target_station = closest_station
        if self.target_station:
             self.target_position = self.target_station.rect.centerx

    def move_to_target(self):
        if self.target_position:
            if self.rect.centerx < self.target_position: self.rect.x += self.speed
            else: self.rect.x -= self.speed

    def take_tool(self, town_center):
        if self.target_station.take_tool():
            self.profession = self.target_station.tool_type
            if self.profession == 'hammer':
                self.state = 'BUILDER'
                self.image.fill(ORANGE)
            elif self.profession == 'bow':
                self.state = 'ARCHER'
                self.image.fill(LIGHT_GREEN)
            elif self.profession == 'scythe':
                self.state = 'FARMER'
                self.image.fill(LIGHT_BROWN)
            self.target_station = None
            self.target_position = town_center.centerx

    def recruit(self):
        self.state = 'VILLAGER_FOLLOWING'
        self.image.fill(WHITE)

# Správce poddaných
class SubjectManager:
    def __init__(self, all_sprites_group, beggar_camp):
        self.all_sprites = all_sprites_group
        self.beggar_camp = beggar_camp
        self.beggars = pygame.sprite.Group()
        self.villagers = pygame.sprite.Group()
        self.builders = pygame.sprite.Group()
        self.archers = pygame.sprite.Group()
        self.farmers = pygame.sprite.Group()
        self.all_npcs = pygame.sprite.Group()

    def spawn_beggar(self, initial=False):
        if initial or not self.beggars:
            new_beggar = NPC(self.beggar_camp.centerx, self.beggar_camp.bottom)
            self.all_npcs.add(new_beggar)
            self.beggars.add(new_beggar)
            self.all_sprites.add(new_beggar)

    def recruit_beggars(self, coins_on_ground):
        recruited = pygame.sprite.groupcollide(self.beggars, coins_on_ground, False, True)
        for beggar, _ in recruited.items():
            beggar.recruit()
            self.beggars.remove(beggar)
            self.villagers.add(beggar)

    def assign_jobs(self, town_center, tool_stations):
        for villager in self.villagers:
            if not villager.target_station:
                villager.find_tool(tool_stations)

            if villager.target_station and villager.rect.colliderect(villager.target_station.rect):
                prev_state = villager.state
                villager.take_tool(town_center)
                if villager.state != prev_state: # Job was taken
                    self.villagers.remove(villager)
                    if villager.state == 'BUILDER': self.builders.add(villager)
                    elif villager.state == 'ARCHER': self.archers.add(villager)
                    elif villager.state == 'FARMER': self.farmers.add(villager)

    def collect_coins(self, coins_on_ground):
        for npc in self.all_npcs:
            if npc.state != 'BEGGAR':
                collected = pygame.sprite.spritecollide(npc, coins_on_ground, True)
                npc.held_coins += len(collected)

    def drop_coins_for_monarch(self, monarch, all_sprites, coins_on_ground):
        for npc in self.all_npcs:
            if npc.held_coins > 0 and abs(npc.rect.centerx - monarch.rect.centerx) < 70:
                for _ in range(npc.held_coins):
                    coin_x = npc.rect.centerx + random.randint(-20, 20)
                    coin_y = npc.rect.bottom - 10
                    new_coin = Coin(coin_x, coin_y)
                    all_sprites.add(new_coin)
                    coins_on_ground.add(new_coin)
                npc.held_coins = 0

    def lose_tool(self, npc):
        if npc.state in ['BUILDER', 'ARCHER', 'FARMER']:
            npc.state = 'VILLAGER_IDLE'
            npc.image.fill(WHITE)
            if npc in self.builders: self.builders.remove(npc)
            elif npc in self.archers: self.archers.remove(npc)
            elif npc in self.farmers: self.farmers.remove(npc)
            self.villagers.add(npc)
            print(f"{npc.profession} lost their tool and became a villager.")

    def update_all(self, monarch, town_center, tool_stations):
        self.all_npcs.update(monarch, town_center, tool_stations)
        self.assign_jobs(town_center, tool_stations)

# Třída pro truhlu s pokladem
class TreasureChest(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.state = 'closed'
        self.image = pygame.Surface((50, 40))
        self.image.fill(BROWN)
        self.rect = self.image.get_rect(midbottom=(x, y))

    def open(self):
        if self.state == 'closed':
            self.state = 'opened'
            self.image.fill((80, 40, 10))
            return 5
        return 0

# Třída pro nástroje (vizuální reprezentace)
class Tool(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((10, 20))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))

# Třída pro stanice s nástroji
class ToolStation:
    def __init__(self, x, y, tool_type, tool_cost, tool_color):
        self.rect = pygame.Rect(x, y, 60, 60)
        self.tool_type = tool_type
        self.tool_cost = tool_cost
        self.tool_color = tool_color
        self.money_paid = 0
        self.tools = pygame.sprite.Group()
        self.max_tools = 4

    def add_coin(self):
        self.money_paid += 1
        if self.money_paid >= self.tool_cost and len(self.tools) < self.max_tools:
            self.money_paid = 0
            self.create_tool()

    def create_tool(self):
        tool_x = self.rect.centerx
        tool_y = self.rect.top - (len(self.tools) * 25) - 15
        new_tool = Tool(tool_x, tool_y, self.tool_color)
        self.tools.add(new_tool)

    def take_tool(self):
        if self.tools:
            tool = self.tools.sprites()[-1]
            tool.kill()
            return True
        return False

    def draw(self, screen, camera_offset_x):
        station_screen_rect = self.rect.copy()
        station_screen_rect.x -= camera_offset_x
        pygame.draw.rect(screen, BROWN, station_screen_rect)
        for tool in self.tools:
            tool_screen_rect = tool.rect.copy()
            tool_screen_rect.x -= camera_offset_x
            screen.blit(tool.image, tool_screen_rect)

# Funkce pro vykreslení UI
def draw_ui(screen, monarch, font):
    coins_text = font.render(f"Coins: {monarch.coin_system.player_coins}", True, WHITE)
    screen.blit(coins_text, (10, 10))

# Hlavní smyčka hry
def main():
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    monarch = Monarch()

    all_sprites = pygame.sprite.Group()
    all_sprites.add(monarch)
    coins_on_ground = pygame.sprite.Group()

    WORLD_WIDTH = WIDTH * 3
    ground_rect = pygame.Rect(0, HEIGHT - 50, WORLD_WIDTH, 50)
    town_center = pygame.Rect(WIDTH * 1.5 - 50, HEIGHT - 50, 100, 10)
    beggar_camp = pygame.Rect(300, HEIGHT - 100, 80, 50)

    subject_manager = SubjectManager(all_sprites, beggar_camp)
    subject_manager.spawn_beggar(initial=True)

    hammer_station = ToolStation(town_center.left - 80, HEIGHT - 110, 'hammer', 3, ORANGE)
    bow_station = ToolStation(town_center.right + 20, HEIGHT - 110, 'bow', 2, LIGHT_GREEN)
    scythe_station = ToolStation(town_center.left - 160, HEIGHT - 110, 'scythe', 4, LIGHT_BROWN)
    tool_stations = [hammer_station, bow_station, scythe_station]

    treasure_chest = TreasureChest(WORLD_WIDTH - 200, HEIGHT - 90)
    all_sprites.add(treasure_chest)
    chests = pygame.sprite.Group(treasure_chest)

    SPAWN_BEGGAR_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_BEGGAR_EVENT, 10000)

    camera_offset_x = 0
    bg_layers = [
        {'rect': pygame.Rect(0, 0, WIDTH, HEIGHT), 'color': SKY_BLUE, 'speed': 0},
        {'rect': pygame.Rect(0, HEIGHT - 250, WIDTH, 150), 'color': (100, 150, 200), 'speed': 0.2},
        {'rect': pygame.Rect(0, HEIGHT - 200, WIDTH, 150), 'color': (50, 100, 150), 'speed': 0.4},
        {'rect': pygame.Rect(0, HEIGHT - 150, WIDTH, 150), 'color': (20, 50, 80), 'speed': 0.6},
    ]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    new_coin = monarch.drop_coin()
                    if new_coin:
                        all_sprites.add(new_coin)
                        coins_on_ground.add(new_coin)
            if event.type == SPAWN_BEGGAR_EVENT:
                subject_manager.spawn_beggar()

        keys = pygame.key.get_pressed()
        monarch.update(keys)
        subject_manager.update_all(monarch, town_center, tool_stations)

        # --- Interakce s mincemi ---
        collected_by_monarch = pygame.sprite.spritecollide(monarch, coins_on_ground, True)
        monarch.coin_system.add_coins(len(collected_by_monarch))

        subject_manager.collect_coins(coins_on_ground)
        subject_manager.recruit_beggars(coins_on_ground)
        subject_manager.drop_coins_for_monarch(monarch, all_sprites, coins_on_ground)

        for station in tool_stations:
            collided_coins = [coin for coin in coins_on_ground if station.rect.colliderect(coin.rect)]
            for coin in collided_coins:
                station.add_coin()
                coin.kill()

        for chest in chests:
            if chest.state == 'closed' and monarch.rect.colliderect(chest.rect):
                coins_to_spawn = chest.open()
                for _ in range(coins_to_spawn):
                    coin_x = chest.rect.centerx + random.randint(-40, 40)
                    coin_y = chest.rect.bottom - 10
                    new_coin = Coin(coin_x, coin_y)
                    all_sprites.add(new_coin)
                    coins_on_ground.add(new_coin)

        # --- Kontroly ---
        if monarch.rect.left < 0: monarch.rect.left = 0
        if monarch.rect.right > WORLD_WIDTH: monarch.rect.right = WORLD_WIDTH
        if monarch.coin_system.player_coins <= 0 or not monarch.crown:
            running = False

        # --- Vykreslování ---
        camera_offset_x = monarch.rect.centerx - WIDTH / 2

        for layer in bg_layers:
            bg_x = -camera_offset_x * layer['speed']
            screen.fill(layer['color'], pygame.Rect(bg_x % WIDTH, layer['rect'].y, WIDTH, layer['rect'].height))
            screen.fill(layer['color'], pygame.Rect(bg_x % WIDTH - WIDTH, layer['rect'].y, WIDTH, layer['rect'].height))

        ground_screen_rect = ground_rect.copy()
        ground_screen_rect.x = -camera_offset_x
        screen.fill(GREEN, ground_screen_rect)

        for loc in [beggar_camp, town_center]:
            loc_screen_rect = loc.copy()
            loc_screen_rect.x -= camera_offset_x
            pygame.draw.rect(screen, BROWN if loc == beggar_camp else GRAY, loc_screen_rect)

        for station in tool_stations:
            station.draw(screen, camera_offset_x)

        for sprite in all_sprites:
            sprite_screen_rect = sprite.rect.copy()
            sprite_screen_rect.x -= camera_offset_x
            screen.blit(sprite.image, sprite_screen_rect)

        draw_ui(screen, monarch, font)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
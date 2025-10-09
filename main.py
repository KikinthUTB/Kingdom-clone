import pygame
import sys

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
ORANGE = (255, 165, 0) # Stavař
LIGHT_GREEN = (144, 238, 144) # Lučištník

# Jezdecké zvíře
class Mount:
    def __init__(self):
        self.normal_speed = 5
        self.sprint_speed = 8

# Monarcha (hráč)
class Monarch(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(midbottom=(WIDTH / 2, HEIGHT - 50))

        self.health = 10  # Počet mincí
        self.mount = Mount()
        self.movementSpeed = self.mount.normal_speed
        self.can_drop_coins = True
        self.crown = True
        self.direction = 1 # 1 = doprava, -1 = doleva

    def update(self, keys):
        # Sprint
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
        if self.health > 0 and self.can_drop_coins:
            self.health -= 1
            # Upustí minci před hráčem
            coin_x = self.rect.centerx + (self.direction * 30)
            coin_y = self.rect.bottom - 10 # Mírně nad zemí
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
        self.state = 'BEGGAR' # Stavy: BEGGAR, VILLAGER_FOLLOWING, VILLAGER_IDLE, BUILDER, ARCHER
        self.image = pygame.Surface((30, 50))
        self.image.fill(GRAY) # Žebrák je šedý
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.speed = 2
        self.target_station = None
        self.profession = None
        self.target_position = None

    def update(self, monarch, town_center, tool_stations):
        if self.state == 'VILLAGER_FOLLOWING':
            # Následuje hráče
            if abs(self.rect.centerx - monarch.rect.centerx) > 50: # Udržuje si odstup
                if self.rect.centerx < monarch.rect.centerx:
                    self.rect.x += self.speed
                else:
                    self.rect.x -= self.speed

            # Zkontroluje, zda dorazil do centra
            if self.rect.colliderect(town_center):
                self.state = 'VILLAGER_IDLE'
                self.image.fill(WHITE)

        elif self.state == 'VILLAGER_IDLE':
            # Nečinný vesničan si hledá práci
            if not self.target_station:
                # Najde nejbližší stanici s nástroji
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
                # Pohyb ke stanici
                if abs(self.rect.centerx - self.target_station.rect.centerx) > self.speed:
                    if self.rect.centerx < self.target_station.rect.centerx:
                        self.rect.x += self.speed
                    else:
                        self.rect.x -= self.speed
                else: # Dorazil
                    if self.target_station.take_tool():
                        self.profession = self.target_station.tool_type
                        if self.profession == 'hammer':
                            self.state = 'BUILDER'
                            self.image.fill(ORANGE)
                        elif self.profession == 'bow':
                            self.state = 'ARCHER'
                            self.image.fill(LIGHT_GREEN)
                        self.target_station = None
                        self.target_position = town_center.centerx

        elif self.state == 'BUILDER' or self.state == 'ARCHER':
            # Vrací se do centra města
            if self.target_position:
                if abs(self.rect.centerx - self.target_position) > self.speed:
                    if self.rect.centerx < self.target_position:
                        self.rect.x += self.speed
                    else:
                        self.rect.x -= self.speed
                else:
                    self.target_position = None

    def recruit(self):
        self.state = 'VILLAGER_FOLLOWING'
        self.image.fill(WHITE)

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
            self.money_paid -= self.tool_cost
            self.create_tool()

    def create_tool(self):
        # Nástroje se objevují na stojanu vedle stanice
        tool_x = self.rect.centerx
        tool_y = self.rect.top - (len(self.tools) * 25) - 15
        new_tool = Tool(tool_x, tool_y, self.tool_color)
        self.tools.add(new_tool)

    def take_tool(self):
        if self.tools:
            tool = self.tools.sprites()[-1] # Vezme poslední přidaný nástroj
            tool.kill()
            return True
        return False

    def draw(self, screen, camera_offset_x):
        # Vykreslení stanice
        station_screen_rect = self.rect.copy()
        station_screen_rect.x -= camera_offset_x
        pygame.draw.rect(screen, BROWN, station_screen_rect)

        # Vykreslení nástrojů
        for tool in self.tools:
            tool_screen_rect = tool.rect.copy()
            tool_screen_rect.x -= camera_offset_x
            screen.blit(tool.image, tool_screen_rect)

# Funkce pro vykreslení UI
def draw_ui(screen, monarch, font):
    health_text = font.render(f"Health: {monarch.health}", True, WHITE)
    screen.blit(health_text, (10, 10))

# Hlavní smyčka hry
def main():
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36) # Defaultní písmo, velikost 36
    monarch = Monarch()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(monarch)
    coins_on_ground = pygame.sprite.Group()
    npcs = pygame.sprite.Group()

    # World setup
    WORLD_WIDTH = WIDTH * 3

    # Země
    ground_rect = pygame.Rect(0, HEIGHT - 50, WORLD_WIDTH, 50)

    # Klíčové lokace
    town_center = pygame.Rect(WIDTH * 1.5 - 50, HEIGHT - 50, 100, 10) # Uprostřed světa
    beggar_camp = pygame.Rect(300, HEIGHT - 100, 80, 50) # Vlevo od startu

    # Stanice s nástroji
    hammer_station = ToolStation(town_center.left - 80, HEIGHT - 110, 'hammer', 3, ORANGE)
    bow_station = ToolStation(town_center.right + 20, HEIGHT - 110, 'bow', 2, LIGHT_GREEN)
    tool_stations = [hammer_station, bow_station]

    # Vytvoření NPC
    beggar = NPC(beggar_camp.centerx, beggar_camp.bottom)
    all_sprites.add(beggar)
    npcs.add(beggar)

    # Spawnování žebráků
    SPAWN_BEGGAR_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_BEGGAR_EVENT, 10000) # Každých 10 sekund

    # Kamera
    camera_offset_x = 0

    # Paralaxní pozadí (jednoduché obdélníky)
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
                # Zkontroluje, zda již existuje žebrák
                beggar_exists = any(npc.state == 'BEGGAR' for npc in npcs)
                if not beggar_exists:
                    new_beggar = NPC(beggar_camp.centerx, beggar_camp.bottom)
                    all_sprites.add(new_beggar)
                    npcs.add(new_beggar)

        keys = pygame.key.get_pressed()
        monarch.update(keys)
        npcs.update(monarch, town_center, tool_stations)

        # Sebrání mincí
        collected_coins = pygame.sprite.spritecollide(monarch, coins_on_ground, True)
        monarch.health += len(collected_coins)

        # Rekrutování žebráků
        recruited_npcs = pygame.sprite.groupcollide(npcs, coins_on_ground, False, True)
        for npc, coin_list in recruited_npcs.items():
            if npc.state == 'BEGGAR':
                if coin_list: # Pokud došlo ke kolizi
                    npc.recruit()

        # Nákup nástrojů u stanic
        for station in tool_stations:
            collided_coins = [coin for coin in coins_on_ground if station.rect.colliderect(coin.rect)]
            for coin in collided_coins:
                station.add_coin()
                coin.kill()

        # Omezení pohybu hráče ve světě
        if monarch.rect.left < 0:
            monarch.rect.left = 0
        if monarch.rect.right > WORLD_WIDTH:
            monarch.rect.right = WORLD_WIDTH

        # Kontrola konce hry
        if monarch.health <= 0 or not monarch.crown:
            running = False

        # Aktualizace kamery, aby sledovala hráče
        camera_offset_x = monarch.rect.centerx - WIDTH / 2

        # Vykreslení
        # Pozadí
        for layer in bg_layers:
             # Posun vrstvy podle kamery a její rychlosti
            bg_x = -camera_offset_x * layer['speed']

            # Vykreslení vrstvy dvakrát pro plynulý přechod
            screen.fill(layer['color'], pygame.Rect(bg_x % WIDTH, layer['rect'].y, WIDTH, layer['rect'].height))
            screen.fill(layer['color'], pygame.Rect(bg_x % WIDTH - WIDTH, layer['rect'].y, WIDTH, layer['rect'].height))


        # Země
        ground_x = -camera_offset_x
        screen.fill(GREEN, pygame.Rect(ground_x, ground_rect.y, ground_rect.width, ground_rect.height))

        # Vykreslení klíčových lokací
        # Tábor žebráků
        beggar_camp_screen_rect = beggar_camp.copy()
        beggar_camp_screen_rect.x -= camera_offset_x
        pygame.draw.rect(screen, BROWN, beggar_camp_screen_rect)

        # Centrum města (ohniště)
        town_center_screen_rect = town_center.copy()
        town_center_screen_rect.x -= camera_offset_x
        pygame.draw.rect(screen, GRAY, town_center_screen_rect)

        # Vykreslení stanic s nástroji
        for station in tool_stations:
            station.draw(screen, camera_offset_x)


        # Vykreslení všech spritů s ohledem na kameru
        for sprite in all_sprites:
            sprite_screen_rect = sprite.rect.copy()
            sprite_screen_rect.x -= camera_offset_x
            screen.blit(sprite.image, sprite_screen_rect)

        # Vykreslení UI
        draw_ui(screen, monarch, font)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
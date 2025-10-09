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

# Hráč
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(midbottom=(WIDTH / 2, HEIGHT - 50))
        self.speed = 5
        self.coins = 10
        self.direction = 1 # 1 = doprava, -1 = doleva

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.direction = -1
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.direction = 1

    def drop_coin(self):
        if self.coins > 0:
            self.coins -= 1
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

# Funkce pro vykreslení UI
def draw_ui(screen, player, font):
    coin_text = font.render(f"Mince: {player.coins}", True, WHITE)
    screen.blit(coin_text, (10, 10))

# Hlavní smyčka hry
def main():
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36) # Defaultní písmo, velikost 36
    player = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    coins_on_ground = pygame.sprite.Group()

    # Země
    ground_rect = pygame.Rect(0, HEIGHT - 50, WIDTH, 50)

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
                    new_coin = player.drop_coin()
                    if new_coin:
                        all_sprites.add(new_coin)
                        coins_on_ground.add(new_coin)

        keys = pygame.key.get_pressed()
        player.update(keys)

        # Sebrání mincí
        collected_coins = pygame.sprite.spritecollide(player, coins_on_ground, True)
        player.coins += len(collected_coins)

        # Omezení pohybu hráče na obrazovce (dočasně, než bude svět větší)
        if player.rect.left < 0:
            player.rect.left = 0
        if player.rect.right > WIDTH:
            player.rect.right = WIDTH

        # Aktualizace kamery, aby sledovala hráče
        camera_offset_x = player.rect.centerx - WIDTH / 2

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
        screen.fill(GREEN, pygame.Rect(ground_x, ground_rect.y, ground_rect.width*2, ground_rect.height))


        # Vykreslení všech spritů s ohledem na kameru
        for sprite in all_sprites:
            sprite_screen_rect = sprite.rect.copy()
            sprite_screen_rect.x -= camera_offset_x
            screen.blit(sprite.image, sprite_screen_rect)

        # Vykreslení UI
        draw_ui(screen, player, font)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
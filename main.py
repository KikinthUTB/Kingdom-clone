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

# Hráč
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(midbottom=(WIDTH / 2, HEIGHT - 50))
        self.speed = 5

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

# Hlavní smyčka hry
def main():
    clock = pygame.time.Clock()
    player = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

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

        keys = pygame.key.get_pressed()
        player.update(keys)

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


        # Vykreslení hráče s ohledem na kameru
        player_screen_rect = player.rect.copy()
        player_screen_rect.x -= camera_offset_x
        screen.blit(player.image, player_screen_rect)


        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
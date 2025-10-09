import pygame

# --- Nastavení a Konstanty ---
WIDTH, HEIGHT = 1280, 720
WORLD_WIDTH = WIDTH * 3

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
PURPLE = (128, 0, 128) # Portál
DARK_BLUE = (0, 0, 50) # Noc
GREED_COLOR = (220, 20, 60) # Greed
CROWN_GOLD = (255, 215, 0) # Koruna

# Herní čas
DAY_LENGTH = 60000  # 60 sekund
NIGHT_LENGTH = 30000 # 30 sekund
# Kratší pro testování
# DAY_LENGTH = 20000
# NIGHT_LENGTH = 15000

# Eventy
SPAWN_BEGGAR_EVENT = pygame.USEREVENT + 1

# Screen
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TILE_SIZE = 64

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 50, 50)
GREEN = (50, 200, 50)
BLUE = (50, 50, 200)
YELLOW = (255, 215, 0)
PURPLE = (150, 0, 150)
BROWN = (139, 69, 19)
SKY_BLUE = (100, 200, 255)
NIGHT_BLUE = (10, 10, 30)

# Layers (Z-Index)
LAYER_BG_FAR = 0
LAYER_BG_MID = 1
LAYER_BG_NEAR = 2
LAYER_GROUND = 3
LAYER_MOUNT_BG = 4 # Behind player
LAYER_PLAYER = 5
LAYER_MOUNT_FG = 6 # In front of player (legs?)
LAYER_UNITS = 7
LAYER_ITEMS = 8 # Coins, Tools
LAYER_BUILDINGS = 9 # Walls need to be behind or in front? Usually behind units. Let's adjust.
# Adjusted Layers
L_BG = 0
L_GROUND = 1
L_BUILDING_BG = 2 # Behind units
L_UNITS = 3
L_PLAYER = 4
L_ITEMS = 5
L_FG = 6
L_UI = 10

# Physics
GRAVITY = 0.8
FRICTION = -0.12
PLAYER_SPEED = 5
PLAYER_RUN_SPEED = 9

# Game Rules
DAY_LENGTH = 3600 # 60 seconds * 60 fps
NIGHT_START_THRESHOLD = 0.6 # 60% of day is light

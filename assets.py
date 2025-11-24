import pygame

def create_pixel_surface(width, height, color):
    """Creates a surface with a solid color, useful for placeholders."""
    surf = pygame.Surface((width, height))
    surf.fill(color)
    return surf

def create_horse_sprite(color):
    """Procedurally draws a simple pixel-art horse."""
    # 32x32 sprite scaled up later if needed
    surf = pygame.Surface((32, 32), pygame.SRCALPHA)

    # Body
    pygame.draw.rect(surf, color, (5, 15, 20, 10))
    # Legs
    pygame.draw.rect(surf, color, (5, 25, 4, 7)) # Back Left
    pygame.draw.rect(surf, color, (9, 25, 4, 7)) # Back Right
    pygame.draw.rect(surf, color, (17, 25, 4, 7)) # Front Left
    pygame.draw.rect(surf, color, (21, 25, 4, 7)) # Front Right
    # Neck/Head
    pygame.draw.rect(surf, color, (20, 5, 6, 12))
    pygame.draw.rect(surf, color, (22, 5, 8, 6)) # Snout

    return surf

def create_monarch_sprite(color):
    """Procedurally draws a simple monarch."""
    surf = pygame.Surface((16, 24), pygame.SRCALPHA)
    # Robe
    pygame.draw.rect(surf, color, (2, 10, 12, 14))
    # Head
    pygame.draw.rect(surf, (255, 200, 150), (4, 2, 8, 8))
    # Crown
    pygame.draw.rect(surf, (255, 215, 0), (4, 0, 8, 3))

    return surf

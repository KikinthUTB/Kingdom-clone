import pygame
from settings import *

class UI:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 20)
        self.large_font = pygame.font.SysFont("Arial", 40)

    def draw_game_ui(self, player, day, is_night):
        # Coin Pouch
        # Draw a bag icon + Number
        pygame.draw.circle(self.screen, (150, 100, 50), (40, 40), 20)
        text = self.font.render(str(player.coins), True, WHITE)
        self.screen.blit(text, (35, 30))

        # Day/Night
        color = (200, 200, 255) if not is_night else (100, 100, 150)
        day_text = self.large_font.render(f"Day {day}", True, color)
        rect = day_text.get_rect(midtop=(SCREEN_WIDTH // 2, 20))
        self.screen.blit(day_text, rect)

        # Controls Help (Fade out logic usually, but keep for now)
        help_text = self.font.render("[WASD] Move  [S] Drop Coin/Interact  [Shift] Run  [P] Debug Cave", True, WHITE)
        self.screen.blit(help_text, (20, SCREEN_HEIGHT - 30))

    def draw_menu(self):
        # Title Screen
        self.screen.fill(BLACK)
        title = self.large_font.render("KINGDOM CLONE", True, YELLOW)
        self.screen.blit(title, (SCREEN_WIDTH//2 - 150, 200))

        sub = self.font.render("Press SPACE to Start", True, WHITE)
        self.screen.blit(sub, (SCREEN_WIDTH//2 - 100, 300))

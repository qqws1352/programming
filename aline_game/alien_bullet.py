import pygame
from pygame.sprite import Sprite

class AlienBullet(Sprite):
    def __init__(self, ai_game, alien):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.rect = pygame.Rect(0, 0, 5, 15)  # 更细的子弹
        self.rect.centerx = alien.rect.centerx
        self.rect.top = alien.rect.bottom
        self.y = float(self.rect.y)

    def update(self):
        """向下移动子弹"""
        self.y += self.settings.alien_bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, (255, 0, 0), self.rect)  # 红色子弹
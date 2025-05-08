import pygame
import random
from pygame.sprite import Sprite
from aline_game.alien_bullet import AlienBullet


class Alien(Sprite):
    """表示单个外星人的类"""
    def __init__(self,ai_game):
        """初始化外星人并设置其初始位置"""
        super().__init__()
        self.screen=ai_game.screen
        self.settings=ai_game.settings
        #加载外星人图像并显示其rect属性
        self.image=pygame.image.load('images/aline.png')
        self.rect=self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)  # 新增mask属性
        #每个外星人最初都在屏幕左上角附近
        self.rect.x=self.rect.width
        self.rect.y=self.rect.height
        #存储外星人的精确水平位置
        self.x=float(self.rect.x)
        self.last_shot = pygame.time.get_ticks()  # 记录上次射击时间

    def try_shoot(self, ai_game):
        """随机射击"""
        now = pygame.time.get_ticks()
        if now - self.last_shot > 2000:  # 每2秒尝试射击一次
            if random.random() < 0.0001:  # 概率
                ai_game.alien_bullets.add(AlienBullet(ai_game, self))
                self.last_shot = now

    def check_edges(self):
        """如果外星人位于屏幕边缘，就返回True"""
        screen_rect=self.screen.get_rect()
        if self.rect.right>=screen_rect.right or self.rect.left<=0:
            return True

    def update(self):
        """向左 向右移动外星人"""
        self.x+=(self.settings.alien_speed*self.settings.fleet_direction)
        self.rect.x=self.x
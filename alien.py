import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    # 表示单个外星人

    def __init__(self, ai_settings, screen):
        # 初始化外星人并设置外星人的初始状态
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # 加载外星人图像并获取该图像的矩形属性
        self.image = pygame.image.load("./images/alien.bmp")
        self.rect = self.image.get_rect()

        # 设置图像的矩形属性
        # 将矩形的初始位置设置为左上角
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 设置外星人的准确位置
        self.x = float(self.rect.x)

    def check_edges(self):
        # 如果外星人位于屏幕边缘就返回TRUE
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
        
    def update(self):
        # 向右或者向左移动外星人
        self.x += self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction
        self.rect.x = self.x

    def blitme(self):
        # 在指定位置绘制外星人
        self.screen.blit(self.image, self.rect)
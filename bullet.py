import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """用来管理飞船发射出去的子弹"""
    def __init__(self, ai_setting, screen, ship):
        # 在飞船当前位置创建一个子弹对象
        super().__init__()
        self.screen = screen

        # 在（0,0）处设置一个矩形子弹，再设置正确的位置
        self.rect = pygame.Rect(0, 0, ai_setting.bullet_width, ai_setting.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # 用小数表示子弹的位置
        self.y = float(self.rect.y)

        self.color = ai_setting.bullet_color
        self.speed_factor = ai_setting.bullet_speed_factor

    def update(self):
        """向上移动子弹"""
        self.y -= self.speed_factor
        """更新子弹的rect位置"""
        self.rect.y = self.y

    def draw_bullet(self):
        """将子弹绘制到屏幕上"""
        pygame.draw.rect(self.screen, self.color, self.rect)

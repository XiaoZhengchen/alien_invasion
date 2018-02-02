import pygame
from pygame.sprite import Group

import game_functions as gf
from settings import Settings
from ship import Ship
from game_states import GameStats
from button import Button
from scoreboard import Scoreboard
"""
创建整个游戏都需要使用的对象
包含游戏的主循环
也是运行游戏需要运行的唯一文件
"""


def run_game():
    print("start")
    pygame.init()
    ai_settings = Settings()
    # 通过设置里面的参数来确定屏幕参数
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height)
    )
    pygame.display.set_caption("Alien Invasion")

    # 创建一个用于存储游戏统计信息的实例,并创建计分板
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    # 创建一艘飞船
    ship = Ship(ai_settings, screen)
    # 创建外星人编组
    aliens = Group()
    # 创建外星人群
    gf.create_fleet(ai_settings, screen, aliens, ship)

    # 创建一个存储子弹的编组
    bullets = Group()
    # 创建Play按钮
    play_button = Button(ai_settings, screen, "Play")

    while True:
        # 响应事件
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)

        if stats.game_active:
            # 更新飞船
            ship.update(ai_settings)
            # 更新子弹
            bullets.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            # 更新外星人
            gf.update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets)

        # 更新屏幕
        gf.update_screen(ai_settings, screen, stats, sb, ship, bullets, aliens, play_button)


run_game()

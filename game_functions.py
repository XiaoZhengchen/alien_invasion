import sys
import pygame

from time import sleep
from bullet import Bullet
from alien import Alien
"""
包含一系列的函数
完成游戏中的大部分工作
"""


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        # 响应右键
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        # 响应左键
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        # 响应空格键
        fire_bullet(bullets, ai_settings, screen, ship)
    elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
        # 响应q键与esc退出
        sys.exit()


def check_keyup_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """响应按键与鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets,
                      mouse_x, mouse_y):
    # 玩家单击play按钮开始游戏
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)

    if button_clicked and not stats.game_active:
        # 重置游戏设置
        ai_settings.initialize_dynamic_settings()

        # 隐藏鼠标光标
        pygame.mouse.set_visible(False)

        # 重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True

        # 重置计分图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群外星人，并让飞船居中
        create_fleet(ai_settings, screen, aliens, ship)
        ship.center_ship()


def fire_bullet(bullets, ai_settings, screen, ship):
    # 创建一颗子弹，并将之加入到bullets的编组中
    # 在创建一颗子弹前，先判断是否当前子弹数量已经超过了限制
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # 删除已经消失的子弹
    # 更新子弹的位置
    # 使用bullets的复制来进行遍历，因为会在遍历的过程中修改bullets
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
            # print(len(bullets))
    # 检查子弹与飞船相撞
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # 检查是否有子弹击中了外星人
    # 如果是这样，就删除相应的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    # 计算得分
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    # 外星人被击杀完
    if len(aliens) == 0:
        # 删除现有的子弹，提高游戏等级，加快游戏节奏，并创建新的一群外星人
        bullets.empty()
        ai_settings.increase_speed()
        # 提高等级
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, aliens, ship)


def check_high_score(stats, sb):
    """检查是否产生了最高得分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def check_fleet_edges(ai_settings, aliens):
    """有外星人到达边缘时采取相应的措施"""
    for alien in aliens:
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """将整群外星人下移，并改正他们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """响应被外星人撞到的飞船"""
    if stats.ships_left > 1:
        # 将ship_left减一
        stats.ships_left -= 1
        # 更新生命值图像
        sb.prep_ships()
        # 清空外星人列表与子弹列表
        aliens.empty()
        bullets.empty()
        # 创建一群新的外星人，并将飞船放到屏幕底部中央
        create_fleet(ai_settings, screen, aliens, ship)
        ship.center_ship()
        # 暂停
        sleep(0.5)

    else:
        stats.game_active = False
        # 使光标可见
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """检查是否有外星人到达了屏幕低端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船被撞到一样进行处理
            ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
            break


def update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets):
    # 检查是否有外星人位于屏幕边缘并更新所有外星人的位置
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # 检查是否有外星人到达屏幕底端
    check_aliens_bottom(ai_settings, stats, sb, screen, ship,aliens, bullets)
    # 检测外星人与飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)


def get_number_aliens_x(ai_settings, alien_width, num):
    # 获得屏幕一行所能显示的外星人的个数
    available_space_x = ai_settings.screen_width - num * alien_width
    number_alien_x = int(available_space_x / (num * alien_width))
    return number_alien_x


def get_number_rows(ai_settings, ship_height, alien_height, num):
    # 计算屏幕可以容纳多少行外星人
    available_space_y = ai_settings.screen_height - ship_height - (num + 1) * alien_height
    number_row =int(available_space_y / (num * alien_height))
    return number_row


def create_alien(ai_settings, screen, aliens, alien_number, row_number, num):
    # 创建一个外星人图像
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + num * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + num * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, aliens, ship):
    # 创建外星人群
    # 创建一个外星人并计算一行可以容纳多少外星人
    # 外星人间距为外星人宽度
    num = 2
    alien = Alien(ai_settings, screen)
    number_alien_x = get_number_aliens_x(ai_settings, alien.rect.width, num)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height, num)
    # 创建第多行外星人
    for row_number in range(number_rows):
        for alien_number in range(number_alien_x):
            # 创建一个外星人并将其加入当前行
            create_alien(ai_settings, screen, aliens, alien_number, row_number, num)


def update_screen(ai_settings, screen, stats, sb, ship, bullets, aliens, play_button):
    """更新屏幕"""
    # 每次循环的时候都重新更新屏幕
    screen.fill(ai_settings.bg_color)
    # 在飞船和外星人后面重新绘制所有子弹
    for bullet in bullets:
        bullet.draw_bullet()
    # 绘制飞船
    ship.blitme()
    # 绘制外星人
    aliens.draw(screen)
    # 显示得分
    sb.show_score()
    # 如果游戏处于非活动状态则绘制play按钮
    if not stats.game_active:
        play_button.draw_button()
    # 使更新后的屏幕可见
    pygame.display.flip()

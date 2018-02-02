class Settings():
    """
    存储所有设置的类
    只包含__init__方法用来初始化基本参数
    """

    def __init__(self):
        """初始游戏的静态设置"""
        # 屏幕设置
        self.screen_width = 1000
        self.screen_height = 700
        self.bg_color = (230, 230, 230)
        # 设置飞船移动的速度
        self.ship_speed_factor = 1.5
        self.ship_limit = 3
        # 子弹设置
        self.bullet_speed_factor = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullet_allowed = 8
        # 设置外星人
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 30
        # 设置击杀外星人的分数
        self.alien_points = 50
        # 设置外星人的移动方向1为右移，-1为左移
        self.fleet_direction = 1
        # 加快游戏的进度
        self.speedup_scale = 1.1
        # 外星人点数的提高速度
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        # 初始化随游戏进行而改变的设置
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        # fleet_direction为1表示向右，为-1不表示向左
        self.fleet_direction = 1

    def increase_speed(self):
        # 提高速度设置和外星人的点数
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
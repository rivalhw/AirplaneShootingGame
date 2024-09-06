import pygame
import random
import os
import game_init
import game_resources
import game_main
import game_end_screen
import game_start_screen

# 游戏版本号和作者信息
GAME_VERSION = "V3.8"
AUTHOR_NAME = "游戏作者: 大伟说AI"

# 初始化游戏
screen, width, height = game_init.initialize_game()

# 加载字体和资源
font, small_font, large_font, medium_font = game_init.load_fonts()
sounds = game_resources.load_sounds()
images = game_resources.load_images()

# 初始化玩家和游戏参数
player = pygame.Rect(370, 500, 60, 60)
player_speed_factor = 5  # 控制平滑移动的速度
missile_count = 10  # 初始导弹数量
missiles = []  # 导弹列表
enemies = []  # 敌机列表
enemy_bullets = []  # 敌机子弹列表
bullets = []  # 玩家子弹列表
score = 0  # 玩家得分
lives = 3  # 玩家生命数
stars = [pygame.Rect(random.randint(0, width - 2), random.randint(0, height - 2), 2, 2) for _ in range(100)]  # 背景星星
game_time = 60  # 游戏时间为60秒



# 重置游戏
def reset_game():
    global player, missiles, enemies, enemy_bullets, bullets, missile_count, lives, score
    player = pygame.Rect(370, 500, 60, 60)  # 重置玩家位置
    missiles = []  # 重置导弹
    enemies = []  # 重置敌机
    enemy_bullets = []  # 重置敌机子弹
    bullets = []  # 重置玩家子弹
    missile_count = 10  # 重置导弹数量
    lives = 3  # 重置玩家生命
    score = 0  # 重置得分

# 游戏主逻辑
reset_game()
game_main.main_game(
    screen, 
    width, 
    height, 
    font, 
    small_font, 
    medium_font, 
    large_font, 
    sounds, 
    images, 
    player, 
    player_speed_factor, 
    missile_count, 
    missiles, 
    enemies, 
    enemy_bullets, 
    bullets, 
    score, 
    lives, 
    stars, 
    game_time
)

import pygame
import sys

# 初始化 Pygame
def initialize_game():
    pygame.init()

    # 设置游戏窗口为全屏
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    width, height = screen.get_size()
    pygame.display.set_caption("大伟说AI：太空大战")

    return screen, width, height

# 字体路径根据操作系统进行选择
def load_fonts():
    if sys.platform.startswith("darwin"):  # MacOS
        font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
    elif sys.platform.startswith("win"):  # Windows
        font_path = "C:/Windows/Fonts/simhei.ttf"  # 例如，使用SimHei字体
    else:
        font_path = None  # 其他系统不指定字体路径

    if font_path:
        font = pygame.font.Font(font_path, 36)
        small_font = pygame.font.Font(font_path, 18)  # 较小字体
        large_font = pygame.font.Font(font_path, 72)  # 大字体
        medium_font = pygame.font.Font(font_path, 48)  # 中等字体
    else:
        font = pygame.font.SysFont(None, 36)  # 默认字体
        small_font = pygame.font.SysFont(None, 18)  # 较小字体
        large_font = pygame.font.SysFont(None, 72)  # 大字体
        medium_font = pygame.font.SysFont(None, 48)  # 中等字体

    return font, small_font, large_font, medium_font

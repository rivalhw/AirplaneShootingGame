import pygame
import sys

# 初始化 Pygame
pygame.init()

# 设置游戏窗口
width = 800
height = 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("太空大战 - 游戏开始")

# 加载背景图片并保持原比例
background_image = pygame.image.load("./images/Transformers/background.png").convert()
background_rect = background_image.get_rect()  # 获取背景图片的原始大小

# 设置透明度为80%（204/255）
background_image.set_alpha(204)

# 计算背景图绘制的起始位置，保持居中且不变形
background_x = (width - background_rect.width) // 2
background_y = (height - background_rect.height) // 2

# 加载背景音乐
pygame.mixer.music.load("./sounds/background_music1.mp3")
pygame.mixer.music.play(-1)  # 循环播放背景音乐

# 加载光标移动声音
cursor_move_sound = pygame.mixer.Sound("./sounds/dada.wav")

# 颜色定义
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# 字体路径根据操作系统进行选择
if sys.platform.startswith("darwin"):  # MacOS
    font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
elif sys.platform.startswith("win"):  # Windows
    font_path = "C:/Windows/Fonts/simhei.ttf"  # 例如，使用SimHei字体
else:
    font_path = None  # 其他系统不指定字体路径

# 字体设置
if font_path:
    font = pygame.font.Font(font_path, 36)
else:
    font = pygame.font.SysFont(None, 36)  # 如果未指定字体路径，则使用默认字体

# 菜单选项
menu_options = ["开始游戏", "结束游戏", "退出游戏"]
selected_option = 0

def draw_menu():
    screen.fill(BLACK)  # 背景为黑色
    screen.blit(background_image, (background_x, background_y))  # 绘制背景图片，保持原比例
    for i, option in enumerate(menu_options):
        if i == selected_option:
            label = font.render(option, True, RED)
        else:
            label = font.render(option, True, WHITE)
        screen.blit(label, (width // 2 - 100, height // 2 + i * 50))
    pygame.display.flip()

def main_menu():
    global selected_option

    while True:
        draw_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                    cursor_move_sound.play()  # 播放光标移动声音
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                    cursor_move_sound.play()  # 播放光标移动声音
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:  # 开始游戏
                        pygame.mixer.music.stop()
                        start_game()  # 调用开始游戏的逻辑
                    elif selected_option == 1:  # 结束游戏
                        pygame.mixer.music.stop()
                        end_game()  # 调用结束游戏的逻辑
                    elif selected_option == 2:  # 退出游戏
                        pygame.quit()
                        sys.exit()

# 加载并运行原先的游戏代码
def start_game():
    import AirplaneShootingGame  # 这里加载原有的游戏代码文件
    AirplaneShootingGame.reset_game()
    AirplaneShootingGame.main_game()

# 调用结束游戏逻辑，进入片尾
def end_game():
    import game_end_screen  # 加载结束游戏画面模块
    game_end_screen.game_over_screen(120, [300, 250, 200, 150, 100])  # 示例分数与排行榜
    import game_start_screen  # 返回主菜单
    game_start_screen.main_menu()

if __name__ == "__main__":
    main_menu()
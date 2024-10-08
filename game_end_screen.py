import pygame
import sys

# 初始化 Pygame
pygame.init()

# 设置全屏模式
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("大伟说AI：太空大战 - 游戏结束")

# 获取全屏窗口的宽高
width, height = screen.get_size()

# 颜色定义
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)

# 字体路径根据操作系统进行选择
if sys.platform.startswith("darwin"):  # MacOS
    font_path = "/System/Library/Fonts/PingFang.ttc"  # 支持中文的字体
elif sys.platform.startswith("win"):  # Windows
    font_path = "C:/Windows/Fonts/simhei.ttf"  # 使用黑体 SimHei 支持中文
else:
    font_path = None  # 其他系统可以选择其他支持中文的字体

# 字体设置
if font_path:
    title_font = pygame.font.Font(font_path, 48)  # 标题字体
    score_font = pygame.font.Font(font_path, 36)  # 分数字体，支持中文
    prompt_font = pygame.font.Font(font_path, 28)  # 提示字体
else:
    title_font = pygame.font.SysFont("Arial Unicode MS", 48)  # 使用 Arial Unicode MS 字体
    score_font = pygame.font.SysFont("Arial Unicode MS", 36)
    prompt_font = pygame.font.SysFont("Arial Unicode MS", 28)

# 加载背景图片并保持比例
background_image = pygame.image.load("./images/Transformers/end_background.png").convert()
background_rect = background_image.get_rect()

# 计算保持比例缩放的尺寸
scale_factor = min(width / background_rect.width, height / background_rect.height)
new_width = int(background_rect.width * scale_factor)
new_height = int(background_rect.height * scale_factor)
background_image = pygame.transform.scale(background_image, (new_width, new_height))

# 创建临时表面用于调整透明度
background_surface = pygame.Surface((new_width, new_height)).convert()
background_surface.blit(background_image, (0, 0))
background_surface.set_alpha(153)  # 设置透明度为60% (153/255)

# 加载结束画面的背景音乐
pygame.mixer.music.load("./sounds/background_music2.mp3")

# 加载按键音效
click_sound = pygame.mixer.Sound("./sounds/click.wav")

# 绘制游戏结束界面
def draw_game_over_screen(final_score, high_scores):
    screen.fill(BLACK)

    # 绘制背景
    screen.blit(background_surface, ((width - new_width) // 2, (height - new_height) // 2))  # 保持比例居中绘制背景

    # 绘制标题
    title_text = title_font.render("游戏结束", True, GOLD)
    screen.blit(title_text, (width // 2 - title_text.get_width() // 2, 100))

    # 显示最终得分
    final_score_text = score_font.render(f"最终得分: {final_score}", True, WHITE)
    screen.blit(final_score_text, (width // 2 - final_score_text.get_width() // 2, 200))

    # 显示最高分排行榜
    high_scores_text = score_font.render("最高分排行榜:", True, GOLD)
    screen.blit(high_scores_text, (width // 2 - high_scores_text.get_width() // 2, 300))

    # 绘制排行榜分数
    for i, score in enumerate(high_scores):
        score_text = f"{i + 1}. {score}"
        score_surface = score_font.render(score_text, True, WHITE)
        screen.blit(score_surface, (width // 2 - score_surface.get_width() // 2, 350 + i * 40))

    # 显示提示信息
    prompt_text = prompt_font.render("按任意键返回主菜单", True, RED)
    screen.blit(prompt_text, (width // 2 - prompt_text.get_width() // 2, 650))

    pygame.display.flip()

# 游戏结束界面逻辑
def game_over_screen(final_score, high_scores):
    # 播放背景音乐
    pygame.mixer.music.play(-1)  # 循环播放背景音乐

    running = True
    while running:
        draw_game_over_screen(final_score, high_scores)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # 播放按键音效
                click_sound.play()
                running = False
                pygame.mixer.music.stop()  # 停止背景音乐
                import game_start_screen  # 返回主菜单
                game_start_screen.main_menu()

# 示例用法：
if __name__ == "__main__":
    game_over_screen(120, [300, 250, 200, 150, 100])

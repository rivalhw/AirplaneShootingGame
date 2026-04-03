import pygame
import sys
import math
import random

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
SILVER = (192, 192, 192)
BRONZE = (205, 127, 50)
CYAN = (0, 255, 255)
PURPLE = (147, 0, 211)
ORANGE = (255, 140, 0)
GREEN = (0, 255, 127)

# 字体路径根据操作系统进行选择
if sys.platform.startswith("darwin"):  # MacOS
    font_path = "/System/Library/Fonts/PingFang.ttc"
elif sys.platform.startswith("win"):  # Windows
    font_path = "C:/Windows/Fonts/simhei.ttf"
else:
    font_path = None

# 字体设置
if font_path:
    title_font = pygame.font.Font(font_path, 72)
    score_font = pygame.font.Font(font_path, 40)
    prompt_font = pygame.font.Font(font_path, 32)
    author_font = pygame.font.Font(font_path, 28)
    rank_font = pygame.font.Font(font_path, 48)
else:
    title_font = pygame.font.SysFont("Arial Unicode MS", 72)
    score_font = pygame.font.SysFont("Arial Unicode MS", 40)
    prompt_font = pygame.font.SysFont("Arial Unicode MS", 32)
    author_font = pygame.font.SysFont("Arial Unicode MS", 28)
    rank_font = pygame.font.SysFont("Arial Unicode MS", 48)

# 加载背景图片并保持比例
try:
    background_image = pygame.image.load("./images/Transformers/end_background.png").convert()
    background_rect = background_image.get_rect()
    scale_factor = min(width / background_rect.width, height / background_rect.height)
    new_width = int(background_rect.width * scale_factor)
    new_height = int(background_rect.height * scale_factor)
    background_image = pygame.transform.scale(background_image, (new_width, new_height))
    
    # 创建临时表面用于调整透明度
    background_surface = pygame.Surface((new_width, new_height)).convert()
    background_surface.blit(background_image, (0, 0))
    background_surface.set_alpha(120)  # 设置透明度为47%
except:
    background_surface = None

# 加载结束画面的背景音乐
pygame.mixer.music.load("./sounds/background_music2.mp3")

# 加载按键音效
click_sound = pygame.mixer.Sound("./sounds/click.wav")

# 初始化背景星星
stars = [(random.randint(0, width), random.randint(0, height), random.randint(1, 3)) for _ in range(150)]

def draw_gradient_text(surface, text, font, x, y, color1, color2, glow=True, glow_color=None, time=0):
    """绘制渐变发光文字"""
    if glow_color is None:
        glow_color = color1
    
    # 创建发光效果（多层阴影）
    if glow:
        for offset in range(10, 0, -2):
            alpha = int(50 - offset * 4)
            glow_surface = font.render(text, True, glow_color)
            glow_surface.set_alpha(alpha)
            # 添加脉动效果
            pulse = math.sin(time * 3) * 2
            surface.blit(glow_surface, (x - offset/2 + pulse, y - offset/2 + pulse))
    
    # 绘制主文字
    text_surface = font.render(text, True, color1)
    surface.blit(text_surface, (x, y))
    
    return text_surface.get_rect(topleft=(x, y))

def draw_decorative_border(surface, rect, color, thickness=3, time=0):
    """绘制装饰性边框"""
    # 外边框
    pygame.draw.rect(surface, color, rect, thickness, border_radius=15)
    
    # 角落装饰
    corner_size = 20
    pulse = math.sin(time * 2) * 3
    
    # 左上
    pygame.draw.line(surface, GOLD, (rect.left - 5, rect.top + corner_size), 
                     (rect.left + corner_size, rect.top - 5), 4)
    # 右上
    pygame.draw.line(surface, GOLD, (rect.right + 5, rect.top + corner_size), 
                     (rect.right - corner_size, rect.top - 5), 4)
    # 左下
    pygame.draw.line(surface, GOLD, (rect.left - 5, rect.bottom - corner_size), 
                     (rect.left + corner_size, rect.bottom + 5), 4)
    # 右下
    pygame.draw.line(surface, GOLD, (rect.right + 5, rect.bottom - corner_size), 
                     (rect.right - corner_size, rect.bottom + 5), 4)
    
    # 发光角点
    for corner in [(rect.left, rect.top), (rect.right, rect.top), 
                   (rect.left, rect.bottom), (rect.right, rect.bottom)]:
        glow_size = int(8 + pulse)
        pygame.draw.circle(surface, color, corner, glow_size, 2)

def draw_ranking_item(surface, rank, score, y_pos, time, is_player_score=False):
    """绘制排行榜条目"""
    # 根据排名设置颜色
    if rank == 1:
        rank_color = GOLD
        glow_color = (255, 215, 0)
    elif rank == 2:
        rank_color = SILVER
        glow_color = (192, 192, 192)
    elif rank == 3:
        rank_color = BRONZE
        glow_color = (205, 127, 50)
    else:
        rank_color = CYAN
        glow_color = (0, 255, 255)
    
    # 高亮当前玩家分数
    if is_player_score:
        rank_color = GREEN
        glow_color = (0, 255, 127)
    
    # 统一计算圆形位置（固定偏移）
    circle_center_x = width // 2 - 180
    circle_center = (circle_center_x, y_pos + 22)
    
    # 文字从固定位置开始（圆形右侧）
    text_x = circle_center_x + 35
    
    text = f"第{rank}名: {score}分"
    
    # 获取文字尺寸
    text_surface = score_font.render(text, True, rank_color)
    
    # 绘制发光效果
    for offset in range(6, 0, -1):
        alpha = int(40 - offset * 5)
        glow = score_font.render(text, True, glow_color)
        glow.set_alpha(alpha)
        surface.blit(glow, (text_x, y_pos))
    
    # 绘制主文字
    surface.blit(text_surface, (text_x, y_pos))
    
    # 绘制排名数字圆形背景
    pygame.draw.circle(surface, rank_color, circle_center, 18)
    pygame.draw.circle(surface, WHITE, circle_center, 18, 2)
    # 绘制排名数字
    rank_num = rank_font.render(str(rank), True, BLACK)
    num_rect = rank_num.get_rect(center=circle_center)
    surface.blit(rank_num, num_rect)

def draw_trophy(surface, x, y, size, time):
    """绘制奖杯动画效果"""
    # 奖杯发光效果
    pulse = (math.sin(time * 4) + 1) / 2  # 0-1之间的脉动值
    glow_radius = int(size * (0.8 + pulse * 0.3))
    
    # 外发光圈
    for r in range(glow_radius, 0, -5):
        alpha = int(30 * (1 - r / glow_radius))
        glow_surface = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, (*GOLD, alpha), (r, r), r)
        surface.blit(glow_surface, (x - r, y - r))
    
    # 奖杯主体（简化版）
    trophy_color = GOLD
    # 杯身
    cup_rect = pygame.Rect(x - size//3, y - size//2, size//1.5, size//1.5)
    pygame.draw.ellipse(surface, trophy_color, cup_rect)
    pygame.draw.ellipse(surface, ORANGE, cup_rect, 3)
    # 杯柄
    pygame.draw.arc(surface, trophy_color, (x - size//2, y - size//3, size//3, size//2), 1.5, 4.5, 4)
    pygame.draw.arc(surface, trophy_color, (x + size//6, y - size//3, size//3, size//2), 4.8, 7.8, 4)

def draw_game_over_screen(final_score, high_scores, time):
    """绘制炫酷的游戏结束界面"""
    # 绘制黑色背景
    screen.fill(BLACK)
    
    # 绘制动态星空背景
    for i, (sx, sy, size) in enumerate(stars):
        # 星星闪烁效果
        twinkle = (math.sin(time * 3 + i) + 1) / 2
        brightness = int(100 + twinkle * 155)
        star_color = (brightness, brightness, brightness)
        pygame.draw.circle(screen, star_color, (sx, sy), size)
        # 星星缓慢下落
        new_y = (sy + 0.5) % height
        stars[i] = (sx, new_y, size)
    
    # 绘制背景图片
    if background_surface:
        screen.blit(background_surface, ((width - new_width) // 2, (height - new_height) // 2))
    
    # 绘制顶部光效
    for i in range(5):
        alpha = int(30 - i * 5)
        glow_surface = pygame.Surface((width, 200), pygame.SRCALPHA)
        pygame.draw.ellipse(glow_surface, (*GOLD, alpha), (0, 0, width, 200))
        screen.blit(glow_surface, (0, -50 + i * 10))
    
    # ========== 标题区域 ==========
    title_text = "游 戏 结 束"
    title_surface = title_font.render(title_text, True, GOLD)
    title_width = title_surface.get_width()
    title_x = width // 2 - title_width // 2
    
    # 绘制标题发光效果
    for offset in range(15, 0, -2):
        alpha = int(60 - offset * 3)
        glow = title_font.render(title_text, True, ORANGE)
        glow.set_alpha(alpha)
        pulse_x = math.sin(time * 2) * 3
        screen.blit(glow, (title_x + pulse_x - offset/2, 90 - offset/2))
    
    # 绘制主标题
    screen.blit(title_surface, (title_x, 90))
    
    # 标题下划线动画
    line_width = int(title_width * (0.5 + 0.5 * math.sin(time * 2)))
    line_x = width // 2 - line_width // 2
    pygame.draw.line(screen, GOLD, (line_x, 165), (line_x + line_width, 165), 3)
    
    # ========== 最终得分区域 ==========
    score_y = 200
    score_text = f"最终得分: {final_score}"
    score_surface = score_font.render(score_text, True, CYAN)
    score_width = score_surface.get_width()
    score_x = width // 2 - score_width // 2
    
    # 得分发光效果
    for offset in range(8, 0, -1):
        alpha = int(50 - offset * 5)
        glow = score_font.render(score_text, True, PURPLE)
        glow.set_alpha(alpha)
        pulse = math.sin(time * 4) * 2
        screen.blit(glow, (score_x + pulse - offset/2, score_y - offset/2))
    
    screen.blit(score_surface, (score_x, score_y))
    
    # ========== 荣誉榜区域 ==========
    board_x = width // 2 - 250
    board_y = 280
    board_width = 500
    board_height = 280
    
    # 绘制荣誉榜背景框
    board_rect = pygame.Rect(board_x, board_y, board_width, board_height)
    board_surface = pygame.Surface((board_width, board_height), pygame.SRCALPHA)
    board_surface.fill((0, 0, 0, 150))
    screen.blit(board_surface, (board_x, board_y))
    
    # 绘制装饰边框
    draw_decorative_border(screen, board_rect, GOLD, 3, time)
    
    # 荣誉榜标题
    rank_title = "★ 荣 誉 榜 ★"
    rank_title_surface = score_font.render(rank_title, True, GOLD)
    rank_title_x = width // 2 - rank_title_surface.get_width() // 2
    screen.blit(rank_title_surface, (rank_title_x, board_y + 15))
    
    # 绘制排行榜分数
    start_y = board_y + 65
    for i, score in enumerate(high_scores[:5]):
        is_player = (score == final_score and final_score > 0)
        draw_ranking_item(screen, i + 1, score, start_y + i * 45, time, is_player)
    
    # ========== 开发者信息 ==========
    author_y = height - 120
    dev_text = "游戏开发者: 大伟"
    dev_surface = author_font.render(dev_text, True, GREEN)
    dev_width = dev_surface.get_width()
    dev_x = width // 2 - dev_width // 2
    
    # 开发者名字发光效果
    for offset in range(6, 0, -1):
        alpha = int(40 - offset * 5)
        glow = author_font.render(dev_text, True, CYAN)
        glow.set_alpha(alpha)
        pulse = math.sin(time * 3 + 1) * 2
        screen.blit(glow, (dev_x + pulse - offset/2, author_y - offset/2))
    
    screen.blit(dev_surface, (dev_x, author_y))
    
    # 分隔线
    pygame.draw.line(screen, GREEN, (width//2 - 150, author_y + 40), (width//2 + 150, author_y + 40), 2)
    
    # ========== 提示信息（闪烁效果）==========
    prompt_y = height - 60
    blink = (math.sin(time * 4) + 1) / 2  # 0-1闪烁
    prompt_color = (
        int(255 - (255-100) * blink),
        int(100 + 100 * blink),
        int(100 + 100 * blink)
    )
    prompt_text = "【 按任意键返回主菜单 】"
    prompt_surface = prompt_font.render(prompt_text, True, prompt_color)
    prompt_x = width // 2 - prompt_surface.get_width() // 2
    screen.blit(prompt_surface, (prompt_x, prompt_y))
    
    pygame.display.flip()

# 游戏结束界面逻辑
def game_over_screen(final_score, high_scores):
    # 播放背景音乐
    pygame.mixer.music.play(-1)
    
    running = True
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    
    while running:
        # 计算动画时间
        elapsed = (pygame.time.get_ticks() - start_time) / 1000.0
        
        draw_game_over_screen(final_score, high_scores, elapsed)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # 播放按键音效
                click_sound.play()
                running = False
                pygame.mixer.music.stop()
                import game_start_screen
                game_start_screen.main_menu()
        
        clock.tick(60)

# 示例用法
if __name__ == "__main__":
    game_over_screen(120, [300, 250, 200, 150, 100])

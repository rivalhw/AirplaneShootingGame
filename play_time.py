import os
import json
import pygame
import sys
from datetime import datetime

# 文件路径，用于存储每日的游戏时长和日期
PLAY_TIME_FILE = "play_time.json"

# 每天最多可以玩10分钟（600秒）
max_daily_time = 600

# 解除限制密码
UNLOCK_PASSWORD = "888888"

# 读取本地文件中已存储的游戏时间
def read_played_time():
    if not os.path.exists(PLAY_TIME_FILE):
        return 0  # 如果文件不存在，表示今天还没玩过游戏

    with open(PLAY_TIME_FILE, "r") as file:
        data = json.load(file)
    
    today = datetime.now().strftime("%Y-%m-%d")  # 获取当前日期
    if data.get("date") == today:
        return data.get("played_time", 0)  # 如果是今天，则返回累计的已玩时间
    else:
        return 0  # 如果是不同日期，则返回0（新的一天）

# 保存游戏时间到本地文件
def save_played_time(played_time):
    today = datetime.now().strftime("%Y-%m-%d")  # 获取当前日期
    data = {
        "date": today,
        "played_time": played_time
    }
    with open(PLAY_TIME_FILE, "w") as file:
        json.dump(data, file)

# 检查是否需要密码解锁（时间已用完）
def check_need_unlock():
    played_time = read_played_time()
    return played_time >= max_daily_time

# 密码输入界面
def password_unlock_screen(screen, width, height, large_font, medium_font, small_font):
    """
    显示密码输入界面，返回是否解锁成功
    """
    # 颜色定义
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    GOLD = (255, 215, 0)
    GRAY = (128, 128, 128)
    CYAN = (0, 255, 255)
    
    input_password = ""
    message = ""
    message_color = WHITE
    cursor_visible = True
    cursor_timer = 0
    
    clock = pygame.time.Clock()
    running = True
    unlocked = False
    
    # 按钮区域
    button_y = height // 2 + 120
    confirm_button = pygame.Rect(width // 2 - 160, button_y, 140, 50)
    back_button = pygame.Rect(width // 2 + 20, button_y, 140, 50)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # ESC返回
                    return False
                elif event.key == pygame.K_RETURN:
                    # 回车确认
                    if input_password == UNLOCK_PASSWORD:
                        # 密码正确，重置今日游戏时间
                        save_played_time(0)
                        message = "密码正确！解除限制成功！"
                        message_color = GREEN
                        unlocked = True
                        # 显示成功信息后延迟返回
                        screen.fill(BLACK)
                        success_text = large_font.render("解除限制成功！", True, GREEN)
                        screen.blit(success_text, (width // 2 - success_text.get_width() // 2, height // 2))
                        pygame.display.flip()
                        pygame.time.delay(1500)
                        return True
                    else:
                        message = "密码错误，请重试！"
                        message_color = RED
                        input_password = ""
                elif event.key == pygame.K_BACKSPACE:
                    # 退格删除
                    input_password = input_password[:-1]
                elif event.unicode.isalnum() and len(input_password) < 10:
                    # 输入字母或数字
                    input_password += event.unicode
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                # 检查确认按钮
                if confirm_button.collidepoint(mouse_pos):
                    if input_password == UNLOCK_PASSWORD:
                        save_played_time(0)
                        unlocked = True
                        screen.fill(BLACK)
                        success_text = large_font.render("解除限制成功！", True, GREEN)
                        screen.blit(success_text, (width // 2 - success_text.get_width() // 2, height // 2))
                        pygame.display.flip()
                        pygame.time.delay(1500)
                        return True
                    else:
                        message = "密码错误，请重试！"
                        message_color = RED
                        input_password = ""
                # 检查返回按钮
                if back_button.collidepoint(mouse_pos):
                    return False
        
        # 绘制界面
        screen.fill(BLACK)
        
        # 绘制警告图标（三角形）
        warning_y = height // 2 - 180
        pygame.draw.polygon(screen, GOLD, [
            (width // 2, warning_y - 40),
            (width // 2 - 50, warning_y + 40),
            (width // 2 + 50, warning_y + 40)
        ])
        pygame.draw.polygon(screen, BLACK, [
            (width // 2, warning_y - 30),
            (width // 2 - 40, warning_y + 30),
            (width // 2 + 40, warning_y + 30)
        ])
        # 感叹号
        exclamation = large_font.render("!", True, GOLD)
        screen.blit(exclamation, (width // 2 - exclamation.get_width() // 2, warning_y - 15))
        
        # 标题
        title_text = large_font.render("今日游戏时间已用完", True, RED)
        screen.blit(title_text, (width // 2 - title_text.get_width() // 2, height // 2 - 120))
        
        # 提示信息
        hint_text = small_font.render("请输入解除密码继续游戏", True, WHITE)
        screen.blit(hint_text, (width // 2 - hint_text.get_width() // 2, height // 2 - 50))
        
        # 密码输入框背景
        input_box = pygame.Rect(width // 2 - 150, height // 2, 300, 50)
        pygame.draw.rect(screen, WHITE, input_box, 2, border_radius=5)
        
        # 绘制输入的密码（显示为星号）
        display_text = "*" * len(input_password)
        password_surface = medium_font.render(display_text, True, WHITE)
        screen.blit(password_surface, (input_box.x + 15, input_box.y + 10))
        
        # 绘制闪烁光标
        cursor_timer += 1
        if cursor_timer % 30 == 0:
            cursor_visible = not cursor_visible
        if cursor_visible:
            cursor_x = input_box.x + 15 + password_surface.get_width()
            pygame.draw.line(screen, WHITE, (cursor_x, input_box.y + 10), 
                           (cursor_x, input_box.y + 40), 2)
        
        # 绘制消息
        if message:
            msg_surface = small_font.render(message, True, message_color)
            screen.blit(msg_surface, (width // 2 - msg_surface.get_width() // 2, height // 2 + 60))
        
        # 获取鼠标位置用于按钮高亮
        mouse_pos = pygame.mouse.get_pos()
        
        # 绘制确认按钮
        confirm_color = GREEN if confirm_button.collidepoint(mouse_pos) else (0, 200, 0)
        pygame.draw.rect(screen, confirm_color, confirm_button, border_radius=5)
        confirm_text = small_font.render("确认", True, BLACK)
        screen.blit(confirm_text, (confirm_button.centerx - confirm_text.get_width() // 2,
                                  confirm_button.centery - confirm_text.get_height() // 2))
        
        # 绘制返回按钮
        back_color = GRAY if back_button.collidepoint(mouse_pos) else (100, 100, 100)
        pygame.draw.rect(screen, back_color, back_button, border_radius=5)
        back_text = small_font.render("返回", True, WHITE)
        screen.blit(back_text, (back_button.centerx - back_text.get_width() // 2,
                               back_button.centery - back_text.get_height() // 2))
        
        # 底部提示
        bottom_hint = small_font.render("按 ESC 返回主菜单", True, GRAY)
        screen.blit(bottom_hint, (width // 2 - bottom_hint.get_width() // 2, height - 50))
        
        pygame.display.flip()
        clock.tick(60)
    
    return unlocked

# 示例用法
if __name__ == "__main__":
    print(f"今日已玩时间：{read_played_time()} 秒")
    save_played_time(600)  # 假设已玩了600秒

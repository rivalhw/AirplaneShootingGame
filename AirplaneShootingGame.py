import pygame
import random
import time
import os
import sys

# 游戏版本号
GAME_VERSION = "V3.6"
AUTHOR_NAME = "游戏作者: 伟大的大伟"

# 初始化 Pygame
pygame.init()

# 设置游戏窗口
width = 800
height = 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("太空大战")

# 颜色定义
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# 加载飞机图标，并将大小调整为60x60
player_image = pygame.image.load("./images/player_fighter.png")
player_image = pygame.transform.scale(player_image, (60, 60))

enemy_image = pygame.image.load("./images/enemy_fighter.png")
enemy_image = pygame.transform.scale(enemy_image, (60, 60))

# 加载擎天柱图像
optimus_prime1 = pygame.image.load("./images/Transformers/optimus_prime1.png")
optimus_prime1 = pygame.transform.scale(optimus_prime1, (60, 60))

optimus_prime2 = pygame.image.load("./images/Transformers/optimus_prime2.png")
optimus_prime2 = pygame.transform.scale(optimus_prime2, (60, 60))

# 加载音效
shoot_sound = pygame.mixer.Sound("./sounds/shoot.wav")
explosion_sound = pygame.mixer.Sound("./sounds/explosion.wav")
collision_sound = pygame.mixer.Sound("./sounds/Transformer/itwillreturn.mp3")
missile_sound = pygame.mixer.Sound("./sounds/missile.mp3")
transform_sound1 = pygame.mixer.Sound("./sounds/Transformer/transformer1.mp3")
transform_sound2 = pygame.mixer.Sound("./sounds/Transformer/transformer2.mp3")
laser_shoot_sound = pygame.mixer.Sound("./sounds/Transformer/LaserShoot.wav")  # 擎天柱发射激光的声音

# 加载背景音乐
pygame.mixer.music.load("./sounds/background_music3.mp3")
pygame.mixer.music.play(-1)  # 循环播放背景音乐

# 加载爆炸图像
explosion_image = pygame.image.load("./images/explosion.gif")
explosion_image = pygame.transform.scale(explosion_image, (60, 60))

# 玩家飞机
player = pygame.Rect(370, 500, 60, 60)
player_speed = 5

# 全局变量声明
missile_count = 10
missiles = []
enemies = []
enemy_bullets = []
bullets = []
score = 0
lives = 3

# 字体路径根据操作系统进行选择
if sys.platform.startswith("darwin"):  # MacOS
    font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
elif sys.platform.startswith("win"):  # Windows
    font_path = "C:/Windows/Fonts/simhei.ttf"  # 例如，使用SimHei字体
else:
    font_path = None  # 其他系统不指定字体路径

# 字体设置
if font_path:
    font = pygame.font.Font(font_path, 26)
    small_font = pygame.font.Font(font_path, 18)  # 调整后的较小字体
else:
    font = pygame.font.SysFont(None, 26)  # 如果未指定字体路径，则使用默认字体
    small_font = pygame.font.SysFont(None, 18)  # 调整后的较小字体

# 游戏时间
game_time = 60  # 游戏时间改为60秒
start_ticks = pygame.time.get_ticks()  # 游戏开始时间

# 星星
stars = [pygame.Rect(random.randint(0, width-2), random.randint(0, height-2), 2, 2) for _ in range(100)]

# 历史最高分文件路径
high_scores_file = "high_scores.txt"

# 读取历史最高分记录
def load_high_scores():
    if os.path.exists(high_scores_file):
        with open(high_scores_file, "r") as file:
            scores = [int(line.strip()) for line in file.readlines()]
            return scores
    return []

# 保存历史最高分记录
def save_high_scores(scores):
    with open(high_scores_file, "w") as file:
        for score in scores:
            file.write(f"{score}\n")

# 更新历史最高分记录
def update_high_scores(new_score):
    scores = load_high_scores()
    scores.append(new_score)
    scores = sorted(set(scores), reverse=True)[:5]  # 只保留前5名，且重复的只显示一条
    save_high_scores(scores)
    return scores

def reset_game():
    global player, missiles, enemies, enemy_bullets, bullets, missile_count, start_ticks, lives, score
    player = pygame.Rect(370, 500, 60, 60)
    missiles = []
    enemies = []
    enemy_bullets = []
    bullets = []
    missile_count = 10
    start_ticks = pygame.time.get_ticks()
    lives = 3
    score = 0

def main_game():
    global lives, score, start_ticks, missile_count, running
    running = True
    clock = pygame.time.Clock()

    while running:
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000  # 计算已过去的时间
        time_left = max(0, game_time - int(seconds))  # 剩余时间

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # 玩家子弹发射两列
                    bullets.append(pygame.Rect(player.left + 10, player.top, 6, 15))
                    bullets.append(pygame.Rect(player.right - 16, player.top, 6, 15))
                    shoot_sound.play()
                if event.key == pygame.K_m and missile_count > 0:
                    missiles.append(pygame.Rect(player.centerx - 5, player.top, 10, 20))  # 玩家导弹
                    missile_count -= 1
                    missile_sound.play()

        # 移动玩家飞机
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.left > 0:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.right < width:
            player.x += player_speed

        # 生成敌机
        if random.randint(1, 60) == 1:
            if random.randint(1, 5) == 1:  # 20% 概率生成擎天柱
                if random.choice([True, False]):  # 随机选择擎天柱的形态
                    enemies.append({"rect": pygame.Rect(random.randint(0, width-60), 0, 60, 60),
                                    "type": "optimus_prime1",  # 擎天柱形态1
                                    "image": optimus_prime1,
                                    "health": 2,
                                    "switch_time": random.randint(3, 6),  # 随机切换时间
                                    "last_shot_time": time.time()})  # 记录上次射击时间
                    random.choice([transform_sound1, transform_sound2]).play()
                else:
                    enemies.append({"rect": pygame.Rect(random.randint(0, width-60), 0, 60, 60),
                                    "type": "optimus_prime2",  # 擎天柱形态2
                                    "image": optimus_prime2,
                                    "health": 2,
                                    "switch_time": random.randint(3, 6),  # 随机切换时间
                                    "last_shot_time": time.time()})  # 记录上次射击时间
                    random.choice([transform_sound1, transform_sound2]).play()
            else:
                enemies.append({"rect": pygame.Rect(random.randint(0, width-60), 0, 60, 60),
                                "type": "regular",
                                "image": enemy_image})

        # 处理擎天柱随机切换形态
        for enemy in enemies:
            if enemy["type"].startswith("optimus_prime"):
                enemy["switch_time"] -= 1 / 60  # 更新倒计时时间
                if enemy["switch_time"] <= 0:
                    if enemy["type"] == "optimus_prime1":
                        enemy["type"] = "optimus_prime2"
                        enemy["image"] = optimus_prime2
                    else:
                        enemy["type"] = "optimus_prime1"
                        enemy["image"] = optimus_prime1
                    enemy["switch_time"] = random.randint(3, 6)  # 重置切换时间
                    random.choice([transform_sound1, transform_sound2]).play()

        # 敌机随机发射子弹
        for enemy in enemies:
            if enemy["type"] == "optimus_prime1":
                # 擎天柱形态1发射子弹，每秒一次
                current_time = time.time()
                if current_time - enemy["last_shot_time"] >= 1:  # 每1秒发射一次
                    enemy_bullets.append(pygame.Rect(enemy["rect"].left + 10, enemy["rect"].bottom, 6, 20))  # 威力大一些
                    enemy_bullets.append(pygame.Rect(enemy["rect"].right - 10, enemy["rect"].bottom, 6, 20))  # 子弹略粗
                    laser_shoot_sound.play()  # 播放发射子弹的声音
                    enemy["last_shot_time"] = current_time
            elif enemy["type"] == "regular":
                # 普通敌机的子弹
                if random.randint(1, 100) == 1:
                    enemy_bullets.append(pygame.Rect(enemy["rect"].left + 10, enemy["rect"].bottom, 6, 15))
                    enemy_bullets.append(pygame.Rect(enemy["rect"].right - 16, enemy["rect"].bottom, 6, 15))

        # 移动敌机
        for enemy in enemies[:]:
            enemy["rect"].y += 2
            if enemy["rect"].top > height:
                enemies.remove(enemy)

        # 移动敌机子弹
        for bullet in enemy_bullets[:]:
            bullet.y += 5
            if bullet.top > height:
                enemy_bullets.remove(bullet)

        # 移动玩家子弹
        for bullet in bullets[:]:
            bullet.y -= 7
            if bullet.bottom < 0:
                bullets.remove(bullet)

        # 移动玩家导弹
        for missile in missiles[:]:
            missile.y -= 10
            if missile.bottom < 0:
                missiles.remove(missile)

        # 检测碰撞
        collision_occurred = False
        for enemy in enemies[:]:
            if player.colliderect(enemy["rect"]):
                collision_sound.play()
                if enemy["type"].startswith("optimus_prime"):
                    enemy["health"] -= 1
                    if enemy["health"] <= 0:
                        enemies.remove(enemy)
                        explosion_sound.play()
                        screen.blit(explosion_image, enemy["rect"].topleft)  # 在敌机位置显示爆炸图片
                        pygame.display.update()
                else:
                    enemies.remove(enemy)
                    explosion_sound.play()
                    screen.blit(explosion_image, enemy["rect"].topleft)  # 在敌机位置显示爆炸图片
                    pygame.display.update()
                lives -= 1
                collision_occurred = True
                break
            for bullet in bullets[:]:
                if bullet.colliderect(enemy["rect"]):
                    if enemy["type"].startswith("optimus_prime"):
                        enemy["health"] -= 1
                        if enemy["health"] <= 0:
                            enemies.remove(enemy)
                            explosion_sound.play()
                            screen.blit(explosion_image, enemy["rect"].topleft)  # 在敌机位置显示爆炸图片
                            pygame.display.update()
                    else:
                        enemies.remove(enemy)
                        bullets.remove(bullet)
                        score += 10
                        explosion_sound.play()
                        screen.blit(explosion_image, enemy["rect"].topleft)  # 在敌机位置显示爆炸图片
                        pygame.display.update()
                    break
            for missile in missiles[:]:
                if missile.colliderect(enemy["rect"]):
                    if enemy["type"].startswith("optimus_prime"):
                        enemy["health"] -= 1  # 导弹对擎天柱造成较大伤害
                        if enemy["health"] <= 0:
                            enemies.remove(enemy)
                            explosion_sound.play()
                            screen.blit(explosion_image, enemy["rect"].topleft)  # 在敌机位置显示爆炸图片
                            pygame.display.update()
                    else:
                        enemies.remove(enemy)
                        missiles.remove(missile)
                        score += 20
                        explosion_sound.play()
                        screen.blit(explosion_image, enemy["rect"].topleft)  # 在敌机位置显示爆炸图片
                        pygame.display.update()
                    break

        # 检测玩家是否被敌机子弹击中
        for bullet in enemy_bullets[:]:
            if player.colliderect(bullet):
                collision_sound.play()
                enemy_bullets.remove(bullet)
                lives -= 1
                collision_occurred = True

        # 如果发生碰撞，暂停3秒并倒计时
        if collision_occurred:
            if lives > 0:
                for i in range(3, 0, -1):
                    screen.fill(BLACK)
                    countdown_text = font.render(f"游戏恢复中: {i}", True, WHITE)
                    screen.blit(countdown_text, (width // 2 - 60, height // 2))
                    pygame.display.flip()
                    time.sleep(1)
            else:
                running = False

        # 绘制游戏画面
        screen.fill(BLACK)
        for star in stars:
            pygame.draw.rect(screen, WHITE, star)
        screen.blit(player_image, player.topleft)
        for enemy in enemies:
            screen.blit(enemy["image"], enemy["rect"].topleft)
        for bullet in bullets:
            pygame.draw.rect(screen, RED, bullet)
        for missile in missiles:
            pygame.draw.rect(screen, GREEN, missile)
        for bullet in enemy_bullets:
            pygame.draw.rect(screen, GREEN, bullet)  # 敌机子弹为绿色

        # 显示积分
        score_text = font.render(f"得分: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # 显示剩余导弹数
        missile_text = font.render(f"导弹: {missile_count}", True, WHITE)
        screen.blit(missile_text, (10, 50))

        # 显示剩余生命
        lives_text = font.render(f"生命: {lives}", True, WHITE)
        screen.blit(lives_text, (10, 90))

        # 显示倒计时
        timer_text = font.render(f"时间: {time_left}秒", True, WHITE)
        screen.blit(timer_text, (width - 200, 10))

        # 显示版本号和开发者信息
        version_text = small_font.render(f"版本: {GAME_VERSION}", True, WHITE)
        author_text = small_font.render(AUTHOR_NAME, True, WHITE)
        screen.blit(version_text, (width - 220, height - 40))
        screen.blit(author_text, (width - 220, height - 70))

        pygame.display.flip()

        # 检查游戏结束条件
        if lives <= 0 or time_left <= 0:
            running = False

        clock.tick(60)

    # 更新历史最高分
    high_scores = update_high_scores(score)

    # 游戏结束，显示最终得分和最高分榜单
    game_over_screen(score, high_scores)

def game_over_screen(final_score, high_scores):
    global running
    running = True
    while running:
        screen.fill(BLACK)
        game_over_text = font.render("游戏结束", True, WHITE)
        final_score_text = font.render(f"最终得分: {final_score}", True, WHITE)
        screen.blit(game_over_text, (width // 2 - 60, height // 2 - 50))
        screen.blit(final_score_text, (width // 2 - 100, height // 2))

        high_scores_text = font.render("最高分排行榜:", True, WHITE)
        screen.blit(high_scores_text, (width // 2 - 100, height // 2 + 50))
        for i, score in enumerate(high_scores):
            score_text = font.render(f"{i + 1}. {score}", True, WHITE)
            screen.blit(score_text, (width // 2 - 50, height // 2 + 100 + i * 30))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                running = False
                pygame.mixer.music.stop()
                # 返回到游戏开始界面
                import game_start_screen  # 导入游戏开始画面模块并重新启动
                game_start_screen.main_menu()

reset_game()
main_game()

import pygame
import random
import time
import game_end_screen
import game_resources
import game_start_screen
import play_time  # 导入每日游戏时间管理
import game_pause  # 导入暂停功能
import game_explosion  # 导入爆炸模块
from datetime import datetime

# 游戏版本号
GAME_VERSION = "V3.8"
AUTHOR_NAME = "游戏作者: 大伟说AI"

def main_game(screen, width, height, font, small_font, medium_font, large_font, sounds, images, player, player_speed_factor, missile_count, missiles, enemies, enemy_bullets, bullets, score, lives, stars, game_time):
    start_ticks = pygame.time.get_ticks()  # 游戏开始时间
    played_time = play_time.read_played_time()  # 获取今天已玩时间
    remaining_time = play_time.max_daily_time - played_time  # 计算剩余时间
    last_shot_time = 0  # 初始化上次发射子弹的时间
    last_save_time = time.time()  # 初始化上次保存游戏时长的时间

    # 初始化玩家目标位置
    player_target_x = player.x  
    player_target_y = player.y  

    if remaining_time <= 0:
        # 今日游戏时间已满，显示提示并退出
        screen.fill(pygame.Color("black"))
        alert_text = large_font.render("今日游戏时间已满，请明日再来！", True, pygame.Color("red"))
        screen.blit(alert_text, (width // 2 - alert_text.get_width() // 2, height // 2))
        pygame.display.flip()
        time.sleep(3)  # 显示3秒钟的提示
        return

    clock = pygame.time.Clock()
    running = True
    start_time = time.time()  # 记录游戏开始时间

    # 在游戏开始时加载爆炸帧
    explosion_frames = game_explosion.load_explosion_frames()
    active_explosions = []  # 用于跟踪当前活动的爆炸动画 [(x, y, start_time)]

    while running:
        current_time = time.time()
        elapsed_time = current_time - start_time  # 计算游戏已玩的时间
        total_played_time = played_time + int(elapsed_time)  # 总已玩时间
        remaining_time = max(0, play_time.max_daily_time - total_played_time)  # 计算剩余时间

        # 每隔30秒保存游戏时长到本地文件
        if current_time - last_save_time >= 30:
            play_time.save_played_time(total_played_time)
            last_save_time = current_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return  # 退出游戏

            # 检查鼠标左键按下
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                bullets.append(pygame.Rect(player.left + 10, player.top, 6, 15))
                bullets.append(pygame.Rect(player.right - 16, player.top, 6, 15))
                sounds["shoot"].play()

            # 检查鼠标移动，更新目标位置
            if event.type == pygame.MOUSEMOTION:
                player_target_x = event.pos[0] - player.width // 2
                player_target_y = event.pos[1] - player.height // 2

        # 检查按键
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if current_time - last_shot_time >= 0.2:  # 子弹发射间隔为0.2秒
                bullets.append(pygame.Rect(player.left + 10, player.top, 6, 15))
                bullets.append(pygame.Rect(player.right - 16, player.top, 6, 15))
                sounds["shoot"].play()
                last_shot_time = current_time  # 更新上次发射子弹的时间

        if keys[pygame.K_m] and missile_count > 0:
            missiles.append(pygame.Rect(player.centerx - 5, player.top, 10, 20))  # 玩家导弹
            missile_count -= 1
            sounds["missile"].play()

        if keys[pygame.K_ESCAPE]:
            game_pause.pause_game(screen, medium_font, width, height)  # 暂停游戏

        # 移动战机到鼠标或键盘目标位置
        if keys[pygame.K_LEFT] and player.left > 0:
            player_target_x = player.x - player_speed_factor
        if keys[pygame.K_RIGHT] and player.right < width:
            player_target_x = player.x + player_speed_factor
        if keys[pygame.K_UP] and player.top > 0:
            player_target_y = player.y - player_speed_factor
        if keys[pygame.K_DOWN] and player.bottom < height:
            player_target_y = player.y + player_speed_factor

        # 平滑移动战机
        if player.x < player_target_x:
            player.x += min(player_speed_factor, player_target_x - player.x)
        elif player.x > player_target_x:
            player.x -= min(player_speed_factor, player.x - player_target_x)

        if player.y < player_target_y:
            player.y += min(player_speed_factor, player_target_y - player.y)
        elif player.y > player_target_y:
            player.y -= min(player_speed_factor, player.y - player_target_y)

        # 限制战机不能超出屏幕边界
        if player.x < 0:
            player.x = 0
        if player.x > width - player.width:
            player.x = width - player.width
        if player.y < 0:
            player.y = 0
        if player.y > height - player.height:
            player.y = height - player.height

        # 生成敌机
        if random.randint(1, 60) == 1:
            if random.randint(1, 10) == 1:  # 10% 概率生成擎天柱
                if random.choice([True, False]):  # 随机选择擎天柱的形态
                    enemies.append({
                        "rect": pygame.Rect(random.randint(0, width - 60), 0, 60, 60),
                        "type": "optimus_prime1",
                        "image": images["optimus_prime1"],
                        "health": 2,
                        "switch_time": random.randint(3, 6),  # 随机切换时间
                        "last_shot_time": time.time(),
                        "horizontal_speed": random.choice([-2, 2])  # 随机设置左右移动速度
                    })
                else:
                    enemies.append({
                        "rect": pygame.Rect(random.randint(0, width - 60), 0, 60, 60),
                        "type": "optimus_prime2",
                        "image": images["optimus_prime2"],
                        "health": 2,
                        "switch_time": random.randint(3, 6),
                        "last_shot_time": time.time(),
                        "horizontal_speed": random.choice([-2, 2])  # 随机设置左右移动速度
                    })
            else:
                enemies.append({
                    "rect": pygame.Rect(random.randint(0, width - 60), 0, 60, 60),
                    "type": "regular",
                    "image": images["enemy"],
                    "horizontal_speed": random.choice([-2, 2])  # 常规敌机左右移动速度
                })

        # 处理擎天柱随机切换形态
        for enemy in enemies:
            if enemy["type"].startswith("optimus_prime"):
                enemy["switch_time"] -= 1 / 60  # 更新倒计时时间
                if enemy["switch_time"] <= 0:
                    if enemy["type"] == "optimus_prime1":
                        enemy["type"] = "optimus_prime2"
                        enemy["image"] = images["optimus_prime2"]
                    else:
                        enemy["type"] = "optimus_prime1"
                        enemy["image"] = images["optimus_prime1"]
                    enemy["switch_time"] = random.randint(3, 6)  # 重置切换时间
                    random.choice([sounds["transform1"], sounds["transform2"]]).play()

        # 敌机随机发射子弹
        for enemy in enemies:
            if enemy["type"] == "optimus_prime1":
                if current_time - enemy["last_shot_time"] >= 1:  # 每1秒发射一次
                    enemy_bullets.append(pygame.Rect(enemy["rect"].left + 10, enemy["rect"].bottom, 6, 20))
                    enemy_bullets.append(pygame.Rect(enemy["rect"].right - 10, enemy["rect"].bottom, 6, 20))
                    sounds["laser_shoot"].play()  # 播放发射子弹的声音
                    enemy["last_shot_time"] = current_time
            elif enemy["type"] == "regular":
                if random.randint(1, 100) == 1:
                    enemy_bullets.append(pygame.Rect(enemy["rect"].left + 10, enemy["rect"].bottom, 6, 15))
                    enemy_bullets.append(pygame.Rect(enemy["rect"].right - 16, enemy["rect"].bottom, 6, 15))

        # 移动敌机（新增左右移动）
        for enemy in enemies[:]:
            enemy["rect"].y += 2
            enemy["rect"].x += enemy["horizontal_speed"]  # 水平移动

            # 如果敌机碰到屏幕边缘，则反向水平速度
            if enemy["rect"].left <= 0 or enemy["rect"].right >= width:
                enemy["horizontal_speed"] *= -1  # 反转移动方向

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
                active_explosions.append((enemy["rect"].x, enemy["rect"].y, pygame.time.get_ticks() / 1000))  # 记录爆炸位置和开始时间
                sounds["collision"].play()
                if enemy["type"].startswith("optimus_prime"):
                    enemy["health"] -= 1
                    if enemy["health"] <= 0:
                        enemies.remove(enemy)
                        sounds["explosion"].play()
                else:
                    enemies.remove(enemy)
                    sounds["explosion"].play()
                lives -= 1
                collision_occurred = True
                break
            for bullet in bullets[:]:
                if bullet.colliderect(enemy["rect"]):
                    active_explosions.append((enemy["rect"].x, enemy["rect"].y, pygame.time.get_ticks() / 1000))  # 记录爆炸位置和开始时间
                    if enemy["type"].startswith("optimus_prime"):
                        enemy["health"] -= 1
                        if enemy["health"] <= 0:
                            enemies.remove(enemy)
                            sounds["explosion"].play()
                    else:
                        enemies.remove(enemy)
                        bullets.remove(bullet)
                        score += 10
                        sounds["explosion"].play()
                    break
            for missile in missiles[:]:
                if missile.colliderect(enemy["rect"]):
                    active_explosions.append((enemy["rect"].x, enemy["rect"].y, pygame.time.get_ticks() / 1000))  # 记录爆炸位置和开始时间
                    if enemy["type"].startswith("optimus_prime"):
                        enemy["health"] -= 1  # 导弹对擎天柱造成较大伤害
                        if enemy["health"] <= 0:
                            enemies.remove(enemy)
                            sounds["explosion"].play()
                    else:
                        enemies.remove(enemy)
                        missiles.remove(missile)
                        score += 20
                        sounds["explosion"].play()
                    break

        # 检测玩家是否被敌机子弹击中
        for bullet in enemy_bullets[:]:
            if player.colliderect(bullet):
                sounds["collision"].play()
                enemy_bullets.remove(bullet)
                lives -= 1
                collision_occurred = True

        # 如果发生碰撞，暂停3秒并倒计时
        if collision_occurred:
            if lives > 0:
                for i in range(3, 0, -1):
                    screen.fill(pygame.Color("black"))
                    recovery_text = medium_font.render("游戏恢复中", True, pygame.Color("white"))
                    screen.blit(recovery_text, (width // 2 - recovery_text.get_width() // 2, height // 2 - 100))
                    countdown_text = large_font.render(str(i), True, pygame.Color("red"))
                    screen.blit(countdown_text, (width // 2 - countdown_text.get_width() // 2, height // 2))
                    pygame.display.flip()
                    time.sleep(1)
            else:
                running = False

        # 绘制游戏画面
        screen.fill(pygame.Color("black"))
        for star in stars:
            pygame.draw.rect(screen, pygame.Color("white"), star)
        screen.blit(images["player"], player.topleft)

        for enemy in enemies:
            screen.blit(enemy["image"], enemy["rect"].topleft)
        for bullet in bullets:
            pygame.draw.rect(screen, pygame.Color("red"), bullet)
        for missile in missiles:
            pygame.draw.rect(screen, pygame.Color("green"), missile)
        for bullet in enemy_bullets:
            pygame.draw.rect(screen, pygame.Color("green"), bullet)  # 敌机子弹为绿色

        # 显示积分
        score_text = font.render(f"得分: {score}", True, pygame.Color("white"))
        screen.blit(score_text, (10, 10))

        # 显示剩余导弹数
        missile_text = font.render(f"导弹: {missile_count}", True, pygame.Color("white"))
        screen.blit(missile_text, (10, 50))

        # 显示剩余生命
        lives_text = font.render(f"生命: {lives}", True, pygame.Color("white"))
        screen.blit(lives_text, (10, 90))

        # 显示今日已玩时间和剩余时间，右上角
        played_time_text = small_font.render(f"今日已玩时间: {total_played_time // 60}分{total_played_time % 60}秒", True, pygame.Color("white"))
        remaining_time_text = small_font.render(f"今日剩余时间: {remaining_time // 60}分{remaining_time % 60}秒", True, pygame.Color("white"))
        screen.blit(played_time_text, (width - 220, 10))
        screen.blit(remaining_time_text, (width - 220, 40))

        # 显示版本号和开发者信息
        version_text = small_font.render(f"版本: {GAME_VERSION}", True, pygame.Color("white"))
        author_text = small_font.render(AUTHOR_NAME, True, pygame.Color("white"))
        screen.blit(version_text, (width - 220, height - 40))
        screen.blit(author_text, (width - 220, height - 70))

        # 播放爆炸动画
        for explosion in active_explosions[:]:
            if game_explosion.play_explosion(screen, explosion[0], explosion[1], explosion_frames, explosion[2]):
                active_explosions.remove(explosion)  # 移除已完成的爆炸

        pygame.display.flip()

        # 检查游戏结束条件
        if lives <= 0 or remaining_time <= 0:
            running = False
            if remaining_time <= 0:
                screen.fill(pygame.Color("black"))
                alert_text = large_font.render("今日游戏时间已满，请明日再来！", True, pygame.Color("red"))
                screen.blit(alert_text, (width // 2 - alert_text.get_width() // 2, height // 2))
                pygame.display.flip()
                time.sleep(3)  # 显示3秒钟的提示

        clock.tick(60)

    # 保存已玩时间
    play_time.save_played_time(total_played_time)

    # 更新历史最高分
    high_scores = game_resources.update_high_scores(score)

    # 游戏结束，调用游戏结束画面模块
    game_end_screen.game_over_screen(score, high_scores)

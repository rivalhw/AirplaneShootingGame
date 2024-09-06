import pygame
import os

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

# 加载所有图片资源
def load_images():
    player_image = pygame.image.load("./images/player_fighter.png")
    player_image = pygame.transform.scale(player_image, (60, 60))

    enemy_image = pygame.image.load("./images/enemy_fighter.png")
    enemy_image = pygame.transform.scale(enemy_image, (60, 60))

    optimus_prime1 = pygame.image.load("./images/Transformers/optimus_prime1.png")
    optimus_prime1 = pygame.transform.scale(optimus_prime1, (60, 60))

    optimus_prime2 = pygame.image.load("./images/Transformers/optimus_prime2.png")
    optimus_prime2 = pygame.transform.scale(optimus_prime2, (60, 60))

    explosion_image = pygame.image.load("./images/explosion.gif")
    explosion_image = pygame.transform.scale(explosion_image, (60, 60))

    return {
        "player": player_image,
        "enemy": enemy_image,
        "optimus_prime1": optimus_prime1,
        "optimus_prime2": optimus_prime2,
        "explosion": explosion_image,
    }

# 加载所有音效资源
def load_sounds():
    shoot_sound = pygame.mixer.Sound("./sounds/shoot.wav")
    explosion_sound = pygame.mixer.Sound("./sounds/explosion.wav")
    collision_sound = pygame.mixer.Sound("./sounds/Transformer/itwillreturn.mp3")
    missile_sound = pygame.mixer.Sound("./sounds/missile.mp3")
    transform_sound1 = pygame.mixer.Sound("./sounds/Transformer/transformer1.mp3")
    transform_sound2 = pygame.mixer.Sound("./sounds/Transformer/transformer2.mp3")
    laser_shoot_sound = pygame.mixer.Sound("./sounds/Transformer/LaserShoot.wav")

    return {
        "shoot": shoot_sound,
        "explosion": explosion_sound,
        "collision": collision_sound,
        "missile": missile_sound,
        "transform1": transform_sound1,
        "transform2": transform_sound2,
        "laser_shoot": laser_shoot_sound,
    }

# 加载背景音乐
def load_background_music():
    pygame.mixer.music.load("./sounds/background_music3.mp3")
    pygame.mixer.music.play(-1)  # 循环播放背景音乐

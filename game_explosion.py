import pygame

# 提前加载爆炸帧
def load_explosion_frames():
    frames = []
    for i in range(1, 97):  # 假设爆炸帧从1到96
        frame = pygame.image.load(f'./images/explosion/explosion_frame_{i}.png').convert_alpha()
        frame = pygame.transform.scale(frame, (120, 120))  # 调整爆炸帧的大小，效果更震撼
        frames.append(frame)
    return frames

# 播放爆炸动画
def play_explosion(screen, x, y, explosion_frames, start_time, frame_duration=0.05):
    current_time = pygame.time.get_ticks() / 1000
    elapsed_time = current_time - start_time
    frame_index = int(elapsed_time // frame_duration)
    if frame_index < len(explosion_frames):
        screen.blit(explosion_frames[frame_index], (x - 60, y - 60))  # 居中绘制爆炸效果
        return False
    return True

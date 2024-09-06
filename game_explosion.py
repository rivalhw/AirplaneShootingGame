import pygame

# 提前加载爆炸帧
def load_explosion_frames():
    frames = []
    for i in range(1, 98):  # 假设爆炸帧从 1 到 97
        frame = pygame.image.load(f'./images/explosion/explosion_frame_{i}.png').convert_alpha()
        frames.append(frame)
    return frames

# 播放爆炸动画
def play_explosion(screen, x, y, explosion_frames, start_time, frame_duration=0.05):
    # 计算爆炸应该显示的帧数
    current_time = pygame.time.get_ticks() / 1000  # 当前时间，单位秒
    elapsed_time = current_time - start_time  # 爆炸已经持续的时间
    frame_index = int(elapsed_time // frame_duration)  # 根据已过时间确定当前帧
    if frame_index < len(explosion_frames):  # 如果还没播放完所有帧
        screen.blit(explosion_frames[frame_index], (x, y))  # 绘制当前帧
        return False  # 返回 False，表示爆炸未完成
    return True  # 返回 True，表示爆炸已完成

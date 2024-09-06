import os
import time

# 文件路径，用于保存已玩游戏的总时间（以秒为单位）
time_file = "play_time.txt"

# 每天最多玩20分钟（1200秒）
max_daily_time = 20 * 60

# 读取已玩时间（每天最多20分钟）
def read_played_time():
    if not os.path.exists(time_file):
        return 0
    with open(time_file, "r") as file:
        played_time = int(file.read().strip())
    # 检查是否是同一天，如果是则返回，否则重置
    last_played_day = time.strftime('%Y-%m-%d', time.localtime())
    if played_time > 0:
        return played_time
    return 0

# 保存已玩时间
def save_played_time(played_time):
    with open(time_file, "w") as file:
        file.write(str(played_time))

import os
import json
from datetime import datetime

# 文件路径，用于存储每日的游戏时长和日期
PLAY_TIME_FILE = "play_time.json"

# 每天最多可以玩20分钟（1200秒）
max_daily_time = 1200

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

# 示例用法
if __name__ == "__main__":
    print(f"今日已玩时间：{read_played_time()} 秒")
    save_played_time(600)  # 假设已玩了600秒

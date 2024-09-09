from PIL import Image
import os

def gif_to_png_folder(gif_path, output_folder):
    # 打开 GIF 文件
    gif = Image.open(gif_path)

    # 如果输出文件夹不存在，创建文件夹
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 获取 GIF 的帧数
    frame_count = gif.n_frames

    # 遍历每一帧并保存为 PNG 文件
    for frame in range(frame_count):
        gif.seek(frame)  # 切换到当前帧
        frame_image = gif.copy()  # 复制当前帧
        # 构建保存路径
        png_filename = os.path.join(output_folder, f"frame_{frame + 1}.png")
        frame_image.save(png_filename, 'PNG')  # 保存为 PNG 格式

    print(f"GIF 文件已成功转换为 {frame_count} 张 PNG 图片并保存在 {output_folder} 文件夹下")

if __name__ == "__main__":
    # 用户输入 GIF 文件的具体路径和文件名
    gif_path = input("请输入要转换的 .gif 文件的完整路径和名称: ")

    # 用户输入输出文件夹名称
    output_folder = input("请输入保存 .png 文件的输出文件夹路径: ")

    # 调用函数进行转换
    gif_to_png_folder(gif_path, output_folder)

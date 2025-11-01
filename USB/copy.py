import os
import shutil
import win32file
import win32con
import time
import tkinter as tk
from tkinter import messagebox
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
import threading
import queue

# 定义要搜索的文件名中的字符串和目标文件夹
TARGET_STRING = "课课练"
DOWNLOADS_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads")

# 定义U盘的盘符
USB_DRIVE_LETTERS = []

# 创建一个简单的图标
def create_image(width, height, color1, color2):
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 2, 0, width, height // 2),
        fill=color2)
    dc.rectangle(
        (0, height // 2, width // 2, height),
        fill=color2)
    return image

# 检测U盘
def detect_usb_drive():
    drive_list = []
    drivebits = win32file.GetLogicalDrives()
    for d in range(1, 26):
        mask = 1 << d
        if drivebits & mask:
            drive_letter = chr(ord('A') + d) + ":"
            drive_type = win32file.GetDriveType(drive_letter)
            if drive_type == win32file.DRIVE_REMOVABLE:
                drive_list.append(drive_letter)
    return drive_list

# 搜索并复制文件
def search_and_copy_file(drive_letter):
    for root, dirs, files in os.walk(drive_letter):
        for file in files:
            if TARGET_STRING in file:
                file_path = os.path.join(root, file)
                target_path = os.path.join(DOWNLOADS_FOLDER, file)
                try:
                    shutil.copy2(file_path, target_path)
                    print(f"文件 {file} 已复制到 {target_path}")
                except Exception as e:
                    print(f"复制文件时出错: {e}")

# 主函数
def main():
    global USB_DRIVE_LETTERS
    while True:
        current_drives = detect_usb_drive()
        new_drives = [d for d in current_drives if d not in USB_DRIVE_LETTERS]
        
        for drive in new_drives:
            print(f"检测到新的U盘插入: {drive}")
            search_and_copy_file(drive)
        
        USB_DRIVE_LETTERS = current_drives
        time.sleep(1)  # 每1秒检查一次

# 创建GUI类
class USBFileCopierApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.message_queue = queue.Queue()
        
        # 定期检查消息队列
        self.check_queue()
    
    def check_queue(self):
        """定期检查消息队列"""
        try:
            while True:
                # 非阻塞获取消息
                message_type = self.message_queue.get_nowait()
                if message_type == "show_info":
                    self.show_message_dialog()
        except queue.Empty:
            pass
        # 每100毫秒检查一次队列
        self.root.after(100, self.check_queue)
    
    def show_message_dialog(self):
        """显示消息对话框"""
        messagebox.showinfo("信息", "果园编程工作室-制作\n\nUSB文件复制器。\n\n这个程序有安全风险：它会在用户不知情的情况下复制文件，可能被用于未经授权的文件获取，在企业环境中可能违反安全政策")
    
    def request_show_message(self):
        """请求显示消息（线程安全）"""
        self.message_queue.put("show_info")
    
    def quit_app(self):
        """退出应用程序"""
        self.root.quit()
        self.root.destroy()
    
    def run(self):
        """运行应用程序"""
        self.root.mainloop()

def create_gui():
    # 创建应用程序实例
    app = USBFileCopierApp()
    
    def show_message(icon, item):
        # 通过队列请求显示消息
        app.request_show_message()
    
    def quit_program(icon, item):
        print("正在退出程序...")
        icon.stop()
        app.quit_app()
    
    # 创建菜单
    menu = Menu(
        MenuItem('显示信息', show_message),
        MenuItem('退出', quit_program)
    )
    
    # 创建系统托盘图标
    icon = Icon(
        "usb_file_copier",
        create_image(64, 64, 'blue', 'white'),
        "USB文件复制器",
        menu
    )
    
    # 设置窗口关闭事件
    app.root.protocol('WM_DELETE_WINDOW', lambda: quit_program(icon, None))
    
    print("系统托盘图标已启动")
    
    # 在单独的线程中运行系统托盘图标
    def run_icon():
        icon.run()
        # 当图标停止时，退出应用程序
        app.quit_app()
    
    icon_thread = threading.Thread(target=run_icon, daemon=True)
    icon_thread.start()
    
    # 运行Tkinter主循环
    app.run()

if __name__ == "__main__":
    # 启动后台监控线程
    monitor_thread = threading.Thread(target=main, daemon=True)
    monitor_thread.start()
    
    print("日志文件：正常运行时看不到")
    print("USB文件复制器已启动...")
    print("程序在系统托盘中运行，右键点击图标可查看菜单")
    print("正在监控U盘插入...")
    
    create_gui()
    print("程序已退出")
import os
import shutil
import win32file
import win32con
import time
import tkinter as tk
from tkinter import messagebox
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw

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
                shutil.copy2(file_path, target_path)
                print(f"文件 {file} 已复制到 {target_path}")

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
        time.sleep(5)  # 每5秒检查一次

# 创建GUI
def create_gui():
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口

    def show_message():
        messagebox.showinfo("信息", "程序正在运行")

    def quit_program():
        icon.stop()
        root.destroy()

    menu = (MenuItem('显示信息', show_message), MenuItem('退出', quit_program))
    icon = Icon("name", create_image(64, 64, 'black', 'white'), "USB File Copier", menu)
    icon.run()

if __name__ == "__main__":
    import threading
    threading.Thread(target=main, daemon=True).start()
    create_gui()
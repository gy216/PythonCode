# 做一个类似360安全卫士的清理工具，清理电脑中垃圾，缓存等，原理是删除后缀名为.tmp、._mp、.log、.gid、.chk、.old 的文件。有GUI，可以选择全盘扫描或扫描任意一个磁盘
import os
import tkinter as tk
from tkinter import filedialog

def scan_disk():
    disk = filedialog.askdirectory()
    if disk:
        for root, dirs, files in os.walk(disk):
            for file in files:
                if file.endswith(('.tmp', '._mp', '.log', '.gid', '.chk', '.old')):
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
        print("Scan complete.")

root = tk.Tk()
root.title("360同款Q毒，清理")

scan_button = tk.Button(root, text="Scan Disk", command=scan_disk)
scan_button.pack()

root.mainloop()
# 这个程序使用了tkinter库来创建一个简单的GUI界面，用户可以点击按钮来选择要扫描的磁盘，然后程序会删除指定后缀名的文件。
# 注意：这个程序会删除指定后缀名的文件，请谨慎使用。


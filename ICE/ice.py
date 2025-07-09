import tkinter as tk
from tkinter import messagebox
import time

def disable_ice_service():
    if messagebox.askokcancel("确认", "真的要禁用吗？不然我就（嘿嘿）……，算了，破解完成后重启生效"):
        time.sleep(5)  # 等待5秒
        messagebox.showinfo("提示", "没有找到冰点服务")

def disable_control_panel():
    if messagebox.askokcancel("确认", "真的要禁用吗？不然我就（嘿嘿）……，算了，破解完成后重启生效，学校book能发现的!"):
        time.sleep(5)  # 等待5秒
        messagebox.showinfo("提示", "没有获取到集控信息")

# 创建主窗口
root = tk.Tk()
root.title("服务禁用")

# 创建按钮并设置点击事件
btn_ice_service = tk.Button(root, text="禁用冰点服务", command=disable_ice_service)
btn_ice_service.pack(pady=10)

btn_control_panel = tk.Button(root, text="禁用集控后台", command=disable_control_panel)
btn_control_panel.pack(pady=10)

# 启动事件循环
root.mainloop()

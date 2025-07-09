import tkinter as tk
from tkinter import messagebox
import webbrowser
import random
from collections import Counter

# 创建主窗口（低级设置）
root = tk.Tk()
root.title("随机数生成器")

# 标签
start_label = tk.Label(root, text="起始数字:")
max_label = tk.Label(root, text="最大数字:")
result_label = tk.Label(root, text="生成的随机数:")

# 输入框
start_entry = tk.Entry(root)
max_entry = tk.Entry(root)

# 生成随机数的函数
def generate_random_number():
    try:
        start = int(start_entry.get())
        max_num = int(max_entry.get())
        
        if start >= max_num:
            result_label.config(text="起始数字必须小于最大数字")
            return
        
        random_number = random.randint(start, max_num)
        result_label.config(text=f"生成的随机数: {random_number}")
    except ValueError:
        result_label.config(text="请输入有效的整数")

# 按钮
generate_button = tk.Button(root, text="生成随机数", command=generate_random_number)

# 布局
start_label.grid(row=0, column=0, padx=10, pady=10)
start_entry.grid(row=0, column=1, padx=10, pady=10)

max_label.grid(row=1, column=0, padx=10, pady=10)
max_entry.grid(row=1, column=1, padx=10, pady=10)

generate_button.grid(row=2, column=0, columnspan=2, pady=20)

result_label.grid(row=3, column=0, columnspan=2, pady=10)

# 创建高级功能窗口
def open_advanced_settings():
    advanced_window = tk.Toplevel(root)
    advanced_window.title("高级功能")

    # 标签
    advanced_start_label = tk.Label(advanced_window, text="起始数字:")
    advanced_max_label = tk.Label(advanced_window, text="最大数字:")
    advanced_repeat_label = tk.Label(advanced_window, text="重复生成次数:")

    # 输入框
    advanced_start_entry = tk.Entry(advanced_window)
    advanced_max_entry = tk.Entry(advanced_window)
    advanced_repeat_entry = tk.Entry(advanced_window)

    # 结果显示区域
    result_text = tk.Text(advanced_window, wrap=tk.WORD, width=40, height=10)
    result_text.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    # 滚动条
    scrollbar = tk.Scrollbar(advanced_window, command=result_text.yview)
    scrollbar.grid(row=4, column=2, sticky='ns')
    result_text.config(yscrollcommand=scrollbar.set)

    # 出现次数最多的数字显示区域
    most_common_text = tk.Text(advanced_window, wrap=tk.WORD, width=40, height=3)
    most_common_text.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    # 生成随机数的函数
    def generate_multiple_random_numbers():
        try:
            start = int(advanced_start_entry.get())
            max_num = int(advanced_max_entry.get())
            repeat_count = int(advanced_repeat_entry.get())
            
            if start >= max_num:
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, "起始数字必须小于最大数字")
                return
            
            result_text.delete(1.0, tk.END)
            random_numbers = []
            for i in range(repeat_count):
                random_number = random.randint(start, max_num)
                random_numbers.append(random_number)
                result_text.insert(tk.END, f"第 {i+1} 次生成的随机数: {random_number}\n")
            
            # 统计出现次数最多的数字
            counter = Counter(random_numbers)
            most_common_number, most_common_count = counter.most_common(1)[0]
            most_common_text.delete(1.0, tk.END)
            most_common_text.insert(tk.END, f"出现次数最多的数字: {most_common_number} (出现次数: {most_common_count})")
        except ValueError:
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, "请输入有效的整数")

    # 按钮
    advanced_generate_button = tk.Button(advanced_window, text="生成随机数", command=generate_multiple_random_numbers)

    # 布局
    advanced_start_label.grid(row=0, column=0, padx=10, pady=10)
    advanced_start_entry.grid(row=0, column=1, padx=10, pady=10)

    advanced_max_label.grid(row=1, column=0, padx=10, pady=10)
    advanced_max_entry.grid(row=1, column=1, padx=10, pady=10)

    advanced_repeat_label.grid(row=2, column=0, padx=10, pady=10)
    advanced_repeat_entry.grid(row=2, column=1, padx=10, pady=10)

    advanced_generate_button.grid(row=3, column=0, columnspan=2, pady=20)

# 创建开发人员窗口
def open_developer_settings():
    developer_window = tk.Toplevel(root)
    developer_window.title("开发人员设置")

    # 密码输入框
    password_label = tk.Label(developer_window, text="密码:")
    password_entry = tk.Entry(developer_window, show="*")

    # 验证密码的函数
    def verify_password():
        if password_entry.get() == "20110216":
            password_entry.config(state=tk.DISABLED)
            messagebox.showinfo("验证结果", "密码正确")
            open_cheat_mode(developer_window)
        else:
            messagebox.showerror("验证结果", "密码错误")

    # 按钮
    verify_button = tk.Button(developer_window, text="验证", command=verify_password)

    # 布局
    password_label.grid(row=0, column=0, padx=10, pady=10)
    password_entry.grid(row=0, column=1, padx=10, pady=10)
    verify_button.grid(row=1, column=0, columnspan=2, pady=20)

# 打开作弊模式窗口
def open_cheat_mode(parent_window):
    cheat_window = tk.Toplevel(parent_window)
    cheat_window.title("作弊模式")

    # 标签
    low_level_label = tk.Label(cheat_window, text="低级功能作弊模式:")
    high_level_label = tk.Label(cheat_window, text="高级功能作弊模式:")

    # 输入框和下拉框
    low_level_cheat_number_entry = tk.Entry(cheat_window)
    low_level_cheat_probability_var = tk.StringVar(cheat_window)
    low_level_cheat_probability_var.set("10%")
    low_level_cheat_probability_menu = tk.OptionMenu(cheat_window, low_level_cheat_probability_var, "10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%")

    high_level_cheat_number_entry = tk.Entry(cheat_window)
    high_level_cheat_probability_var = tk.StringVar(cheat_window)
    high_level_cheat_probability_var.set("10%")
    high_level_cheat_probability_menu = tk.OptionMenu(cheat_window, high_level_cheat_probability_var, "10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%")

    # 设置作弊模式的函数
    def set_low_level_cheat():
        try:
            cheat_number = int(low_level_cheat_number_entry.get())
            probability = int(low_level_cheat_probability_var.get().strip("%"))
            messagebox.showinfo("作弊模式", f"低级功能的作弊模式已开启，数字 {cheat_number} 的概率为 {probability}%")
            # 更新生成随机数的函数
            generate_random_number_with_cheat(cheat_number, probability)
        except ValueError:
            messagebox.showerror("错误", "请输入有效的整数和概率")

    def set_high_level_cheat():
        try:
            cheat_number = int(high_level_cheat_number_entry.get())
            probability = int(high_level_cheat_probability_var.get().strip("%"))
            messagebox.showinfo("作弊模式", f"高级功能的作弊模式已开启，数字 {cheat_number} 的概率为 {probability}%")
            # 更新生成随机数的函数
            generate_multiple_random_numbers_with_cheat(cheat_number, probability, advanced_generate_button)
        except ValueError:
            messagebox.showerror("错误", "请输入有效的整数和概率")

    # 复原按钮的函数
    def reset_low_level_cheat():
        low_level_cheat_number_entry.delete(0, tk.END)
        low_level_cheat_probability_var.set("10%")
        messagebox.showinfo("复原", "低级功能的作弊设置已复原")
        # 复原生成随机数的函数
        generate_random_number_with_cheat(None, None)

    def reset_high_level_cheat():
        high_level_cheat_number_entry.delete(0, tk.END)
        high_level_cheat_probability_var.set("10%")
        messagebox.showinfo("复原", "高级功能的作弊设置已复原")
        # 复原生成随机数的函数
        generate_multiple_random_numbers_with_cheat(None, None, advanced_generate_button)

    # 按钮
    low_level_cheat_button = tk.Button(cheat_window, text="设置低级功能作弊", command=set_low_level_cheat)
    high_level_cheat_button = tk.Button(cheat_window, text="设置高级功能作弊", command=set_high_level_cheat)
    reset_low_level_button = tk.Button(cheat_window, text="复原低级功能作弊", command=reset_low_level_cheat)
    reset_high_level_button = tk.Button(cheat_window, text="复原高级功能作弊", command=reset_high_level_cheat)

    # 布局
    low_level_label.grid(row=0, column=0, padx=10, pady=10)
    low_level_cheat_number_entry.grid(row=0, column=1, padx=10, pady=10)
    low_level_cheat_probability_menu.grid(row=0, column=2, padx=10, pady=10)
    low_level_cheat_button.grid(row=1, column=0, columnspan=3, pady=10)
    reset_low_level_button.grid(row=2, column=0, columnspan=3, pady=10)

    high_level_label.grid(row=3, column=0, padx=10, pady=10)
    high_level_cheat_number_entry.grid(row=3, column=1, padx=10, pady=10)
    high_level_cheat_probability_menu.grid(row=3, column=2, padx=10, pady=10)
    high_level_cheat_button.grid(row=4, column=0, columnspan=3, pady=10)
    reset_high_level_button.grid(row=5, column=0, columnspan=3, pady=10)

# 更新生成随机数的函数
def generate_random_number_with_cheat(cheat_number, probability):
    def generate_random_number():
        try:
            start = int(start_entry.get())
            max_num = int(max_entry.get())
            
            if start >= max_num:
                result_label.config(text="起始数字必须小于最大数字")
                return
            
            if cheat_number is not None and probability is not None:
                weights = [1] * (max_num - start + 1)
                weights[cheat_number - start] = probability
                random_number = random.choices(range(start, max_num + 1), weights=weights)[0]
            else:
                random_number = random.randint(start, max_num)
            
            result_label.config(text=f"生成的随机数: {random_number}")
        except ValueError:
            result_label.config(text="请输入有效的整数")
    
    generate_button.config(command=generate_random_number)

# 更新生成多个随机数的函数
def generate_multiple_random_numbers_with_cheat(cheat_number, probability, advanced_generate_button):
    def generate_multiple_random_numbers():
        try:
            start = int(advanced_start_entry.get())
            max_num = int(advanced_max_entry.get())
            repeat_count = int(advanced_repeat_entry.get())
            
            if start >= max_num:
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, "起始数字必须小于最大数字")
                return
            
            result_text.delete(1.0, tk.END)
            random_numbers = []
            for i in range(repeat_count):
                if cheat_number is not None and probability is not None:
                    weights = [1] * (max_num - start + 1)
                    weights[cheat_number - start] = probability
                    random_number = random.choices(range(start, max_num + 1), weights=weights)[0]
                else:
                    random_number = random.randint(start, max_num)
                
                random_numbers.append(random_number)
                result_text.insert(tk.END, f"第 {i+1} 次生成的随机数: {random_number}\n")
            
            # 统计出现次数最多的数字
            counter = Counter(random_numbers)
            most_common_number, most_common_count = counter.most_common(1)[0]
            most_common_text.delete(1.0, tk.END)
            most_common_text.insert(tk.END, f"出现次数最多的数字: {most_common_number} (出现次数: {most_common_count})")
        except ValueError:
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, "请输入有效的整数")
    
    advanced_generate_button.config(command=generate_multiple_random_numbers)

# 打开关于窗口
def open_about_window():
    about_window = tk.Toplevel(root)
    about_window.title("关于")

    # 标签
    about_label = tk.Label(about_window, text="果园编程制作")
    about_label.pack(padx=20, pady=20)

    # 按钮
    def open_website():
        webbrowser.open("https://gy216.github.io")

    website_button = tk.Button(about_window, text="访问果园编程", command=open_website)
    website_button.pack(pady=10)

# 创建菜单栏
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# 创建高级功能菜单
advanced_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="高级功能", menu=advanced_menu)

advanced_menu.add_command(label="高级功能", command=open_advanced_settings)

# 创建开发人员菜单
developer_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="开发人员", menu=developer_menu)

developer_menu.add_command(label="开发人员设置", command=open_developer_settings)

# 创建关于菜单
about_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="关于", menu=about_menu)

about_menu.add_command(label="关于", command=open_about_window)

# 运行主循环
root.mainloop()
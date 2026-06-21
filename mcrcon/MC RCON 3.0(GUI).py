import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import re
from mcrcon import MCRcon
import socket

class RCONClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Minecraft RCON 客户端")
        self.root.geometry("900x700")
        
        # 颜色代码映射
        self.color_codes = {
            '0': '#000000',  # 黑色
            '1': '#0000AA',  # 深蓝色
            '2': '#00AA00',  # 深绿色
            '3': '#00AAAA',  # 深青色
            '4': '#AA0000',  # 深红色
            '5': '#AA00AA',  # 紫色
            '6': '#FFAA00',  # 金色
            '7': '#AAAAAA',  # 灰色
            '8': '#555555',  # 深灰色
            '9': '#5555FF',  # 蓝色
            'a': '#55FF55',  # 绿色
            'b': '#55FFFF',  # 青色
            'c': '#FF5555',  # 红色
            'd': '#FF55FF',  # 粉色
            'e': '#FFFF55',  # 黄色
            'f': '#FFFFFF',  # 白色
            'l': '',  # 粗体 (tkinter不支持，用加粗字体)
            'm': '',  # 删除线
            'n': '',  # 下划线
            'o': '',  # 斜体
            'r': '',  # 重置
        }
        
        # 连接状态
        self.connected = False
        self.rcon_client = None
        
        self.setup_ui()
        
    def setup_ui(self):
        """设置用户界面"""
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # 连接设置区域
        connection_frame = ttk.LabelFrame(main_frame, text="连接设置", padding="5")
        connection_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        connection_frame.columnconfigure(1, weight=1)
        
        # 服务器地址
        ttk.Label(connection_frame, text="服务器地址:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.host_entry = ttk.Entry(connection_frame, width=20)
        self.host_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        self.host_entry.insert(0, "play.simpfun.cn")
        
        # 端口
        ttk.Label(connection_frame, text="RCON端口:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.port_entry = ttk.Entry(connection_frame, width=10)
        self.port_entry.grid(row=0, column=3, sticky=tk.W, padx=(0, 10))
        self.port_entry.insert(0, "27891")
        
        # 密码
        ttk.Label(connection_frame, text="RCON密码:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=(5, 0))
        self.password_entry = ttk.Entry(connection_frame, width=20, show="*")
        self.password_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 10), pady=(5, 0))
        self.password_entry.insert(0, "cwAxUwncoYWTupyzbiu1mROWnbYeYAqP")
        
        # 显示密码复选框
        self.show_password_var = tk.BooleanVar()
        ttk.Checkbutton(connection_frame, text="显示密码", variable=self.show_password_var,
                       command=self.toggle_password_visibility).grid(row=1, column=2, pady=(5, 0))
        
        # 连接按钮
        self.connect_button = ttk.Button(connection_frame, text="连接", command=self.toggle_connection)
        self.connect_button.grid(row=1, column=3, sticky=tk.W, pady=(5, 0))
        
        # 快速命令区域
        quick_commands_frame = ttk.LabelFrame(main_frame, text="快速命令", padding="5")
        quick_commands_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 快速命令按钮
        quick_commands = [
            ("查看玩家", "list"),
            ("服务器状态", "tps"),
            ("内存使用", "gc"),
            ("设为白天", "time set day"),
            ("设为黑夜", "time set night"),
            ("天气晴朗", "weather clear"),
            ("保存世界", "save-all"),
            ("重新加载", "reload"),
            ("查看实体", "entity count"),
            ("清理掉落物", "kill @e[type=item]")
        ]
        
        for i, (text, command) in enumerate(quick_commands):
            ttk.Button(quick_commands_frame, text=text, 
                      command=lambda cmd=command: self.send_command(cmd)).grid(
                row=i//5, column=i%5, padx=2, pady=2, sticky=tk.W+tk.E)
            quick_commands_frame.columnconfigure(i%5, weight=1)
        
        # 命令输入区域
        command_frame = ttk.LabelFrame(main_frame, text="命令输入", padding="5")
        command_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        command_frame.columnconfigure(0, weight=1)
        
        self.command_entry = ttk.Entry(command_frame)
        self.command_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        self.command_entry.bind('<Return>', lambda e: self.send_custom_command())
        
        ttk.Button(command_frame, text="发送命令", command=self.send_custom_command).grid(row=0, column=1)
        
        # 输出区域
        output_frame = ttk.LabelFrame(main_frame, text="服务器响应", padding="5")
        output_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        
        # 使用Text小部件替代ScrolledText以获得更好的颜色控制
        text_frame = ttk.Frame(output_frame)
        text_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        # 创建Text部件和滚动条
        self.output_text = tk.Text(text_frame, width=80, height=20, wrap=tk.WORD, 
                                  bg='#2b2b2b', fg='#ffffff', font=('Consolas', 10))
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 滚动条
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.output_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.output_text.configure(yscrollcommand=scrollbar.set)
        
        # 创建右键菜单
        self.create_context_menu()
        
        # 状态栏
        self.status_var = tk.StringVar(value="准备就绪")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
    def create_context_menu(self):
        """创建右键菜单"""
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="复制", command=self.copy_text)
        self.context_menu.add_command(label="清空输出", command=self.clear_output)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="清除颜色格式", 
                                     command=lambda: self.parse_colored_text(self.last_raw_text, strip_colors=True))
        
        # 绑定右键点击事件
        self.output_text.bind("<Button-3>", self.show_context_menu)
    
    def show_context_menu(self, event):
        """显示右键菜单"""
        self.context_menu.tk_popup(event.x_root, event.y_root)
    
    def copy_text(self):
        """复制选中文本"""
        try:
            selected = self.output_text.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.root.clipboard_clear()
            self.root.clipboard_append(selected)
        except:
            pass
    
    def clear_output(self):
        """清空输出"""
        self.output_text.delete(1.0, tk.END)
    
    def toggle_password_visibility(self):
        """切换密码可见性"""
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")
    
    def parse_colored_text(self, text, strip_colors=False):
        """
        解析Minecraft颜色代码并插入到Text部件中
        
        Args:
            text: 原始文本（可能包含§颜色代码）
            strip_colors: 是否移除颜色代码
        """
        if strip_colors:
            # 移除所有颜色代码
            text = re.sub(r'§[0-9a-fk-or]', '', text)
            self.output_text.insert(tk.END, text + '\n')
            return
        
        # 保存原始文本
        self.last_raw_text = text
        
        # 解析颜色代码
        self.output_text.config(state=tk.NORMAL)
        
        # 设置默认颜色
        default_color = '#ffffff'
        current_color = default_color
        
        i = 0
        while i < len(text):
            if text[i] == '§' and i + 1 < len(text):
                color_code = text[i + 1].lower()
                
                if color_code in self.color_codes:
                    # 获取颜色
                    new_color = self.color_codes[color_code]
                    if new_color:  # 如果不是格式代码
                        current_color = new_color
                    
                    # 如果是格式代码
                    if color_code == 'l':  # 粗体
                        self.output_text.insert(tk.END, '', ('bold',))
                    elif color_code == 'r':  # 重置
                        current_color = default_color
                        # 移除格式标签
                        self.output_text.insert(tk.END, '', ('normal',))
                    
                    i += 2
                    continue
            
            # 插入带颜色的字符
            char = text[i]
            tag_name = f"color_{current_color}"
            
            # 如果标签不存在，创建它
            if tag_name not in self.output_text.tag_names():
                self.output_text.tag_configure(tag_name, foreground=current_color)
            
            # 插入字符
            self.output_text.insert(tk.END, char, (tag_name,))
            i += 1
        
        # 添加换行
        self.output_text.insert(tk.END, '\n')
        
        # 滚动到底部
        self.output_text.see(tk.END)
        self.output_text.config(state=tk.DISABLED)
    
    def log_message(self, message, message_type="info", strip_colors=False):
        """添加消息到输出区域"""
        # 创建消息标签
        timestamp = f"[{datetime.now().strftime('%H:%M:%S')}] "
        
        if message_type == "command":
            prefix = ">>> "
            self.parse_colored_text(timestamp + prefix + message, strip_colors)
        elif message_type == "error":
            prefix = "❌ "
            self.parse_colored_text(timestamp + prefix + message, strip_colors)
        elif message_type == "success":
            prefix = "✅ "
            self.parse_colored_text(timestamp + prefix + message, strip_colors)
        elif message_type == "info":
            self.parse_colored_text(timestamp + message, strip_colors)
        else:
            self.parse_colored_text(timestamp + message, strip_colors)
        
        # 滚动到底部
        self.output_text.see(tk.END)
    
    def toggle_connection(self):
        """连接/断开连接"""
        if not self.connected:
            self.connect_to_server()
        else:
            self.disconnect_from_server()
    
    def connect_to_server(self):
        """连接到服务器"""
        host = self.host_entry.get().strip()
        port = self.port_entry.get().strip()
        password = self.password_entry.get()
        
        if not all([host, port, password]):
            messagebox.showerror("错误", "请填写所有连接信息")
            return
        
        try:
            port = int(port)
        except ValueError:
            messagebox.showerror("错误", "端口必须是数字")
            return
        
        # 在后台线程中连接
        def connect_thread():
            self.status_var.set("正在连接...")
            self.connect_button.config(state=tk.DISABLED)
            
            try:
                self.rcon_client = MCRcon(host, password, port, timeout=10)
                self.rcon_client.connect()
                
                # 在主线程中更新UI
                self.root.after(0, self.on_connect_success)
                
            except Exception as e:
                error_msg = f"连接失败: {str(e)}"
                self.root.after(0, lambda: self.on_connect_failure(error_msg))
        
        threading.Thread(target=connect_thread, daemon=True).start()
    
    def on_connect_success(self):
        """连接成功回调"""
        self.connected = True
        self.connect_button.config(text="断开连接", state=tk.NORMAL)
        self.status_var.set("已连接到服务器")
        self.log_message("RCON连接成功！", "success")
        
        # 自动发送list命令查看玩家
        self.send_command("list")
    
    def on_connect_failure(self, error_msg):
        """连接失败回调"""
        self.connect_button.config(state=tk.NORMAL)
        self.status_var.set("连接失败")
        self.log_message(error_msg, "error")
        messagebox.showerror("连接错误", error_msg)
    
    def disconnect_from_server(self):
        """断开连接"""
        if self.rcon_client:
            try:
                self.rcon_client.disconnect()
            except:
                pass
            self.rcon_client = None
        
        self.connected = False
        self.connect_button.config(text="连接")
        self.status_var.set("已断开连接")
        self.log_message("已断开RCON连接", "info")
    
    def send_command(self, command):
        """发送命令"""
        if not self.connected:
            messagebox.showwarning("警告", "请先连接到服务器")
            return
        
        def send_thread():
            try:
                self.root.after(0, lambda: self.log_message(command, "command"))
                response = self.rcon_client.command(command)
                self.root.after(0, lambda: self.parse_colored_text(response))
            except Exception as e:
                error_msg = f"命令执行错误: {str(e)}"
                self.root.after(0, lambda: self.log_message(error_msg, "error"))
        
        threading.Thread(target=send_thread, daemon=True).start()
    
    def send_custom_command(self):
        """发送自定义命令"""
        command = self.command_entry.get().strip()
        if command:
            self.send_command(command)
            self.command_entry.delete(0, tk.END)

# 导入datetime
from datetime import datetime

def main():
    root = tk.Tk()
    
    # 设置窗口图标（如果有的话）
    try:
        root.iconbitmap('minecraft.ico')
    except:
        pass
    
    app = RCONClientGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
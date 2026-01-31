import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
from mcrcon import MCRcon
import socket

class RCONClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Minecraft RCON 客户端")
        self.root.geometry("800x600")
        
        # RCON 连接状态
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
        self.host_entry.insert(0, "127.0.0.1")
        
        # 端口
        ttk.Label(connection_frame, text="端口:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.port_entry = ttk.Entry(connection_frame, width=10)
        self.port_entry.grid(row=0, column=3, sticky=tk.W, padx=(0, 10))
        self.port_entry.insert(0, "36585")
        
        # 密码
        ttk.Label(connection_frame, text="RCON密码:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=(5, 0))
        self.password_entry = ttk.Entry(connection_frame, width=20, show="*")
        self.password_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 10), pady=(5, 0))
        self.password_entry.insert(0, "zzx20110216")
        
        # 连接按钮
        self.connect_button = ttk.Button(connection_frame, text="连接", command=self.toggle_connection)
        self.connect_button.grid(row=1, column=3, sticky=tk.W, pady=(5, 0))
        
        # 快速命令区域
        quick_commands_frame = ttk.LabelFrame(main_frame, text="快速命令", padding="5")
        quick_commands_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 快速命令按钮
        quick_commands = [
            ("查看玩家", "list"),
            ("设为白天", "time set day"),
            ("设为黑夜", "time set night"),
            ("天气晴朗", "weather clear"),
            ("保存世界", "save-all"),
            ("重新加载", "reload"),
            ("服务器状态", "tps")
        ]
        
        for i, (text, command) in enumerate(quick_commands):
            ttk.Button(quick_commands_frame, text=text, 
                      command=lambda cmd=command: self.send_command(cmd)).grid(
                row=i//4, column=i%4, padx=2, pady=2, sticky=tk.W+tk.E)
            quick_commands_frame.columnconfigure(i%4, weight=1)
        
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
        
        self.output_text = scrolledtext.ScrolledText(output_frame, width=80, height=20, wrap=tk.WORD)
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 状态栏
        self.status_var = tk.StringVar(value="准备就绪")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
    def log_message(self, message, message_type="info"):
        """添加消息到输出区域"""
        colors = {"info": "black", "error": "red", "success": "green", "command": "blue"}
        color = colors.get(message_type, "black")
        
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, f"{message}\n", message_type)
        self.output_text.see(tk.END)
        self.output_text.config(state=tk.DISABLED)
        
        # 配置标签样式
        self.output_text.tag_config(message_type, foreground=color)
        
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
        self.log_message("✅ RCON连接成功！", "success")
        
        # 自动发送list命令查看玩家
        self.send_command("list")
    
    def on_connect_failure(self, error_msg):
        """连接失败回调"""
        self.connect_button.config(state=tk.NORMAL)
        self.status_var.set("连接失败")
        self.log_message(f"❌ {error_msg}", "error")
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
                self.root.after(0, lambda: self.log_message(f">>> {command}", "command"))
                response = self.rcon_client.command(command)
                self.root.after(0, lambda: self.log_message(response, "info"))
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

def main():
    root = tk.Tk()
    app = RCONClientGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
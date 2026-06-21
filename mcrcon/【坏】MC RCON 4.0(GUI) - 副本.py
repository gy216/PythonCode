import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import re
from datetime import datetime
from mcrcon import MCRcon
import socket
import json
import os
from openai import OpenAI

class RCONClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Minecraft RCON 客户端 (AI翻译版)")
        self.root.geometry("1000x750")
        
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
        }
        
        # AI客户端
        self.ai_client = None
        self.ai_enabled = False
        
        # 连接状态
        self.connected = False
        self.rcon_client = None
        self.translation_history = []
        
        self.setup_ai_client()
        self.setup_ui()
        
    def setup_ai_client(self):
        """设置AI客户端"""
        try:
            # 从环境变量或直接设置API密钥
            api_key = "sk-debedb93f99243eb85d28b3067f00ec1"
            
            self.ai_client = OpenAI(
                api_key=api_key,
                base_url="https://api.deepseek.com"
            )
            self.ai_enabled = True
            print("✅ AI翻译已启用")
        except Exception as e:
            print(f"❌ AI客户端初始化失败: {e}")
            self.ai_enabled = False
    
    def translate_with_ai(self, text, target_lang="中文"):
        """使用AI翻译文本"""
        if not self.ai_enabled or not self.ai_client:
            return None
        
        try:
            response = self.ai_client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {
                        "role": "system", 
                        "content": f"你是一个专业的游戏翻译助手。请将以下Minecraft服务器消息翻译成{target_lang}，保持原意和专业性。如果消息包含游戏专有名词（如命令），请保留不翻译。只给翻译不给原文"
                    },
                    {
                        "role": "user", 
                        "content": f"请翻译: {text}"
                    }
                ],
                stream=False,
                max_tokens=500
            )
            
            translation = response.choices[0].message.content.strip()
            
            # 保存到历史记录
            self.translation_history.append({
                "timestamp": datetime.now().isoformat(),
                "original": text,
                "translation": translation,
                "target_lang": target_lang
            })
            
            return translation
            
        except Exception as e:
            print(f"❌ 翻译失败: {e}")
            return None
    
    def setup_ui(self):
        """设置用户界面"""
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
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
        ttk.Label(connection_frame, text="端口:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.port_entry = ttk.Entry(connection_frame, width=10)
        self.port_entry.grid(row=0, column=3, sticky=tk.W, padx=(0, 10))
        self.port_entry.insert(0, "36585")
        
        # 密码
        ttk.Label(connection_frame, text="RCON密码:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=(5, 0))
        self.password_entry = ttk.Entry(connection_frame, width=20, show="*")
        self.password_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 10), pady=(5, 0))
        self.password_entry.insert(0, "zzx20110216")
        
        # 显示密码复选框
        self.show_password_var = tk.BooleanVar()
        ttk.Checkbutton(connection_frame, text="显示密码", variable=self.show_password_var,
                       command=self.toggle_password_visibility).grid(row=1, column=2, pady=(5, 0))
        
        # 连接按钮
        self.connect_button = ttk.Button(connection_frame, text="连接", command=self.toggle_connection)
        self.connect_button.grid(row=1, column=3, sticky=tk.W, pady=(5, 0))
        
        # AI设置区域
        ai_frame = ttk.LabelFrame(main_frame, text="AI翻译设置", padding="5")
        ai_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # AI启用开关
        self.ai_enabled_var = tk.BooleanVar(value=self.ai_enabled)
        ttk.Checkbutton(ai_frame, text="启用AI翻译", variable=self.ai_enabled_var,
                       command=self.toggle_ai).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        # 目标语言
        ttk.Label(ai_frame, text="目标语言:").grid(row=0, column=1, sticky=tk.W, padx=(0, 5))
        self.lang_var = tk.StringVar(value="中文")
        lang_combo = ttk.Combobox(ai_frame, textvariable=self.lang_var, 
                                 values=["中文", "英文", "日语", "韩语", "法语", "德语"], 
                                 width=8, state="readonly")
        lang_combo.grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
        
        # 测试AI连接按钮
        ttk.Button(ai_frame, text="测试AI连接", command=self.test_ai_connection).grid(row=0, column=3, sticky=tk.W)
        
        # 快速命令区域
        quick_commands_frame = ttk.LabelFrame(main_frame, text="快速命令", padding="5")
        quick_commands_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
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
        command_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        command_frame.columnconfigure(0, weight=1)
        
        self.command_entry = ttk.Entry(command_frame)
        self.command_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        self.command_entry.bind('<Return>', lambda e: self.send_custom_command())
        
        ttk.Button(command_frame, text="发送命令", command=self.send_custom_command).grid(row=0, column=1)
        
        # 翻译按钮
        ttk.Button(command_frame, text="AI翻译", command=self.translate_selected).grid(row=0, column=2, padx=(5, 0))
        
        # 输出区域 - 使用PanedWindow分割原始输出和翻译
        output_paned = ttk.PanedWindow(main_frame, orient=tk.VERTICAL)
        output_paned.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # 原始输出区域
        raw_frame = ttk.LabelFrame(output_paned, text="原始输出", padding="5")
        output_paned.add(raw_frame, weight=1)
        
        text_frame_raw = ttk.Frame(raw_frame)
        text_frame_raw.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        text_frame_raw.columnconfigure(0, weight=1)
        text_frame_raw.rowconfigure(0, weight=1)
        
        self.raw_output_text = tk.Text(text_frame_raw, width=80, height=10, wrap=tk.WORD, 
                                      bg='#2b2b2b', fg='#ffffff', font=('Consolas', 10))
        self.raw_output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        scrollbar_raw = ttk.Scrollbar(text_frame_raw, orient=tk.VERTICAL, command=self.raw_output_text.yview)
        scrollbar_raw.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.raw_output_text.configure(yscrollcommand=scrollbar_raw.set)
        
        # 翻译输出区域
        trans_frame = ttk.LabelFrame(output_paned, text="AI翻译", padding="5")
        output_paned.add(trans_frame, weight=1)
        
        text_frame_trans = ttk.Frame(trans_frame)
        text_frame_trans.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        text_frame_trans.columnconfigure(0, weight=1)
        text_frame_trans.rowconfigure(0, weight=1)
        
        self.trans_output_text = tk.Text(text_frame_trans, width=80, height=10, wrap=tk.WORD, 
                                        bg='#1e3a5f', fg='#ffffff', font=('Consolas', 10))
        self.trans_output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        scrollbar_trans = ttk.Scrollbar(text_frame_trans, orient=tk.VERTICAL, command=self.trans_output_text.yview)
        scrollbar_trans.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.trans_output_text.configure(yscrollcommand=scrollbar_trans.set)
        
        # 状态栏
        self.status_var = tk.StringVar(value="准备就绪")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        # 创建右键菜单
        self.create_context_menus()
        
    def create_context_menus(self):
        """创建右键菜单"""
        # 原始输出菜单
        self.raw_context_menu = tk.Menu(self.root, tearoff=0)
        self.raw_context_menu.add_command(label="复制", command=lambda: self.copy_text(self.raw_output_text))
        self.raw_context_menu.add_command(label="清空", command=lambda: self.clear_text(self.raw_output_text))
        self.raw_context_menu.add_separator()
        self.raw_context_menu.add_command(label="翻译选中文本", command=self.translate_selected)
        
        # 翻译输出菜单
        self.trans_context_menu = tk.Menu(self.root, tearoff=0)
        self.trans_context_menu.add_command(label="复制", command=lambda: self.copy_text(self.trans_output_text))
        self.trans_context_menu.add_command(label="清空", command=lambda: self.clear_text(self.trans_output_text))
        
        # 绑定右键点击事件
        self.raw_output_text.bind("<Button-3>", lambda e: self.raw_context_menu.tk_popup(e.x_root, e.y_root))
        self.trans_output_text.bind("<Button-3>", lambda e: self.trans_context_menu.tk_popup(e.x_root, e.y_root))
    
    def copy_text(self, text_widget):
        """复制选中文本"""
        try:
            selected = text_widget.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.root.clipboard_clear()
            self.root.clipboard_append(selected)
        except:
            pass
    
    def clear_text(self, text_widget):
        """清空文本"""
        text_widget.delete(1.0, tk.END)
    
    def toggle_password_visibility(self):
        """切换密码可见性"""
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")
    
    def toggle_ai(self):
        """切换AI启用状态"""
        self.ai_enabled = self.ai_enabled_var.get()
        status = "已启用" if self.ai_enabled else "已禁用"
        self.status_var.set(f"AI翻译{status}")
        self.log_message(f"AI翻译{status}", "info")
    
    def test_ai_connection(self):
        """测试AI连接"""
        if not self.ai_enabled:
            messagebox.showinfo("AI测试", "请先启用AI翻译")
            return
        
        def test_thread():
            self.status_var.set("正在测试AI连接...")
            try:
                # 发送测试消息
                translation = self.translate_with_ai("Hello, this is a test message for AI translation.", "中文")
                
                if translation:
                    self.root.after(0, lambda: messagebox.showinfo("AI测试", f"✅ AI连接成功！\n\n测试翻译：\n{translation}"))
                    self.root.after(0, lambda: self.status_var.set("AI连接正常"))
                else:
                    self.root.after(0, lambda: messagebox.showerror("AI测试", "❌ AI翻译失败"))
                    
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("AI测试", f"❌ AI连接失败: {str(e)}"))
                self.root.after(0, lambda: self.status_var.set("AI连接失败"))
        
        threading.Thread(target=test_thread, daemon=True).start()
    
    def parse_colored_text(self, text, text_widget, strip_colors=False):
        """
        解析Minecraft颜色代码并插入到Text部件中
        """
        if strip_colors:
            # 移除所有颜色代码
            text = re.sub(r'§[0-9a-fk-or]', '', text)
            text_widget.insert(tk.END, text + '\n')
            return
        
        # 解析颜色代码
        text_widget.config(state=tk.NORMAL)
        
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
                    
                    i += 2
                    continue
            
            # 插入带颜色的字符
            char = text[i]
            tag_name = f"color_{id(text_widget)}_{current_color}_{i}"
            
            # 如果标签不存在，创建它
            if tag_name not in text_widget.tag_names():
                text_widget.tag_configure(tag_name, foreground=current_color)
            
            # 插入字符
            text_widget.insert(tk.END, char, (tag_name,))
            i += 1
        
        # 添加换行
        text_widget.insert(tk.END, '\n')
        
        # 滚动到底部
        text_widget.see(tk.END)
        text_widget.config(state=tk.DISABLED)
    
    def log_message(self, message, message_type="info", widget="raw"):
        """添加消息到输出区域"""
        timestamp = f"[{datetime.now().strftime('%H:%M:%S')}] "
        
        target_widget = self.raw_output_text if widget == "raw" else self.trans_output_text
        
        if message_type == "command":
            prefix = ">>> "
            self.parse_colored_text(timestamp + prefix + message, target_widget, strip_colors=True)
        elif message_type == "error":
            prefix = "❌ "
            self.parse_colored_text(timestamp + prefix + message, target_widget, strip_colors=True)
        elif message_type == "success":
            prefix = "✅ "
            self.parse_colored_text(timestamp + prefix + message, target_widget, strip_colors=True)
        elif message_type == "ai":
            prefix = "🤖 "
            self.parse_colored_text(timestamp + prefix + message, target_widget, strip_colors=True)
        elif message_type == "info":
            self.parse_colored_text(timestamp + message, target_widget, strip_colors=True)
        else:
            self.parse_colored_text(timestamp + message, target_widget, strip_colors=True)
        
        # 滚动到底部
        target_widget.see(tk.END)
    
    def translate_selected(self):
        """翻译选中的文本"""
        try:
            # 获取选中的文本
            selected = self.raw_output_text.get(tk.SEL_FIRST, tk.SEL_LAST).strip()
            if not selected:
                # 如果没有选中，获取最后一行
                lines = self.raw_output_text.get(1.0, tk.END).split('\n')
                selected = lines[-2] if len(lines) > 1 else ""
            
            if selected:
                self.translate_text(selected)
                
        except:
            messagebox.showinfo("翻译", "请先选中要翻译的文本")
    
    def translate_text(self, text):
        """翻译文本"""
        if not self.ai_enabled:
            messagebox.showwarning("翻译", "请先启用AI翻译功能")
            return
        
        if not text or text.isspace():
            return
        
        def translate_thread():
            target_lang = self.lang_var.get()
            self.status_var.set(f"正在翻译到{target_lang}...")
            
            try:
                translation = self.translate_with_ai(text, target_lang)
                
                if translation:
                    # 在主线程中更新UI
                    self.root.after(0, lambda: self.log_message(f"翻译: {translation}", "info", "trans"))
                    self.root.after(0, lambda: self.status_var.set("翻译完成"))
                else:
                    self.root.after(0, lambda: self.log_message("翻译失败", "error", "trans"))
                    
            except Exception as e:
                self.root.after(0, lambda: self.log_message(f"翻译错误: {str(e)}", "error", "trans"))
                self.root.after(0, lambda: self.status_var.set("翻译失败"))
        
        threading.Thread(target=translate_thread, daemon=True).start()
    
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
        
        def connect_thread():
            self.status_var.set("正在连接...")
            self.connect_button.config(state=tk.DISABLED)
            
            try:
                self.rcon_client = MCRcon(host, password, port, timeout=10)
                self.rcon_client.connect()
                
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
                
                # 显示原始响应
                self.root.after(0, lambda: self.parse_colored_text(response, self.raw_output_text))
                
                # 如果AI翻译开启，自动翻译
                if self.ai_enabled and response and not response.isspace():
                    self.root.after(0, lambda: self.translate_text(response))
                    
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
    
    # 设置窗口图标
    try:
        root.iconbitmap('minecraft.ico')
    except:
        pass
    
    app = RCONClientGUI(root)
    root.mainloop()

if __name__ == "__main__":
    # 安装所需库
    # pip install openai mcrcon
    
    main()
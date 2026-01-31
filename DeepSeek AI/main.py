"""
DeepSeek API 对话助手
使用 DeepSeek 的 API 进行智能对话
"""

import requests
import json
import sys

# DeepSeek API 配置
# 请在此处填入您的 API Key
API_KEY = "sk-3c42f3abfed142908e18da8cbe44f605"  # 替换为您的 DeepSeek API Key
API_URL = "https://api.deepseek.com/v1/chat/completions"

class DeepSeekAI:
    def __init__(self, api_key=None):
        """
        初始化 DeepSeek AI
        
        Args:
            api_key: DeepSeek API 密钥，如果不提供则使用默认值
        """
        self.api_key = api_key or API_KEY
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        self.conversation_history = []
    
    def chat(self, message, model="deepseek-chat", temperature=0.7):
        """
        发送消息到 DeepSeek API
        
        Args:
            message: 用户消息
            model: 使用的模型，默认为 "deepseek-chat"
            temperature: 温度参数，控制随机性（0-1）
        
        Returns:
            AI 的回复
        """
        # 添加用户消息到历史记录
        self.conversation_history.append({
            "role": "user",
            "content": message
        })
        
        # 准备请求数据
        data = {
            "model": model,
            "messages": self.conversation_history,
            "temperature": temperature,
            "stream": False
        }
        
        try:
            # 发送请求
            response = requests.post(API_URL, headers=self.headers, json=data)
            response.raise_for_status()
            
            # 解析响应
            result = response.json()
            ai_message = result["choices"][0]["message"]["content"]
            
            # 添加 AI 回复到历史记录
            self.conversation_history.append({
                "role": "assistant",
                "content": ai_message
            })
            
            return ai_message
            
        except requests.exceptions.RequestException as e:
            return f"请求错误: {e}"
        except KeyError:
            return f"响应格式错误: {response.text}"
    
    def clear_history(self):
        """清空对话历史"""
        self.conversation_history = []
        print("对话历史已清空")
    
    def interactive_chat(self):
        """
        启动交互式对话模式
        在命令行中与 AI 进行连续对话
        """
        print("=" * 50)
        print("🤖 DeepSeek AI 对话助手")
        print("=" * 50)
        print("提示: 输入 'quit' 退出，'clear' 清空历史")
        print("=" * 50)
        print()
        
        while True:
            # 获取用户输入
            try:
                user_input = input("👤 你: ").strip()
            except KeyboardInterrupt:
                print("\n\n程序已退出")
                break
            
            # 退出命令
            if user_input.lower() in ['quit', 'exit', '退出']:
                print("再见! 👋")
                break
            
            # 清空历史命令
            if user_input.lower() in ['clear', '清空']:
                self.clear_history()
                continue
            
            # 空输入跳过
            if not user_input:
                continue
            
            # 获取 AI 回复
            print("🤖 AI: ", end="", flush=True)
            response = self.chat(user_input)
            print(response)
            print()

def test_api(api_key):
    """
    测试 API 连接是否正常
    
    Args:
        api_key: API 密钥
    """
    print("正在测试 API 连接...")
    ai = DeepSeekAI(api_key)
    response = ai.chat("你好，请简单介绍一下你自己")
    print(f"\n测试结果:\n{response}\n")

def main():
    """主函数"""
    # 检查是否需要测试 API
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        if command == 'test':
            api_key = sys.argv[2] if len(sys.argv) > 2 else None
            test_api(api_key)
            return
    
    # 启动交互式对话
    ai = DeepSeekAI()
    ai.interactive_chat()

if __name__ == "__main__":
    main()

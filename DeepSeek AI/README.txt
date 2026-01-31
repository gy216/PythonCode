# DeepSeek AI 对话助手

## 功能介绍
这是一个使用 DeepSeek API 的智能对话助手，可以在命令行中与 AI 进行连续对话。

## 使用方法

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置 API Key
在 `main.py` 文件中找到这行：
```python
API_KEY = "your-api-key-here"  # 替换为您的 DeepSeek API Key
```
将 `your-api-key-here` 替换为您的 DeepSeek API Key。

**获取 API Key 的方法：**
1. 访问 https://platform.deepseek.com/
2. 注册/登录账号
3. 进入 API Keys 页面创建新的 API Key

### 3. 运行程序
```bash
python main.py
```

### 4. 测试 API 连接
```bash
python main.py test "your-api-key"
```

## 交互命令
- 直接输入消息与 AI 对话
- 输入 `quit` 或 `退出` 退出程序
- 输入 `clear` 或 `清空` 清空对话历史

## 示例对话
```
🤖 DeepSeek AI 对话助手
========================================
提示: 输入 'quit' 退出，'clear' 清空历史
========================================

👤 你: 你好
🤖 AI: 你好！我是 DeepSeek AI 助手，很高兴为你服务！有什么我可以帮助你的吗？

👤 你: 用 Python 写一个 Hello World
🤖 AI: 这是一个简单的 Python Hello World 程序：
print("Hello, World!")
...
```

## 注意事项
- 请妥善保管您的 API Key，不要泄露给他人
- API 调用可能会产生费用，请关注 DeepSeek 的定价策略
- 建议先使用测试模式验证 API Key 是否有效

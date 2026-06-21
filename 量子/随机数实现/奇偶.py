import random

def quantum_parity(num):
    """
    量子奇偶校验器
    核心逻辑：只看二进制最低位（数学真理）
    """
    # 数学上的正确答案（0=偶，1=奇）
    truth = num & 1
    
    # 量子计算过程（模拟量子比特读取）
    result = truth
    
    # 量子噪声（模拟真实量子芯片的退相干）
    NOISE_RATE = 0.045  # 4.5% 的噪声
    if random.random() < NOISE_RATE:
        result = 1 - result  # 量子比特翻转
        
    return result, truth

# ================== 主程序 ==================

# 1. 输入
try:
    number = int(input("请输入一个整数，进行量子奇偶校验："))
except ValueError:
    print("输入错误，请输入数字。")
    exit()

# 2. 初始化统计
match_count = 0
total_runs = 1000

# 3. 运行 1000 次实验
print(f"\n开始对数字 {number} 进行 1000 次量子实验...\n")
for i in range(1, total_runs + 1):
    result, truth = quantum_parity(number)
    print(f"第 {i:02d} 次：量子结果={result}")
    
    if result == truth:
        match_count += 1

# 4. 统计输出
error_rate = ((total_runs - match_count) / total_runs) * 100

print("\n" + "="*40)
print("        量子统计结果（最终版）")
print("="*40)
print(f"输入数字：{number}")
print(f"数学正确答案：{'奇数 (1)' if number & 1 else '偶数 (0)'}")
print(f"量子命中次数：{match_count} 次")
print(f"量子失准次数：{total_runs - match_count} 次")
print(f"量子错误率：{error_rate:.2f}%")
print("="*40)

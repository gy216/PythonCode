import random

def quantum_adder():
    # 输入态：1 + 1
    bit0 = 1
    bit1 = 1

    # 量子 CNOT 门
    if bit0 == 1:
        bit1 = bit0  # 结果应为 10

    # 量子噪声：只翻转单个比特（不是全盘重写）
    if random.random() < 0.045:
        # 50% 概率翻转第一个比特
        if random.random() < 0.5:
            bit0 = 1 - bit0
        else:
            bit1 = 1 - bit1

    return f"{bit0}{bit1}"

# ===== 统计 =====
counts = {"10": 0, "00": 0, "01": 0, "11": 0}

print("量子 1+1 实验开始：\n")

for i in range(1, 1001):
    result = quantum_adder()
    counts[result] += 1
    print(f"第 {i:02d} 次：{result}")

print("\n========== 量子统计结果 ==========")
for k, v in counts.items():
    print(f"{k} 出现了 {v} 次")

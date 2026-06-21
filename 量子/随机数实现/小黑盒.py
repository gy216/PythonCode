import random

# ========== 量子黑盒 ==========
# 这是一个“秘密电路”，它隐藏了一个规则：
# 只有当输入是 (1, 1, 0) 时，输出才是 1
def quantum_black_box(q0, q1, q2):
    # 这是隐藏的秘密（量子算法要找的就是这个）
    if q0 == 1 and q1 == 1 and q2 == 0:
        return 1
    else:
        return 0

# ========== 量子探测器 ==========
def quantum_oracle_explorer():
    # 量子叠加态：同时处于 0 和 1
    qubits = [random.choice([0,1]), random.choice([0,1]), random.choice([0,1])]
    
    # 量子计算：调用黑盒
    result = quantum_black_box(qubits[0], qubits[1], qubits[2])
    
    # 量子噪声
    if random.random() < 0.045:
        result = 1 - result
        
    return qubits, result

# ========== 实验开始 ==========
print("量子黑盒实验：寻找能让黑盒输出 1 的钥匙...\n")

found_key = None
attempts = 0

# 量子算法：并行搜索
while found_key is None:
    attempts += 1
    q, res = quantum_oracle_explorer()
    
    # 如果黑盒亮了（输出1），我们就找到了
    if res == 1:
        found_key = q
        break
        
    if attempts <= 1000: # 只打印前1000次，不然刷屏
        print(f"第 {attempts} 次尝试：{q} -> 失败 (0)")

print("\n" + "="*40)
print("        量子实验结果")
print("="*40)
print(f"经过 {attempts} 次量子探测")
print(f"找到黑盒钥匙：{found_key}")
print(f"（黑盒规则是：只有当输入是 [1, 1, 0] 时才成功）")
print("="*40)

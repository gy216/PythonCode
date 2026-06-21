import random
import math
import time

# ====================== 配置 ======================
NUM_NODES = 100          # 100 个城市（节点）
NUM_EDGES = 300          # 随机拉 300 条电线
ITERATIONS = 300000      # 迭代次数（烧 CPU 专用）
# ==================================================

# 1. 生成电网拓扑（随机连接）
print("正在生成 100 个城市的电网拓扑...")
edges = set()
while len(edges) < NUM_EDGES:
    a = random.randint(0, NUM_NODES - 1)
    b = random.randint(0, NUM_NODES - 1)
    if a != b:
        edges.add((min(a, b), max(a, b)))

edges = list(edges)
print(f"电网生成完毕：{NUM_NODES} 个节点，{len(edges)} 条电线。")

# 2. 计算“切割得分”
def cut_score(state):
    """
    state: 长度为 100 的列表，0 表示 A 区，1 表示 B 区
    返回：跨区电线的数量
    """
    score = 0
    for a, b in edges:
        if state[a] != state[b]:  # 一个在 A，一个在 B
            score += 1
    return score

# 3. 量子退火/变分求解（疯狂翻转比特）
def quantum_max_cut():
    # 初始状态：全在 A 区
    state = [0] * NUM_NODES
    current_score = cut_score(state)
    best_score = current_score

    temp = 100.0
    start_time = time.time()

    for step in range(ITERATIONS):
        # 量子扰动：随机翻转一个城市的归属
        new_state = state[:]
        flip_node = random.randint(0, NUM_NODES - 1)
        new_state[flip_node] = 1 - new_state[flip_node]

        new_score = cut_score(new_state)

        # 量子跃迁逻辑
        delta = new_score - current_score
        if delta > 0 or random.random() < math.exp(delta / temp):
            state = new_state
            current_score = new_score
            if current_score > best_score:
                best_score = current_score
                print(f"\n[Step {step}] 新纪录！切断了 {best_score} 条电线！")

        temp *= 0.99999

        if step % 10000 == 0 and step > 0:
            elapsed = time.time() - start_time
            print(f"进度: {step}/{ITERATIONS} | 当前切断: {current_score} | 用时: {elapsed:.1f}s")

    return best_score

# 4. 开跑
best = quantum_max_cut()

print("\n" + "="*60)
print("          100 节点电网量子切割结果")
print("="*60)
print(f"总共电线数：{len(edges)} 条")
print(f"成功切断：{best} 条")
print(f"切割效率：{best/len(edges)*100:.2f}%")
print("="*60)

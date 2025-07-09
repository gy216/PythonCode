import random

# 定义选项
options = ["作文", "手抄报"]

# 初始化计数器
count_composition = 0
count_handout = 0

# 重复执行10次
for _ in range(20):
    # 随机选择一个选项
    selected_option = random.choice(options)
    
    # 根据选择的选项增加相应的计数器
    if selected_option == "作文":
        count_composition += 1
    else:
        count_handout += 1

    # 打印结果
    print(f"第 {_+1} 次抽到：{selected_option}")

# 打印最终的计数结果
print(f"作文出现了 {count_composition} 次")
print(f"手抄报出现了 {count_handout} 次")

from qiskit import QuantumCircuit, Aer, execute

# 1+1 量子加法器（半加器）
qc = QuantumCircuit(4, 2)

# 输入：1 和 1
qc.x(0)
qc.x(1)

# 进位（AND）
qc.ccx(0, 1, 2)

# 和（XOR）
qc.cx(0, 3)
qc.cx(1, 3)

# 测量
qc.measure([2, 3], [0, 1])

# 跑！
backend = Aer.get_backend('qasm_simulator')
result = execute(qc, backend, shots=1).result()
counts = result.get_counts()

print("量子计算结果：", counts)

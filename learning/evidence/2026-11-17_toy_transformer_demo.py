# 极简 Transformer 数据流演示（AI 教学演示，非用户掌握证据）
# 句子: "我爱机器学习"  d_model=4, 单头, 1 层 Block, 词表 6
# 所有权重随机虚构（seed=42），输出 token 无语义 —— 本演示只看数据流和 shape
import math, random

random.seed(42)
NEG = float('-inf')

def mat(A, B):  # 纯 Python 矩阵乘
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]

def T(A):  # 转置
    return [list(r) for r in zip(*A)]

def add(A, B):
    return [[a + b for a, b in zip(ra, rb)] for ra, rb in zip(A, B)]

def relu(A):
    return [[max(0.0, x) for x in r] for r in A]

def softmax(v):  # 数值稳定，支持 -inf
    m = max(x for x in v if x != NEG)
    ex = [0.0 if x == NEG else math.exp(x - m) for x in v]
    s = sum(ex)
    return [e / s for e in ex]

def show(name, M, note=""):
    print(f"\n{name}  {len(M)}x{len(M[0])}  {note}")
    for r in M:
        print("   [" + "  ".join(f"{x:6.2f}" for x in r) + "]")

# ---------- 词表与权重（全部虚构） ----------
vocab = ["<pad>", "我", "爱", "机器", "学习", "<eos>"]
ids = [1, 2, 3, 4]                      # "我 爱 机器 学习"
R = lambda r, c: [[round(random.uniform(-0.5, 0.5), 2) for _ in range(c)] for _ in range(r)]
E, Wq, Wk, Wv = R(6, 4), R(4, 4), R(4, 4), R(4, 4)
Wo, W1, W2, Wlm = R(4, 4), R(4, 8), R(8, 4), R(4, 6)

print(f"输入: '{''.join(vocab[i] for i in ids)}'  ids={ids}")
print(f"组件: E 词表嵌入 6x4 | Wq/Wk/Wv/Wo 4x4 | FFN 4->8->4 | lm_head 4x6 | d_model=4, d_k=4")

# ---------- Prefill：整段并行 ----------
X = [E[i] for i in ids]                 # (4,4) 嵌入查找
show("X = 嵌入(查 E 表)", X)

Q, K, V = mat(X, Wq), mat(X, Wk), mat(X, Wv)   # 三次投影 = 注意力里唯一的权重运算
S = [[s / math.sqrt(4) for s in row] for row in mat(Q, T(K))]  # 缩放 1/sqrt(d_k)
for i in range(4):                      # Causal Mask：上三角 -inf
    for j in range(i + 1, 4):
        S[i][j] = NEG
A = [softmax(r) for r in S]             # 每行 softmax
show("A = softmax(mask(S))", A, "← 注意上三角全 0：第 i 行只能看 0..i")

Attn = mat(A, V)                        # 加权求和
H = add(X, mat(Attn, Wo))               # W_O 混合 + 残差1: x + Attn(x)
F = add(H, mat(relu(mat(H, W1)), W2))   # FFN(4->8->ReLU->4) + 残差2

logits_vec = mat([F[-1]], Wlm)[0]       # ★ 只有最后一行进 lm_head: 4维 -> 6维
probs = softmax(logits_vec)
nxt = max(range(6), key=lambda i: probs[i])
print("\nlogits(最后一行·Wlm) =", [f"{x:5.2f}" for x in logits_vec])
print(f"采样概率 = {[f'{p:.2f}' for p in probs]}  → Prefill 产出首 token: '{vocab[nxt]}' (id={nxt})")

# ---------- Decode 一步：只喂新 token，复用缓存 ----------
Kc, Vc = [r[:] for r in K], [r[:] for r in V]   # KV Cache：Prefill 写入 4 行
q1, k1, v1 = mat([E[nxt]], Wq)[0], mat([E[nxt]], Wk)[0], mat([E[nxt]], Wv)[0]
Kc.append(k1); Vc.append(v1)                    # 缓存追加：4 行 → 5 行，历史行原封不动
s1 = [x / math.sqrt(4) for x in [sum(q1[j] * kc[j] for j in range(4)) for kc in Kc]]
a1 = softmax(s1)                                # 无需 mask：缓存里只有过去+当前
o1 = [sum(a1[i] * vc[i] for i in range(5)) for vc in T(Vc)]     # (1,4) 加权 V
h1 = [e + o for e, o in zip(E[nxt], mat([o1], Wo)[0])]           # 残差1
h2 = [a + b for a, b in zip(h1, mat(relu(mat([h1], W1)), W2)[0])]  # FFN + 残差2
p2 = softmax(mat([h2], Wlm)[0])
n2 = max(range(6), key=lambda i: p2[i])
print(f"\n--- Decode 步 --- 新 token '{vocab[nxt]}' 仅 1 行过权重(GEMV)")
print(f"缓存: K {len(K)}行 -> {len(Kc)}行 (历史 4 行逐元素未变: {[K[0]==Kc[0], K[3]==Kc[3]]})")
print(f"该步注意力权重(5个历史位置) = {[f'{x:.2f}' for x in a1]}")
print(f"采样概率 = {[f'{p:.2f}' for p in p2]}  → 下一 token: '{vocab[n2]}' (id={n2})")
print("\n要点: ①上三角=0 证明因果 ②缓存只追加不重算 ③过权重的只有新 token 1 行 ④输出无语义，权重是虚构的")

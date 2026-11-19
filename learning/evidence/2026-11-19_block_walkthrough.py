# 单个 Decoder Block 逐步手算演示（AI 教学演示，非用户掌握证据）
# 输入: "什么是注意力机制" 5 个 token, d_model=4, 单头, d_ff=8, 词表 6
# 权重随机虚构(seed=7)；每步打印真实数值
import math, random

random.seed(7)
NEG = float('-inf')

def mat(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]

def T(A): return [list(r) for r in zip(*A)]

def show(name, M, note=""):
    print(f"\n[{name}]  {len(M)}x{len(M[0])}  {note}")
    for r in M:
        print("   [" + "  ".join(("  -inf" if x == NEG else f"{x:6.2f}") for x in r) + "]")

def rmsnorm_row(x, eps=1e-5):
    rms = math.sqrt(sum(v * v for v in x) / len(x) + eps)
    return [v / rms for v in x], rms

def softmax(v):
    m = max(x for x in v if x != NEG)
    ex = [0.0 if x == NEG else math.exp(x - m) for x in v]
    s = sum(ex)
    return [e / s for e in ex]

vocab = ["<pad>", "什么", "是", "注意", "力", "机制"]   # "什么是注意力机制" → 5 个 token
ids = [1, 2, 3, 4, 5]
R = lambda r, c: [[round(random.uniform(-1, 1), 2) for _ in range(c)] for _ in range(r)]
E, Wq, Wk, Wv, Wo, W1, W2, Wlm = R(6, 4), R(4, 4), R(4, 4), R(4, 4), R(4, 4), R(4, 8), R(8, 4), R(4, 6)

print(f"输入: '{''.join(vocab[i] for i in ids)}'  ids={ids}  d_model=4, d_k=4, d_ff=8")
X = [E[i] for i in ids]
show("Step3-0  X = 查嵌入表 E", X)

# ---- 第1行: x_norm = RMSNorm(X) ----
print("\n===== 第1行 RMSNorm：逐行独立计算，演示第0行('什么') =====")
x0 = X[0]
rms0 = math.sqrt(sum(v * v for v in x0) / 4)
xn0 = [v / rms0 for v in x0]
print(f"  第0行 x     = {x0}")
print(f"  RMS = sqrt((x0²+x1²+x2²+x3²)/4) = {rms0:.4f}")
print(f"  第0行 x_norm = 每个元素除以 RMS = {[round(v, 3) for v in xn0]}   ← 整行共享同一个 RMS")
XN = [rmsnorm_row(r)[0] for r in X]
show("Step3-1  x_norm = RMSNorm(X)（每行各自归一）", XN)

# ---- 第2行: attn_out = MaskedSelfAttention(x_norm) ----
Q, K, V = mat(XN, Wq), mat(XN, Wk), mat(XN, Wv)
S = [[s / 2 for s in row] for row in mat(Q, T(K))]
for i in range(5):
    for j in range(i + 1, 5):
        S[i][j] = NEG
A = [softmax(r) for r in S]
show("Step3-2a 打分 S = Q·Kᵀ/√d_k + Causal Mask", S, "上三角 -inf")
show("Step3-2b A = softmax(S) 每行", A, "行0=[1,0,0,0,0]：'什么'只能看自己")
attn = mat(A, V)
show("Step3-2c 加权求和 A·V", attn)
attn_o = mat(attn, Wo)

# ---- 第3行: H = X + attn_out ----
H = [[x + a for x, a in zip(rx, ra)] for rx, ra in zip(X, attn_o)]
print("\n===== 第3行 残差：H = X + attn_out（逐元素加，演示第0行） =====")
print(f"  X[0]       = {X[0]}")
print(f"  attn_out[0]= {[round(v, 2) for v in attn_o[0]]}")
print(f"  H[0]       = {[round(v, 2) for v in H[0]]}   ← 加回主流，不是替换")
show("Step3-3  H 全貌", H)

# ---- 第4-6行: FFN + 残差 ----
h_norm = [rmsnorm_row(r)[0] for r in H]
hidden = [[max(0.0, v) for v in r] for r in mat(h_norm, W1)]   # ReLU(→8维)
ffn_out = mat(hidden, W2)
X2 = [[h + f for h, f in zip(rh, rf)] for rh, rf in zip(H, ffn_out)]
print("\n===== 第4-5行 FFN：演示第0行（4 -> 8 -> ReLU -> 4） =====")
print(f"  h_norm[0]      = {[round(v, 3) for v in h_norm[0]]}")
print(f"  升维·W1 后(8维)= {[round(v, 2) for v in mat([h_norm[0]], W1)[0]]}")
print(f"  ReLU 后        = {[round(v, 2) for v in hidden[0]]}")
print(f"  降维·W2 后     = {[round(v, 2) for v in ffn_out[0]]}")
print("===== 第6行 第二次残差：X2 = H + ffn_out =====")
show("Block 输出 X2", X2, "形状 (5,4) 与输入 X 完全相同 → 可堆下一层")

# ---- Step4-6: 最终归一 + lm_head（只算最后一行） ----
last = rmsnorm_row(X2[-1])[0]
logits = mat([last], Wlm)[0]
probs = softmax(logits)
nxt = max(range(6), key=lambda i: probs[i])
print("\n===== Step4-6（Prefill 收尾） =====")
print(f"  只有最后一行('机制'位置)进 lm_head: logits = {[round(v, 2) for v in logits]}")
print(f"  softmax → 概率 = {[f'{p:.2f}' for p in probs]}")
print(f"  采样 → 下一 token: '{vocab[nxt]}' (id={nxt})   ← 权重虚构，无语义")

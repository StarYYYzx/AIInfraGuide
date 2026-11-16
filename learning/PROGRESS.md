# AI Infra 学习进展记录

> 自动由 progress.json 生成。修改真实状态后运行 python learning/tools/progress.py render；不直接改本文件。

- 更新：2026-11-16（revision 3）
- 主线验收通过：0/120 学习日
- 当前：第1学习日 / W1D1 / 系统地图与培训前导入
- 状态：in_progress；能力证据等级：explained
- 已核实学习事实：仅完成课程规划、文档索引和接手档案；尚无用户答题、练习或实验结果证明掌握。

## 下一位AI从这里继续

- 首读顺序：[I11 · 1.1-LLM推理基础](../docs/guides/%E6%A8%A1%E5%9D%97%E5%9B%9B-%E6%8E%A8%E7%90%86%E4%BC%98%E5%8C%96/%E7%AC%AC1%E7%AB%A0-LLM%E6%8E%A8%E7%90%86%E5%9F%BA%E7%A1%80/1.1-LLM%E6%8E%A8%E7%90%86%E5%9F%BA%E7%A1%80.md) → [R0 · AI Infra学习路线](../docs/guides/AI%20Infra%E5%AD%A6%E4%B9%A0%E8%B7%AF%E7%BA%BF.md)
- 当天限定范围：I11§1–3：只读Prefill/Decode、KV和TTFT/TPOT/E2E；R0只看路线与验收
- 当前精确断点：I11 §1-3：§1-2 复述通过(explained)；§3 指标算例未做；Memory-bound 判据与 Transformer Q/K/V 基础双回补中
- 下一动作：回补模式：按 remediation_stack 第二条读 3.2/3.3/3.7 限定小节并回答三问；回补通过后先答 Memory-bound 判据题，再补 §3 指标算例，最后判 Day1 gate。
- 待提问：回补验收三问（3.2/3.3/3.7 限定小节）：①'过一遍网络'过的是什么②K/V 从哪来、为什么缓存 K/V 不缓存 Q③Causal Mask 为什么让 Prefill 能并行而因果不乱。回补完成后回到原题：不借助提示说明 Decode 为何访存受限。
- 回补栈：原目标：Day1 gate 独立练习通过 I11 §1-3 → 当前回补：算术强度判据（每步读固定权重+当前全部KV，只换回1个token的计算）→ 返回条件：不借助提示说出 Decode 每步读取字节数大而计算量极小、时间由显存带宽主导，故为 Memory-bound → 原目标：Day1 gate 独立练习通过 → 当前回补：Transformer 最小基础（Q/K/V 投影来源、Decoder Block 逐层结构、lm head）→ 返回条件：能答出三问——①过一遍网络过的是什么②K/V从哪来为何缓存它们③Causal Mask为何允许Prefill并行；限定阅读 3.2§2.2-2.3/§4.1-4.2、3.3§2-3、3.7§2-3.2
- 下次汇报：已讲解并复述通过：Prefill并行处理已知Prompt（决定TTFT）、Decode每步串行+更新KV Cache（决定TPOT）；KV Cache账例0.5MB/token。未验证：Memory-bound判据未独立复现；指标算例未做。

## 当前阻塞与环境

- Memory-bound 机制未独立复现，Day1 gate 未通过，cursor 停留 Day1。
- GPU/实测环境未确认（不影响理论环节）。
- 用户指示：时间灵活，不按固定分钟计时，有时间时主动来窗口即可。

- 环境：本地课程可读；跨设备应重新核对软件与硬件。
- 实验条件：GPU型号、运行时、模型/数据权限和多卡条件均未确认。

## 最近会话

- [learning/sessions/2026-11-16_01.md](sessions/2026-11-16_01.md)
- [learning/sessions/2026-11-16_00_setup.md](sessions/2026-11-16_00_setup.md)

## 120学习日进度

[完整逐日进度表](DAY_PROGRESS.csv) · [文档能力清单](NODE_PROGRESS.csv) · [课程索引](2026-11-16_AIInfra_逐日文档与概念回补索引.md)

| 学习日 | 主课 | 状态 | 证据等级 | 最近会话 |
|---|---|---|---|---|
| 1 / W1D1 | I11 → R0 | in_progress | explained | learning/sessions/2026-11-16_01.md |
| 2 / W1D2 | P4 → P2 | not_started | unverified | — |
| 3 / W1D3 | Q41 | not_started | unverified | — |
| 4 / W1D4 | P3 → P2 | not_started | unverified | — |
| 5 / W1D5 | I11 → P4 → Q41 → P2 | not_started | unverified | — |
| 6 / W2D1 | R1 → T2 → T9 | not_started | unverified | — |
| 7 / W2D2 | T8 → I12 → P3 | not_started | unverified | — |
| 8 / W2D3 | E91 → I11 | not_started | unverified | — |
| 9 / W2D4 | P1 | not_started | unverified | — |
| 10 / W2D5 | I11 → T2 → E91 | not_started | unverified | — |
| 11 / W3D1 | P2 → P3 | not_started | unverified | — |
| 12 / W3D2 | P2 | not_started | unverified | — |
| 13 / W3D3 | P2 → P3 | not_started | unverified | — |
| 14 / W3D4 | P3 → P2 | not_started | unverified | — |
| 15 / W3D5 | P3 | not_started | unverified | — |
| 16 / W4D1 | T1 → T9 → T2 | not_started | unverified | — |
| 17 / W4D2 | T3 → P2 | not_started | unverified | — |
| 18 / W4D3 | T3 | not_started | unverified | — |
| 19 / W4D4 | T4 → P2 | not_started | unverified | — |
| 20 / W4D5 | T3 → T4 → T2 | not_started | unverified | — |
| 21 / W5D1 | T5 → T9 | not_started | unverified | — |
| 22 / W5D2 | T6 → P2 | not_started | unverified | — |
| 23 / W5D3 | T7 → T2 | not_started | unverified | — |
| 24 / W5D4 | T8 → T9 → P2 | not_started | unverified | — |
| 25 / W5D5 | T7 → T8 → P2 | not_started | unverified | — |
| 26 / W6D1 | P3 → P1 | not_started | unverified | — |
| 27 / W6D2 | P3 | not_started | unverified | — |
| 28 / W6D3 | P3 | not_started | unverified | — |
| 29 / W6D4 | P3 → P2 | not_started | unverified | — |
| 30 / W6D5 | P3 | not_started | unverified | — |
| 31 / W7D1 | D31 → D11 → P2 | not_started | unverified | — |
| 32 / W7D2 | P2 | not_started | unverified | — |
| 33 / W7D3 | P3 → P2 | not_started | unverified | — |
| 34 / W7D4 | P3 → P2 | not_started | unverified | — |
| 35 / W7D5 | P3 → I11 | not_started | unverified | — |
| 36 / W8D1 | C11 → P1 → P4 | not_started | unverified | — |
| 37 / W8D2 | C12 | not_started | unverified | — |
| 38 / W8D3 | C13 | not_started | unverified | — |
| 39 / W8D4 | C14 | not_started | unverified | — |
| 40 / W8D5 | C14 → P1 | not_started | unverified | — |
| 41 / W9D1 | C21 | not_started | unverified | — |
| 42 / W9D2 | C22 → P2 | not_started | unverified | — |
| 43 / W9D3 | C23 | not_started | unverified | — |
| 44 / W9D4 | C24 | not_started | unverified | — |
| 45 / W9D5 | C22 → C23 → C24 | not_started | unverified | — |
| 46 / W10D1 | C31 | not_started | unverified | — |
| 47 / W10D2 | C31 → C24 | not_started | unverified | — |
| 48 / W10D3 | C31 → C21 | not_started | unverified | — |
| 49 / W10D4 | C31 → P2 | not_started | unverified | — |
| 50 / W10D5 | C31 | not_started | unverified | — |
| 51 / W11D1 | P2 → C41 | not_started | unverified | — |
| 52 / W11D2 | C41 | not_started | unverified | — |
| 53 / W11D3 | C41 → C13 | not_started | unverified | — |
| 54 / W11D4 | C41 → P2 | not_started | unverified | — |
| 55 / W11D5 | C41 | not_started | unverified | — |
| 56 / W12D1 | C41 → C23 | not_started | unverified | — |
| 57 / W12D2 | C22 → C41 | not_started | unverified | — |
| 58 / W12D3 | C41 | not_started | unverified | — |
| 59 / W12D4 | C41 → P4 | not_started | unverified | — |
| 60 / W12D5 | C41 | not_started | unverified | — |
| 61 / W13D1 | P2 → C51 | not_started | unverified | — |
| 62 / W13D2 | C51 → C31 | not_started | unverified | — |
| 63 / W13D3 | C52 → P2 | not_started | unverified | — |
| 64 / W13D4 | C51 → C52 | not_started | unverified | — |
| 65 / W13D5 | C51 → C52 | not_started | unverified | — |
| 66 / W14D1 | T3 → C61 | not_started | unverified | — |
| 67 / W14D2 | C61 → C41 | not_started | unverified | — |
| 68 / W14D3 | C52 → C61 | not_started | unverified | — |
| 69 / W14D4 | C62 → C23 | not_started | unverified | — |
| 70 / W14D5 | C61 → C62 | not_started | unverified | — |
| 71 / W15D1 | C71 | not_started | unverified | — |
| 72 / W15D2 | C71 → C51 | not_started | unverified | — |
| 73 / W15D3 | P3 → R2 → OC8 | not_started | unverified | — |
| 74 / W15D4 | C23 → C22 → P4 | not_started | unverified | — |
| 75 / W15D5 | C71 | not_started | unverified | — |
| 76 / W16D1 | D11 → D31 | not_started | unverified | — |
| 77 / W16D2 | P6 → D21 | not_started | unverified | — |
| 78 / W16D3 | D21 → P6 | not_started | unverified | — |
| 79 / W16D4 | D12 → P1 | not_started | unverified | — |
| 80 / W16D5 | D12 → D21 | not_started | unverified | — |
| 81 / W17D1 | D41 → D42 | not_started | unverified | — |
| 82 / W17D2 | P3 → OD8 → P2 | not_started | unverified | — |
| 83 / W17D3 | D41 → D42 → OD5 | not_started | unverified | — |
| 84 / W17D4 | OD6 → OD7 → T4 → V62 → V63 | not_started | unverified | — |
| 85 / W17D5 | D42 | not_started | unverified | — |
| 86 / W18D1 | I21 → I11 | not_started | unverified | — |
| 87 / W18D2 | I22 | not_started | unverified | — |
| 88 / W18D3 | I23 → T9 | not_started | unverified | — |
| 89 / W18D4 | I24 → I25 | not_started | unverified | — |
| 90 / W18D5 | I12 → I11 | not_started | unverified | — |
| 91 / W19D1 | N31 → N32 | not_started | unverified | — |
| 92 / W19D2 | N33 | not_started | unverified | — |
| 93 / W19D3 | N34 | not_started | unverified | — |
| 94 / W19D4 | N35 → N36 | not_started | unverified | — |
| 95 / W19D5 | N32 → N34 → N35 → N36 | not_started | unverified | — |
| 96 / W20D1 | Q41 → P2 | not_started | unverified | — |
| 97 / W20D2 | Q41 → Q42 | not_started | unverified | — |
| 98 / W20D3 | Q42 | not_started | unverified | — |
| 99 / W20D4 | Q43 → P2 | not_started | unverified | — |
| 100 / W20D5 | Q46 → I12 | not_started | unverified | — |
| 101 / W21D1 | Q44 → Q45 | not_started | unverified | — |
| 102 / W21D2 | Q45 → P2 → P5 | not_started | unverified | — |
| 103 / W21D3 | Q45 | not_started | unverified | — |
| 104 / W21D4 | E91 → Q46 | not_started | unverified | — |
| 105 / W21D5 | Q46 | not_started | unverified | — |
| 106 / W22D1 | E91 | not_started | unverified | — |
| 107 / W22D2 | C12 → P2 → E91 | not_started | unverified | — |
| 108 / W22D3 | E91 → P3 | not_started | unverified | — |
| 109 / W22D4 | Q46 → E91 | not_started | unverified | — |
| 110 / W22D5 | E91 → I11 | not_started | unverified | — |
| 111 / W23D1 | S51 → S54 | not_started | unverified | — |
| 112 / W23D2 | V61 → V62 → V63 → V64 | not_started | unverified | — |
| 113 / W23D3 | V65 → V66 → D12 | not_started | unverified | — |
| 114 / W23D4 | S55 → V66 | not_started | unverified | — |
| 115 / W23D5 | S54 → V61 | not_started | unverified | — |
| 116 / W24D1 | R0 → I11 → Q46 → E91 | not_started | unverified | — |
| 117 / W24D2 | I12 → I11 | not_started | unverified | — |
| 118 / W24D3 | Q46 → C31 → C41 | not_started | unverified | — |
| 119 / W24D4 | P3 → R2 → N36 | not_started | unverified | — |
| 120 / W24D5 | R0 | not_started | unverified | — |

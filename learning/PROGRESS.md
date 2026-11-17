# AI Infra 学习进展记录

> 自动由 progress.json 生成。修改真实状态后运行 python learning/tools/progress.py render；不直接改本文件。

- 更新：2026-11-17（revision 4）
- 主线验收通过：0/120 学习日
- 当前：第1学习日 / W1D1 / 系统地图与培训前导入
- 状态：in_progress；能力证据等级：explained
- 已核实学习事实：11-16会话证据支持I11§1–2复述通过；Day1仍in_progress/explained。指标算例未做，Transformer数据流与访存判据需回补，尚无实测。11-17仅更新指导与资源事实，不增加学习通过项。

## 下一位AI从这里继续

- 首读顺序：[T2 · 3.2 Transformer全貌及代码实现](../docs/guides/%E6%A8%A1%E5%9D%97%E4%B8%80-%E5%89%8D%E7%BD%AE%E7%9F%A5%E8%AF%86/transformer/3.2%20Transformer%E5%85%A8%E8%B2%8C%E5%8F%8A%E4%BB%A3%E7%A0%81%E5%AE%9E%E7%8E%B0.md) → [T3 · 3.3 Self-Attention机制深入理解](../docs/guides/%E6%A8%A1%E5%9D%97%E4%B8%80-%E5%89%8D%E7%BD%AE%E7%9F%A5%E8%AF%86/transformer/3.3%20Self-Attention%E6%9C%BA%E5%88%B6%E6%B7%B1%E5%85%A5%E7%90%86%E8%A7%A3.md) → [T7 · 3.7 Transformer Decoder Block完整解析](../docs/guides/%E6%A8%A1%E5%9D%97%E4%B8%80-%E5%89%8D%E7%BD%AE%E7%9F%A5%E8%AF%86/transformer/3.7%20Transformer%20Decoder%20Block%E5%AE%8C%E6%95%B4%E8%A7%A3%E6%9E%90.md) → [I11 · 1.1-LLM推理基础](../docs/guides/%E6%A8%A1%E5%9D%97%E5%9B%9B-%E6%8E%A8%E7%90%86%E4%BC%98%E5%8C%96/%E7%AC%AC1%E7%AB%A0-LLM%E6%8E%A8%E7%90%86%E5%9F%BA%E7%A1%80/1.1-LLM%E6%8E%A8%E7%90%86%E5%9F%BA%E7%A1%80.md) → [P2 · 第2章-数学基础](../docs/guides/%E6%A8%A1%E5%9D%97%E4%B8%80-%E5%89%8D%E7%BD%AE%E7%9F%A5%E8%AF%86/%E7%AC%AC2%E7%AB%A0-%E6%95%B0%E5%AD%A6%E5%9F%BA%E7%A1%80.md) → [P4 · gpu-basics](../docs/guides/%E6%A8%A1%E5%9D%97%E4%B8%80-%E5%89%8D%E7%BD%AE%E7%9F%A5%E8%AF%86/gpu/gpu-basics.md)
- 当前计划版本：2026-11-17.1（[近期更新](PLAN_UPDATE_2026-11-17.md)，实际回补栈优先）
- 当天限定范围：保留Day1：先T2§5.3/6.1–6.2（Decoder-only）→T3§2/3.1–3.5→T7§2–3.2；必要补T9词嵌入与P2§2；回到I11§3指标算例及§4瓶颈，算术强度补P2§3.2–3.3/P4§3.3。分多个工作日，一次一题。
- 当前精确断点：I11 §1-3：§1-2 复述通过(explained)；§3 指标算例未做；Memory-bound 判据与 Transformer Q/K/V 基础双回补中
- 下一动作：按11-17更新：T2§5.3/6.1-6.2→T3§2/3.1-3.5→T7§2-3.2；一次一题等待回答，回补通过再做I11§3指标算例及§4条件化瓶颈解释，最后判Day1 gate。环境核对仅准备，不推进学习成绩；通过后依次Day2必要硬件/数值、Day3最小推理。
- 待提问：先只问第一题：一个token ID怎样变成隐藏状态，经多层Decoder Block和lm head得到logits并选出下一token？等待用户回答后再问QKV来源/缓存与causal mask；不要一次抛三问或直接给答案。
- 回补栈：原目标：Day1 gate 独立练习通过 I11 §1-3 → 当前回补：算术强度判据（每步读固定权重+当前全部KV，只换回1个token的计算）→ 返回条件：不借助提示说明低batch等条件下权重复用低、FLOPs/Bytes低为何可能访存受限，并知道batch/上下文/backend会改变瓶颈；不把所有Decode视作必然Memory-bound → 原目标：Day1 gate 独立练习通过 → 当前回补：Transformer 最小基础（Q/K/V 投影来源、Decoder Block 逐层结构、lm head）→ 返回条件：能答出三问——①过一遍网络过的是什么②K/V从哪来为何缓存它们③Causal Mask为何允许Prefill并行；限定首读 T2(3.2)§5.3/§6.1-6.2→T3(3.3)§2/§3.1-3.5→T7(3.7)§2-3.2；3.2§2/§4仅Encoder-Decoder背景。输入/shape不懂补T9/P2必要小节
- 下次汇报：已讲解并复述通过：Prefill并行处理已知Prompt（决定TTFT）、Decode每步串行+更新KV Cache（决定TPOT）；KV Cache账例0.5MB/token。未验证：Memory-bound判据未独立复现；指标算例未做。

## 当前阻塞与环境

- Memory-bound 机制未独立复现，Day1 gate 未通过，cursor 停留 Day1。
- 11-17用户报告Pro6000服务器已可用；具体SKU、显存、驱动/运行时、模型/数据与权限仍待核，不宣称可运行或已测。
- 用户指示：时间灵活，不按固定分钟计时，有时间时主动来窗口即可。

- 环境：11-17用户报告Pro6000服务器已可用；这是资源可用自述，不是现场配置核验。
- 实验条件：具体GPU型号/显存、操作系统、驱动、隔离环境、PyTorch/CUDA/vLLM、模型授权、下载/执行权限与共享资源规则待核；没有实际连接、安装或运行。

## 最近会话

- [learning/sessions/2026-11-17_00_plan_update.md](sessions/2026-11-17_00_plan_update.md)
- [learning/sessions/2026-11-16_01.md](sessions/2026-11-16_01.md)
- [learning/sessions/2026-11-16_00_setup.md](sessions/2026-11-16_00_setup.md)

## 120学习日进度

[完整逐日进度表](DAY_PROGRESS.csv) · [文档能力清单](NODE_PROGRESS.csv) · [课程索引](2026-11-16_AIInfra_逐日文档与概念回补索引.md)

| 学习日 | 主课 | 状态 | 证据等级 | 最近会话 |
|---|---|---|---|---|
| 1 / W1D1 | T2 → T3 → T7 → I11 → P2 → P4 | in_progress | explained | learning/sessions/2026-11-16_01.md |
| 2 / W1D2 | P4 → P2 → P1 → I12 | not_started | unverified | — |
| 3 / W1D3 | I12 → I11 → P3 | not_started | unverified | — |
| 4 / W1D4 | P3 → P2 → Q41 → Q45 → E91 | not_started | unverified | — |
| 5 / W1D5 | I11 → I12 → P2 → Q41 | not_started | unverified | — |
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

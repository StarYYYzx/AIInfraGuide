# 任意AI接手协议

## 目标与不可变约定

- 系统学习AI Infra为主线：评测导入→必要前置与训练→CUDA算子→分布式→引擎/量化/端侧。实习只作一个关联案例或明确截止的补充。
- 时间灵活，以一个闭环为单位；75分钟仅参考，不固定计时、不报告超支。可分限定阅读、独立练习与汇报整理，周末不学习、不整理、不补课；休假与验收失败按工作日顺延。
- 最新近期指导见PLAN_UPDATE_2026-11-17.md与plan_update.json；实际cursor/回补栈优先于近期覆盖，再看curriculum.json，禁止回到旧首读安排。
- 导师每天见面；晨间汇报上一工作日，周一材料周五准备。每天汇报一个核心问题和真实证据，不要求每日PPT。
- 数据/服务器/板子条件没有确认时不预设可用GPU、多卡、FP4或特定软件栈。
- 文件图谱是教学建议，不是官方引用；正文、复习、提纲分开。概览可以先读，深入小节卡住再回补，避免必须先读完全部前置的死锁。

## 3分钟接手

1. 如果能执行Git：在改动前检查 `git status --short`；干净时先拉取本fork最新记录。脏工作区不能自动覆盖，先告知用户并解决。
2. 读取 `progress.json`（唯一当前状态），看revision、cursor.day/section、remediation_stack、pending_question、next_action、blockers及recent_sessions。
3. 只读取最近相关会话/证据，先看plan_update.json和PLAN_UPDATE_2026-11-17.md近期指导，再看该日curriculum.json.days[day-1]（生成后已应用覆盖）；实际回补栈优先。定位nodes[id].path。服务器可用自述不等于配置核验；Day1未过不直接进入最小推理。
4. 向用户用两三句复述：已核实什么、断点在哪里、今天要验证什么。若时间不足，用一个复习题降级，不增加周末作业。
5. 从pending_question开始；一次一题，等待用户回答。已通过的小节不从零重教，未过的回补/练习必须继续；不因为日期已经过了11-16就跳过Day1。

## 每次教学循环

诊断一题→定位具体小节→解释/推导→用户独立复述或做题→指出错误并重验→记录证据→准备导师汇报→保留精确断点。

遇到概念不懂：查 `curriculum.json.concepts` 或文字索引；沿requires只补相关小节。remediation_stack按“原目标 / 当前回补 / 返回条件”记录，回补不是新的主线学习日，不自动推进cursor。

教学时必须区分：用户原回答、AI提示、修正后回答、是否借助答案、验收结论。AI自己生成的解答不算用户掌握证据。长课文只读指定节，实验跨多日正常。

## 进度真相源和字段协议

`progress.json`是可修改的当前状态；`sessions/`是追加式过程与证据历史；`PROGRESS.md`及两个CSV是派生视图，不能作为第二个可独立编辑的状态源。图谱只是导航，点击/选日不改变学习状态，不使用浏览器localStorage做跨设备进度。

- `revision`每次状态更新加1；`updated_at`填写实际日期，禁止凭日期推断进度。
- `cursor`记录最早未验收的主线日、目标文档、小节、pending_question、next_action、返回栈。
- 每日 `status`：not_started / in_progress / blocked / passed。
- `level`：unverified / read / explained / exercise_passed / measured；能力是分层证据，不意味着后者自动覆盖整篇所有小节。
- `gate`：pending / exercise / measurement。普通学习日通过独立练习即可passed；明确实验日若没有实际运行，应blocked或in_progress，不能用代码走读替代实测验收。
- `days[n].sessions`与`evidence`写仓库根相对路径；禁止私人绝对路径。`nodes[id].notes`必须限定实际学过的小节，不能将一个小节推成全篇掌握。
- 要标exercise_passed/measured必须附证据；measured至少包含可复现环境、输入、命令/代码位置、结果和测量边界。测量需要实际运行，不允许编造数值。
- 主线passed连续推进；暂时先学未来章节只记录节点/会话，不跳过未完成主线。推进cursor到下一日时更新该日目标、scope和问题。
- 未确认的自述可以记录“用户自述，待验收”，仍保持unverified；先做短诊断再调整。

## 会话结束的写入顺序

1. 复制 `templates/SESSION_TEMPLATE.md` 为 `sessions/YYYY-MM-DD_NN.md`（按真实日期、当日递增序号，跨设备避免同名覆盖）。完成后历史不重写；修正另追加新记录并引用旧会话。
2. 将可公开的练习/图/代码/日志写入 `evidence/`，使用相对链接；含公司数据的证据仅记脱敏结论，不上传原件。
3. 更新progress.json：revision/updated_at、当天level/status/gate/refs、相关node限定小节、cursor/blockers/recent_sessions（最近5条，完整历史仍在sessions）。
4. 运行 `python learning/tools/progress.py render`，校验并生成PROGRESS.md/CSV。验证失败先修真实记录，不降低验证规则。
5. 读回摘要，向用户说明这次真正通过什么、还缺什么、下次从哪一题继续。
6. 检查Git差异和敏感内容；按README同步。推送失败明确说明本地已保存、远端未更新，不伪称跨设备同步完成。

## 汇报卡

当前问题 / 课程位置 / 我自己的解释 / 一张推导或对照证据 / 未验证部分 / 一条可选实习关联 / 下一工作日目标。

无新实测可汇报修正推导、失败实验与错误定位；三条prompt只叫冒烟，不叫完整质量评测；小样本不报告稳定P95/P99。

## 冲突与保密

两台设备不得同时编辑同一进度；每次开始先pull，结束commit/push。冲突不能直接选ours/theirs，必须合并会话历史后逐条核对真实进度并提高revision。不得强推、硬重置、改写已共享历史、绕过钩子或偷偷更改提交身份。

仓库可能公开：不上传公司名称/会议原文、内网地址、账号、密钥、专有SDK、未授权数据、私人机器路径、原始实验输出。只保留通用任务和经用户认可的脱敏学习证据。

## 能力不足时

没有本地执行能力：仍可读JSON/Markdown指导，向用户给出精确拟修改字段与会话内容，但不可声称已经写入或同步。没有GPU：做原理/走读并保留待实测。没有完整专题：列已有基础和外补缺口，不虚构课程文件。

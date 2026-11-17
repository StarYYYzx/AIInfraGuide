# AI Agent 学习指导入口

本fork同时用于个人AI Infra学习。课程正文在 `docs/guides/`，学习档案在 `learning/`。

## 接手必读顺序

1. `learning/AI_HANDOFF.md`：教学规则与记录协议。
2. `learning/progress.json`：唯一当前进度真相源；确认revision、cursor、最近会话与阻塞。
3. `learning/PROGRESS.md`：人类可读摘要，若与JSON不一致，以JSON及会话证据核查，不盲信自动摘要。
4. `learning/curriculum.json`：当前学习日首读ID、小节范围、概念回补与依赖。
5. `progress.json`指向的最近会话/证据，再读取当前课文对应小节。

不要先通读整仓库或全部3000行索引。课程为主线，工作日时间灵活，75分钟仅参考且含汇报；周末不学、不整理、不补课。计划完成不等于学习掌握。

当前状态每次以progress.json及最近证据为准，不能照初始化文字重新开始。最新执行补充见learning/PLAN_UPDATE_2026-11-17.md及plan_update.json；先回补Decoder-only数据流/QKV，再返回Day1指标与瓶颈验收，之后核环境、最小推理。一次一题，等用户回答；不把计划或服务器可用当实测。

用户时间灵活，75分钟仅参考，不固定计时、不报告超支。Pro6000已可用为用户报告，具体SKU/显存/软件/权限待核。培训12个Day与个人120学习日独立，不按培训日期跳课程。

会话结束更新JSON、追加会话证据，运行 `python learning/tools/progress.py render`。支持Git时按使用说明同步；需要授权或冲突时停下说明，禁止强推、覆盖远程记录或提交敏感资料。

本入口只指导学习档案工作；不要求修改课程原文、网站或构建配置。

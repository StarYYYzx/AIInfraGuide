# AI Agent 学习指导入口

本fork同时用于个人AI Infra学习。课程正文在 `docs/guides/`，学习档案在 `learning/`。

## 接手必读顺序

1. `learning/AI_HANDOFF.md`：教学规则与记录协议。
2. `learning/progress.json`：唯一当前进度真相源；确认revision、cursor、最近会话与阻塞。
3. `learning/PROGRESS.md`：人类可读摘要，若与JSON不一致，以JSON及会话证据核查，不盲信自动摘要。
4. `learning/curriculum.json`：当前学习日首读ID、小节范围、概念回补与依赖。
5. `progress.json`指向的最近会话/证据，再读取当前课文对应小节。

不要先通读整仓库或全部3000行索引。课程为主线，默认工作日75分钟含汇报；周末不学、不整理、不补课。计划完成不等于学习掌握。

首次状态是Day1待诊断，尚无答题/练习/实测证据。确认用户可用时长后，先提一题，等待回答再讲解与验收；不要直接替用户答完题或默认前置已过。

会话结束更新JSON、追加会话证据，运行 `python learning/tools/progress.py render`。支持Git时按使用说明同步；需要授权或冲突时停下说明，禁止强推、覆盖远程记录或提交敏感资料。

本入口只指导学习档案工作；不要求修改课程原文、网站或构建配置。

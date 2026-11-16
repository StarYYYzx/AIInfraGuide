# AI Infra 跨设备学习档案 · 使用说明

## 从哪里开始

- [当前真实学习进度](PROGRESS.md)：任何设备/AI先看它，并核对[progress.json](progress.json)。
- [AI接手协议](AI_HANDOFF.md)：新AI必读；仓库根[AGENTS.md](../AGENTS.md)也会指向这里。
- [逐日文档与概念回补索引](2026-11-16_AIInfra_逐日文档与概念回补索引.md)。
- [交互知识图谱HTML](2026-11-16_AIInfra_文档级学习知识图谱.html)：下载/clone仓库后本地打开。GitHub文件页面不会直接运行HTML；需要下载后打开，不代表已经部署GitHub Pages。
- [全部120日进度](DAY_PROGRESS.csv) / [文档能力记录](NODE_PROGRESS.csv)。

初始进度为Day1待诊断，0/120日验收通过。导航、学习计划与档案已创建，但没有用户答题/练习/实测证据，所以不标任何课程已掌握。

## 文件职责

| 文件 | 用途 | 修改规则 |
|---|---|---|
| progress.json | 当前断点、能力、阻塞、证据引用、revision | 唯一当前状态源，由AI据证据更新 |
| PROGRESS.md / DAY_PROGRESS.csv / NODE_PROGRESS.csv | 人类可读派生视图 | 由脚本生成，不独立改状态 |
| curriculum.json | 120日首读/范围、102文档、概念依赖 | 由图谱脚本生成；不是学习进度 |
| sessions/ | 每次学习过程及用户回答/验收 | 每会话新文件，追加历史 |
| evidence/ | 脱敏练习、推导、实验和汇报证据 | 必须可复查，不放公司敏感原料 |
| templates/ | 会话、证据、汇报模板 | 复制使用，不当真实完成记录 |
| tools/ | 跨设备路径解析/生成/验证 | Python3标准库，无需第三方包 |

课程路径全部相对仓库根，不再依赖某台Windows电脑的盘符。HTML课文链接支持相对路径和GitHub在线查看；“复制路径”复制仓库相对路径。

## 每天与AI怎么学

把仓库文件夹交给AI，并发送：

> 请先读AGENTS.md、learning/AI_HANDOFF.md、learning/progress.json与最近会话。按当前断点带我学习，不把计划当已完成。我今天有75分钟。先告诉我已核实进展，再提一个诊断/验收题，等待我回答；结束更新学习档案和导师汇报卡，检查后同步GitHub。周末不学。

每天只推进一个核心问题。先读首读的限定小节，不懂再查概念回补，补完返回目标。验收没过接续同一个学习日，不因日期改变自动跳日。

## 跨设备Git流程

首次获取（Git命令在终端执行）：

```bash
git clone https://github.com/StarYYYzx/AIInfraGuide.git
```

进入clone出的仓库后，每次学习前：

```bash
git status --short
git pull --ff-only origin main
python learning/tools/progress.py check
```

若工作区有修改、分支不是main、pull失败或出现冲突，停止并核对，不覆盖本地/远程记录。在原工作区，保留原origin，上述origin替换为用户fork远程 `learning-fork`。

每次学习结束，AI按接手协议写记录，然后：

```bash
python learning/tools/progress.py render
git diff --check
git status --short
git add learning AGENTS.md
git diff --cached --stat
git commit -m "Record AI Infra learning session"
git push origin main
```

推送前必须查看实际暂存差异并确认没有敏感内容，而不只看统计。原工作区使用 `git push learning-fork main`，不推到课程原仓库。不使用force/reset hard；不绕过钩子。不要复制token到记录里。

换设备必须先结束并推送上一设备；提交与push不是自动发生，必须看到push成功。若无写权限，通过GitHub账号授予正常仓库访问，不在聊天或文档中暴露密钥。

## 生成和校验

```bash
python learning/tools/build_learning_graph.py
python learning/tools/progress.py render
python learning/tools/progress.py check
```

图谱生成只重建课程导航，不更改真实progress.json或会话。progress init仅用于首次创建，会拒绝覆盖已有进度。若课程新增/删除，图谱严格校验会提示，需要重新核对分类和计划，再迁移新增节点状态，不能用重置init清空历史。

## 导师汇报与边界

常规5–8分钟，实际以导师安排为准：课程位置→核心问题→自己的解释→证据→未知项→下一工作日。一条实习关联可选，不为了汇报把Infra学习变成每天救火。

周末不学、不整理、不补课；周一材料周五准备。服务器、模型、运行时与数据权限未确认，不假定实验可用。公开仓库只存通用、脱敏学习材料；完整公司会议纪要和私人工作记录不会同步。

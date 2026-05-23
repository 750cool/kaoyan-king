[README.md](https://github.com/user-attachments/files/28172459/README.md)
# Kaoyan Spaced Review

一个本地运行的考研逐页复习系统：把教材内容按页转成填空题卡，记录“知道 / 不知道”，再根据复习结果安排后续复习。

## 功能

- 按教材页码逐页推进复习。
- 将知识点、公式、方法总结、例题转成填空题卡。
- 每张卡支持 `知道` / `不知道` 反馈。
- 本地保存复习记录和下次复习时间。
- 可展示本地教材页图，方便对照原书。
- 支持每日页数规则，例如：
  - 高等数学：每天 30 页。
  - 线性代数：每天 10 页。
  - 概率论与数理统计：每天 10 页。
  - 信号与系统：默认每天 10 页，可自行调整。

## 版权说明

本仓库只开源工具代码和学习流程，不包含任何教材 PDF、扫描页图或受版权保护的教材内容。

请不要提交：

- 教材 PDF。
- 教材扫描图或截图。
- 个人复习记录。
- 从教材中生成的私有题卡数据。
- 大段教材原文。

`.gitignore` 已默认排除这些本地私有文件。你可以在自己电脑上放教材和生成题卡，但不要上传到公开仓库。

## 快速开始

1. 将你自己合法持有的 PDF 放到本地目录：

```text
assets/textbooks/higher_math/
assets/textbooks/linear_algebra/
assets/textbooks/probability/
assets/textbooks/signals_systems/
```

2. 启动本地复习服务：

```bash
node scripts/review_server.js
```

3. 打开浏览器：

```text
http://127.0.0.1:8765/data/review_app/index.html
```

开源版本默认加载 `data/review_app/cards-sample.js` 示例卡片。实际学习时，可以在本地生成或创建 `data/review_app/cards-local.js`，该文件不会被 Git 提交。

## 使用说明

### 用 `cc` 或 `cx` 打开

如果你本地已经配置了 Codex 命令行别名，可以在项目目录中启动：

```bash
cd path/to/kaoyan-spaced-review
cc
```

或：

```bash
cd path/to/kaoyan-spaced-review
cx
```

不同人的别名可能不一样：`cc` / `cx` 本质上都是进入 Codex 工作环境的方式。进入后，让 Codex 读取本项目的 `SKILL.md`，并按你的教材目录生成复习内容即可。

可以直接对 Codex 说：

```text
使用 kaoyan-spaced-review skill，按 page_progress.json 的进度，生成今天的交互式填空复习卡。
高数每天 30 页，线代和概率每天 10 页，专业课默认每天 10 页。
输出到 data/review_app/cards-local.js，并更新 page_progress.json。
```

### 本地启动交互页面

生成卡片后，启动本地服务：

```bash
node scripts/review_server.js
```

然后打开：

```text
http://127.0.0.1:8765/data/review_app/index.html
```

页面中每张卡都有：

- 填空题。
- 查看答案。
- `知道` / `不知道`。
- 可选教材页图。
- 本地复习记录。

### 定时推送

如果你使用 Codex App 的自动任务功能，可以创建一个每天上午 9 点运行的任务。

推荐任务内容：

```text
使用 kaoyan-spaced-review skill 生成当天的交互式填空复习。

要求：
1. 读取 data/plans/daily_page_rules.md 和 data/plans/page_progress.json。
2. 按当前书本和页码继续推进。
3. 高数每天 30 页，线代每天 10 页，概率每天 10 页，专业课默认每天 10 页。
4. 将知识点、公式、方法总结、编号例题转成填空卡。
5. 输出到 data/review_app/cards-local.js。
6. 更新 data/plans/page_progress.json。
7. 确保 scripts/review_server.js 可运行。
8. 最后只回复本地页面链接、今日页码范围、卡片数量、下一次页码。
```

如果不用 Codex App，也可以用系统定时任务实现。

Windows 任务计划程序可以每天 9 点运行：

```powershell
cd path\to\kaoyan-spaced-review
node scripts\review_server.js
```

不过更推荐让 Codex 自动生成当天卡片，再由 `review_server.js` 提供页面服务。

## 目录结构

```text
SKILL.md                         Codex skill 入口
references/                      规划、卡片格式、反幻觉规则
scripts/review_server.js          本地 HTML 服务和复习记录接口
scripts/inspect_pdfs.py           PDF 检查脚本
scripts/plan_due_reviews.py       到期复习卡筛选脚本
scripts/update_review_result.py   复习结果更新脚本
data/review_app/                  交互式复习页面
data/plans/                       页码进度和每日规则
assets/                           本地教材和资料目录
```

## 卡片格式

题卡是 JavaScript 对象，示例：

```js
{
  id: "sample-function-definition",
  page: "PDF p.TBD / 印刷 p.TBD",
  image: "",
  topic: "函数定义",
  prompt: "若每个输入 x 都对应 ____ 个输出 y，则可以把 y 视为 x 的函数。",
  answer: "唯一确定的一",
  source: "sample",
  intervalDays: 0
}
```

## 复习机制

- 点击 `知道`：下次复习时间延后。
- 点击 `不知道`：优先安排到下一次或次日复习。
- 复习记录保存在本地 `data/review_app/review_state.json`。

## 许可证

本仓库中的代码使用 MIT License。

教材、教材截图、以及由教材生成的私有学习数据不包含在本仓库中，也不属于本许可证授权范围。

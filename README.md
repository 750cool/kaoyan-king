[README.md](https://github.com/user-attachments/files/28172334/README.md)
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

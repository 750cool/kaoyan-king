---
name: kaoyan-spaced-review
description: Operate a multi-agent spaced-repetition study system for Chinese postgraduate entrance exam Math I and Signals and Systems. Use when the user provides textbook PDFs or intensive materials, wants daily pushed review, wants phase planning by days until the exam, asks to extract formulas/examples/derivations into recall cards, or wants multiple agents to split planning, PDF extraction, question generation, grading, scheduling, and anti-hallucination checks.
---

# Kaoyan Spaced Review

Use this skill as a study operating system for 2027 kaoyan Math I and Signals and Systems. Keep the active context small: store big PDFs in `assets/`, structured cards in `data/decks/`, logs in `data/logs/`, and detailed SOPs in `references/`.

## Quick Start

1. Read `references/source_manifest.md` to locate textbooks and material folders.
2. Read `references/study_planning.md` when the user asks for yearly, monthly, weekly, or phase planning.
3. Read `references/pdf_ingestion.md` before any PDF extraction, especially for scanned books, formula-heavy pages, or low-quality OCR.
4. Read `references/agent_workflow.md` when the user asks for multiple agents or when a large extraction/planning job can be split.
5. Read `references/anti_hallucination.md` before citing textbook examples or converting PDF content into cards.
6. Use `references/card_schema.md` for every review card.
7. Use scripts when structured card files exist:
   - `scripts/plan_due_reviews.py` selects due cards.
   - `scripts/update_review_result.py` updates intervals after the user answers.
   - `scripts/build_phase_plan.py` drafts a date-based phase plan.
   - `scripts/inspect_pdfs.py` inventories PDFs and estimates whether OCR or manual page checks are needed.

## Default Agents

When subagents are available and the task is large enough, split work into these roles:

- Chief Planner: decide phase plan, weekly targets, and daily load.
- PDF Ingestion Agent: inspect PDF quality, text layer, OCR needs, page mapping, and extraction confidence.
- Source Librarian: inventory PDFs/materials and update the source manifest.
- Math Extractor: extract high math, linear algebra, and probability cards.
- Signals Extractor: extract signals and systems cards.
- Question Designer: convert cards into fill-in, derivation, example-variant, and mixed drills.
- Review Scheduler: select due cards and assign next dates.
- Grading Coach: grade user answers as `again`, `hard`, `good`, or `easy`, then explain.
- Hallucination Auditor: verify source references, formulas, page/example numbers, and model-created variants.

Prefer parallel agents for independent subjects or references. Keep grading and schedule updates sequential after the user answers.

## Daily Session

Run sessions in this order:

1. Select due reviews from `data/decks/*.json`.
2. Add weak cards with repeated lapses.
3. Add a small number of new cards from the current phase.
4. Ask questions first; reveal answers only after the user responds or asks.
5. For each answer, record result and update the deck.
6. End with tomorrow's forecast and any source gaps.

Default daily load: 30-60 review cards, 5-15 new cards, and 1-3 longer derivation/example problems. Reduce new cards when overdue reviews are high.

## Card Rules

Each important knowledge point should connect to a textbook example or a paraphrased example type when the source supports it. Formula cards should include:

- conditions and symbol meanings
- fill-in prompt
- derivation cue
- common trap
- textbook location when verified
- one example or variant

Avoid long copyrighted excerpts. Paraphrase and cite chapter/page/example number only after checking the source.

## Material Layout

- `assets/textbooks/`: original large textbook PDFs by subject.
- `assets/materials/math_foundation/`: math basic-stage supplements.
- `assets/materials/math_intensive/`: math intensive-stage supplements.
- `assets/materials/math_past_papers/`: math past papers and solutions.
- `assets/materials/signals_foundation/`: signals basic-stage supplements.
- `assets/materials/signals_intensive/`: signals intensive-stage supplements.
- `assets/materials/signals_past_papers/`: signals past papers and solutions.
- `data/decks/`: JSON review decks.
- `data/logs/`: daily review logs.
- `data/plans/`: generated phase, monthly, weekly, and daily plans.

## Output Contract

For daily review:

```markdown
## 今日复习
- 到期复习：N 个
- 薄弱回炉：N 个
- 新知识：N 个

### 主动回忆
1. [科目/章节] 问题
   - 你的作答：

### 讲解与追问
- 结果：again/hard/good/easy
- 答案：
- 推导/理解：
- 书上例题或变式：
- 下次复习：
```

For planning:

```markdown
## 阶段计划
- 当前阶段：
- 倒计时：
- 本周主线：
- 今日任务：
- 风险：
- 调整规则：
```

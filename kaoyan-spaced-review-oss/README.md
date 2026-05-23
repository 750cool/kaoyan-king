# Kaoyan Spaced Review

An interactive local study system for turning page-by-page exam preparation into fill-in-the-blank cards with spaced repetition.

## Features

- Page-based textbook workflow.
- Fill-in-the-blank review cards.
- `知道` / `不知道` buttons for every card.
- Local review history and next-review scheduling.
- Optional local page-image display for privately owned materials.
- Daily quotas, for example:
  - Higher mathematics: 30 pages/day.
  - Linear algebra: 10 pages/day.
  - Probability and statistics: 10 pages/day.
  - Signals and systems: configurable, default 10 pages/day.

## Copyright Boundary

This repository is for the tool code and workflow only.

Do **not** commit:

- Textbook PDFs.
- Scanned textbook page images.
- Personal review records.
- Generated cards that closely reproduce copyrighted textbook content.
- Large verbatim textbook excerpts.

The `.gitignore` excludes these files by default. Keep your own textbooks and generated cards local.

## Quick Start

1. Put your privately owned PDFs in the local-only folders:

```text
assets/textbooks/higher_math/
assets/textbooks/linear_algebra/
assets/textbooks/probability/
assets/textbooks/signals_systems/
```

2. Start the local app:

```bash
node scripts/review_server.js
```

3. Open:

```text
http://127.0.0.1:8765/data/review_app/index.html
```

The open-source copy loads `data/review_app/cards-sample.js` by default. For personal study, create a private `data/review_app/cards-local.js` or replace the sample locally. Private card files are ignored by Git.

## Project Layout

```text
SKILL.md                         Codex skill entry point
references/                      Planning, card schema, and anti-hallucination rules
scripts/review_server.js          Local HTML app server and review recorder
scripts/inspect_pdfs.py           PDF inventory helper
scripts/plan_due_reviews.py       Due-card selector
scripts/update_review_result.py   Review result updater
data/review_app/                  Interactive review app
data/plans/                       Page quotas and progress config
assets/                           Local-only materials
```

## Card Shape

Cards are JavaScript objects with fields such as:

```js
{
  id: "sample-function-definition",
  page: "PDF p.TBD / print p.TBD",
  image: "",
  topic: "Function definition",
  prompt: "If each input x maps to ____ output y, y can be treated as a function of x.",
  answer: "one unique",
  source: "sample",
  intervalDays: 0
}
```

## License

MIT for the code in this repository. Textbooks, page images, and generated textbook-derived study data are not included and remain subject to their own copyrights.

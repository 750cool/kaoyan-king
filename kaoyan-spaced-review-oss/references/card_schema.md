# Review Card Schema

Use this schema for JSON decks or Markdown tables.

Required fields:

- `id`: stable slug, e.g. `math-high-derivative-taylor-001`.
- `subject`: `higher_math`, `linear_algebra`, `probability`, or `signals_systems`.
- `chapter`: textbook chapter or topic.
- `source`: textbook/name plus page or section when known.
- `type`: `concept`, `formula`, `derivation`, `method`, `example`, or `trap`.
- `front`: question shown before answer.
- `back`: concise answer and reasoning.
- `example_prompt`: textbook example, paraphrased or transformed into a problem type.
- `difficulty`: 1-5.
- `exam_frequency`: 1-5.
- `interval_days`: current spacing interval.
- `due`: next due date in `YYYY-MM-DD`.
- `lapses`: number of `again` results.

Optional fields:

- `formula_fill_blank`: cloze/fill-in version of a formula.
- `derivation_steps`: short ordered hints, not a full copied textbook section.
- `common_mistakes`: traps and boundary conditions.
- `tags`: short labels such as `fourier`, `laplace`, `series`, `matrix-rank`.
- `history`: dated review results.

Minimal JSON example:

```json
{
  "id": "signals-fourier-time-shift-001",
  "subject": "signals_systems",
  "chapter": "Fourier transform properties",
  "source": "TBD",
  "type": "formula",
  "front": "State the Fourier transform time-shift property and its phase factor.",
  "back": "If x(t) <-> X(jw), then x(t-t0) <-> e^{-jw t0}X(jw). The shift changes phase, not magnitude.",
  "example_prompt": "Given a shifted rectangular pulse, write its transform using the base pulse transform.",
  "difficulty": 3,
  "exam_frequency": 5,
  "interval_days": 1,
  "due": "2026-05-24",
  "lapses": 0
}
```

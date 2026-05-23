#!/usr/bin/env python3
"""Select due spaced-repetition cards from a JSON deck.

Input deck format: a JSON list of card objects following references/card_schema.md.
This script prints due cards as JSON; it does not mutate the deck.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path


def parse_date(value: str | None) -> dt.date:
    if not value:
        return dt.date.today()
    return dt.date.fromisoformat(value)


def priority(card: dict) -> tuple:
    lapses = int(card.get("lapses", 0) or 0)
    exam_frequency = int(card.get("exam_frequency", 3) or 3)
    difficulty = int(card.get("difficulty", 3) or 3)
    interval = int(card.get("interval_days", 1) or 1)
    return (-lapses, -exam_frequency, -difficulty, interval, card.get("id", ""))


def main() -> int:
    parser = argparse.ArgumentParser(description="Select due kaoyan review cards.")
    parser.add_argument("deck", help="Path to JSON deck")
    parser.add_argument("--date", help="Session date, YYYY-MM-DD")
    parser.add_argument("--limit", type=int, default=60, help="Maximum due cards")
    parser.add_argument("--subject", action="append", help="Filter by subject; repeatable")
    args = parser.parse_args()

    today = parse_date(args.date)
    cards = json.loads(Path(args.deck).read_text(encoding="utf-8-sig"))
    subjects = set(args.subject or [])

    due_cards = []
    for card in cards:
        if subjects and card.get("subject") not in subjects:
            continue
        due = parse_date(card.get("due"))
        if due <= today:
            item = dict(card)
            item["days_overdue"] = (today - due).days
            due_cards.append(item)

    due_cards.sort(key=priority)
    print(json.dumps(due_cards[: args.limit], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

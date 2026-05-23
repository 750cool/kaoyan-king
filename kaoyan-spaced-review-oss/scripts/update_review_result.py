#!/usr/bin/env python3
"""Update one review card after a recall result."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path


NEXT_INTERVAL = {
    "again": 1,
    "hard": 3,
    "good": None,
    "easy": None,
}


def parse_date(value: str | None) -> dt.date:
    if not value:
        return dt.date.today()
    return dt.date.fromisoformat(value)


def next_interval(card: dict, result: str) -> int:
    old = int(card.get("interval_days", 1) or 1)
    if result in ("again", "hard"):
        return NEXT_INTERVAL[result]
    if result == "good":
        return max(5, round(old * 2.0))
    if result == "easy":
        return max(10, round(old * 2.8))
    raise ValueError("result must be one of: again, hard, good, easy")


def main() -> int:
    parser = argparse.ArgumentParser(description="Update card spacing after review.")
    parser.add_argument("deck", help="Path to JSON deck")
    parser.add_argument("card_id", help="Card id to update")
    parser.add_argument("result", choices=["again", "hard", "good", "easy"])
    parser.add_argument("--date", help="Review date, YYYY-MM-DD")
    args = parser.parse_args()

    path = Path(args.deck)
    cards = json.loads(path.read_text(encoding="utf-8-sig"))
    today = parse_date(args.date)

    for card in cards:
        if card.get("id") != args.card_id:
            continue
        interval = next_interval(card, args.result)
        card["interval_days"] = interval
        card["due"] = (today + dt.timedelta(days=interval)).isoformat()
        if args.result == "again":
            card["lapses"] = int(card.get("lapses", 0) or 0) + 1
        history = list(card.get("history", []))
        history.append({"date": today.isoformat(), "result": args.result, "next_due": card["due"]})
        card["history"] = history
        path.write_text(json.dumps(cards, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(card, ensure_ascii=False, indent=2))
        return 0

    raise SystemExit(f"Card not found: {args.card_id}")


if __name__ == "__main__":
    raise SystemExit(main())

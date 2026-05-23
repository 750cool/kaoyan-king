#!/usr/bin/env python3
"""Draft a kaoyan phase plan from today's date and exam date."""

from __future__ import annotations

import argparse
import datetime as dt
import json


PHASES = [
    ("基础", 0.35, "建立教材知识框架，完成核心公式、定义、基础例题卡。"),
    ("强化", 0.30, "按题型和方法块突破，加入强化资料、综合题和易错题。"),
    ("真题", 0.22, "按年份和专题刷真题，建立错题回炉和高频模型。"),
    ("冲刺", 0.10, "限时套卷、公式默写、薄弱专题回炉。"),
    ("考前回炉", 0.03, "只看高频错题、公式条件、典型例题和稳定拿分流程。"),
]


def parse_date(value: str) -> dt.date:
    return dt.date.fromisoformat(value)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a date-based kaoyan phase plan.")
    parser.add_argument("--today", default=dt.date.today().isoformat(), help="YYYY-MM-DD")
    parser.add_argument("--exam-date", required=True, help="YYYY-MM-DD")
    args = parser.parse_args()

    today = parse_date(args.today)
    exam = parse_date(args.exam_date)
    total_days = max((exam - today).days, 1)
    cursor = today
    plan = []

    for index, (name, ratio, goal) in enumerate(PHASES):
        if index == len(PHASES) - 1:
            end = exam
        else:
            days = max(round(total_days * ratio), 1)
            end = min(cursor + dt.timedelta(days=days - 1), exam)
        plan.append(
            {
                "phase": name,
                "start": cursor.isoformat(),
                "end": end.isoformat(),
                "goal": goal,
            }
        )
        cursor = end + dt.timedelta(days=1)
        if cursor > exam:
            break

    print(json.dumps({"today": today.isoformat(), "exam_date": exam.isoformat(), "days_left": total_days, "phases": plan}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Inventory PDF files and estimate extraction risk.

This script uses lightweight checks only. It reports file size and, when pypdf
is installed, page count plus a small text-layer sample.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def inspect_pdf(path: Path) -> dict:
    result = {
        "path": str(path),
        "size_mb": round(path.stat().st_size / 1024 / 1024, 2),
        "page_count": None,
        "text_layer_sample_chars": None,
        "pdf_type_guess": "unknown",
        "quality_guess": "manual_check_required",
        "notes": [],
    }
    try:
        from pypdf import PdfReader  # type: ignore
    except Exception:
        result["notes"].append("pypdf not installed; only file size was checked")
        return result

    try:
        reader = PdfReader(str(path))
        result["page_count"] = len(reader.pages)
        sample_pages = list(range(min(3, len(reader.pages))))
        if len(reader.pages) > 6:
            sample_pages.append(len(reader.pages) // 2)
        chars = 0
        for index in sample_pages:
            text = reader.pages[index].extract_text() or ""
            chars += len(text.strip())
        result["text_layer_sample_chars"] = chars
        if chars > 800:
            result["pdf_type_guess"] = "native_text_or_mixed"
            result["quality_guess"] = "medium"
            result["notes"].append("text layer exists; formulas and page numbers still need spot checks")
        elif chars > 100:
            result["pdf_type_guess"] = "mixed_or_sparse_text"
            result["quality_guess"] = "low"
            result["notes"].append("sparse text layer; OCR or screenshots may be needed")
        else:
            result["pdf_type_guess"] = "scanned_image_likely"
            result["quality_guess"] = "low"
            result["notes"].append("little extractable text; OCR/manual verification needed")
    except Exception as exc:
        result["pdf_type_guess"] = "corrupt_or_locked"
        result["quality_guess"] = "blocked"
        result["notes"].append(f"read failed: {exc}")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect PDFs for kaoyan review ingestion.")
    parser.add_argument("root", help="Skill root or material folder")
    args = parser.parse_args()

    root = Path(args.root)
    pdfs = sorted(root.rglob("*.pdf"))
    print(json.dumps([inspect_pdf(pdf) for pdf in pdfs], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

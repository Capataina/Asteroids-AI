"""
Shared helpers for report sections.
"""

from typing import Iterable, Tuple, List, Optional


def write_takeaways(f, takeaways: Iterable[str], title: str = "Takeaways"):
    items = [t for t in takeaways if t]
    if not items:
        return
    f.write(f"### {title}\n\n")
    for item in items:
        f.write(f"- {item}\n")
    f.write("\n")


def write_warnings(f, warnings: Iterable[str], title: str = "Warnings"):
    items = [w for w in warnings if w]
    if not items:
        return
    f.write(f"### {title}\n\n")
    for item in items:
        f.write(f"- {item}\n")
    f.write("\n")


def write_glossary(f, entries: List[Tuple[str, str]], title: str = "Glossary"):
    if not entries:
        return
    f.write(f"### {title}\n\n")
    for label, desc in entries:
        f.write(f"- **{label}:** {desc}\n")
    f.write("\n")


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def safe_div(numerator: float, denominator: float, default: float = 0.0) -> float:
    if denominator == 0:
        return default
    return numerator / denominator

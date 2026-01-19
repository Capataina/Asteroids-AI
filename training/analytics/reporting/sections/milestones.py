"""
Milestone tracking section.

Identifies the first generation to achieve specific performance benchmarks.
"""

from typing import List, Dict, Any

from training.analytics.reporting.sections.common import write_takeaways, write_glossary
from training.analytics.reporting.glossary import glossary_entries

def write_milestone_timeline(f, generations_data: List[Dict[str, Any]]):
    """Write milestone timeline.

    Args:
        f: File handle to write to
        generations_data: List of generation data dictionaries
    """
    if not generations_data:
        return

    milestones = []

    best_fitness_series = [g.get('best_fitness', 0.0) for g in generations_data]
    avg_fitness_series = [g.get('avg_fitness', 0.0) for g in generations_data]
    max_kills_series = [g.get('max_kills', 0.0) for g in generations_data]

    def _first_crossing(series: List[float], threshold: float) -> int:
        for idx, value in enumerate(series):
            if value >= threshold:
                return idx
        return -1

    def _add_relative_milestones(series, label, thresholds, formatter, kind):
        max_val = max(series) if series else 0.0
        if max_val <= 0:
            return
        for pct in thresholds:
            target = max_val * pct
            idx = _first_crossing(series, target)
            if idx >= 0:
                gen = generations_data[idx]['generation']
                milestones.append({
                    "gen": gen,
                    "type": kind,
                    "value": formatter(series[idx]),
                    "desc": f"{label} reached {int(pct * 100)}% of run peak",
                })

    _add_relative_milestones(
        best_fitness_series,
        "Best fitness",
        [0.25, 0.5, 0.75, 0.9, 0.95, 0.98],
        lambda v: f"{v:.0f}",
        "Fitness",
    )
    _add_relative_milestones(
        avg_fitness_series,
        "Avg fitness",
        [0.25, 0.5, 0.75, 0.9],
        lambda v: f"{v:.0f}",
        "Avg Fitness",
    )
    _add_relative_milestones(
        max_kills_series,
        "Max kills",
        [0.25, 0.5, 0.75, 0.9],
        lambda v: f"{v:.0f}",
        "Kills",
    )

    # First positive average fitness
    first_positive_avg = next((g for g in generations_data if g.get('avg_fitness', 0) > 0), None)
    if first_positive_avg:
        milestones.append({
            "gen": first_positive_avg["generation"],
            "type": "Viability",
            "value": f"{first_positive_avg.get('avg_fitness', 0):.0f}",
            "desc": "Average fitness turned positive",
        })

    if not milestones:
        f.write("## Milestone Timeline\n\nNo major milestones reached yet.\n\n")
        return

    f.write("## Milestone Timeline\n\n")
    f.write("| Generation | Category | Value | Description |\n")
    f.write("|------------|----------|-------|-------------|\n")
    
    # Sort by generation
    milestones.sort(key=lambda x: x['gen'])
    
    for m in milestones:
        f.write(f"| {m['gen']} | {m['type']} | {m['value']} | {m['desc']} |\n")
    
    f.write("\n")

    takeaways = [
        f"Total milestones reached: {len(milestones)}.",
    ]
    if milestones:
        takeaways.append(f"Latest milestone at Gen {milestones[-1]['gen']} ({milestones[-1]['type']}).")

    write_takeaways(f, takeaways)
    write_glossary(
        f,
        glossary_entries([
            "best_fitness",
            "avg_fitness",
            "max_kills",
        ])
    )

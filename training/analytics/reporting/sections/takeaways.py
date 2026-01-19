"""
Unified report takeaways.

Produces a concise bullet list covering every major report section.
"""

from typing import List, Dict, Any

from training.analytics.reporting.insights import trend_stats
from training.config.analytics import AnalyticsConfig


def _has_metric(generations_data: List[Dict[str, Any]], key: str) -> bool:
    return bool(generations_data) and key in generations_data[-1]


def collect_report_takeaways(
    generations_data: List[Dict[str, Any]],
    summary: Dict[str, Any],
    has_behavior: bool,
    has_fresh_game: bool
) -> List[str]:
    takeaways: List[str] = []

    # Quick Trend Overview
    takeaways.append("Quick Trend Overview: sparklines summarize phase-based metric direction and confidence.")

    # Training Configuration
    takeaways.append("Training Configuration: report includes a full hyperparameter snapshot for reproducibility.")

    # Overall Summary
    takeaways.append(
        f"Overall Summary: best fitness {summary.get('all_time_best_fitness', 0):.2f} at Gen {summary.get('best_generation', 0)}."
    )

    # Best Agent Deep Profile
    if _has_metric(generations_data, 'best_agent_kills'):
        best_gen = max(generations_data, key=lambda x: x.get('best_fitness', 0))
        takeaways.append(
            f"Best Agent Deep Profile: Gen {best_gen.get('generation', 0)} with {best_gen.get('best_agent_kills', 0)} kills."
        )
    else:
        takeaways.append("Best Agent Deep Profile: no detailed best-agent stats recorded yet.")

    # Heatmaps
    if _has_metric(generations_data, 'best_agent_positions'):
        takeaways.append("Heatmaps: spatial patterns available for best agent and population.")
    else:
        takeaways.append("Heatmaps: no spatial samples recorded yet.")

    # Generation Highlights
    takeaways.append("Generation Highlights: top improvements/regressions and record runs flagged.")

    # Milestones
    takeaways.append("Milestone Timeline: milestones are run-relative (percent-of-peak thresholds).")

    # Training Progress by Phase
    takeaways.append("Training Progress by Phase: 4 equal phases used for normalized comparisons.")

    # Distribution Analysis
    if _has_metric(generations_data, 'std_dev'):
        spread = trend_stats(generations_data, 'std_dev', higher_is_better=False, phase_count=AnalyticsConfig.PHASE_COUNT)
        takeaways.append(f"Distribution Analysis: fitness spread trend is {spread['tag']}.")
    else:
        takeaways.append("Distribution Analysis: no spread data available.")

    # Kill Efficiency
    if _has_metric(generations_data, 'avg_kills'):
        takeaways.append("Kill Efficiency: phase-level kill rates and shot efficiency tracked.")
    else:
        takeaways.append("Kill Efficiency: no kill metrics recorded.")

    # Learning Velocity
    takeaways.append("Learning Velocity: phase-based fitness deltas and acceleration reported.")

    # Reward Component Evolution
    if _has_metric(generations_data, 'avg_reward_breakdown'):
        takeaways.append("Reward Component Evolution: per-component shifts tracked across 4 phases.")
    else:
        takeaways.append("Reward Component Evolution: no reward breakdown recorded.")

    # Reward Balance Analysis
    takeaways.append("Reward Balance Analysis: dominance, entropy, and penalty skew checked.")

    # Population Health
    takeaways.append("Population Health Dashboard: diversity, elite gap, and floor trends summarized.")

    # Stagnation
    takeaways.append("Stagnation Analysis: plateau lengths compared to run history.")

    # Generalization
    if has_fresh_game:
        takeaways.append("Generalization Analysis: fresh-game ratios and reward transfer gaps reported.")
    else:
        takeaways.append("Generalization Analysis: no fresh-game data recorded.")

    # Correlation
    takeaways.append("Correlation Analysis: fitness vs kills/survival/accuracy correlations reported.")

    # Survival Distribution
    if _has_metric(generations_data, 'avg_steps'):
        takeaways.append("Survival Distribution: phase-level survival averages and max survival summarized.")
    else:
        takeaways.append("Survival Distribution: no survival metrics recorded.")

    # Behavioral Summary
    if has_behavior:
        takeaways.append("Behavioral Summary: recent kills, steps, and accuracy summarized.")
    else:
        takeaways.append("Behavioral Summary: no behavioral metrics recorded.")

    # Learning Progress
    takeaways.append("Learning Progress: phase comparisons for best/avg/min fitness.")

    # Neural Analysis
    if _has_metric(generations_data, 'avg_output_saturation'):
        takeaways.append("Neural & Behavioral Complexity: saturation and entropy trends reported.")
    else:
        takeaways.append("Neural & Behavioral Complexity: no saturation/entropy metrics recorded.")

    # Risk Analysis
    if _has_metric(generations_data, 'avg_min_dist'):
        takeaways.append("Risk Profile Analysis: proximity trends and archetypes reported.")
    else:
        takeaways.append("Risk Profile Analysis: no risk metrics recorded.")

    # Control Diagnostics
    if _has_metric(generations_data, 'avg_turn_deadzone_rate'):
        takeaways.append("Control Diagnostics: turn bias, frontness, danger, and movement diagnostics reported.")
    else:
        takeaways.append("Control Diagnostics: no control diagnostics recorded.")

    # Convergence Analysis
    takeaways.append("Convergence Analysis: recent diversity and range trends summarized.")

    # Behavioral Trends
    if has_behavior:
        takeaways.append("Behavioral Trends: action mix and intra-episode scoring patterns reported.")
    else:
        takeaways.append("Behavioral Trends: no behavioral trends available.")

    # Recent Generations Table
    if generations_data:
        takeaways.append(f"Recent Generations: last {min(AnalyticsConfig.RECENT_TABLE_WINDOW, len(generations_data))} gens tabulated.")

    # Top Generations Table
    if generations_data:
        best_gen = max(generations_data, key=lambda x: x.get('best_fitness', 0))
        takeaways.append(f"Top Generations: best run is Gen {best_gen.get('generation', 0)}.")

    # Trend Analysis
    takeaways.append("Trend Analysis: phase-based fitness trend table provided.")

    # ASCII Chart
    takeaways.append("ASCII Chart: best vs avg fitness progression visualized.")

    # Technical Appendix
    takeaways.append("Technical Appendix: runtime costs, operator stats, and ES optimizer diagnostics reported when available.")

    return takeaways


def write_report_takeaways(f, takeaways: List[str]):
    if not takeaways:
        f.write("No report takeaways available.\n\n")
        return

    f.write("## Report Takeaways (All Sections)\n\n")
    for item in takeaways:
        f.write(f"- {item}\n")
    f.write("\n")

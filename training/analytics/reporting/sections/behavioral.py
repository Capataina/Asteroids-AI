"""
Behavioral trends report section.

Generates behavioral metrics trends analysis.
"""

from typing import List, Dict, Any

from training.analytics.analysis.behavioral import calculate_behavioral_by_quarter
from training.analytics.analysis.action_classification import classify_behavior, get_action_rates
from training.analytics.reporting.insights import trend_stats
from training.analytics.reporting.sections.common import write_takeaways, write_warnings, write_glossary
from training.analytics.reporting.glossary import glossary_entries
from training.config.analytics import AnalyticsConfig


def write_behavioral_trends(f, generations_data: List[Dict[str, Any]]):
    """Analyze and write behavioral metrics trends.

    Args:
        f: File handle to write to
        generations_data: List of generation data dictionaries
    """
    if not generations_data or 'avg_kills' not in generations_data[-1]:
        f.write("No behavioral data available.\n\n")
        return

    quarters = calculate_behavioral_by_quarter(generations_data)
    if not quarters:
        f.write("Not enough data for behavioral trend analysis.\n\n")
        return

    f.write("### Performance Metrics by Quarter\n\n")
    f.write("| Period | Avg Kills | Avg Steps | Avg Accuracy | Safe Dist | Max Kills |\n")
    f.write("|--------|-----------|-----------|--------------|-----------|----------|\n")

    for q in quarters:
        safe_dist = q.get('avg_asteroid_dist', 0.0)
        f.write(f"| Q{q['quarter']} | {q['avg_kills']:.2f} | {q['avg_steps']:.0f} | "
                f"{q['avg_accuracy']*100:.1f}% | {safe_dist:.1f}px | {q['max_kills']} |\n")

    f.write("\n")

    # Check if we have action data for the latest quarter
    # (Checking the first quarter might fail if we resumed training with new code)
    has_action_data = 'avg_thrust_frames' in generations_data[-1]

    baseline_rates = None
    if has_action_data:
        all_rates = [get_action_rates(q) for q in quarters if 'avg_thrust_frames' in q]
        if all_rates:
            baseline_rates = {
                'thrust_rate': sum(r['thrust_rate'] for r in all_rates) / len(all_rates),
                'turn_rate': sum(r['turn_rate'] for r in all_rates) / len(all_rates),
                'shoot_rate': sum(r['shoot_rate'] for r in all_rates) / len(all_rates),
            }

        f.write("### Action Distribution & Strategy Evolution\n\n")
        f.write("Analysis of how the population's physical behavior has changed over time.\n\n")
        f.write("| Period | Thrust % | Turn % | Shoot % | Dominant Strategy |\n")
        f.write("|--------|----------|--------|---------|-------------------|\n")

        for q in quarters:
            # Reconstruct a 'metrics' dict from the quarter averages to pass to the classifier
            # The 'quarters' list from calculate_behavioral_by_quarter aggregates keys dynamically
            # providing they exist in the source data.
            
            # Note: We need to handle cases where old data doesn't have these keys
            if 'avg_thrust_frames' not in q:
                f.write(f"| Q{q['quarter']} | N/A | N/A | N/A | *Legacy Data* |\n")
                continue

            rates = get_action_rates(q)
            label = classify_behavior(q, baseline_rates=baseline_rates)
            
            f.write(f"| Q{q['quarter']} | {rates['thrust_rate']*100:.1f}% | "
                    f"{rates['turn_rate']*100:.1f}% | {rates['shoot_rate']*100:.1f}% | "
                    f"**{label}** |\n")
        
        f.write("\n")
        
        # Input Control Style Table
        if 'avg_thrust_duration' in quarters[-1]:
            f.write("### Input Control Style\n\n")
            f.write("| Period | Thrust Dur | Turn Dur | Shoot Dur | Idle Rate | Wraps |\n")
            f.write("|--------|------------|----------|-----------|-----------|-------|\n")
            
            for q in quarters:
                f.write(f"| Q{q['quarter']} | {q.get('avg_thrust_duration', 0):.1f}f | "
                        f"{q.get('avg_turn_duration', 0):.1f}f | {q.get('avg_shoot_duration', 0):.1f}f | "
                        f"{q.get('avg_idle_rate', 0)*100:.1f}% | {q.get('avg_screen_wraps', 0):.1f} |\n")
            f.write("\n")

    takeaways = [
        f"Kills trend: {trend_stats(generations_data, 'avg_kills', True, AnalyticsConfig.PHASE_COUNT)['tag']}.",
        f"Accuracy trend: {trend_stats(generations_data, 'avg_accuracy', True, AnalyticsConfig.PHASE_COUNT)['tag']}.",
    ]
    warnings = []
    if 'avg_idle_rate' in generations_data[-1]:
        idle_trend = trend_stats(generations_data, 'avg_idle_rate', higher_is_better=False, phase_count=AnalyticsConfig.PHASE_COUNT)
        takeaways.append(f"Idle rate trend: {idle_trend['tag']}.")
        if "regression" in idle_trend["tag"]:
            warnings.append("Idle rate is increasing; agents are spending more time with no actions.")

    write_takeaways(f, takeaways)
    write_warnings(f, warnings)
    write_glossary(
        f,
        glossary_entries([
            "avg_kills",
            "avg_steps",
            "avg_accuracy",
            "avg_asteroid_dist",
            "avg_thrust_frames",
            "avg_turn_frames",
            "avg_shoot_frames",
            "avg_thrust_duration",
            "avg_turn_duration",
            "avg_shoot_duration",
            "avg_idle_rate",
            "avg_screen_wraps",
        ])
    )

def write_intra_episode_analysis(f, generations_data: List[Dict[str, Any]]):
    """Analyze score distribution within episodes.

    Args:
        f: File handle to write to
        generations_data: List of generation data dictionaries
    """
    if not generations_data:
        return
        
    last_gen = generations_data[-1]
    quarters = last_gen.get('avg_quarterly_scores', [])
    
    if not quarters or len(quarters) != 4:
        return
        
    total_score = sum(quarters)
    if total_score == 0:
        return
        
    f.write("### Intra-Episode Score Breakdown\n\n")
    f.write("Analysis of when agents earn their reward during an episode (Early vs Late game).\n\n")
    f.write("| Quarter | Avg Score | Share of Total | Play Style |\n")
    f.write("|---------|-----------|----------------|------------|\n")
    
    labels = ["Start (0-25%)", "Mid-Game (25-50%)", "Late-Game (50-75%)", "End-Game (75-100%)"]
    
    for i, score in enumerate(quarters):
        pct = (score / total_score) * 100
        
        # Simple heuristic for play style based on when they score
        style = "Balanced"
        if pct > (100 / len(quarters)) * 1.5:
            style = "Front-loaded" if i == 0 else "Back-loaded" if i == len(quarters) - 1 else "Mid-loaded"
        
        f.write(f"| {labels[i]} | {score:.1f} | {pct:.1f}% | {style} |\n")
        
    f.write("\n")

    takeaways = []
    dominant = max(range(len(quarters)), key=lambda i: quarters[i])
    dominant_share = (quarters[dominant] / total_score) * 100 if total_score else 0.0
    takeaways.append(f"Highest scoring quarter: {labels[dominant]} ({dominant_share:.1f}% of episode reward).")

    write_takeaways(f, takeaways, title="Intra-Episode Takeaways")
    write_glossary(
        f,
        glossary_entries([
            "avg_quarterly_scores",
        ]),
        title="Intra-Episode Glossary"
    )

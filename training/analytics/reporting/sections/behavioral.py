"""
Behavioral trends report section.

Generates behavioral metrics trends analysis.
"""

from typing import List, Dict, Any

from training.analytics.analysis.behavioral import calculate_behavioral_by_quarter
from training.analytics.analysis.action_classification import classify_behavior, get_action_rates


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

    if has_action_data:
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
            label = classify_behavior(q)
            
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
        style = ""
        if i == 0 and pct > 40: style = "Sprinter"
        elif i == 3 and pct > 40: style = "Survivor"
        else: style = "Balanced"
        
        f.write(f"| {labels[i]} | {score:.1f} | {pct:.1f}% | {style} |\n")
        
    f.write("\n")

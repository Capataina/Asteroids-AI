"""
Risk vs Reward Analysis.

Reports on agent risk-taking behavior (proximity to asteroids).
"""

from typing import List, Dict, Any
from training.config.analytics import AnalyticsConfig

def write_risk_analysis(f, generations_data: List[Dict[str, Any]]):
    """Write risk analysis section.

    Args:
        f: File handle.
        generations_data: History.
    """
    if not generations_data:
        return

    window = AnalyticsConfig.RECENT_TABLE_WINDOW
    recent = generations_data[-window:]
    if not recent:
        return
        
    # Check if we have the new metrics
    if 'avg_min_dist' not in recent[-1]:
        return

    f.write("## Risk Profile Analysis\n\n")
    f.write("Analysis of how close agents let asteroids get before reacting or killing them.\n\n")
    
    f.write("| Gen | Avg Min Dist | Fitness | Kills | Archetype |\n")
    f.write("|-----|--------------|---------|-------|-----------|\n")
    
    for gen in recent:
        min_dist = gen.get('avg_min_dist', 0.0)
        fit = gen.get('avg_fitness', 0.0)
        kills = gen.get('avg_kills', 0.0)
        
        # Simple archetype heuristic
        # High fitness + Low dist = Daredevil
        # High fitness + High dist = Sniper
        # Low fitness + Low dist = Victim
        
        archetype = "Learner"
        if fit > 500: # Decent fitness
            if min_dist < 60: # Player radius is ~20, Asteroid ~30. <60 is VERY close.
                archetype = "Daredevil"
            elif min_dist > 150:
                archetype = "Sniper"
            else:
                archetype = "Balanced"
        else:
            if min_dist < 50:
                archetype = "Victim"
        
        f.write(f"| {gen['generation']} | {min_dist:6.1f}px | {fit:6.1f} | {kills:4.1f} | {archetype} |\n")
        
    f.write("\n")

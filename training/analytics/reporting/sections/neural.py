"""
Neural and Behavioral Complexity Analysis.

Reports on neural network health (saturation) and behavioral entropy.
"""

from typing import List, Dict, Any
from training.config.analytics import AnalyticsConfig

def write_neural_analysis(f, generations_data: List[Dict[str, Any]]):
    """Write neural and behavioral complexity analysis.

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
    if 'avg_output_saturation' not in recent[-1]:
        return

    f.write("## Neural & Behavioral Complexity\n\n")
    
    f.write("| Gen | Saturation | Entropy | Control Style |\n")
    f.write("|-----|------------|---------|---------------|\n")
    
    for gen in recent:
        sat = gen.get('avg_output_saturation', 0.0)
        ent = gen.get('avg_action_entropy', 0.0)
        
        # Interpret saturation
        style = "Balanced"
        if sat > 0.8: style = "Bang-Bang (Binary)"
        elif sat < 0.2: style = "Analog (Smooth)"
        
        # Interpret entropy (heuristic)
        if ent < 0.5: style += " / Repetitive"
        elif ent > 2.0: style += " / Chaotic"
        
        f.write(f"| {gen['generation']} | {sat*100:5.1f}% | {ent:5.2f} | {style} |\n")
        
    f.write("\n**Metrics Explanation:**\n")
    f.write("- **Saturation**: % of time neurons are stuck at hard limits (0 or 1). High (>80%) means binary control; Low means analog control.\n")
    f.write("- **Entropy**: Measure of input unpredictability. Low = simple loops; High = random/complex.\n\n")

"""
Distribution analysis report section.

Generates ASCII Mean +/- StdDev charts for key metrics over recent generations.
"""

from typing import List, Dict, Any
from training.config.analytics import AnalyticsConfig

def _draw_distribution_bar(mean: float, std: float, min_val: float, max_val: float, width: int = 40) -> str:
    """Draw a single ASCII bar representing Mean +/- StdDev. 
    
    Format: |------O------|
           (mean-std) (mean) (mean+std)
    """
    if max_val == min_val:
        return " " * width + " (Single Value)"
        
    range_val = max_val - min_val
    if range_val == 0: range_val = 1.0
    
    def pos(val):
        p = int((val - min_val) / range_val * width)
        return max(0, min(width - 1, p))
        
    left_std = mean - std
    right_std = mean + std
    
    p_mean = pos(mean)
    p_left = pos(left_std)
    p_right = pos(right_std)
    
    chars = [' '] * width
    
    # Draw range line
    for i in range(p_left, p_right + 1):
        chars[i] = '-'
        
    # Draw ends
    chars[p_left] = '|'
    chars[p_right] = '|'
    
    # Draw mean
    chars[p_mean] = 'O'
    
    return "".join(chars)

def write_distribution_charts(f, generations_data: List[Dict[str, Any]]):
    """Write distribution charts for key metrics. 
    
    Args:
        f: File handle.
        generations_data: History.
    """
    if not generations_data:
        return

    window = AnalyticsConfig.DISTRIBUTION_WINDOW
    recent = generations_data[-window:]
    
    if not recent:
        return
        
    f.write(f"### Metric Distributions (Last {len(recent)} Generations)\n\n")
    f.write("Visualizing population consistency: `|---O---|` represents Mean ± 1 StdDev.\n")
    f.write("- **Narrow bar**: Consistent population (Convergence)\n")
    f.write("- **Wide bar**: Chaotic/Diverse population\n\n")
    
    metrics = [
        ('avg_accuracy', 'std_dev_accuracy', 'Accuracy', True),
        ('avg_steps', 'std_dev_steps', 'Survival Steps', False),
        ('avg_kills', 'std_dev_kills', 'Kills', False),
        ('avg_fitness', 'std_dev', 'Fitness', False)
    ]
    
    for mean_key, std_key, label, is_pct in metrics:
        # Check if data exists in the last generation
        if mean_key not in recent[-1] or std_key not in recent[-1]:
            continue
            
        f.write(f"**{label} Distribution**\n")
        f.write("```\n")
        
        # Calculate global scale for this window
        vals_low = [g.get(mean_key, 0) - g.get(std_key, 0) for g in recent]
        vals_high = [g.get(mean_key, 0) + g.get(std_key, 0) for g in recent]
        
        if not vals_low: continue

        global_min = min(vals_low)
        global_max = max(vals_high)
        
        # Adjust range logic
        if is_pct:
            global_min = max(0.0, global_min) # Clamp bottom to 0%
            global_max = min(1.0, global_max) # Clamp top to 100% (if applicable)
            if global_max < 0.1: global_max = 0.1 # Ensure non-zero width
        else:
            global_min = min(0.0, global_min)
            if global_max == 0: global_max = 1.0
            global_max *= 1.1 # Padding
            
        for g in recent:
            mean = g.get(mean_key, 0)
            std = g.get(std_key, 0)
            bar = _draw_distribution_bar(mean, std, global_min, global_max, AnalyticsConfig.CHART_WIDTH)
            
            if is_pct:
                f.write(f"Gen {g['generation']:3d}: {bar} {mean*100:5.1f}% ± {std*100:4.1f}%\n")
            else:
                f.write(f"Gen {g['generation']:3d}: {bar} {mean:6.1f} ± {std:5.1f}\n")
        
        f.write("```\n\n")
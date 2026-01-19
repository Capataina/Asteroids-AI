"""
Heatmap generator for spatial analytics.
"""

import math
from typing import List, Tuple, Dict, Any

from training.config.analytics import AnalyticsConfig
from training.analytics.reporting.sections.common import write_takeaways, write_glossary

def generate_ascii_heatmap(points: List[Tuple[int, int]], width: int = 800, height: int = 600, rows: int = 30, cols: int = 120) -> List[str]:
    """Generate an ASCII heatmap from a list of points.

    Args:
        points: List of (x, y) tuples.
        width: Game world width.
        height: Game world height.
        rows: Number of grid rows.
        cols: Number of grid cols.

    Returns:
        List of strings (lines of the heatmap).
    """
    if not points:
        return ["(No data)"]

    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    
    cell_w = width / cols
    cell_h = height / rows
    
    for x, y in points:
        # Wrap coordinates just in case
        x = x % width
        y = y % height
        
        c = int(x / cell_w)
        r = int(y / cell_h)
        
        c = min(max(c, 0), cols - 1)
        r = min(max(r, 0), rows - 1)
        grid[r][c] += 1
        
    # Find max density for normalization
    max_val = max(max(row) for row in grid)
    if max_val == 0:
        return ["(Empty)"]
        
    # ASCII gradient
    chars = " .:-=+*#%@"
    
    # Precompute log max for scaling
    log_max = math.log1p(max_val)
    if log_max == 0: log_max = 1.0
    
    lines = []
    # Print top to bottom (Row 9 down to 0)
    for r in range(rows - 1, -1, -1):
        line = "|"
        for c in range(cols):
            val = grid[r][c]
            # Logarithmic scaling to show trails against high-density start points
            norm = math.log1p(val) / log_max
            char_idx = int(norm * (len(chars) - 1))
            line += chars[char_idx]
        line += "|"
        lines.append(line)
        
    return lines

def write_heatmaps(f, generations_data: List[Dict[str, Any]], width: int, height: int):
    """Write spatial heatmaps to the report.

    Args:
        f: File handle.
        generations_data: History.
        width: Screen width.
        height: Screen height.
    """
    if not generations_data:
        return

    # Determine how many generations to aggregate
    window_size = AnalyticsConfig.HEATMAP_WINDOW
    num_gens = min(len(generations_data), window_size)
    recent_gens = generations_data[-num_gens:]
    
    # Aggregate data
    agg_best_positions = []
    agg_best_kills = []
    agg_pop_positions = []
    agg_pop_kills = []

    for gen in recent_gens:
        agg_best_positions.extend(gen.get('best_agent_positions', []))
        agg_best_kills.extend(gen.get('best_agent_kill_events', []))
        agg_pop_positions.extend(gen.get('population_positions', []))
        agg_pop_kills.extend(gen.get('population_kill_events', []))
    
    start_gen = recent_gens[0]['generation']
    end_gen = recent_gens[-1]['generation']
    range_str = f"Generations {start_gen}-{end_gen}" if start_gen != end_gen else f"Generation {start_gen}"

    if not agg_best_positions:
        return
        
    f.write(f"### Spatial Analytics (Best Agent - {range_str})\n\n")
    
    f.write("**Position Heatmap (Where does it fly?)**\n")
    f.write("```\n")
    lines = generate_ascii_heatmap(agg_best_positions, width, height)
    for line in lines:
        f.write(line + "\n")
    f.write("```\n\n")
    
    if agg_best_kills:
        f.write("**Kill Zone Heatmap (Where does it kill?)**\n")
        f.write("```\n")
        lines = generate_ascii_heatmap(agg_best_kills, width, height)
        for line in lines:
            f.write(line + "\n")
        f.write("```\n\n")
    else:
        f.write("**Kill Zone Heatmap:** (No kills recorded)\n\n")

    # --- Population Average Heatmaps ---
    
    if not agg_pop_positions:
        return
        
    f.write(f"### Spatial Analytics (Population Average - {range_str})\n\n")
    
    f.write("**Position Heatmap (Where do they fly?)**\n")
    f.write("```\n")
    lines = generate_ascii_heatmap(agg_pop_positions, width, height)
    for line in lines:
        f.write(line + "\n")
    f.write("```\n\n")
    
    if agg_pop_kills:
        f.write("**Kill Zone Heatmap (Where do they kill?)**\n")
        f.write("```\n")
        lines = generate_ascii_heatmap(agg_pop_kills, width, height)
        for line in lines:
            f.write(line + "\n")
        f.write("```\n\n")
    else:
        f.write("**Kill Zone Heatmap:** (No kills recorded)\n\n")

    takeaways = [
        f"Heatmaps aggregate spatial samples over the last {num_gens} generations.",
        "Best-agent and population heatmaps highlight spatial biases and kill zones.",
    ]
    write_takeaways(f, takeaways, title="Heatmap Takeaways")
    write_glossary(
        f,
        [
            ("Position heatmap", "Density of sampled player positions during evaluation."),
            ("Kill heatmap", "Density of player positions at kill events (proxy for engagement zones)."),
        ],
        title="Heatmap Glossary",
    )

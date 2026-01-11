"""
Heatmap generator for spatial analytics.
"""

from typing import List, Tuple, Dict, Any

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
        
        # Invert row because Y is usually up in Cartesian but down in grids? 
        # Arcade Y=0 is bottom. Grid row 0 is top.
        # So y=600 is row 0. y=0 is row 9.
        # r = rows - 1 - r
        # Actually let's keep it Cartesian: Row 0 = Bottom.
        
        c = min(max(c, 0), cols - 1)
        r = min(max(r, 0), rows - 1)
        grid[r][c] += 1
        
    # Find max density for normalization
    max_val = max(max(row) for row in grid)
    if max_val == 0:
        return ["(Empty)"]
        
    # ASCII gradient
    chars = " .:-=+*#%@"
    
    lines = []
    # Print top to bottom (Row 9 down to 0)
    for r in range(rows - 1, -1, -1):
        line = "|"
        for c in range(cols):
            val = grid[r][c]
            norm = val / max_val
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
        
    last_gen = generations_data[-1]
    positions = last_gen.get('best_agent_positions', [])
    kills = last_gen.get('best_agent_kill_events', [])
    
    if not positions:
        return
        
    f.write("### Spatial Analytics (Best Agent)\n\n")
    
    f.write("**Position Heatmap (Where does it fly?)**\n")
    f.write("```\n")
    lines = generate_ascii_heatmap(positions, width, height)
    for line in lines:
        f.write(line + "\n")
    f.write("```\n\n")
    
    if kills:
        f.write("**Kill Zone Heatmap (Where does it kill?)**\n")
        f.write("```\n")
        lines = generate_ascii_heatmap(kills, width, height)
        for line in lines:
            f.write(line + "\n")
        f.write("```\n\n")
    else:
        f.write("**Kill Zone Heatmap:** (No kills recorded)\n\n")


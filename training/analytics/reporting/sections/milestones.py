"""
Milestone tracking section.

Identifies the first generation to achieve specific performance benchmarks.
"""

from typing import List, Dict, Any

def write_milestone_timeline(f, generations_data: List[Dict[str, Any]]):
    """Write milestone timeline.

    Args:
        f: File handle to write to
        generations_data: List of generation data dictionaries
    """
    if not generations_data:
        return

    milestones = []
    
    # Define thresholds
    fitness_thresholds = [100, 500, 1000, 2000, 5000, 10000]
    kill_thresholds = [1, 5, 10, 20, 50, 100]
    
    # Track which have been met to avoid duplicate entries
    met_fitness = set()
    met_kills = set()
    
    # Iterate through history
    for gen in generations_data:
        g_num = gen['generation']
        best_fit = gen['best_fitness']
        # Handle cases where max_kills might not be present in early data
        max_kills = gen.get('max_kills', 0)
        
        # Check fitness
        for t in fitness_thresholds:
            if t not in met_fitness and best_fit >= t:
                met_fitness.add(t)
                milestones.append({
                    'gen': g_num,
                    'type': 'Fitness',
                    'value': f"{best_fit:.0f}",
                    'desc': f"Best fitness crossed {t}"
                })
        
        # Check kills
        for t in kill_thresholds:
            if t not in met_kills and max_kills >= t:
                met_kills.add(t)
                milestones.append({
                    'gen': g_num,
                    'type': 'Kills',
                    'value': f"{max_kills}",
                    'desc': f"First agent to achieve {t} kills"
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

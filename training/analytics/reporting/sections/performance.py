"""
Performance reporting section.

Analyzes computational performance (timing) and genetic operator statistics.
"""

from typing import List, Dict, Any

def write_computational_performance(f, generations_data: List[Dict[str, Any]]):
    """Write computational performance analysis.

    Args:
        f: File handle to write to
        generations_data: List of generation data dictionaries
    """
    if not generations_data:
        return

    # Check for timing data
    has_timing = 'evaluation_duration' in generations_data[-1]
    if not has_timing:
        f.write("No computational timing data available.\n\n")
        return

    f.write("## System Performance\n\n")
    
    # Calculate averages over last 10 generations
    recent = generations_data[-10:]
    avg_eval = sum(g.get('evaluation_duration', 0) for g in recent) / len(recent)
    avg_evol = sum(g.get('evolution_duration', 0) for g in recent) / len(recent)
    avg_total = sum(g.get('total_gen_duration', 0) for g in recent) / len(recent)
    
    f.write(f"**Average Duration (Last 10 Generations):** {avg_total:.2f}s\n")
    f.write(f"- **Evaluation (Simulation):** {avg_eval:.2f}s ({(avg_eval/avg_total)*100:.1f}%)\n")
    f.write(f"- **Evolution (GA Operators):** {avg_evol:.4f}s ({(avg_evol/avg_total)*100:.1f}%)\n\n")
    
    f.write("| Gen Range | Avg Eval Time | Avg Evol Time | Total Time |\n")
    f.write("|-----------|---------------|---------------|------------|\n")
    
    # Group by deciles
    chunk_size = max(1, len(generations_data) // 10)
    for i in range(0, len(generations_data), chunk_size):
        chunk = generations_data[i:i+chunk_size]
        start = chunk[0]['generation']
        end = chunk[-1]['generation']
        
        c_eval = sum(g.get('evaluation_duration', 0) for g in chunk) / len(chunk)
        c_evol = sum(g.get('evolution_duration', 0) for g in chunk) / len(chunk)
        c_total = sum(g.get('total_gen_duration', 0) for g in chunk) / len(chunk)
        
        f.write(f"| {start}-{end} | {c_eval:.2f}s | {c_evol:.4f}s | {c_total:.2f}s |\n")
        
    f.write("\n")

def write_genetic_operator_stats(f, generations_data: List[Dict[str, Any]]):
    """Write genetic operator statistics.

    Args:
        f: File handle to write to
        generations_data: List of generation data dictionaries
    """
    if not generations_data:
        return

    # Check for operator stats
    has_ops = 'crossover_events' in generations_data[-1]
    if not has_ops:
        return # Silent return if no data, as this is an advanced section

    f.write("## Genetic Operator Statistics\n\n")
    
    # Calculate recent averages
    recent = generations_data[-10:]
    avg_cross = sum(g.get('crossover_events', 0) for g in recent) / len(recent)
    avg_mut = sum(g.get('mutation_events', 0) for g in recent) / len(recent)
    avg_elite = sum(g.get('elite_count', 0) for g in recent) / len(recent)
    pop_size = generations_data[-1].get('population_size', 100)
    
    f.write(f"**Recent Averages (Population: {pop_size})**\n")
    f.write(f"- **Crossovers:** {avg_cross:.1f} ({(avg_cross/pop_size)*100:.1f}%)\n")
    f.write(f"- **Mutations:** {avg_mut:.1f} ({(avg_mut/pop_size)*100:.1f}%)\n")
    f.write(f"- **Elites Preserved:** {avg_elite:.1f}\n\n")


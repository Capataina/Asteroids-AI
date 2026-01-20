"""
Performance reporting section.

Analyzes computational performance (timing) and genetic operator statistics.
"""

from typing import List, Dict, Any

from training.analytics.analysis.phases import split_generations
from training.analytics.reporting.sections.common import write_takeaways, write_warnings, write_glossary
from training.analytics.reporting.glossary import glossary_entries
from training.config.analytics import AnalyticsConfig

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
    
    eval_pct = (avg_eval/avg_total)*100 if avg_total > 0 else 0.0
    evol_pct = (avg_evol/avg_total)*100 if avg_total > 0 else 0.0
    
    f.write(f"- **Evaluation (Simulation):** {avg_eval:.2f}s ({eval_pct:.1f}%)\n")
    f.write(f"- **Evolution (Operators):** {avg_evol:.4f}s ({evol_pct:.1f}%)\n\n")
    
    f.write("| Phase | Gen Range | Avg Eval Time | Avg Evol Time | Total Time |\n")
    f.write("|-------|-----------|---------------|---------------|------------|\n")

    phases = split_generations(generations_data, phase_count=AnalyticsConfig.PHASE_COUNT)
    for phase in phases:
        chunk = phase["data"]
        start = chunk[0]['generation']
        end = chunk[-1]['generation']

        c_eval = sum(g.get('evaluation_duration', 0) for g in chunk) / len(chunk)
        c_evol = sum(g.get('evolution_duration', 0) for g in chunk) / len(chunk)
        c_total = sum(g.get('total_gen_duration', 0) for g in chunk) / len(chunk)

        f.write(f"| {phase['label']} | {start}-{end} | {c_eval:.2f}s | {c_evol:.4f}s | {c_total:.2f}s |\n")

    f.write("\n")

    takeaways = [
        f"Evaluation accounts for {eval_pct:.1f}% of generation time.",
        f"Evolution accounts for {evol_pct:.1f}% of generation time.",
    ]
    warnings = []
    if eval_pct > 90:
        warnings.append("Evaluation dominates runtime; optimization gains likely come from faster rollouts.")
    if evol_pct > 20:
        warnings.append("Evolution time is a sizable share; operator optimization could help.")

    write_takeaways(f, takeaways)
    write_warnings(f, warnings)
    write_glossary(
        f,
        glossary_entries([
            "evaluation_duration",
            "evolution_duration",
            "total_gen_duration",
        ])
    )

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

    write_takeaways(
        f,
        [
            f"Recent crossover rate: {(avg_cross/pop_size)*100:.1f}%.",
            f"Recent mutation rate: {(avg_mut/pop_size)*100:.1f}%.",
        ],
        title="Operator Takeaways",
    )
    write_glossary(
        f,
        [
            ("Crossovers", "Number of crossover events per generation."),
            ("Mutations", "Number of mutation events per generation."),
            ("Elites", "Individuals preserved without mutation."),
        ],
        title="Operator Glossary",
    )

    # NEAT-specific diagnostics (when available)
    has_neat = 'species_count' in generations_data[-1] or 'avg_nodes' in generations_data[-1]
    if not has_neat:
        return

    f.write("\n## NEAT Speciation & Topology Statistics\n\n")
    recent = generations_data[-10:]

    def _avg(key: str) -> float:
        return sum(g.get(key, 0.0) for g in recent) / len(recent)

    species_count = _avg('species_count')
    species_min = _avg('species_min_size')
    species_med = _avg('species_median_size')
    species_max = _avg('species_max_size')
    pruned = _avg('species_pruned')

    avg_nodes = _avg('avg_nodes')
    avg_conns = _avg('avg_connections')
    best_nodes = _avg('best_nodes')
    best_conns = _avg('best_connections')

    thr = _avg('compatibility_threshold')
    cmean = _avg('compatibility_mean')
    cp10 = _avg('compatibility_p10')
    cp90 = _avg('compatibility_p90')

    add_node = _avg('add_node_events')
    add_conn = _avg('add_connection_events')
    wmut = _avg('weight_mutation_events')
    innov_survival = _avg('innovation_survival_rate')

    f.write("**Recent Averages (Last 10 Generations):**\n")
    f.write(f"- **Species count:** {species_count:.2f}\n")
    f.write(f"- **Species size (min/median/max):** {species_min:.1f} / {species_med:.1f} / {species_max:.1f}\n")
    f.write(f"- **Species pruned:** {pruned:.2f}\n")
    f.write(f"- **Topology (avg nodes / avg enabled conns):** {avg_nodes:.2f} / {avg_conns:.2f}\n")
    f.write(f"- **Topology (best nodes / best enabled conns):** {best_nodes:.2f} / {best_conns:.2f}\n")
    f.write(f"- **Compatibility (threshold / mean / p10 / p90):** {thr:.3f} / {cmean:.3f} / {cp10:.3f} / {cp90:.3f}\n")
    f.write(f"- **Structural ops (add-node / add-conn):** {add_node:.2f} / {add_conn:.2f}\n")
    f.write(f"- **Weight mutations (per-gen counter):** {wmut:.1f}\n")
    f.write(f"- **Innovation survival rate:** {innov_survival:.2f}\n\n")

    takeaways = [
        "Species count and compatibility-distance stats indicate whether speciation is separating the population.",
        "Topology growth (nodes/connections) indicates whether structure is changing, not just weights."
    ]
    warnings = []
    if species_count <= 1.1:
        warnings.append("Speciation appears collapsed (≈1 species); reduce compatibility threshold or enable/adapt thresholding.")
    if thr > 0 and cmean / thr < 0.25:
        warnings.append("Compatibility threshold is much larger than observed distances; most genomes will land in one species.")
    if innov_survival < 0.2:
        warnings.append("Low innovation survival; structural mutations may be getting eliminated too quickly.")

    write_takeaways(f, takeaways, title="NEAT Takeaways")
    write_warnings(f, warnings, title="NEAT Warnings")

    write_glossary(
        f,
        [
            ("Species count", "Number of species in the population (diversity via speciation)."),
            ("Compatibility distance", "Speciation distance based on excess/disjoint genes and weight differences."),
            ("Avg nodes/connections", "Mean topology size across the population (growth signal)."),
            ("Innovation survival rate", "Fraction of newly created structural innovations that persist into the next generation."),
        ],
        title="NEAT Glossary",
    )


def write_es_optimizer_stats(f, generations_data: List[Dict[str, Any]]):
    """Write ES optimizer diagnostics when available."""
    if not generations_data:
        return

    has_es_stats = 'cov_diag_mean' in generations_data[-1] or 'sigma' in generations_data[-1]
    if not has_es_stats:
        return

    recent = generations_data[-10:]
    def _avg(key: str) -> float:
        return sum(g.get(key, 0.0) for g in recent) / len(recent)

    avg_sigma = _avg('sigma')
    avg_cov_mean = _avg('cov_diag_mean')
    avg_cov_std = _avg('cov_diag_std')
    avg_cov_mean_abs = _avg('cov_diag_mean_abs_dev')
    avg_cov_max_abs = _avg('cov_diag_max_abs_dev')
    avg_cov_scale = _avg('cov_lr_scale')
    avg_cov_rate = _avg('cov_lr_effective_rate')

    f.write("## ES Optimizer Diagnostics\n\n")
    f.write("**Recent Averages (Last 10 Generations):**\n")
    f.write(f"- **Sigma:** {avg_sigma:.5f}\n")
    f.write(f"- **Cov diag mean:** {avg_cov_mean:.5f}\n")
    f.write(f"- **Cov diag std:** {avg_cov_std:.6f}\n")
    f.write(f"- **Cov diag mean abs dev:** {avg_cov_mean_abs:.6f}\n")
    f.write(f"- **Cov diag max abs dev:** {avg_cov_max_abs:.6f}\n")
    f.write(f"- **Cov lr scale:** {avg_cov_scale:.2f}\n")
    f.write(f"- **Cov lr effective rate:** {avg_cov_rate:.6f}\n\n")

    write_takeaways(
        f,
        [
            "CMA-ES step-size and diagonal covariance movement are tracked across recent generations.",
        ],
        title="Optimizer Takeaways",
    )
    write_glossary(
        f,
        glossary_entries([
            "sigma",
            "cov_diag_mean",
            "cov_diag_std",
            "cov_diag_mean_abs_dev",
            "cov_diag_max_abs_dev",
            "cov_lr_scale",
            "cov_lr_effective_rate",
        ]),
        title="Optimizer Glossary",
    )

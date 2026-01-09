"""
Training Analytics and Summary Report Generation

Tracks detailed training metrics including:
- Fitness statistics (best, avg, median, std dev, percentiles)
- Behavioral metrics (kills, accuracy, survival time)
- Learning progress (stagnation detection, improvement rates)
- Population diversity
"""

import json
import math
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path


class TrainingAnalytics:
    """Tracks detailed training metrics across generations."""

    SCHEMA_VERSION = "2.0"  # Updated schema with fresh game and distribution tracking

    def __init__(self):
        self.generations_data = []
        self.start_time = datetime.now()
        self.config = {}
        # Track all-time best for stagnation detection
        self.all_time_best_fitness = float('-inf')
        self.all_time_best_generation = 0
        self.generations_since_improvement = 0

        # Fresh game tracking
        self.fresh_game_data = {}  # generation -> fresh_game metrics

        # Distribution tracking (per-agent arrays)
        self.distributions_data = {}  # generation -> distribution arrays

    def record_generation(self, generation: int, fitness_scores: List[float],
                         behavioral_metrics: Optional[Dict[str, Any]] = None,
                         best_agent_stats: Optional[Dict[str, Any]] = None):
        """Record metrics for a generation."""
        if not fitness_scores:
            return

        sorted_scores = sorted(fitness_scores)
        n = len(sorted_scores)

        gen_data = {
            'generation': generation,
            # Fitness statistics
            'best_fitness': max(fitness_scores),
            'avg_fitness': sum(fitness_scores) / len(fitness_scores),
            'min_fitness': min(fitness_scores),
            'median_fitness': self._median(fitness_scores),
            'std_dev': self._std_dev(fitness_scores),
            'population_size': len(fitness_scores),
            # Percentiles for understanding distribution
            'p25_fitness': sorted_scores[n // 4] if n >= 4 else sorted_scores[0],
            'p75_fitness': sorted_scores[3 * n // 4] if n >= 4 else sorted_scores[-1],
            'p90_fitness': sorted_scores[int(n * 0.9)] if n >= 10 else sorted_scores[-1],
        }

        # Calculate improvement metrics
        if self.generations_data:
            prev_best = self.generations_data[-1]['best_fitness']
            prev_avg = self.generations_data[-1]['avg_fitness']
            gen_data['best_improvement'] = gen_data['best_fitness'] - prev_best
            gen_data['avg_improvement'] = gen_data['avg_fitness'] - prev_avg
        else:
            gen_data['best_improvement'] = 0.0
            gen_data['avg_improvement'] = 0.0

        # Track all-time best and stagnation
        if gen_data['best_fitness'] > self.all_time_best_fitness:
            self.all_time_best_fitness = gen_data['best_fitness']
            self.all_time_best_generation = generation
            self.generations_since_improvement = 0
        else:
            self.generations_since_improvement += 1

        gen_data['all_time_best'] = self.all_time_best_fitness
        gen_data['generations_since_improvement'] = self.generations_since_improvement

        # Add behavioral metrics if available
        if behavioral_metrics:
            gen_data['avg_kills'] = behavioral_metrics.get('avg_kills', 0)
            gen_data['avg_steps'] = behavioral_metrics.get('avg_steps_survived', 0)
            gen_data['avg_accuracy'] = behavioral_metrics.get('avg_accuracy', 0)
            gen_data['avg_shots'] = behavioral_metrics.get('avg_shots_fired', 0)
            gen_data['total_kills'] = behavioral_metrics.get('total_kills', 0)
            gen_data['max_kills'] = behavioral_metrics.get('max_kills', 0)
            gen_data['max_steps'] = behavioral_metrics.get('max_steps', 0)
            gen_data['best_agent_kills'] = behavioral_metrics.get('best_agent_kills', 0)
            gen_data['best_agent_steps'] = behavioral_metrics.get('best_agent_steps', 0)
            gen_data['best_agent_accuracy'] = behavioral_metrics.get('best_agent_accuracy', 0)
            gen_data['avg_reward_breakdown'] = behavioral_metrics.get('avg_reward_breakdown', {})

        # Add best agent stats if available
        if best_agent_stats:
            gen_data.update(best_agent_stats)

        self.generations_data.append(gen_data)

    def set_config(self, config: Dict[str, Any]):
        """Store training configuration."""
        self.config = config

    def record_fresh_game(self, generation: int, fresh_game_data: Dict[str, Any],
                          generalization_metrics: Dict[str, Any]):
        """Record fresh game test results for a generation.

        Args:
            generation: Generation number
            fresh_game_data: Fresh game performance metrics
            generalization_metrics: Comparison to training performance
        """
        self.fresh_game_data[generation] = {
            'fresh_game': fresh_game_data,
            'generalization_metrics': generalization_metrics
        }

        # Also attach to the generation data if it exists
        for gen_data in self.generations_data:
            if gen_data['generation'] == generation:
                gen_data['fresh_game'] = fresh_game_data
                gen_data['generalization_metrics'] = generalization_metrics
                break

    def record_distributions(self, generation: int, fitness_values: List[float],
                            per_agent_metrics: List[Dict[str, Any]]):
        """Record per-agent distribution data for a generation.

        Args:
            generation: Generation number
            fitness_values: List of all fitness scores (sorted)
            per_agent_metrics: List of per-agent behavioral metrics
        """
        sorted_fitness = sorted(fitness_values)
        sorted_kills = sorted([m.get('kills', 0) for m in per_agent_metrics])
        sorted_steps = sorted([m.get('steps_survived', 0) for m in per_agent_metrics])
        sorted_accuracy = sorted([m.get('accuracy', 0) for m in per_agent_metrics])
        sorted_shots = sorted([m.get('shots_fired', 0) for m in per_agent_metrics])

        # Calculate distribution statistics
        n = len(sorted_fitness)
        mean = sum(sorted_fitness) / n if n > 0 else 0
        std_dev = self._std_dev(sorted_fitness)

        # Skewness calculation (Fisher's)
        if std_dev > 0 and n > 2:
            skewness = (n / ((n - 1) * (n - 2))) * sum(((x - mean) / std_dev) ** 3 for x in sorted_fitness)
        else:
            skewness = 0.0

        # Kurtosis calculation (Fisher's, excess kurtosis)
        if std_dev > 0 and n > 3:
            m4 = sum((x - mean) ** 4 for x in sorted_fitness) / n
            kurtosis = (m4 / (std_dev ** 4)) - 3
        else:
            kurtosis = 0.0

        # Count viable (positive fitness) vs failed agents
        viable_count = sum(1 for f in sorted_fitness if f > 0)
        failed_count = n - viable_count

        distributions = {
            'fitness_values': sorted_fitness,
            'kills_values': sorted_kills,
            'steps_values': sorted_steps,
            'accuracy_values': sorted_accuracy,
            'shots_values': sorted_shots,
        }

        distribution_stats = {
            'fitness_skewness': skewness,
            'fitness_kurtosis': kurtosis,
            'viable_agent_count': viable_count,
            'failed_agent_count': failed_count,
        }

        self.distributions_data[generation] = {
            'distributions': distributions,
            'distribution_stats': distribution_stats
        }

        # Also attach to generation data if it exists
        for gen_data in self.generations_data:
            if gen_data['generation'] == generation:
                gen_data['distributions'] = distributions
                gen_data['distribution_stats'] = distribution_stats
                break

    def _median(self, values: List[float]) -> float:
        """Calculate median value."""
        sorted_vals = sorted(values)
        n = len(sorted_vals)
        if n % 2 == 0:
            return (sorted_vals[n//2 - 1] + sorted_vals[n//2]) / 2
        return sorted_vals[n//2]

    def _std_dev(self, values: List[float]) -> float:
        """Calculate standard deviation."""
        if len(values) < 2:
            return 0.0
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return math.sqrt(variance)

    def _percentile(self, values: List[float], p: float) -> float:
        """Calculate percentile."""
        sorted_vals = sorted(values)
        idx = int(len(sorted_vals) * p / 100)
        return sorted_vals[min(idx, len(sorted_vals) - 1)]

    def get_summary_stats(self) -> Dict[str, Any]:
        """Get overall training summary statistics."""
        if not self.generations_data:
            return {}

        all_best = [g['best_fitness'] for g in self.generations_data]
        all_avg = [g['avg_fitness'] for g in self.generations_data]
        all_min = [g['min_fitness'] for g in self.generations_data]

        # Calculate improvement trends
        early_avg = sum(all_avg[:10]) / min(10, len(all_avg)) if all_avg else 0
        late_avg = sum(all_avg[-10:]) / min(10, len(all_avg[-10:])) if all_avg else 0

        # Behavioral metrics summary (if available)
        has_behavior = 'avg_kills' in self.generations_data[-1]

        summary = {
            'total_generations': len(self.generations_data),
            'training_duration': str(datetime.now() - self.start_time),
            'final_best_fitness': all_best[-1],
            'all_time_best_fitness': max(all_best),
            'final_avg_fitness': all_avg[-1],
            'final_min_fitness': all_min[-1],
            'avg_improvement_early_to_late': late_avg - early_avg,
            'best_generation': all_best.index(max(all_best)) + 1,
            'worst_generation': all_best.index(min(all_best)) + 1,
            'final_stagnation': self.generations_since_improvement,
        }

        if has_behavior:
            # Average behavioral metrics over last 10 generations
            recent = self.generations_data[-10:]
            summary['final_avg_kills'] = sum(g.get('avg_kills', 0) for g in recent) / len(recent)
            summary['final_avg_steps'] = sum(g.get('avg_steps', 0) for g in recent) / len(recent)
            summary['final_avg_accuracy'] = sum(g.get('avg_accuracy', 0) for g in recent) / len(recent)
            summary['max_kills_ever'] = max(g.get('max_kills', 0) for g in self.generations_data)
            summary['max_steps_ever'] = max(g.get('max_steps', 0) for g in self.generations_data)

        # Fresh game aggregations
        fresh_games = [g for g in self.generations_data if 'fresh_game' in g]
        if fresh_games:
            gen_metrics = [g.get('generalization_metrics', {}) for g in fresh_games]
            fresh_data = [g.get('fresh_game', {}) for g in fresh_games]

            # Calculate fresh game stats
            fitness_ratios = [m.get('fitness_ratio', 0) for m in gen_metrics if m.get('fitness_ratio', 0) > 0]
            if fitness_ratios:
                summary['avg_generalization_ratio'] = sum(fitness_ratios) / len(fitness_ratios)
                summary['worst_generalization_ratio'] = min(fitness_ratios)
                summary['best_generalization_ratio'] = max(fitness_ratios)

            # Find best fresh game performance
            fresh_fitnesses = [(g['generation'], g['fresh_game']['fitness'])
                              for g in fresh_games if g.get('fresh_game', {}).get('fitness')]
            if fresh_fitnesses:
                best_fresh = max(fresh_fitnesses, key=lambda x: x[1])
                summary['best_fresh_fitness'] = best_fresh[1]
                summary['best_fresh_generation'] = best_fresh[0]

            # Average fresh game kills
            fresh_kills = [d.get('kills', 0) for d in fresh_data]
            if fresh_kills:
                summary['avg_fresh_kills'] = sum(fresh_kills) / len(fresh_kills)

            # Episode completion rate
            completed = sum(1 for d in fresh_data if d.get('completed_full_episode', False))
            summary['fresh_episode_completion_rate'] = completed / len(fresh_data) if fresh_data else 0

        return summary

    def generate_markdown_report(self, output_path: str = "training_summary.md"):
        """Generate comprehensive markdown training report."""
        summary = self.get_summary_stats()
        has_behavior = 'final_avg_kills' in summary
        has_fresh_game = 'avg_generalization_ratio' in summary

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# Training Summary Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Schema Version:** {self.SCHEMA_VERSION}\n\n")

            # Quick Trend Overview (Sparklines) - NEW
            f.write("## Quick Trend Overview\n\n")
            self._write_sparklines(f)

            # Training Configuration
            f.write("## Training Configuration\n\n")
            f.write("```\n")
            for key, value in self.config.items():
                f.write(f"{key}: {value}\n")
            f.write("```\n\n")

            # Overall Summary
            f.write("## Overall Summary\n\n")
            f.write(f"- **Total Generations:** {summary.get('total_generations', 0)}\n")
            f.write(f"- **Training Duration:** {summary.get('training_duration', 'N/A')}\n")
            f.write(f"- **All-Time Best Fitness:** {summary.get('all_time_best_fitness', 0):.2f}\n")
            f.write(f"- **Best Generation:** {summary.get('best_generation', 0)}\n")
            f.write(f"- **Final Best Fitness:** {summary.get('final_best_fitness', 0):.2f}\n")
            f.write(f"- **Final Average Fitness:** {summary.get('final_avg_fitness', 0):.2f}\n")
            f.write(f"- **Avg Improvement (Early->Late):** {summary.get('avg_improvement_early_to_late', 0):.2f}\n")
            f.write(f"- **Stagnation:** {summary.get('final_stagnation', 0)} generations since improvement\n")

            # Fresh game summary (if available)
            if has_fresh_game:
                f.write(f"\n**Generalization (Fresh Game Performance):**\n")
                f.write(f"- Avg Generalization Ratio: {summary.get('avg_generalization_ratio', 0):.2f}\n")
                f.write(f"- Best Fresh Fitness: {summary.get('best_fresh_fitness', 0):.2f} (Gen {summary.get('best_fresh_generation', 0)})\n")
                f.write(f"- Episode Completion Rate: {summary.get('fresh_episode_completion_rate', 0)*100:.1f}%\n")
            f.write("\n")

            # Training Progress by Decile - NEW
            f.write("## Training Progress by Decile\n\n")
            self._write_decile_breakdown(f)

            # Kill Efficiency Analysis - NEW
            f.write("## Kill Efficiency Analysis\n\n")
            self._write_kill_efficiency(f)

            # Reward Component Evolution - NEW
            f.write("## Reward Component Evolution\n\n")
            self._write_reward_evolution(f)

            # Population Health Dashboard - NEW (Phase 2)
            f.write("## Population Health Dashboard\n\n")
            self._write_population_health(f)

            # Stagnation Analysis - ENHANCED
            f.write("## Stagnation Analysis\n\n")
            self._write_stagnation_analysis(f)

            # Generalization Analysis (Fresh Game) - NEW
            if has_fresh_game:
                f.write("## Generalization Analysis (Fresh Game)\n\n")
                self._write_generalization_analysis(f)

            # Correlation Matrix - NEW (Phase 2)
            f.write("## Correlation Analysis\n\n")
            self._write_correlation_matrix(f)

            # Survival Distribution - NEW (Phase 2)
            f.write("## Survival Distribution\n\n")
            self._write_survival_distribution(f)

            # Behavioral Summary (if available)
            if has_behavior:
                f.write("## Behavioral Summary (Last 10 Generations)\n\n")
                f.write(f"- **Avg Kills per Agent:** {summary.get('final_avg_kills', 0):.2f}\n")
                f.write(f"- **Avg Steps Survived:** {summary.get('final_avg_steps', 0):.0f}\n")
                f.write(f"- **Avg Accuracy:** {summary.get('final_avg_accuracy', 0)*100:.1f}%\n")
                f.write(f"- **Max Kills (Any Agent Ever):** {summary.get('max_kills_ever', 0)}\n")
                f.write(f"- **Max Steps (Any Agent Ever):** {summary.get('max_steps_ever', 0)}\n\n")

            # Learning Progress
            f.write("## Learning Progress\n\n")
            self._write_learning_progress(f)

            # Convergence Analysis
            f.write("## Convergence Analysis\n\n")
            self._write_convergence_analysis(f)

            # Behavioral Trends (if available)
            if has_behavior:
                f.write("## Behavioral Trends\n\n")
                self._write_behavioral_trends(f)

            # Recent Generations Table
            f.write("## Recent Generations (Last 30)\n\n")
            self._write_generation_table(f, limit=30, include_behavior=has_behavior)

            # Best Generations
            f.write("\n## Top 10 Best Generations\n\n")
            self._write_best_generations(f, include_behavior=has_behavior)

            # Trend Analysis
            f.write("\n## Trend Analysis\n\n")
            self._write_trend_analysis(f)

            # ASCII Charts
            f.write("\n## Fitness Progression (ASCII Chart)\n\n")
            self._write_ascii_chart(f)

        print(f"\n[OK] Training summary saved to: {output_path}")
        return output_path

    # ============ NEW ANALYTICS METHODS ============

    def _write_sparklines(self, f):
        """Generate ASCII sparklines for quick trend visualization."""
        if len(self.generations_data) < 2:
            f.write("Not enough data for sparklines.\n\n")
            return

        sparkline_chars = "▁▂▃▄▅▆▇█"

        def make_sparkline(values, width=10):
            """Create sparkline from values."""
            if not values:
                return "N/A"
            # Sample to width points
            step = max(1, len(values) // width)
            sampled = values[::step][:width]
            if len(sampled) < 2:
                return "▄" * len(sampled)

            min_val = min(sampled)
            max_val = max(sampled)
            range_val = max_val - min_val

            if range_val == 0:
                return "▄" * len(sampled)

            result = ""
            for v in sampled:
                idx = int((v - min_val) / range_val * 7)
                idx = max(0, min(7, idx))
                result += sparkline_chars[idx]
            return result

        # Gather metrics
        best_fitness = [g['best_fitness'] for g in self.generations_data]
        avg_fitness = [g['avg_fitness'] for g in self.generations_data]
        avg_kills = [g.get('avg_kills', 0) for g in self.generations_data]
        avg_accuracy = [g.get('avg_accuracy', 0) for g in self.generations_data]
        avg_steps = [g.get('avg_steps', 0) for g in self.generations_data]
        std_devs = [g.get('std_dev', 0) for g in self.generations_data]

        def pct_change(values):
            if len(values) < 2 or values[0] == 0:
                return 0
            return ((values[-1] - values[0]) / abs(values[0])) * 100

        f.write("```\n")
        f.write(f"Best Fitness: {best_fitness[0]:.0f} → {best_fitness[-1]:.0f}   [{make_sparkline(best_fitness)}] {pct_change(best_fitness):+.0f}%\n")
        f.write(f"Avg Fitness:  {avg_fitness[0]:.0f} → {avg_fitness[-1]:.0f}   [{make_sparkline(avg_fitness)}] {pct_change(avg_fitness):+.0f}%\n")
        if any(avg_kills):
            f.write(f"Avg Kills:    {avg_kills[0]:.1f} → {avg_kills[-1]:.1f}   [{make_sparkline(avg_kills)}] {pct_change(avg_kills):+.0f}%\n")
        if any(avg_accuracy):
            f.write(f"Avg Accuracy: {avg_accuracy[0]*100:.0f}% → {avg_accuracy[-1]*100:.0f}%   [{make_sparkline(avg_accuracy)}] {pct_change(avg_accuracy):+.0f}%\n")
        if any(avg_steps):
            f.write(f"Avg Steps:    {avg_steps[0]:.0f} → {avg_steps[-1]:.0f}   [{make_sparkline(avg_steps)}] {pct_change(avg_steps):+.0f}%\n")
        if any(std_devs):
            f.write(f"Diversity:    {std_devs[0]:.0f} → {std_devs[-1]:.0f}   [{make_sparkline(std_devs)}] {pct_change(std_devs):+.0f}%\n")
        f.write("```\n\n")

    def _write_decile_breakdown(self, f):
        """Write training progress broken down by decile (10 equal phases)."""
        n = len(self.generations_data)
        if n < 10:
            # For short runs, use fewer phases
            if n < 5:
                f.write("Not enough data for decile breakdown (need at least 5 generations).\n\n")
                return
            num_phases = n
        else:
            num_phases = 10

        phase_size = max(1, n // num_phases)

        f.write("| Phase | Gens | Best Fit | Avg Fit | Avg Kills | Avg Acc | Avg Steps | Diversity |\n")
        f.write("|-------|------|----------|---------|-----------|---------|-----------|----------|\n")

        for phase in range(num_phases):
            start_idx = phase * phase_size
            end_idx = min(start_idx + phase_size, n)
            if phase == num_phases - 1:
                end_idx = n  # Include all remaining in last phase

            phase_data = self.generations_data[start_idx:end_idx]
            if not phase_data:
                continue

            start_gen = phase_data[0]['generation']
            end_gen = phase_data[-1]['generation']
            best_fit = max(g['best_fitness'] for g in phase_data)
            avg_fit = sum(g['avg_fitness'] for g in phase_data) / len(phase_data)
            avg_kills = sum(g.get('avg_kills', 0) for g in phase_data) / len(phase_data)
            avg_acc = sum(g.get('avg_accuracy', 0) for g in phase_data) / len(phase_data)
            avg_steps = sum(g.get('avg_steps', 0) for g in phase_data) / len(phase_data)
            diversity = sum(g.get('std_dev', 0) for g in phase_data) / len(phase_data)

            pct_start = int((phase / num_phases) * 100)
            pct_end = int(((phase + 1) / num_phases) * 100)

            f.write(f"| {pct_start}-{pct_end}% | {start_gen}-{end_gen} | {best_fit:.0f} | {avg_fit:.0f} | "
                   f"{avg_kills:.1f} | {avg_acc*100:.0f}% | {avg_steps:.0f} | {diversity:.0f} |\n")

        f.write("\n")

    def _write_kill_efficiency(self, f):
        """Write kill efficiency analysis."""
        if not self.generations_data or 'avg_kills' not in self.generations_data[-1]:
            f.write("No behavioral data available for kill efficiency analysis.\n\n")
            return

        # Get final phase data (last 10%)
        n = len(self.generations_data)
        final_phase = self.generations_data[-max(1, n // 10):]
        first_phase = self.generations_data[:max(1, n // 10)]

        def calc_efficiency(data):
            avg_kills = sum(g.get('avg_kills', 0) for g in data) / len(data)
            avg_steps = sum(g.get('avg_steps', 1) for g in data) / len(data)
            avg_shots = sum(g.get('avg_shots', 1) for g in data) / len(data)
            avg_accuracy = sum(g.get('avg_accuracy', 0) for g in data) / len(data)

            kills_per_100 = (avg_kills / max(1, avg_steps)) * 100
            shots_per_kill = avg_shots / max(0.1, avg_kills)
            conversion_rate = avg_kills / max(1, avg_shots)

            return kills_per_100, shots_per_kill, conversion_rate, avg_kills

        final_k100, final_spk, final_conv, final_kills = calc_efficiency(final_phase)
        first_k100, first_spk, first_conv, first_kills = calc_efficiency(first_phase)

        f.write("### Current Performance (Final Phase)\n\n")
        f.write(f"- **Kills per 100 Steps:** {final_k100:.2f} (up from {first_k100:.2f} in Phase 1)\n")
        f.write(f"- **Shots per Kill:** {final_spk:.2f} (down from {first_spk:.2f} in Phase 1)\n")
        f.write(f"- **Kill Conversion Rate:** {final_conv*100:.1f}% (up from {first_conv*100:.1f}% in Phase 1)\n")
        f.write(f"- **Average Kills per Episode:** {final_kills:.1f}\n\n")

        # Efficiency trend table
        f.write("### Efficiency Trend\n\n")
        f.write("| Phase | Kills/100 Steps | Shots/Kill | Conversion Rate |\n")
        f.write("|-------|-----------------|------------|----------------|\n")

        num_phases = min(5, n)
        phase_size = max(1, n // num_phases)

        for phase in range(num_phases):
            start_idx = phase * phase_size
            end_idx = min(start_idx + phase_size, n)
            if phase == num_phases - 1:
                end_idx = n

            phase_data = self.generations_data[start_idx:end_idx]
            k100, spk, conv, _ = calc_efficiency(phase_data)
            f.write(f"| Phase {phase + 1} | {k100:.2f} | {spk:.2f} | {conv*100:.1f}% |\n")

        # Assessment
        spk_improvement = ((first_spk - final_spk) / max(0.1, first_spk)) * 100
        f.write(f"\n**Assessment:** ")
        if spk_improvement > 50:
            f.write(f"Agent has learned efficient killing. Shots per kill dropped {spk_improvement:.0f}%.\n\n")
        elif spk_improvement > 20:
            f.write(f"Agent has improved efficiency moderately. Shots per kill dropped {spk_improvement:.0f}%.\n\n")
        elif spk_improvement > 0:
            f.write(f"Agent shows slight efficiency improvement. Shots per kill dropped {spk_improvement:.0f}%.\n\n")
        else:
            f.write("Agent efficiency has not improved significantly.\n\n")

    def _write_reward_evolution(self, f):
        """Write reward component evolution across training phases."""
        if not self.generations_data or 'avg_reward_breakdown' not in self.generations_data[-1]:
            f.write("No reward component data available.\n\n")
            return

        # Get phases
        n = len(self.generations_data)
        num_phases = min(10, n)
        phase_size = max(1, n // num_phases)

        # Get component names from last generation
        components = list(self.generations_data[-1].get('avg_reward_breakdown', {}).keys())
        if not components:
            f.write("No reward breakdown data available.\n\n")
            return

        # Calculate average for each component in first and last phase
        first_phase = self.generations_data[:phase_size]
        mid_phase = self.generations_data[n//2 - phase_size//2:n//2 + phase_size//2] or self.generations_data[n//2:n//2+1]
        last_phase = self.generations_data[-phase_size:]

        def avg_component(data, comp):
            values = [g.get('avg_reward_breakdown', {}).get(comp, 0) for g in data]
            return sum(values) / len(values) if values else 0

        f.write("| Component | Phase 1 | Mid | Final | Trend | Status |\n")
        f.write("|-----------|---------|-----|-------|-------|--------|\n")

        for comp in sorted(components, key=lambda c: abs(avg_component(last_phase, c)), reverse=True):
            first_val = avg_component(first_phase, comp)
            mid_val = avg_component(mid_phase, comp)
            last_val = avg_component(last_phase, comp)

            # Calculate trend
            if first_val != 0:
                pct_change = ((last_val - first_val) / abs(first_val)) * 100
            else:
                pct_change = 100 if last_val > 0 else -100 if last_val < 0 else 0

            # Trend indicator
            if pct_change > 100:
                trend = "↑↑↑"
            elif pct_change > 50:
                trend = "↑↑"
            elif pct_change > 10:
                trend = "↑"
            elif pct_change < -100:
                trend = "↓↓↓"
            elif pct_change < -50:
                trend = "↓↓"
            elif pct_change < -10:
                trend = "↓"
            else:
                trend = "→"

            # Status
            if last_val > 0 and pct_change > 10:
                status = "Learned"
            elif last_val > 0:
                status = "Stable"
            elif last_val < 0 and first_val < last_val:
                status = "Improving"
            elif last_val < 0:
                status = "Not learned"
            else:
                status = "Negligible"

            f.write(f"| {comp} | {first_val:+.1f} | {mid_val:+.1f} | {last_val:+.1f} | {trend} {pct_change:+.0f}% | {status} |\n")

        f.write("\n")

    def _write_population_health(self, f):
        """Write population health dashboard."""
        if len(self.generations_data) < 5:
            f.write("Not enough data for population health analysis.\n\n")
            return

        recent = self.generations_data[-10:]
        early = self.generations_data[:10]

        # Calculate metrics
        avg_std_recent = sum(g['std_dev'] for g in recent) / len(recent)
        avg_std_early = sum(g['std_dev'] for g in early) / len(early)
        avg_mean_recent = sum(g['avg_fitness'] for g in recent) / len(recent)

        # Diversity index (coefficient of variation)
        diversity_index = avg_std_recent / max(1, abs(avg_mean_recent))

        # Elite gap
        avg_best_recent = sum(g['best_fitness'] for g in recent) / len(recent)
        elite_gap = (avg_best_recent - avg_mean_recent) / max(1, abs(avg_mean_recent))

        # Floor trend (min fitness improvement)
        min_first = sum(g['min_fitness'] for g in early) / len(early)
        min_last = sum(g['min_fitness'] for g in recent) / len(recent)
        floor_trend = min_last - min_first

        # Ceiling trend
        best_first = sum(g['best_fitness'] for g in early) / len(early)
        best_last = sum(g['best_fitness'] for g in recent) / len(recent)
        ceiling_trend = best_last - best_first

        # IQR trend
        iqr_early = sum(g['p75_fitness'] - g['p25_fitness'] for g in early) / len(early)
        iqr_recent = sum(g['p75_fitness'] - g['p25_fitness'] for g in recent) / len(recent)

        # Overall health status
        warnings = []
        if diversity_index < 0.2:
            health_status = "Warning"
            warnings.append("Low diversity - population may be prematurely converged")
        elif diversity_index > 1.0:
            health_status = "Warning"
            warnings.append("High diversity - population may be too chaotic")
        elif elite_gap > 3.0:
            health_status = "Warning"
            warnings.append("High elite gap - knowledge not spreading to population")
        elif floor_trend < 0:
            health_status = "Watch"
            warnings.append("Floor declining - worst agents getting worse")
        else:
            health_status = "Healthy"

        f.write(f"### Current Status: {'🟢' if health_status == 'Healthy' else '🟡' if health_status == 'Watch' else '🔴'} {health_status}\n\n")

        f.write("| Metric | Value | Trend (Recent) | Status |\n")
        f.write("|--------|-------|----------------|--------|\n")

        div_status = "🟢 Good" if 0.3 <= diversity_index <= 0.7 else "🟡 Watch" if 0.2 <= diversity_index <= 1.0 else "🔴 Warning"
        div_trend = "↓ Decreasing" if avg_std_recent < avg_std_early else "↑ Increasing" if avg_std_recent > avg_std_early else "→ Stable"
        f.write(f"| Diversity Index | {diversity_index:.2f} | {div_trend} | {div_status} |\n")

        gap_status = "🟢 Good" if 0.5 <= elite_gap <= 2.0 else "🟡 Watch" if elite_gap <= 3.0 else "🔴 Warning"
        f.write(f"| Elite Gap | {elite_gap:.2f} | → | {gap_status} |\n")

        floor_status = "🟢 Good" if floor_trend >= 0 else "🟡 Watch"
        f.write(f"| Min Fitness Trend | {floor_trend:+.1f} | {'↑' if floor_trend > 0 else '↓'} | {floor_status} |\n")

        ceiling_status = "🟢 Good" if ceiling_trend > 0 else "🟡 Watch"
        f.write(f"| Max Fitness Trend | {ceiling_trend:+.1f} | {'↑' if ceiling_trend > 0 else '↓'} | {ceiling_status} |\n")

        iqr_change = iqr_recent - iqr_early
        f.write(f"| IQR (p75-p25) | {iqr_recent:.0f} | {'↓' if iqr_change < 0 else '↑'} {abs(iqr_change):.0f} | 🟢 |\n")

        f.write("\n")

        if warnings:
            f.write("### Warnings\n\n")
            for w in warnings:
                f.write(f"- ⚠️ {w}\n")
            f.write("\n")

    def _write_generalization_analysis(self, f):
        """Write generalization analysis from fresh game data."""
        fresh_games = [g for g in self.generations_data if 'fresh_game' in g]
        if not fresh_games:
            f.write("No fresh game data available.\n\n")
            return

        # Recent fresh game stats
        recent = fresh_games[-10:] if len(fresh_games) >= 10 else fresh_games

        f.write("### Recent Fresh Game Performance\n\n")
        f.write("| Gen | Training Fit | Fresh Fit | Ratio | Grade | Cause of Death |\n")
        f.write("|-----|--------------|-----------|-------|-------|----------------|\n")

        for g in recent[-10:]:
            train_fit = g.get('best_fitness', 0)
            fresh = g.get('fresh_game', {})
            gen_met = g.get('generalization_metrics', {})
            f.write(f"| {g['generation']} | {train_fit:.0f} | {fresh.get('fitness', 0):.0f} | "
                   f"{gen_met.get('fitness_ratio', 0):.2f} | {gen_met.get('generalization_grade', 'N/A')} | "
                   f"{fresh.get('cause_of_death', 'N/A')} |\n")

        f.write("\n")

        # Summary stats
        all_ratios = [g.get('generalization_metrics', {}).get('fitness_ratio', 0) for g in fresh_games]
        valid_ratios = [r for r in all_ratios if r > 0]
        if valid_ratios:
            avg_ratio = sum(valid_ratios) / len(valid_ratios)
            min_ratio = min(valid_ratios)
            max_ratio = max(valid_ratios)

            f.write("### Generalization Summary\n\n")
            f.write(f"- **Average Fitness Ratio:** {avg_ratio:.2f}\n")
            f.write(f"- **Best Ratio:** {max_ratio:.2f}\n")
            f.write(f"- **Worst Ratio:** {min_ratio:.2f}\n")

            # Grade distribution
            grades = [g.get('generalization_metrics', {}).get('generalization_grade', 'N/A') for g in fresh_games]
            grade_counts = {}
            for grade in grades:
                grade_counts[grade] = grade_counts.get(grade, 0) + 1

            f.write(f"\n**Grade Distribution:** ")
            for grade in ['A', 'B', 'C', 'D', 'F']:
                count = grade_counts.get(grade, 0)
                if count > 0:
                    f.write(f"{grade}:{count} ")
            f.write("\n\n")

    def _write_correlation_matrix(self, f):
        """Write correlation analysis between metrics."""
        if len(self.generations_data) < 10:
            f.write("Not enough data for correlation analysis.\n\n")
            return

        # Get distributions data or calculate from aggregates
        has_distributions = any('distributions' in g for g in self.generations_data)

        if has_distributions:
            # Use full distribution data
            all_fitness = []
            all_kills = []
            all_steps = []
            all_accuracy = []

            for g in self.generations_data:
                if 'distributions' in g:
                    all_fitness.extend(g['distributions'].get('fitness_values', []))
                    all_kills.extend(g['distributions'].get('kills_values', []))
                    all_steps.extend(g['distributions'].get('steps_values', []))
                    all_accuracy.extend(g['distributions'].get('accuracy_values', []))
        else:
            # Use generation-level averages as proxy
            all_fitness = [g['avg_fitness'] for g in self.generations_data]
            all_kills = [g.get('avg_kills', 0) for g in self.generations_data]
            all_steps = [g.get('avg_steps', 0) for g in self.generations_data]
            all_accuracy = [g.get('avg_accuracy', 0) for g in self.generations_data]

        def pearson_correlation(x, y):
            """Calculate Pearson correlation coefficient."""
            if len(x) != len(y) or len(x) < 2:
                return 0.0
            n = len(x)
            mean_x = sum(x) / n
            mean_y = sum(y) / n
            std_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x) / n)
            std_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y) / n)
            if std_x == 0 or std_y == 0:
                return 0.0
            cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
            return cov / (std_x * std_y)

        # Calculate correlations
        corr_kills = pearson_correlation(all_fitness, all_kills)
        corr_steps = pearson_correlation(all_fitness, all_steps)
        corr_accuracy = pearson_correlation(all_fitness, all_accuracy)

        def strength(r):
            r = abs(r)
            if r >= 0.7:
                return "Strong"
            elif r >= 0.4:
                return "Moderate"
            else:
                return "Weak"

        f.write("### Fitness Correlations\n\n")
        f.write("| Metric | Correlation | Strength |\n")
        f.write("|--------|-------------|----------|\n")
        f.write(f"| Kills | {corr_kills:+.2f} | {strength(corr_kills)} |\n")
        f.write(f"| Steps Survived | {corr_steps:+.2f} | {strength(corr_steps)} |\n")
        f.write(f"| Accuracy | {corr_accuracy:+.2f} | {strength(corr_accuracy)} |\n")
        f.write("\n")

        # Interpretation
        f.write("### Interpretation\n\n")
        strongest = max([(abs(corr_kills), 'kills', corr_kills),
                        (abs(corr_steps), 'survival time', corr_steps),
                        (abs(corr_accuracy), 'accuracy', corr_accuracy)])
        f.write(f"Fitness is most strongly predicted by {strongest[1]} (r={strongest[2]:.2f}).\n\n")

    def _write_survival_distribution(self, f):
        """Write survival distribution analysis."""
        if not self.generations_data or 'avg_steps' not in self.generations_data[-1]:
            f.write("No survival data available.\n\n")
            return

        # Get survival data from last phase
        n = len(self.generations_data)
        final_phase = self.generations_data[-max(1, n // 10):]

        avg_survival = sum(g.get('avg_steps', 0) for g in final_phase) / len(final_phase)
        max_survival = max(g.get('max_steps', 0) for g in final_phase)

        # Estimate completion rate (survived to max_steps)
        max_steps_config = self.config.get('max_steps', 1500)

        f.write("### Survival Statistics (Final Phase)\n\n")
        f.write(f"- **Mean Survival:** {avg_survival:.0f} steps ({avg_survival/max_steps_config*100:.1f}% of max)\n")
        f.write(f"- **Max Survival:** {max_survival:.0f} steps\n")

        # Progression over training
        first_phase = self.generations_data[:max(1, n // 10)]
        first_avg_survival = sum(g.get('avg_steps', 0) for g in first_phase) / len(first_phase)

        f.write(f"\n### Survival Progression\n\n")
        f.write("| Phase | Mean Steps | Change |\n")
        f.write("|-------|------------|--------|\n")

        num_phases = min(5, n)
        phase_size = max(1, n // num_phases)
        prev_survival = None

        for phase in range(num_phases):
            start_idx = phase * phase_size
            end_idx = min(start_idx + phase_size, n)
            if phase == num_phases - 1:
                end_idx = n

            phase_data = self.generations_data[start_idx:end_idx]
            phase_survival = sum(g.get('avg_steps', 0) for g in phase_data) / len(phase_data)

            change = ""
            if prev_survival is not None:
                delta = phase_survival - prev_survival
                change = f"{delta:+.0f}"

            f.write(f"| Phase {phase + 1} | {phase_survival:.0f} | {change} |\n")
            prev_survival = phase_survival

        f.write("\n")

    def _write_reward_analysis(self, f):
        """Analyze and write reward component contributions from the last generation."""
        if not self.generations_data or 'avg_reward_breakdown' not in self.generations_data[-1]:
            f.write("No reward component data available for analysis.\n\n")
            return

        # Analyze the last generation for the most relevant snapshot
        last_gen_breakdown = self.generations_data[-1].get('avg_reward_breakdown', {})
        
        if not last_gen_breakdown:
            f.write("Reward breakdown for the last generation is empty.\n\n")
            return

        # Calculate total positive rewards to use as a base for percentages
        total_positive_rewards = sum(v for v in last_gen_breakdown.values() if v > 0)
        
        sorted_components = sorted(last_gen_breakdown.items(), key=lambda item: abs(item[1]), reverse=True)

        f.write("Based on the average scores from the final generation:\n\n")
        f.write("| Reward Component | Avg. Score per Episode | Pct of Positive Rewards |\n")
        f.write("|------------------|------------------------|-------------------------|\n")

        for component, avg_score in sorted_components:
            percentage = (avg_score / total_positive_rewards) * 100 if total_positive_rewards > 0 else 0
            f.write(f"| {component} | {avg_score:,.2f} | {percentage:+.1f}% |\n")
        
        f.write("\n")
        f.write("*Note: Percentages are relative to the sum of all positive rewards in the final generation.*\n\n")

    def _write_learning_progress(self, f):
        """Analyze learning progress."""
        if len(self.generations_data) < 5:
            f.write("Not enough data for learning analysis.\n\n")
            return

        # Compare first 10% to last 10%
        n = len(self.generations_data)
        early_n = max(1, n // 10)
        early = self.generations_data[:early_n]
        late = self.generations_data[-early_n:]

        early_best_avg = sum(g['best_fitness'] for g in early) / len(early)
        late_best_avg = sum(g['best_fitness'] for g in late) / len(late)
        early_avg_avg = sum(g['avg_fitness'] for g in early) / len(early)
        late_avg_avg = sum(g['avg_fitness'] for g in late) / len(late)

        best_improvement = ((late_best_avg - early_best_avg) / max(1, abs(early_best_avg))) * 100
        avg_improvement = ((late_avg_avg - early_avg_avg) / max(1, abs(early_avg_avg))) * 100

        f.write(f"**Comparing First {early_n} vs Last {early_n} Generations:**\n\n")
        f.write(f"| Metric | Early | Late | Change |\n")
        f.write(f"|--------|-------|------|--------|\n")
        f.write(f"| Best Fitness | {early_best_avg:.1f} | {late_best_avg:.1f} | {best_improvement:+.1f}% |\n")
        f.write(f"| Avg Fitness | {early_avg_avg:.1f} | {late_avg_avg:.1f} | {avg_improvement:+.1f}% |\n\n")

        # Learning verdict
        if best_improvement > 50 and avg_improvement > 30:
            f.write("**Verdict:** Strong learning - both best and average fitness improved significantly.\n\n")
        elif best_improvement > 20 or avg_improvement > 20:
            f.write("**Verdict:** Moderate learning - some improvement but room for more training.\n\n")
        elif best_improvement > 0 or avg_improvement > 0:
            f.write("**Verdict:** Weak learning - minimal improvement, consider tuning parameters.\n\n")
        else:
            f.write("**Verdict:** No learning detected - fitness may have decreased. Check for issues.\n\n")

    def _write_convergence_analysis(self, f):
        """Analyze population convergence."""
        if not self.generations_data:
            f.write("No data available.\n\n")
            return

        recent_gens = self.generations_data[-20:]
        avg_std_dev = sum(g['std_dev'] for g in recent_gens) / len(recent_gens)
        avg_range = sum(g['best_fitness'] - g['min_fitness'] for g in recent_gens) / len(recent_gens)

        # Calculate diversity trend
        if len(self.generations_data) >= 20:
            early_std = sum(g['std_dev'] for g in self.generations_data[:10]) / 10
            late_std = sum(g['std_dev'] for g in self.generations_data[-10:]) / 10
            diversity_change = ((late_std - early_std) / max(1, early_std)) * 100
        else:
            diversity_change = 0

        f.write(f"**Recent 20 Generations Analysis:**\n\n")
        f.write(f"- Average Standard Deviation: {avg_std_dev:.2f}\n")
        f.write(f"- Average Range (Best-Min): {avg_range:.2f}\n")
        f.write(f"- Diversity Change: {diversity_change:+.1f}%\n")

        if avg_std_dev < 300:
            f.write(f"- **Status:** Population is converging (low diversity)\n")
        elif avg_std_dev < 800:
            f.write(f"- **Status:** Population has moderate diversity (healthy)\n")
        else:
            f.write(f"- **Status:** High diversity - population is still exploring\n")

        f.write("\n")

    def _write_behavioral_trends(self, f):
        """Analyze behavioral metrics trends."""
        if not self.generations_data or 'avg_kills' not in self.generations_data[-1]:
            f.write("No behavioral data available.\n\n")
            return

        # Compare quarters
        n = len(self.generations_data)
        if n < 4:
            f.write("Not enough data for behavioral trend analysis.\n\n")
            return

        quarter = n // 4
        quarters = [
            self.generations_data[:quarter],
            self.generations_data[quarter:quarter*2],
            self.generations_data[quarter*2:quarter*3],
            self.generations_data[quarter*3:]
        ]

        f.write("| Period | Avg Kills | Avg Steps | Avg Accuracy | Max Kills |\n")
        f.write("|--------|-----------|-----------|--------------|----------|\n")

        for i, q in enumerate(quarters, 1):
            if not q:
                continue
            avg_kills = sum(g.get('avg_kills', 0) for g in q) / len(q)
            avg_steps = sum(g.get('avg_steps', 0) for g in q) / len(q)
            avg_acc = sum(g.get('avg_accuracy', 0) for g in q) / len(q)
            max_kills = max(g.get('max_kills', 0) for g in q)

            f.write(f"| Q{i} | {avg_kills:.2f} | {avg_steps:.0f} | {avg_acc*100:.1f}% | {max_kills} |\n")

        f.write("\n")

    def _write_stagnation_analysis(self, f):
        """Analyze stagnation patterns."""
        if not self.generations_data:
            f.write("No data available.\n\n")
            return

        # Find stagnation periods
        stagnation_periods = []
        current_stagnation = 0
        best_so_far = float('-inf')

        for g in self.generations_data:
            if g['best_fitness'] > best_so_far:
                if current_stagnation > 0:
                    stagnation_periods.append(current_stagnation)
                current_stagnation = 0
                best_so_far = g['best_fitness']
            else:
                current_stagnation += 1

        if current_stagnation > 0:
            stagnation_periods.append(current_stagnation)

        if not stagnation_periods:
            f.write("No stagnation periods detected - fitness improved every generation!\n\n")
            return

        avg_stagnation = sum(stagnation_periods) / len(stagnation_periods)
        max_stagnation = max(stagnation_periods)
        current = self.generations_since_improvement

        f.write(f"- **Current Stagnation:** {current} generations\n")
        f.write(f"- **Average Stagnation Period:** {avg_stagnation:.1f} generations\n")
        f.write(f"- **Longest Stagnation:** {max_stagnation} generations\n")
        f.write(f"- **Number of Stagnation Periods:** {len(stagnation_periods)}\n\n")

        if current > max_stagnation:
            f.write("**Warning:** Current stagnation exceeds previous maximum. Consider:\n")
            f.write("- Increasing mutation rate\n")
            f.write("- Reducing elitism\n")
            f.write("- Adding fresh random individuals\n\n")

    def _write_generation_table(self, f, limit=30, include_behavior=False):
        """Write detailed generation table."""
        recent = self.generations_data[-limit:]

        if include_behavior:
            f.write("| Gen | Best | Avg | StdDev | Kills | Steps | Acc% | Stag |\n")
            f.write("|-----|------|-----|--------|-------|-------|------|------|\n")

            for gen_data in recent:
                f.write(f"| {gen_data['generation']} | ")
                f.write(f"{gen_data['best_fitness']:.0f} | ")
                f.write(f"{gen_data['avg_fitness']:.0f} | ")
                f.write(f"{gen_data['std_dev']:.0f} | ")
                f.write(f"{gen_data.get('avg_kills', 0):.1f} | ")
                f.write(f"{gen_data.get('avg_steps', 0):.0f} | ")
                f.write(f"{gen_data.get('avg_accuracy', 0)*100:.0f} | ")
                f.write(f"{gen_data.get('generations_since_improvement', 0)} |\n")
        else:
            f.write("| Gen | Best | Avg | Min | Median | StdDev | Best D | Avg D |\n")
            f.write("|-----|------|-----|-----|--------|--------|--------|-------|\n")

            for gen_data in recent:
                f.write(f"| {gen_data['generation']} | ")
                f.write(f"{gen_data['best_fitness']:.1f} | ")
                f.write(f"{gen_data['avg_fitness']:.1f} | ")
                f.write(f"{gen_data['min_fitness']:.1f} | ")
                f.write(f"{gen_data['median_fitness']:.1f} | ")
                f.write(f"{gen_data['std_dev']:.1f} | ")
                f.write(f"{gen_data['best_improvement']:+.1f} | ")
                f.write(f"{gen_data['avg_improvement']:+.1f} |\n")

        f.write("\n")

    def _write_best_generations(self, f, include_behavior=False):
        """Write top performing generations."""
        sorted_gens = sorted(self.generations_data, key=lambda x: x['best_fitness'], reverse=True)[:10]

        if include_behavior:
            f.write("| Rank | Gen | Best | Avg | Kills | Steps | Accuracy |\n")
            f.write("|------|-----|------|-----|-------|-------|----------|\n")

            for i, gen_data in enumerate(sorted_gens, 1):
                f.write(f"| {i} | {gen_data['generation']} | ")
                f.write(f"{gen_data['best_fitness']:.0f} | ")
                f.write(f"{gen_data['avg_fitness']:.0f} | ")
                f.write(f"{gen_data.get('best_agent_kills', 0)} | ")
                f.write(f"{gen_data.get('best_agent_steps', 0)} | ")
                f.write(f"{gen_data.get('best_agent_accuracy', 0)*100:.1f}% |\n")
        else:
            f.write("| Rank | Gen | Best Fitness | Avg Fitness | Min Fitness |\n")
            f.write("|------|-----|--------------|-------------|-------------|\n")

            for i, gen_data in enumerate(sorted_gens, 1):
                f.write(f"| {i} | {gen_data['generation']} | ")
                f.write(f"{gen_data['best_fitness']:.2f} | ")
                f.write(f"{gen_data['avg_fitness']:.2f} | ")
                f.write(f"{gen_data['min_fitness']:.2f} |\n")

        f.write("\n")

    def _write_trend_analysis(self, f):
        """Analyze fitness trends over time."""
        if len(self.generations_data) < 10:
            f.write("Not enough data for trend analysis.\n\n")
            return

        # Split into quarters
        total = len(self.generations_data)
        quarter = total // 4

        quarters = [
            self.generations_data[:quarter],
            self.generations_data[quarter:quarter*2],
            self.generations_data[quarter*2:quarter*3],
            self.generations_data[quarter*3:]
        ]

        f.write("| Period | Avg Best | Avg Mean | Avg Min | Improvement |\n")
        f.write("|--------|----------|----------|---------|-------------|\n")

        prev_avg_best = None
        for i, q in enumerate(quarters, 1):
            if not q:
                continue
            avg_best = sum(g['best_fitness'] for g in q) / len(q)
            avg_mean = sum(g['avg_fitness'] for g in q) / len(q)
            avg_min = sum(g['min_fitness'] for g in q) / len(q)

            improvement = ""
            if prev_avg_best is not None:
                delta = avg_best - prev_avg_best
                improvement = f"{delta:+.1f}"

            f.write(f"| Q{i} | {avg_best:.1f} | {avg_mean:.1f} | {avg_min:.1f} | {improvement} |\n")
            prev_avg_best = avg_best

        f.write("\n")

    def _write_ascii_chart(self, f):
        """Generate ASCII chart of fitness progression."""
        if not self.generations_data:
            f.write("No data available.\n\n")
            return

        # Sample data points (every Nth generation for readability)
        step = max(1, len(self.generations_data) // 50)
        sampled = self.generations_data[::step]

        all_best = [g['best_fitness'] for g in sampled]
        all_avg = [g['avg_fitness'] for g in sampled]

        max_val = max(all_best)
        min_val = min(min(all_avg), 0)
        range_val = max_val - min_val

        if range_val == 0:
            f.write("Not enough variance to chart.\n\n")
            return

        f.write("```\n")
        f.write("Best Fitness (*) vs Avg Fitness (o) Over Generations\n\n")

        # Create chart (15 rows for compactness)
        chart_height = 15
        for row in range(chart_height, -1, -1):
            threshold = min_val + (range_val * row / chart_height)

            # Y-axis label
            f.write(f"{threshold:8.0f} |")

            # Plot points
            for i in range(len(sampled)):
                best = all_best[i]
                avg = all_avg[i]

                if best >= threshold and (row == chart_height or best < min_val + (range_val * (row + 1) / chart_height)):
                    f.write("*")
                elif avg >= threshold and (row == chart_height or avg < min_val + (range_val * (row + 1) / chart_height)):
                    f.write("o")
                else:
                    f.write(" ")

            f.write("\n")

        # X-axis
        f.write("         " + "-" * len(sampled) + "\n")
        f.write(f"         Gen 1{' ' * (len(sampled) - 15)}Gen {self.generations_data[-1]['generation']}\n")
        f.write("```\n\n")

    def save_json(self, output_path: str = "training_data.json"):
        """Save raw training data as JSON."""
        data = {
            'schema_version': self.SCHEMA_VERSION,
            'config': self.config,
            'start_time': self.start_time.isoformat(),
            'end_time': datetime.now().isoformat(),
            'summary': self.get_summary_stats(),
            'generations': self.generations_data,
            'fresh_game_data': self.fresh_game_data,
            'distributions_data': self.distributions_data,
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

        print(f"[OK] Raw training data saved to: {output_path}")
        return output_path

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

    def __init__(self):
        self.generations_data = []
        self.start_time = datetime.now()
        self.config = {}
        # Track all-time best for stagnation detection
        self.all_time_best_fitness = float('-inf')
        self.all_time_best_generation = 0
        self.generations_since_improvement = 0

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

        return summary

    def generate_markdown_report(self, output_path: str = "training_summary.md"):
        """Generate comprehensive markdown training report."""
        summary = self.get_summary_stats()
        has_behavior = 'final_avg_kills' in summary

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# Training Summary Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

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
            f.write(f"- **Stagnation:** {summary.get('final_stagnation', 0)} generations since improvement\n\n")

            # Reward Component Analysis
            f.write("## Reward Component Analysis\n\n")
            self._write_reward_analysis(f)

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

            # Convergence Analysis
            f.write("## Convergence Analysis\n\n")
            self._write_convergence_analysis(f)

            # Behavioral Trends (if available)
            if has_behavior:
                f.write("## Behavioral Trends\n\n")
                self._write_behavioral_trends(f)

            # Stagnation Analysis
            f.write("## Stagnation Analysis\n\n")
            self._write_stagnation_analysis(f)

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
            'config': self.config,
            'start_time': self.start_time.isoformat(),
            'end_time': datetime.now().isoformat(),
            'summary': self.get_summary_stats(),
            'generations': self.generations_data
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

        print(f"[OK] Raw training data saved to: {output_path}")
        return output_path

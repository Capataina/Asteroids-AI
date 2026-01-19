"""
Training Analytics and Summary Report Generation

Tracks detailed training metrics including:
- Fitness statistics (best, avg, median, std dev, percentiles)
- Behavioral metrics (kills, accuracy, survival time)
- Learning progress (stagnation detection, improvement rates)
- Population diversity

This module provides a facade (TrainingAnalytics) that delegates to
specialized modules for data collection, analysis, and reporting.
"""

from datetime import datetime
from typing import List, Dict, Any, Optional

from training.analytics.collection.models import AnalyticsData
from training.analytics.collection.collectors import (
    record_generation as _record_generation,
    record_fresh_game as _record_fresh_game,
    record_distributions as _record_distributions
)
from training.analytics.analysis.phases import split_generations
from training.analytics.reporting.markdown import MarkdownReporter
from training.analytics.reporting.json_export import save_json as _save_json


class TrainingAnalytics:
    """Tracks detailed training metrics across generations.

    This class serves as the main entry point for training analytics,
    preserving the original public API while delegating to specialized modules.
    """

    SCHEMA_VERSION = AnalyticsData.SCHEMA_VERSION

    def __init__(self):
        self._data = AnalyticsData()

    @property
    def generations_data(self) -> List[Dict[str, Any]]:
        """Access to generation data for external consumers."""
        return self._data.generations_data

    @property
    def all_time_best_fitness(self) -> float:
        """Access to all-time best fitness."""
        return self._data.all_time_best_fitness

    @property
    def all_time_best_generation(self) -> int:
        """Access to generation number of all-time best."""
        return self._data.all_time_best_generation

    @property
    def generations_since_improvement(self) -> int:
        """Access to stagnation counter."""
        return self._data.generations_since_improvement

    @property
    def config(self) -> Dict[str, Any]:
        """Access to training configuration."""
        return self._data.config

    @property
    def start_time(self) -> datetime:
        """Access to training start time."""
        return self._data.start_time

    @property
    def fresh_game_data(self) -> Dict[int, Dict[str, Any]]:
        """Access to fresh game data."""
        return self._data.fresh_game_data

    @property
    def distributions_data(self) -> Dict[int, Dict[str, Any]]:
        """Access to distributions data."""
        return self._data.distributions_data

    def set_config(self, config: Dict[str, Any]):
        """Store training configuration.

        Args:
            config: Training configuration dictionary
        """
        self._data.set_config(config)

    def record_generation(self, generation: int, fitness_scores: List[float],
                          behavioral_metrics: Optional[Dict[str, Any]] = None,
                          best_agent_stats: Optional[Dict[str, Any]] = None,
                          timing_stats: Optional[Dict[str, float]] = None,
                          operator_stats: Optional[Dict[str, int]] = None):
        """Record metrics for a generation.

        Args:
            generation: Generation number
            fitness_scores: List of fitness scores for all agents
            behavioral_metrics: Optional aggregated behavioral metrics
            best_agent_stats: Optional stats for the best agent
            timing_stats: Optional timing metrics
            operator_stats: Optional genetic operator statistics
        """
        _record_generation(self._data, generation, fitness_scores,
                           behavioral_metrics, best_agent_stats,
                           timing_stats, operator_stats)

    def record_fresh_game(self, generation: int, fresh_game_data: Dict[str, Any],
                          generalization_metrics: Dict[str, Any]):
        """Record fresh game test results for a generation.

        Args:
            generation: Generation number
            fresh_game_data: Fresh game performance metrics
            generalization_metrics: Comparison to training performance
        """
        _record_fresh_game(self._data, generation, fresh_game_data,
                           generalization_metrics)

    def record_distributions(self, generation: int, fitness_values: List[float],
                             per_agent_metrics: List[Dict[str, Any]]):
        """Record per-agent distribution data for a generation.

        Args:
            generation: Generation number
            fitness_values: List of all fitness scores
            per_agent_metrics: List of per-agent behavioral metrics
        """
        _record_distributions(self._data, generation, fitness_values, per_agent_metrics)

    def get_summary_stats(self) -> Dict[str, Any]:
        """Get overall training summary statistics.

        Returns:
            Dictionary with summary statistics
        """
        if not self._data.generations_data:
            return {}

        all_best = [g['best_fitness'] for g in self._data.generations_data]
        all_avg = [g['avg_fitness'] for g in self._data.generations_data]
        all_min = [g['min_fitness'] for g in self._data.generations_data]

        # Calculate improvement trends using phase-based windows
        phases = split_generations(self._data.generations_data, phase_count=4)
        if phases:
            early_vals = [g.get('avg_fitness', 0) for g in phases[0]["data"]]
            late_vals = [g.get('avg_fitness', 0) for g in phases[-1]["data"]]
            early_avg = sum(early_vals) / len(early_vals) if early_vals else 0
            late_avg = sum(late_vals) / len(late_vals) if late_vals else 0
        else:
            early_avg = 0
            late_avg = 0

        # Behavioral metrics summary (if available)
        has_behavior = 'avg_kills' in self._data.generations_data[-1]

        summary = {
            'total_generations': len(self._data.generations_data),
            'training_duration': str(datetime.now() - self._data.start_time),
            'final_best_fitness': all_best[-1],
            'all_time_best_fitness': max(all_best),
            'final_avg_fitness': all_avg[-1],
            'final_min_fitness': all_min[-1],
            'avg_improvement_early_to_late': late_avg - early_avg,
            'best_generation': all_best.index(max(all_best)) + 1,
            'worst_generation': all_best.index(min(all_best)) + 1,
            'final_stagnation': self._data.generations_since_improvement,
        }

        if has_behavior:
            # Average behavioral metrics over last 10 generations
            recent = self._data.generations_data[-10:]
            summary['final_avg_kills'] = sum(g.get('avg_kills', 0) for g in recent) / len(recent)
            summary['final_avg_steps'] = sum(g.get('avg_steps', 0) for g in recent) / len(recent)
            summary['final_avg_accuracy'] = sum(g.get('avg_accuracy', 0) for g in recent) / len(recent)
            summary['max_kills_ever'] = max(g.get('max_kills', 0) for g in self._data.generations_data)
            summary['max_steps_ever'] = max(g.get('max_steps', 0) for g in self._data.generations_data)

        # Fresh game aggregations
        fresh_games = [g for g in self._data.generations_data if 'fresh_game' in g]
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

    def generate_markdown_report(self, output_path: str = "training_summary.md") -> str:
        """Generate comprehensive markdown training report.

        Args:
            output_path: Path to write the report

        Returns:
            Path to the generated report
        """
        summary = self.get_summary_stats()
        reporter = MarkdownReporter(self._data)
        return reporter.generate_report(output_path, summary)

    def save_json(self, output_path: str = "training_data.json") -> str:
        """Save raw training data as JSON.

        Args:
            output_path: Path to write the JSON file

        Returns:
            Path to the saved file
        """
        summary = self.get_summary_stats()
        return _save_json(output_path, self._data, summary)

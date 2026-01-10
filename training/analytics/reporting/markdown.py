"""
Markdown report generator.

Orchestrates the generation of comprehensive markdown training reports.
"""

from datetime import datetime
from typing import Dict, Any

from training.analytics.collection.models import AnalyticsData
from training.analytics.reporting.sections.sparklines import write_sparklines
from training.analytics.reporting.sections.summary import (
    write_config,
    write_overall_summary,
    write_behavioral_summary
)
from training.analytics.reporting.sections.decile import write_decile_breakdown
from training.analytics.reporting.sections.kill_efficiency import write_kill_efficiency
from training.analytics.reporting.sections.rewards import write_reward_evolution
from training.analytics.reporting.sections.population_health import write_population_health
from training.analytics.reporting.sections.stagnation import write_stagnation_analysis
from training.analytics.reporting.sections.generalization import write_generalization_analysis
from training.analytics.reporting.sections.correlation import write_correlation_matrix
from training.analytics.reporting.sections.survival import write_survival_distribution
from training.analytics.reporting.sections.learning import write_learning_progress
from training.analytics.reporting.sections.convergence import write_convergence_analysis
from training.analytics.reporting.sections.behavioral import write_behavioral_trends
from training.analytics.reporting.sections.tables import write_generation_table, write_best_generations
from training.analytics.reporting.sections.trends import write_trend_analysis
from training.analytics.reporting.sections.charts import write_ascii_chart
from training.analytics.reporting.sections.velocity import write_learning_velocity
from training.analytics.reporting.sections.highlights import write_generation_highlights, write_best_agent_profile
from training.analytics.reporting.sections.warnings import write_reward_warnings
from training.analytics.reporting.sections.performance import write_computational_performance, write_genetic_operator_stats
from training.analytics.reporting.sections.milestones import write_milestone_timeline


class MarkdownReporter:
    """Generates comprehensive markdown training reports."""

    def __init__(self, data: AnalyticsData):
        """Initialize the reporter.

        Args:
            data: AnalyticsData instance containing training data
        """
        self.data = data

    def generate_report(self, output_path: str, summary: Dict[str, Any]) -> str:
        """Generate comprehensive markdown training report.

        Args:
            output_path: Path to write the report
            summary: Summary statistics dictionary

        Returns:
            Path to the generated report
        """
        has_behavior = 'final_avg_kills' in summary
        has_fresh_game = 'avg_generalization_ratio' in summary

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# Training Summary Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Schema Version:** {self.data.SCHEMA_VERSION}\n\n")

            # Quick Trend Overview (Sparklines)
            f.write("## Quick Trend Overview\n\n")
            write_sparklines(f, self.data.generations_data)

            # Training Configuration
            write_config(f, self.data.config)

            # Overall Summary
            write_overall_summary(f, summary, has_fresh_game)
            
            # Best Agent Deep Profile
            write_best_agent_profile(f, self.data.generations_data)

            # Generation Highlights
            f.write("## Generation Highlights\n\n")
            write_generation_highlights(f, self.data.generations_data)
            
            # Milestone Timeline
            write_milestone_timeline(f, self.data.generations_data)

            # Training Progress by Decile
            f.write("## Training Progress by Decile\n\n")
            write_decile_breakdown(f, self.data.generations_data)

            # Kill Efficiency Analysis
            f.write("## Kill Efficiency Analysis\n\n")
            write_kill_efficiency(f, self.data.generations_data)

            # Learning Velocity
            f.write("## Learning Velocity\n\n")
            write_learning_velocity(f, self.data.generations_data)

            # Reward Component Evolution
            f.write("## Reward Component Evolution\n\n")
            write_reward_evolution(f, self.data.generations_data)

            # Reward Balance Warnings
            f.write("## Reward Balance Analysis\n\n")
            write_reward_warnings(f, self.data.generations_data)

            # Population Health Dashboard
            f.write("## Population Health Dashboard\n\n")
            write_population_health(f, self.data.generations_data)

            # Stagnation Analysis
            f.write("## Stagnation Analysis\n\n")
            write_stagnation_analysis(f, self.data.generations_data,
                                      self.data.generations_since_improvement)

            # Generalization Analysis (Fresh Game)
            if has_fresh_game:
                f.write("## Generalization Analysis (Fresh Game)\n\n")
                write_generalization_analysis(f, self.data.generations_data)

            # Correlation Matrix
            f.write("## Correlation Analysis\n\n")
            write_correlation_matrix(f, self.data.generations_data)

            # Survival Distribution
            f.write("## Survival Distribution\n\n")
            write_survival_distribution(f, self.data.generations_data, self.data.config)

            # Behavioral Summary (if available)
            if has_behavior:
                write_behavioral_summary(f, summary)

            # Learning Progress
            f.write("## Learning Progress\n\n")
            write_learning_progress(f, self.data.generations_data)

            # Convergence Analysis
            f.write("## Convergence Analysis\n\n")
            write_convergence_analysis(f, self.data.generations_data)

            # Behavioral Trends (if available)
            if has_behavior:
                f.write("## Behavioral Trends\n\n")
                write_behavioral_trends(f, self.data.generations_data)

            # Recent Generations Table
            f.write("## Recent Generations (Last 30)\n\n")
            write_generation_table(f, self.data.generations_data, limit=30,
                                   include_behavior=has_behavior)

            # Best Generations
            f.write("\n## Top 10 Best Generations\n\n")
            write_best_generations(f, self.data.generations_data,
                                   include_behavior=has_behavior)

            # Trend Analysis
            f.write("\n## Trend Analysis\n\n")
            write_trend_analysis(f, self.data.generations_data)

            # ASCII Charts
            f.write("\n## Fitness Progression (ASCII Chart)\n\n")
            write_ascii_chart(f, self.data.generations_data)
            
            # Performance Appendix
            f.write("\n---\n\n# Technical Appendix\n\n")
            write_computational_performance(f, self.data.generations_data)
            write_genetic_operator_stats(f, self.data.generations_data)

        print(f"\n[OK] Training summary saved to: {output_path}")
        return output_path

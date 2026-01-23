"""
Markdown report generator.

Orchestrates the generation of comprehensive markdown training reports.
"""

from datetime import datetime
from typing import Dict, Any

from training.config.analytics import AnalyticsConfig
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
from training.analytics.reporting.sections.behavioral import write_behavioral_trends, write_intra_episode_analysis
from training.analytics.reporting.sections.tables import write_generation_table, write_best_generations
from training.analytics.reporting.sections.trends import write_trend_analysis
from training.analytics.reporting.sections.charts import write_ascii_chart
from training.analytics.reporting.sections.velocity import write_learning_velocity
from training.analytics.reporting.sections.highlights import write_generation_highlights, write_best_agent_profile
from game import globals
from training.analytics.reporting.sections.warnings import write_reward_warnings
from training.analytics.reporting.sections.performance import (
    write_computational_performance,
    write_genetic_operator_stats,
    write_es_optimizer_stats,
)
from training.analytics.reporting.sections.milestones import write_milestone_timeline
from training.analytics.reporting.sections.toc import write_table_of_contents
from training.analytics.reporting.sections.heatmaps import write_heatmaps
from training.analytics.reporting.sections.distribution import write_distribution_charts
from training.analytics.reporting.sections.neural import write_neural_analysis
from training.analytics.reporting.sections.risk import write_risk_analysis
from training.analytics.reporting.sections.control import write_control_diagnostics
from training.analytics.reporting.sections.takeaways import collect_report_takeaways, write_report_takeaways
from training.analytics.reporting.sections.sac_diagnosis import write_sac_diagnosis


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
        has_sac = 'sac' in str(self.data.config.get("method", "")).lower()
        if not has_sac and self.data.generations_data:
            has_sac = any(k.startswith("sac_") for k in self.data.generations_data[-1].keys())

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# Training Summary Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Schema Version:** {self.data.SCHEMA_VERSION}\n\n")
            
            # Table of Contents
            write_table_of_contents(f, has_behavior, has_fresh_game, has_sac)

            # Quick Trend Overview (Sparklines)
            if AnalyticsConfig.ENABLE_QUICK_TRENDS:
                f.write("## Quick Trend Overview\n\n")
                write_sparklines(f, self.data.generations_data)

            # Report Takeaways (all sections)
            takeaways = collect_report_takeaways(
                self.data.generations_data,
                summary,
                has_behavior,
                has_fresh_game
            )
            write_report_takeaways(f, takeaways)

            # Training Configuration
            write_config(f, self.data.config)

            # Overall Summary
            write_overall_summary(f, summary, has_fresh_game)
            
            # Best Agent Deep Profile
            if AnalyticsConfig.ENABLE_BEST_AGENT_PROFILE:
                write_best_agent_profile(f, self.data.generations_data)
            
            # Heatmaps (New)
            if AnalyticsConfig.ENABLE_HEATMAPS:
                write_heatmaps(f, self.data.generations_data, globals.SCREEN_WIDTH, globals.SCREEN_HEIGHT)

            # Generation Highlights
            if AnalyticsConfig.ENABLE_GENERATION_HIGHLIGHTS:
                f.write("## Generation Highlights\n\n")
                write_generation_highlights(f, self.data.generations_data)
            
            # Milestone Timeline
            write_milestone_timeline(f, self.data.generations_data)

            # Training Progress by Phase
            if AnalyticsConfig.ENABLE_PROGRESS_DECILES:
                f.write("## Training Progress by Phase\n\n")
                write_decile_breakdown(f, self.data.generations_data)

            # Distribution Charts (New)
            if AnalyticsConfig.ENABLE_DISTRIBUTIONS:
                write_distribution_charts(f, self.data.generations_data)

            # Kill Efficiency Analysis
            if AnalyticsConfig.ENABLE_KILL_EFFICIENCY:
                f.write("## Kill Efficiency Analysis\n\n")
                write_kill_efficiency(f, self.data.generations_data)

            # Learning Velocity
            if AnalyticsConfig.ENABLE_LEARNING_VELOCITY:
                f.write("## Learning Velocity\n\n")
                write_learning_velocity(f, self.data.generations_data)

            # Reward Component Evolution
            if AnalyticsConfig.ENABLE_REWARD_EVOLUTION:
                f.write("## Reward Component Evolution\n\n")
                write_reward_evolution(f, self.data.generations_data)

            # Reward Balance Warnings
            f.write("## Reward Balance Analysis\n\n")
            write_reward_warnings(f, self.data.generations_data)

            # Population Health Dashboard
            if AnalyticsConfig.ENABLE_POPULATION_HEALTH:
                f.write("## Population Health Dashboard\n\n")
                write_population_health(f, self.data.generations_data)

            # Stagnation Analysis
            if AnalyticsConfig.ENABLE_STAGNATION_ANALYSIS:
                f.write("## Stagnation Analysis\n\n")
                write_stagnation_analysis(f, self.data.generations_data,
                                          self.data.generations_since_improvement)

            # Generalization Analysis (Fresh Game)
            if has_fresh_game and AnalyticsConfig.ENABLE_FRESH_GAME_ANALYSIS:
                f.write("## Generalization Analysis (Fresh Game)\n\n")
                write_generalization_analysis(f, self.data.generations_data)

            # Correlation Matrix
            if AnalyticsConfig.ENABLE_CORRELATIONS:
                f.write("## Correlation Analysis\n\n")
                write_correlation_matrix(f, self.data.generations_data)

            # Survival Distribution
            if AnalyticsConfig.ENABLE_SURVIVAL_DISTRIBUTION:
                f.write("## Survival Distribution\n\n")
                write_survival_distribution(f, self.data.generations_data, self.data.config)

            # Behavioral Summary (if available)
            if has_behavior and AnalyticsConfig.ENABLE_BEHAVIORAL_SUMMARY:
                write_behavioral_summary(f, summary)

            # Learning Progress
            f.write("## Learning Progress\n\n")
            write_learning_progress(f, self.data.generations_data)

            # Neural Analysis (New)
            if AnalyticsConfig.ENABLE_NEURAL_ANALYSIS:
                write_neural_analysis(f, self.data.generations_data)

            # Risk Analysis (New)
            if AnalyticsConfig.ENABLE_RISK_ANALYSIS:
                write_risk_analysis(f, self.data.generations_data)

            # Control Diagnostics
            if AnalyticsConfig.ENABLE_CONTROL_DIAGNOSTICS:
                write_control_diagnostics(f, self.data.generations_data)

            # SAC Diagnostics (GNN-SAC only)
            if has_sac and AnalyticsConfig.ENABLE_SAC_DIAGNOSIS:
                write_sac_diagnosis(f, self.data.generations_data, self.data.config)

            # Convergence Analysis
            if AnalyticsConfig.ENABLE_CONVERGENCE_ANALYSIS:
                f.write("## Convergence Analysis\n\n")
                write_convergence_analysis(f, self.data.generations_data)

            # Behavioral Trends (if available)
            if has_behavior and AnalyticsConfig.ENABLE_BEHAVIORAL_TRENDS:
                f.write("## Behavioral Trends\n\n")
                write_behavioral_trends(f, self.data.generations_data)
                write_intra_episode_analysis(f, self.data.generations_data)

            # Recent Generations Table
            if AnalyticsConfig.ENABLE_RECENT_TABLE:
                f.write(f"## Recent Generations (Last {AnalyticsConfig.RECENT_TABLE_WINDOW})\n\n")
                write_generation_table(f, self.data.generations_data, limit=AnalyticsConfig.RECENT_TABLE_WINDOW,
                                       include_behavior=has_behavior)

            # Best Generations
            if AnalyticsConfig.ENABLE_TOP_GENERATIONS:
                f.write("\n## Top 10 Best Generations\n\n")
                write_best_generations(f, self.data.generations_data,
                                       include_behavior=has_behavior)

            # Trend Analysis
            f.write("\n## Trend Analysis\n\n")
            write_trend_analysis(f, self.data.generations_data)

            # ASCII Charts
            if AnalyticsConfig.ENABLE_ASCII_CHARTS:
                f.write("\n## Fitness Progression (ASCII Chart)\n\n")
                write_ascii_chart(f, self.data.generations_data)
            
            # Performance Appendix
            f.write("\n---\n\n# Technical Appendix\n\n")
            write_computational_performance(f, self.data.generations_data)
            write_genetic_operator_stats(f, self.data.generations_data)
            write_es_optimizer_stats(f, self.data.generations_data)

        print(f"\n[OK] Training summary saved to: {output_path}")
        return output_path

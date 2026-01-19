"""
Table of Contents generator for markdown reports.
"""

def write_table_of_contents(f, has_behavior: bool, has_fresh_game: bool):
    """Write a clickable Table of Contents.

    Args:
        f: File handle to write to
        has_behavior: Whether behavioral sections are included
        has_fresh_game: Whether fresh game sections are included
    """
    f.write("## Table of Contents\n\n")
    f.write("- [Quick Trend Overview](#quick-trend-overview)\n")
    f.write("- [Report Takeaways (All Sections)](#report-takeaways-all-sections)\n")
    f.write("- [Training Configuration](#training-configuration)\n")
    f.write("- [Overall Summary](#overall-summary)\n")
    f.write("- [Best Agent Deep Profile](#best-agent-deep-profile)\n")
    f.write("- [Generation Highlights](#generation-highlights)\n")
    f.write("- [Milestone Timeline](#milestone-timeline)\n")
    f.write("- [Training Progress by Phase](#training-progress-by-phase)\n")
    f.write("- [Distribution Analysis](#distribution-analysis)\n")
    f.write("- [Kill Efficiency Analysis](#kill-efficiency-analysis)\n")
    f.write("- [Learning Velocity](#learning-velocity)\n")
    f.write("- [Reward Component Evolution](#reward-component-evolution)\n")
    f.write("- [Reward Balance Analysis](#reward-balance-analysis)\n")
    f.write("- [Population Health Dashboard](#population-health-dashboard)\n")
    f.write("- [Stagnation Analysis](#stagnation-analysis)\n")
    
    if has_fresh_game:
        f.write("- [Generalization Analysis (Fresh Game)](#generalization-analysis-fresh-game)\n")

    f.write("- [Correlation Analysis](#correlation-analysis)\n")
    f.write("- [Survival Distribution](#survival-distribution)\n")
    
    if has_behavior:
        f.write("- [Behavioral Summary](#behavioral-summary-last-10-generations)\n")

    f.write("- [Learning Progress](#learning-progress)\n")
    f.write("- [Neural & Behavioral Complexity](#neural--behavioral-complexity)\n")
    f.write("- [Risk Profile Analysis](#risk-profile-analysis)\n")
    f.write("- [Control Diagnostics](#control-diagnostics)\n")
    f.write("- [Convergence Analysis](#convergence-analysis)\n")
    
    if has_behavior:
        f.write("- [Behavioral Trends](#behavioral-trends)\n")

    f.write("- [Recent Generations](#recent-generations-last-30)\n")
    f.write("- [Top 10 Best Generations](#top-10-best-generations)\n")
    f.write("- [Trend Analysis](#trend-analysis)\n")
    f.write("- [Fitness Progression](#fitness-progression-ascii-chart)\n")
    f.write("- [Technical Appendix](#technical-appendix)\n")
    f.write("\n---\n\n")

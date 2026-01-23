"""
Analytics Configuration

Centralized configuration for training reports and analysis.
Controls which sections are generated and their specific data windows.
"""

class AnalyticsConfig:
    # --- Output Settings ---
    REPORT_FILENAME = "training_summary.md"
    DATA_FILENAME = "training_data.json"
    
    # --- Section Toggles ---
    ENABLE_QUICK_TRENDS = True
    ENABLE_BEST_AGENT_PROFILE = True
    ENABLE_GENERATION_HIGHLIGHTS = True
    ENABLE_PROGRESS_DECILES = True
    ENABLE_KILL_EFFICIENCY = True
    ENABLE_LEARNING_VELOCITY = True
    ENABLE_REWARD_EVOLUTION = True
    ENABLE_POPULATION_HEALTH = True
    ENABLE_STAGNATION_ANALYSIS = True
    ENABLE_FRESH_GAME_ANALYSIS = True
    ENABLE_CORRELATIONS = True
    ENABLE_SURVIVAL_DISTRIBUTION = True
    ENABLE_BEHAVIORAL_SUMMARY = True
    ENABLE_CONVERGENCE_ANALYSIS = True
    ENABLE_BEHAVIORAL_TRENDS = True
    ENABLE_RECENT_TABLE = True
    ENABLE_TOP_GENERATIONS = True
    ENABLE_ASCII_CHARTS = True
    
    # New Sections
    ENABLE_DISTRIBUTIONS = True  # Mean +/- StdDev charts
    ENABLE_HEATMAPS = True       # Spatial analytics
    ENABLE_NEURAL_ANALYSIS = True # Saturation & Entropy
    ENABLE_RISK_ANALYSIS = True   # Min proximity tracking
    ENABLE_CONTROL_DIAGNOSTICS = True # Turn/aim/danger diagnostics
    ENABLE_SAC_DIAGNOSIS = True      # GNN-SAC specific diagnostics section

    # --- Phase Settings ---
    PHASE_COUNT = 4  # Default report phases (25% each)
    
    # --- Window Sizes (Granular) ---
    # Number of recent generations to include in analysis/visualization
    
    # Heatmaps: Aggregating too many turns into a blob; too few is noisy.
    HEATMAP_WINDOW = 10
    
    # Distributions: How many generations back to show the ASCII bars for
    DISTRIBUTION_WINDOW = 10
    
    # Behavioral Trends: For the "Recent Generations" detailed table
    RECENT_TABLE_WINDOW = 30
    
    # Fresh Game: Generalization analysis often needs a longer history
    FRESH_GAME_WINDOW = 20
    
    # Behavioral Summary: "Last X Generations" stats
    BEHAVIORAL_SUMMARY_WINDOW = 10
    
    # Convergence: How far back to look for stability/diversity trends
    CONVERGENCE_WINDOW = 20
    
    # --- Visual Settings ---
    CHART_WIDTH = 50  # Character width for ASCII bars
    SPARKLINE_WIDTH = 20  # Quick trend sparkline columns (5% bins)

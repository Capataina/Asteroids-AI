# Training Analytics System

## Overview

The training system now includes comprehensive analytics tracking and automatic report generation. Every generation's performance is recorded with detailed metrics, and when training completes (or is interrupted), a full analysis report is automatically generated.

## What Gets Tracked

### Per-Generation Metrics

For each generation, the following metrics are recorded:

- **Best Fitness**: Highest fitness score in the generation
- **Average Fitness**: Mean fitness across all agents
- **Minimum Fitness**: Lowest fitness score in the generation
- **Median Fitness**: Middle value of fitness distribution
- **Standard Deviation**: Measure of population diversity
- **Best Improvement**: Change in best fitness from previous generation
- **Average Improvement**: Change in average fitness from previous generation

### Console Output

During training, you'll now see more detailed output:

```
Generation 143: Best=1566.40, Avg=463.72, Min=21.21, Median=450.00, StdDev=420.15, All-time Best=35957.21
```

This helps you monitor:
- Whether the population is improving (Avg should trend up)
- Population diversity (StdDev - higher = more exploration)
- Convergence (gap between Best and Min should narrow over time)

## Generated Reports

When training completes or is interrupted, two files are automatically saved:

### 1. `training_summary.md` - Human-Readable Report

A comprehensive markdown report containing:

#### Training Configuration
- Population size, generations, mutation/crossover parameters
- All hyperparameters used

#### Overall Summary
- Total generations completed
- Training duration
- All-time best fitness and when it occurred
- Final population statistics
- Average improvement from early to late training

#### Convergence Analysis
- Recent 20 generations analysis
- Population diversity metrics
- Convergence status indicator:
  - 🟢 Green: Population converging well (low std dev)
  - 🟡 Yellow: Moderate diversity
  - 🔴 Red: High diversity, not converging (potential issue)

#### Recent Generations Table
Detailed table of last 50 generations with all metrics

#### Top 10 Best Generations
Ranked list of best-performing generations

#### Trend Analysis
Breaks training into quarters to show progression over time

#### ASCII Fitness Chart
Visual representation of Best vs Average fitness over time

### 2. `training_data.json` - Raw Data

Complete training data in JSON format for:
- Custom analysis
- Plotting with external tools
- Comparing different training runs
- Archiving results

## Interpreting Results

### Good Learning Indicators

✅ **Average fitness increasing steadily**
- Shows the whole population is improving, not just lucky outliers

✅ **Min fitness improving**
- Even the worst agents are getting better

✅ **Standard deviation decreasing over time**
- Population is converging toward optimal behavior

✅ **Gap between Best and Average narrowing**
- Consistent performance across population

### Warning Signs

⚠️ **Average staying flat while Best increases**
- Only elite agents improving (your current issue!)
- May need: higher mutation rate, more exploration, better reward structure

⚠️ **High standard deviation throughout**
- Population not converging
- May need: stronger selection pressure, more generations

⚠️ **Min fitness staying near zero**
- Many agents are failing completely
- May need: curriculum learning, easier initial tasks

⚠️ **Best fitness plateauing early**
- Local optimum found
- May need: more exploration, restart with different initialization

## Example Output

```markdown
# Training Summary Report

**Generated:** 2026-01-04 15:30:22

## Training Configuration
```
population_size: 100
num_generations: 500
mutation_probability: 0.35
mutation_gaussian_sigma: 0.3
...
```

## Overall Summary
- **Total Generations:** 165
- **Training Duration:** 2:45:33
- **All-Time Best Fitness:** 35957.21
- **Best Generation:** 89
- **Final Average Fitness:** 1100.00
- **Avg Improvement (Early→Late):** +850.30

## Convergence Analysis
**Recent 20 Generations Analysis:**
- Average Standard Deviation: 1250.45
- Average Range (Best-Min): 3000.20
- **Status:** 🟡 Population showing moderate diversity

...
```

## Usage Tips

1. **Monitor during training**: Watch the console output to see if learning is happening
2. **Review summary after training**: Check convergence analysis for issues
3. **Compare runs**: Save summaries with different names to compare configurations
4. **Look for trends**: The quarter-by-quarter analysis shows if learning stalled
5. **Check ASCII chart**: Quick visual indication of overall progress

## What Your Current Data Shows

From your console output, I can see:
- **Best fitness is very high** (35957.21) - great!
- **Min/Avg aren't improving** - population not learning from the best
- **High variance** - suggests agents are very different, not converging

This indicates your GA might need:
- Stronger elitism (keep more top performers)
- Better crossover to spread good traits
- More generations for convergence
- Or the reward structure needs tuning

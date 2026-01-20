# Training Summary Report

**Generated:** 2026-01-20 01:35:49
**Schema Version:** 2.1

## Table of Contents

- [Quick Trend Overview](#quick-trend-overview)
- [Report Takeaways (All Sections)](#report-takeaways-all-sections)
- [Training Configuration](#training-configuration)
- [Overall Summary](#overall-summary)
- [Best Agent Deep Profile](#best-agent-deep-profile)
- [Generation Highlights](#generation-highlights)
- [Milestone Timeline](#milestone-timeline)
- [Training Progress by Phase](#training-progress-by-phase)
- [Distribution Analysis](#distribution-analysis)
- [Kill Efficiency Analysis](#kill-efficiency-analysis)
- [Learning Velocity](#learning-velocity)
- [Reward Component Evolution](#reward-component-evolution)
- [Reward Balance Analysis](#reward-balance-analysis)
- [Population Health Dashboard](#population-health-dashboard)
- [Stagnation Analysis](#stagnation-analysis)
- [Generalization Analysis (Fresh Game)](#generalization-analysis-fresh-game)
- [Correlation Analysis](#correlation-analysis)
- [Survival Distribution](#survival-distribution)
- [Behavioral Summary](#behavioral-summary-last-10-generations)
- [Learning Progress](#learning-progress)
- [Neural & Behavioral Complexity](#neural--behavioral-complexity)
- [Risk Profile Analysis](#risk-profile-analysis)
- [Control Diagnostics](#control-diagnostics)
- [Convergence Analysis](#convergence-analysis)
- [Behavioral Trends](#behavioral-trends)
- [Recent Generations](#recent-generations-last-30)
- [Top 10 Best Generations](#top-10-best-generations)
- [Trend Analysis](#trend-analysis)
- [Fitness Progression](#fitness-progression-ascii-chart)
- [Technical Appendix](#technical-appendix)

---

## Quick Trend Overview

```
Best Fitness     96 -> 60  [: :::=--*@%+:=:-   .]  slight regression (low confidence)
Avg Fitness      -127 -> -151  [::--=*%%%#@*+:::   :]  slight regression (moderate confidence)
Min Fitness      -235 -> -245  [#+-+--##%#@#-+*+ - :]  slight regression (moderate confidence)
Fitness Spread   78 -> 66  [ .:-=+=*+@%*==-:   .]  steady improvement (moderate confidence)
Avg Kills        3.3 -> 2.3  [.:-:=*%@##%++:..   .]  slight regression (moderate confidence)
Avg Accuracy     29% -> 25%  [*==:=+%#%@%*=-:: ..-]  stagnation (low confidence)
Avg Steps        509 -> 447  [-:-:=*%@%#%++:-: . :]  slight regression (moderate confidence)
Action Entropy   1.50 -> 1.64  [  :=+:  --:-**+=::%@]  stagnation (low confidence)
Output Saturation 38% -> 50%  [ ::..=*#**##++**%@**]  stagnation (low confidence (noisy))
Frontness Avg    52% -> 52%  [:+-*-      -=#:==:@+]  stagnation (low confidence)
Danger Exposure  14% -> 15%  [= = :#--.-=-.- -*++@]  volatile (low confidence (noisy))
Seed Fitness Std 105.8 -> 89.1  [.:-:-*#@###+=:..   :]  steady improvement (moderate confidence)
```

### Quick Trend Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Average fitness:** Mean fitness across the population for a generation.
- **Minimum fitness:** Lowest fitness in the population for a generation.
- **Fitness std dev:** Standard deviation of fitness across the population (diversity proxy).
- **Average kills:** Mean kills per episode across the population.
- **Accuracy:** Hits divided by shots fired (0 to 1).
- **Average steps:** Mean steps survived per episode across the population.
- **Action entropy:** Entropy of action combinations (higher = more varied control).
- **Output saturation:** Share of NN outputs near 0 or 1 (binary control tendency).
- **Frontness average:** Alignment of nearest asteroid with ship heading (1 ahead, 0 behind).
- **Danger exposure rate:** Fraction of frames with a nearby asteroid inside danger radius.
- **Soft-min TTC:** Weighted time-to-collision proxy that emphasizes the nearest threats (seconds).
- **Seed fitness std:** Average per-agent fitness std dev across seeds (evaluation noise proxy).

## Report Takeaways (All Sections)

- Quick Trend Overview: sparklines summarize phase-based metric direction and confidence.
- Training Configuration: report includes a full hyperparameter snapshot for reproducibility.
- Overall Summary: best fitness 384.59 at Gen 25.
- Best Agent Deep Profile: Gen 25 with 18.4 kills.
- Heatmaps: spatial patterns available for best agent and population.
- Generation Highlights: top improvements/regressions and record runs flagged.
- Milestone Timeline: milestones are run-relative (percent-of-peak thresholds).
- Training Progress by Phase: 4 equal phases used for normalized comparisons.
- Distribution Analysis: fitness spread trend is steady improvement.
- Kill Efficiency: phase-level kill rates and shot efficiency tracked.
- Learning Velocity: phase-based fitness deltas and acceleration reported.
- Reward Component Evolution: per-component shifts tracked across 4 phases.
- Reward Balance Analysis: dominance, entropy, and penalty skew checked.
- Population Health Dashboard: diversity, elite gap, and floor trends summarized.
- Stagnation Analysis: plateau lengths compared to run history.
- Generalization Analysis: fresh-game ratios and reward transfer gaps reported.
- Correlation Analysis: fitness vs kills/survival/accuracy correlations reported.
- Survival Distribution: phase-level survival averages and max survival summarized.
- Behavioral Summary: recent kills, steps, and accuracy summarized.
- Learning Progress: phase comparisons for best/avg/min fitness.
- Neural & Behavioral Complexity: saturation and entropy trends reported.
- Risk Profile Analysis: proximity trends and archetypes reported.
- Control Diagnostics: turn bias, frontness, danger, and movement diagnostics reported.
- Convergence Analysis: recent diversity and range trends summarized.
- Behavioral Trends: action mix and intra-episode scoring patterns reported.
- Recent Generations: last 30 gens tabulated.
- Top Generations: best run is Gen 25.
- Trend Analysis: phase-based fitness trend table provided.
- ASCII Chart: best vs avg fitness progression visualized.
- Technical Appendix: runtime costs, operator stats, and ES optimizer diagnostics reported when available.

## Training Configuration

```
method: NEAT
population_size: 50
num_generations: 500
seeds_per_agent: 5
use_common_seeds: True
compatibility_threshold: 0.25
c1: 1.0
c2: 1.0
c3: 0.4
weight_mutation_prob: 0.1
weight_mutation_sigma: 0.5
add_connection_prob: 0.05
add_node_prob: 0.03
crossover_prob: 0.75
inherit_disabled_prob: 0.75
elitism_per_species: 1
species_stagnation: 7
max_nodes: None
max_connections: None
novelty_enabled: True
diversity_enabled: True
turn_deadzone: 0.03
max_workers: 16
```

### Config Takeaways

- Configuration snapshot captures the exact training parameters for reproducibility.

### Config Glossary

- **Config value:** Literal hyperparameter or run setting recorded at training start.

## Overall Summary

- **Total Generations:** 49
- **Training Duration:** 1:07:00.974410
- **All-Time Best Fitness:** 384.59
- **Best Generation:** 25
- **Final Best Fitness:** 69.23
- **Final Average Fitness:** -135.86
- **Avg Improvement (Phase 1->Phase 4):** -23.78
- **Stagnation:** 24 generations since improvement

**Generalization (Fresh Game Performance):**
- Avg Generalization Ratio: 3.31
- Best Fresh Fitness: 544.62 (Gen 22)
- Episode Completion Rate: 20.4%

### Takeaways

- Best fitness achieved: 384.59 (Gen 25).
- Final avg fitness: -135.86.
- Current stagnation: 24 generations without improvement.

### Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Average fitness:** Mean fitness across the population for a generation.
- **Minimum fitness:** Lowest fitness in the population for a generation.
- **Avg improvement (Phase 1->Phase 4):** Difference between average fitness in the first and last 25% of training.
- **Generalization ratio:** Fresh-game fitness divided by training fitness (averaged across fresh runs).
- **Episode completion rate:** Share of fresh-game episodes that completed the full max-step window.

## Best Agent Deep Profile

The most fit agent appeared in **Generation 25** with a fitness of **384.59**.

### Combat Efficiency

- **Total Kills:** 18.4
- **Survival Time:** 22.9 seconds (1375.4 steps)
- **Accuracy:** 48.9%
- **Shots per Kill:** 2.0
- **Time per Kill:** 1.25 seconds

### Behavioral Signature

**Classification:** `Balanced`

| Action | Rate (per step) | Description |
|--------|-----------------|-------------|
| **Thrust** | 37.7% | Movement frequency |
| **Turn** | 97.7% | Rotation frequency |
| **Shoot** | 74.7% | Trigger discipline |

### Takeaways

- Best agent achieved 18.4 kills with 48.9% accuracy.
- Behavioral classification: Balanced.

### Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Accuracy:** Hits divided by shots fired (0 to 1).
- **Average steps:** Mean steps survived per episode across the population.
- **Shots per kill:** Shots fired divided by kills (lower is more efficient).

### Spatial Analytics (Best Agent - Generations 40-49)

**Position Heatmap (Where does it fly?)**
```
|                .                 .       :     .         .     ...  :   ..                                             |
|                                    .      .                 .  : :             .     . ::::                            |
|                              .                          .      .  .         .  .. .     .      .     .   .             |
|                      .                  .              .    .   .         .      .        .        .                   |
|                 .                                       . .            ..                          .       .           |
|                                     .                                  .      .    ..     .   .                        |
|.        .         .                                         ..  :  :..    .      .:              .                 .   |
|                                    .         .       . ::...    .  ..     ..  .                  .    .       . .      |
|                                                .:.   :  . : .  . ..:   ..       .      .    .         .    :           |
|              .                                .    :   .      .:::.:.                     .    .   .  ..               |
|.                                      .     .    .    .  .  . ...:: -.     .    .. . .  .. .      .      .             |
|                  .            .              . ..::  .    .  ..  .:  .   .    ..--     .  .      .              ..     |
|   .                          .. .           :     ...     ::::. .   . .     . .       .    ..  ...    :                |
|                                 .        . ..    .  ..:-:- =::-. :..  ..    .  ..   . :   :..  ..       .       . .    |
|                     .       .       .      .     :   ..:---@==--::-. ::            ..  ..:  . :   .:              .    |
|      .                   .              .  .  .: ....:. ::.-: : -:.. :  . .  .  .  .  ::::..                  .   . .  |
|  .                .    . .     .    . ..                 .:=..=.   : . .. .: .    .   .    .  .   .   .         .      |
|         .                 .          .  .    .       ... :   ::.:=.::::: .    .          :. .                          |
|                                     :    .    .        .. . ...    : ...::             ...  ....   . .               . |
|.         .                                          . ...   .  .       .  .  :   .     . .      .    .       . .       |
|                              .    .              ..        .. .     .            .. .   .        .         .           |
|.               .                                :      .              :       .         ... .       .                  |
|          .                        .      .        .    ..                     .                 ..                     |
|                     .          .          .             .           .         . .         .                            |
|             .            .                  .          .        . :                     .:                             |
|                               .                        .        .                                                      |
|                  .        .                                       . .   .        . .     :                             |
|         .                   .               :                       .             .               .                    |
|                .          .     .           .                      .       .            .                              |
|                         .       .                        .       :     .      .       : .   . .                        |
```

**Kill Zone Heatmap (Where does it kill?)**
```
|                                                                 ::  :         ::-      :                               |
|                                        :                     : :::          :   :       ::-       -                    |
|                           :   :        :               : :     :  :      :   :  -                        :             |
|                                                         :                ::      :                 :                   |
|                     :                                                       :              :     :       ::            |
|                                            :              :           :            :              :   ::               |
| :     :                                   :                 : ::        :        ::              ::                :   |
|                                      :   :  :         ::-  ::              :     :                    :                |
|                                                  ::  : :  :   :        :      :                            :           |
|                                                          :    : :- -                   :   :   :  :   :   :  :         |
|::                    :                      :         -   :   :-: : =             : :            ::                    |
|                              :                 : :      :    -:   :      : :   -:      :      : :      :     :         |
|                                 :           :     -  :   :::=:  :     :   : :         :     :              :           |
|     :       :                 :            -    :    :=+- -=:--::  :             :   : :  ::=  :                       |
|            :      :                      :       =  :   -+:@+:- =-  -:               :   -  :::                        |
|                                              : :-   :    : +: : -  :                   :   -          :                |
|                           :   ::                     :   + #  #   :       :=                                           |
|                            : :       :             :::::     =: -%:: :-::               :                              |
|                                     :     :           : :   : :    :   -  ::    :    :            :                :   |
|                                                     :       ::         :        :      -       :                :      |
|               :                      :      :              :        :         :  : :                                   |
|                             :                        ::                       :        : ::         :                  |
|          :                       ::      :     :                              -      :        : :::                    |
|            ::      :                                            :             ::                                       |
|                                                :       =            :          : : :   : :     :         :             |
|           :                 :             :               :                            :                               |
|                              :           :                         ::                    : :                           |
|                                            :    :                   -    :      :    :   :                             |
|                           ::         :                            :                                                    |
|                                      : :                         :    :      :                   :                     |
```

### Spatial Analytics (Population Average - Generations 40-49)

**Position Heatmap (Where do they fly?)**
```
|      .              . . .   .   .        .     ..   .  . : ..   ... ..  :    . .. . .     . . . . .           .        |
|     .                  . .         .              .     .. :  ..... .. ..  . :.   . . ....... . .      ..     .     .  |
|             .     .. .  .   ..        ..  . .. .    . ..  ..... . : .    . ...... .  .. .. .... ....  ..   .. . .    . |
|                .     .    .   .              :  ... .  .:::.:::::... .    . .:.    .  .  .. : .     ..  .              |
|.               ..   .    . .. ..  .      . ... ...:...  ::. . :::..:.:.:.:.. .   .     ...  . .    .    .. .   .    .  |
|    ..   .:  . . .         :   .     .        ...     :. .  ... ....::....:.:...  . ..     . ..... .    .. .  ..      . |
|     .       .  .       .   .        .... .  .  .    ... .... .:....... ::::::::: ...........: . ......   . .. . .    . |
|.     ..         . .       ...    .  .  . .   .  . .. : ......  ......:...::.:::.::   .. : ::........ ... .  ..   .. .  |
|.  .      .     ..    .      .  ..        ...   ........:::....:....:...:.....-:..:-:: .: ..... :.  . :..... .  ..  .   |
| ..  ..  .. . .  ..       .    .        . .   .. ..:. . .::. :.::.::..::-.:::.:-=---....:::::..:::.:.:: . ..   :.... :. |
|....    .       ..     ..   .      ..  :.. ..   ......::. ......:..::-:.-::::---:==-..:.:.:::.:.:::::...:.:: ::......   |
|... . . . .  .     . .   . ...   .   . .    ... . . ::...:.::::::::-:::..::-.::=-=#. ..:::::::: :-::-:::.::.   .. .:. . |
| . :. ...   . . ...  .   .    ...      .  .    . ..:::.:.::::-:::-:::-::-::::::-:-.:::.:::.::.::--+--:---:::.:.:. ..  . |
|.. ..  .       .         . .       ..       .. ....::.::.-::---:-------:::.::::::..:::.::.:::.:::-.:::-:::-::..:....:.. |
|.. :.. .  ...  .     . ..     .  .. .. .  . ..: .:-: :::--==@=-----:::::.:.::..: :...:::::::::::::.::::::..::..::.::..  |
|.... .   .      .     .   .          . .:.  ....: . .:::--===---::::::-:.: .: .:.:....::::--:::-::::-:::.:.:.:.:. .:...:|
| :....   .....     .      .   ...  .   ... . :..   ....:-:::-::-:.:::.:...:....:..:...::---:--:::-.::.:::: ::::...:.:.. |
|... .... ..  ...  .   .  ..  .        .. ..... . :. . .:.::.::::::-..::::.. :.::..:..:.=*=-----:-=:-:::::::::..:.. . .:.|
|..    ..    .  .    .....      .         . .   ...  ..:.:.::.::....... :.: ... . . ...:::-::-:::---::::... .:  :... . ..|
|. . .    .   .     .  .     .   .    ..       ..    . ...:. .:. .... .. ....: ..:.::... :.:. ::.:-.::::: ::...: . ...  .|
|.   ..:  . ..       .         .         .  .   .  .....   . .: .... ..: . ::... . :.:. .. .. ....:.:.:.:.. ...  :     ..|
|.  . . .     .. .   ..         .  .              .  .   .  .. ..   .. . .:. : ...: ......  .... .....:  . ........ :  . |
|..        . . ..   . .   . .     .        .        ..   .: ..  .  ..  ...  .....     .. .  ...   :.:.::.:  .:  ... . .  |
|.      . ... . .  .  .     .       .   .  .   .  .     ...   . .      .    .. ....:.. ... . .:. ... .  .... .....       |
|         .     .  .  ..     .                   .  .  .   .. .  ..  ......  . .. . ... . . ... . :.   ::.      .    .   |
|     .    .   ..             . .  .    .      . .        .  . ....   .    . .. . .. ..  .  . . .      .. .   .     .    |
|   .   .    ..  . .. .    ..     .     .          .   .    . . ..  . .. .   .  .  ...     ..    . .  :...               |
|     . .        .              .        .       .   ..  .   .:.. ..  .. .. . . .      ... .     .     .. .      .       |
|      .              .     ..    .   .                .   ...    ..  .  . . .  .  . . ....         .       ...          |
|  ..           .    .   .      . ..      .      . .   ... .   .  .   .. . .  ...   .. ....  .. .     .   .        .. .  |
```

**Kill Zone Heatmap (Where do they kill?)**
```
|.  : . .:    .  .  . :      .      .   ..       .:  .:    .  . .:    .   .   .:.:: .  :. .. .   ..         . .    . .. .|
|  . .         .      . .  .  .. .   :   :     . ..    .  : ..:: :.:.  : .:..:. ... .:  : :::  :.   :   .:.    .   .  .  |
| .        .  .    .. .  .:.:   .       ..  .   : . :.. :-::  ..::  : :....: :..:::        . ..: ..:. ..   .      .      |
|       . :..           :.   . ..   . :.      ..  .. :.....:.   :  .::.   .-.. ..  ..      : .:.  :.   :.: .    . . ..  .|
|:.     .       .  ...   : -....     .. .     :      - : .:. .     .. :  ::...: ... .   ... :::-   ::  .  ....  .      . |
|.            .:..  .  .    :.      .   .    .  .     :.  ..  ..  :..- :::   ..:.. . .... .. ::..:: . . ..  ..     .: .: |
|. ...:.       .    .. ..    .. .          :::..          :  . :::: . ... :    .: .: - .:   ..: ..:-: ... :  :. .. :     |
|    . .    .  .: ..   .         . .       . ..  .: ..::.:.:..: :: :........:::: ..: :: . ..:..::  .::  .  ..:.   .: .   |
| .    : : :.    :..    :   .  .   . .  .  :. .  . . -   -:::.. :..: .... :. . .:. :.--: : .: . :.-.     :. .::.  :    . |
|  . :.......   .  .:.    . :   .   :     - : .:..:  .. :: ::.. ..:--..-:-.-: .=:.. .: =..  :.  .-:.:  :.  ..  .: . . :  |
|. . .        ..:   .      .  .     :  ..: . :..    .. .- ...: . .::=:--::: =+=-:+- ...::. :.:-::.::-.-:: . : :.   ...   |
|.   :. - .. .      . .:  .   .:       .   . ....  ....:..  ::--.::-:=:...:...:-:-.-=:-=+:.:.: :::-.:::  :.:  .. . .. ::.|
| ... . .     .  .. . :      .          . . . .   :- .-:.. ::.=:::=:::::::-..::::.:::.::-.-.=--::-..-=-:-:-:.-:. .: ..   |
|..  ::.. :....  . ..  .   ..  :    ..   .. . . .... .::: . --==:-:--=::---..::. :.::=.=:=-.:-==-:::..::=--. .  .....:. .|
|    .:    : .  .   :     .    :.     ..  :. ...: .=::=.:=++=@+=::=:.:=--:. :- .. :. :=-:..: :=::=:..:-  .: -:::    -  ..|
|  .   :    .      ::    .     .:  :. . :      :.:: ..::-:.=*+:::::===..:.--- . .: : :+---:::=-==:-:--::.-::.=--.:   ..: |
|..:  :    .. :.            .: :.:        ..  ::. .  . .:=:=+= .*- .=: .::: .: . .-.  :=: -:==-:- -...::-:=.:-::- ::: :- |
|.    .  . .  .:.   .  :.   .. - .   ..: : : ..    : :.::.:::=.-: .+:..: -.  .  . :: ::..:=-::---:-::: --:=.::-:..: :.   |
|   : . .   :....   . .  .  - . :      .   .:.. .   .  :..-=:.:..::. ... -::......:: . .::::.:::. -:-::- :  :. :.... . ..|
|.  . .         : .    .. ..   :  .            .  ...:.. ..-. .:  . : :::. - :.  -::::. . ::-....:.: :.    :.. .::.:.: :.|
|.    .:. :.    .   . .:   .        .    ..   .    :  .:  . . . .   ....  . . ..-:.- . : .:..:: :.:..:   - :.. ::: :    .|
|. . ..    .        .: .     ..    .     .  ..  . .  . .  : .:  ..  : ..     ..::.. :.:: : ...: .:  ..:.  :.:. ..: :  :: |
| ..  ...:  :: .   .      .   . :        :    .     . . ..    ..   .   ::....  ::.   :.-:. :   :   --.    .   . .     .  |
|.    ..  .: ..     ...  .   .              .   . .  .  ..  .:   :.: ..:...  : :.:::.: : : .... . : . . :  .            .|
| .     .. .       :             .  .   .   .   .. ..      ... :.  .  ::. . . . .::: ... - .. :  ..  .  :: .      .      |
|    ..:.     .         ..    ...  . .   :              ..  ... ..  :  .    .  .:. ::. - .  .  :    .  .::       . .     |
|   .      .  .  ...   .. .  .  .....:. .           .     .     .:.::.. ..   . : . .. : ..: :. ...     . . .      .      |
|:   . .:       ..             .-           .         .  :. ... .  .: :    ::...... .    . . . . :    :  .             : |
|      :..    .  . .:   .   .   .  .   .  :    . .  . :      :. :.. ..    :. .   .:  .... .   .     .  .  .           .  |
|  .    .      ::.          .    .    .  .     ..    .. :.     :.     .::...  .: . .. . : :. : : .:.. .       .. .     . |
```

### Heatmap Takeaways

- Heatmaps aggregate spatial samples over the last 10 generations.
- Best-agent and population heatmaps highlight spatial biases and kill zones.

### Heatmap Glossary

- **Position heatmap:** Density of sampled player positions during evaluation.
- **Kill heatmap:** Density of player positions at kill events (proxy for engagement zones).

## Generation Highlights

### Best Improvement

**Generation 20**: Best fitness jumped +147.2 (+148.7%)
- New best fitness: 246.2

### Worst Regression

**Generation 26**: Best fitness dropped -200.4 (-52.1%)
- New best fitness: 184.2
- Note: this can be normal variation after a lucky outlier

### Most Accurate Generation

**Generation 24**: Population accuracy reached 34.9%

### Most Kills (Single Agent)

**Generation 25**: An agent achieved 18 kills

### Most Diverse Generation

**Generation 17**: Diversity index 3.31

### Most Converged Generation

**Generation 41**: Diversity index 0.30

### Takeaways

- Best improvement at Gen 20 (+147.2).
- Worst regression at Gen 26 (-200.4).

### Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Average fitness:** Mean fitness across the population for a generation.
- **Accuracy:** Hits divided by shots fired (0 to 1).
- **Max kills:** Highest kills achieved by any agent in the generation.
- **Fitness std dev:** Standard deviation of fitness across the population (diversity proxy).

## Milestone Timeline

| Generation | Category | Value | Description |
|------------|----------|-------|-------------|
| 1 | Kills | 11 | Max kills reached 25% of run peak |
| 1 | Kills | 11 | Max kills reached 50% of run peak |
| 2 | Fitness | 121 | Best fitness reached 25% of run peak |
| 14 | Fitness | 197 | Best fitness reached 50% of run peak |
| 15 | Kills | 14 | Max kills reached 75% of run peak |
| 20 | Kills | 17 | Max kills reached 90% of run peak |
| 23 | Fitness | 311 | Best fitness reached 75% of run peak |
| 25 | Fitness | 385 | Best fitness reached 90% of run peak |
| 25 | Fitness | 385 | Best fitness reached 95% of run peak |
| 25 | Fitness | 385 | Best fitness reached 98% of run peak |

### Takeaways

- Total milestones reached: 10.
- Latest milestone at Gen 25 (Fitness).

### Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Average fitness:** Mean fitness across the population for a generation.
- **Max kills:** Highest kills achieved by any agent in the generation.

## Training Progress by Phase

| Phase | Gens | Best Fit | Avg Fit | Avg Kills | Avg Acc | Avg Steps | Diversity |
|-------|------|----------|---------|-----------|---------|-----------|----------|
| Phase 1 (0-27%) | 1-13 | 155 | -127 | 3.3 | 29% | 509 | 78 |
| Phase 2 (27-51%) | 14-25 | 385 | -67 | 5.6 | 34% | 675 | 101 |
| Phase 3 (51-76%) | 26-37 | 257 | -111 | 3.8 | 29% | 531 | 92 |
| Phase 4 (76-100%) | 38-49 | 120 | -151 | 2.3 | 25% | 447 | 66 |

### Takeaways

- Phase breakdown uses equal 25% blocks for run-normalized comparisons.

### Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Average fitness:** Mean fitness across the population for a generation.
- **Average kills:** Mean kills per episode across the population.
- **Accuracy:** Hits divided by shots fired (0 to 1).
- **Average steps:** Mean steps survived per episode across the population.
- **Fitness std dev:** Standard deviation of fitness across the population (diversity proxy).

## Distribution Analysis

### Metric Distributions (Last 10 Generations)

Visualizing population consistency: `|---O---|` represents Mean +/- 1 StdDev.
- **Narrow bar**: Consistent population (convergence)
- **Wide bar**: Diverse or noisy population

**Accuracy Distribution**
```
Gen  40: |---------------------O---------------------|       21.8% +/- 12.7%
Gen  41:     |-------------------O--------------------|      23.2% +/- 11.8%
Gen  42:      |--------------------O--------------------|    24.1% +/- 12.0%
Gen  43:               |----------------O---------------|    26.8% +/-  9.5%
Gen  44:          |-----------------O----------------|       24.4% +/- 10.2%
Gen  45:            |---------------O----------------|       24.9% +/-  9.4%
Gen  46:            |---------------O----------------|       25.0% +/-  9.5%
Gen  47:                  |-------------O--------------|     27.1% +/-  8.2%
Gen  48:                    |--------------O--------------|  28.8% +/-  8.7%
Gen  49:                |---------------O--------------|     26.9% +/-  8.8%
```

**Survival Steps Distribution**
```
Gen  40:              |-----------O----------|               414.6 +/- 189.6
Gen  41:                 |--------O--------|                 423.8 +/- 151.8
Gen  42:                |----------O---------|               431.9 +/- 180.3
Gen  43:               |--------------O---------------|      496.0 +/- 256.6
Gen  44:                  |--------O---------|               444.1 +/- 159.7
Gen  45:               |--------O---------|                  394.9 +/- 160.7
Gen  46:              |---------O---------|                  393.2 +/- 163.8
Gen  47:                |----------O----------|              439.3 +/- 180.9
Gen  48:                   |----------O----------|           485.8 +/- 187.5
Gen  49:                 |------------O------------|         488.5 +/- 220.6
```

**Kills Distribution**
```
Gen  40: |------------------O------------------|               2.0 +/-   2.5
Gen  41:      |-----------O------------|                       1.8 +/-   1.7
Gen  42:   |-------------O-------------|                       1.7 +/-   1.8
Gen  43:       |-------------O-------------|                   2.2 +/-   1.8
Gen  44:    |---------------O---------------|                  2.1 +/-   2.1
Gen  45:       |--------------O--------------|                 2.3 +/-   1.9
Gen  46:    |----------------O---------------|                 2.1 +/-   2.2
Gen  47:        |----------------O----------------|            2.7 +/-   2.2
Gen  48:      |----------------O-----------------|             2.5 +/-   2.3
Gen  49:         |------------------O-----------------|        3.1 +/-   2.4
```

**Fitness Distribution**
```
Gen  40: |--------------------O--------------------|        -165.4 +/-  73.6
Gen  41:       |--------------O-------------|               -165.6 +/-  50.3
Gen  42:    |----------------O---------------|              -168.8 +/-  58.2
Gen  43:         |-----------------O-----------------|      -147.1 +/-  62.7
Gen  44:        |----------------O-----------------|        -152.3 +/-  61.7
Gen  45:      |------------------O-----------------|        -155.4 +/-  63.5
Gen  46:    |------------------O------------------|         -161.3 +/-  65.2
Gen  47:         |------------------O------------------|    -143.2 +/-  65.8
Gen  48:         |-------------------O------------------|   -140.9 +/-  67.1
Gen  49:        |---------------------O-------------------| -135.9 +/-  76.4
```

**Aim Frontness Distribution**
```
Gen  40:                 |---------O----------|              52.1% +/-  4.5%
Gen  41:                 |---------O---------|               52.0% +/-  4.2%
Gen  42:            |---------------O--------------|         52.4% +/-  6.5%
Gen  43:             |-------------O-------------|           52.1% +/-  5.9%
Gen  44: |--------------O--------------|                     47.2% +/-  6.4%
Gen  45:                        |------------O------------|  56.5% +/-  5.6%
Gen  46:                   |-------------O------------|      54.5% +/-  5.7%
Gen  47:                 |------------O------------|         53.5% +/-  5.5%
Gen  48:             |--------------O---------------|        52.6% +/-  6.5%
Gen  49:                |-----------O----------|             52.3% +/-  4.9%
```

**Danger Exposure Distribution**
```
Gen  40:        |---------------O---------------|            15.4% +/-  3.7%
Gen  41:          |------------O------------|                15.1% +/-  3.1%
Gen  42:   |----------------O----------------|               14.5% +/-  3.9%
Gen  43:               |---------------O----------------|    17.1% +/-  3.8%
Gen  44: |---------------O----------------|                  13.9% +/-  4.0%
Gen  45:         |---------------O----------------|          15.7% +/-  3.8%
Gen  46:   |----------------O----------------|               14.6% +/-  4.0%
Gen  47:      |-----------------O------------------|         15.5% +/-  4.4%
Gen  48:       |--------------O--------------|               15.0% +/-  3.5%
Gen  49:                  |---------------O---------------|  17.8% +/-  3.8%
```

**Turn Deadzone Distribution**
```
Gen  40: |---------O------------|                             2.1% +/-  2.7%
Gen  41: |------O-------|                                     1.5% +/-  1.5%
Gen  42: |------O------|                                      1.5% +/-  1.4%
Gen  43:   |------O-----|                                     1.9% +/-  1.3%
Gen  44: |-------O-------|                                    1.7% +/-  1.6%
Gen  45:    |------O-------|                                  2.2% +/-  1.5%
Gen  46:     |--------O--------|                              2.7% +/-  1.7%
Gen  47:   |------O------|                                    1.9% +/-  1.4%
Gen  48:    |-------O------|                                  2.2% +/-  1.6%
Gen  49:   |-------O-------|                                  2.1% +/-  1.6%
```

**Coverage Ratio Distribution**
```
Gen  40:   |-----------------O-----------------|             35.4% +/- 13.8%
Gen  41:  |-------------------O--------------------|         36.1% +/- 15.9%
Gen  42: |-----------------O------------------|              33.9% +/- 14.4%
Gen  43:  |-------------------O-------------------|          35.8% +/- 15.5%
Gen  44:        |-------------------O-------------------|    40.7% +/- 15.2%
Gen  45:          |-------------------O-------------------|  42.7% +/- 15.5%
Gen  46:        |-------------------O------------------|     40.4% +/- 15.1%
Gen  47:           |----------------O----------------|       40.4% +/- 13.2%
Gen  48:       |-------------------O-------------------|     40.0% +/- 15.5%
Gen  49:      |---------------O---------------|              36.1% +/- 12.6%
```

**Seed Fitness Std Distribution**
```
Gen  40:        |---------------O---------------|             89.3 +/-  60.8
Gen  41:         |------------O-------------|                 83.6 +/-  52.2
Gen  42:        |----------O----------|                       70.1 +/-  42.4
Gen  43:           |------------O-----------|                 89.0 +/-  47.2
Gen  44:        |---------------O---------------|             89.4 +/-  61.8
Gen  45:        |------------O-----------|                    77.3 +/-  47.7
Gen  46:     |----------------O----------------|              81.6 +/-  64.9
Gen  47:             |------------O------------|              96.8 +/-  50.3
Gen  48:           |------------O-------------|               90.8 +/-  52.3
Gen  49:             |----------------O---------------|      111.6 +/-  62.1
```

### Takeaways

- Fitness spread trend: steady improvement (moderate confidence).
- Seed variance trend: steady improvement (moderate confidence).

### Glossary

- **Fitness std dev:** Standard deviation of fitness across the population (diversity proxy).
- **Seed fitness std:** Average per-agent fitness std dev across seeds (evaluation noise proxy).
- **Accuracy:** Hits divided by shots fired (0 to 1).
- **Accuracy std dev:** Standard deviation of accuracy across the population.
- **Average steps:** Mean steps survived per episode across the population.
- **Steps std dev:** Standard deviation of survival steps across the population.
- **Average kills:** Mean kills per episode across the population.
- **Kills std dev:** Standard deviation of kills across the population.
- **Frontness average:** Alignment of nearest asteroid with ship heading (1 ahead, 0 behind).
- **Frontness std dev:** Standard deviation of frontness across the population.
- **Danger exposure rate:** Fraction of frames with a nearby asteroid inside danger radius.
- **Danger exposure std dev:** Standard deviation of danger exposure across the population.
- **Soft-min TTC:** Weighted time-to-collision proxy that emphasizes the nearest threats (seconds).
- **Soft-min TTC std dev:** Standard deviation of soft-min TTC across the population.
- **Turn deadzone rate:** Fraction of frames where signed turn input is exactly zero (deadzone currently disabled).
- **Deadzone std dev:** Standard deviation of the per-agent zero-turn rate across the population (deadzone currently disabled).
- **Coverage ratio:** Fraction of spatial grid cells visited (0 to 1).
- **Coverage std dev:** Standard deviation of coverage ratio across the population.

## Kill Efficiency Analysis

### Current Performance (Final Phase)

- **Kills per 100 Steps:** 0.52 (Phase 1: 0.65)
- **Shots per Kill:** 8.05 (Phase 1: 7.06)
- **Kill Conversion Rate:** 12.4% (Phase 1: 14.2%)
- **Average Kills per Episode:** 2.3

### Efficiency Trend (Phase Averages)

| Phase | Kills/100 Steps | Shots/Kill | Conversion Rate |
|-------|-----------------|------------|----------------|
| Phase 1 (0-27%) | 0.65 | 7.06 | 14.2% |
| Phase 2 (27-51%) | 0.83 | 6.38 | 15.7% |
| Phase 3 (51-76%) | 0.72 | 7.17 | 13.9% |
| Phase 4 (76-100%) | 0.52 | 8.05 | 12.4% |

### Takeaways

- Kill rate changed from 0.65 to 0.52 kills/100 steps.
- Shots per kill moved from 7.06 to 8.05.

### Glossary

- **Average kills:** Mean kills per episode across the population.
- **Average steps:** Mean steps survived per episode across the population.
- **Average shots:** Mean shots fired per episode across the population.
- **Accuracy:** Hits divided by shots fired (0 to 1).
- **Shots per kill:** Shots fired divided by kills (lower is more efficient).

## Learning Velocity

### Velocity by Phase

| Phase | Fitness Delta | Delta/Gen | Velocity Band |
|-------|---------------|-----------|---------------|
| Phase 1 (0-27%) | +97 | +7.5 | Fast |
| Phase 2 (27-51%) | +188 | +15.6 | Fast |
| Phase 3 (51-76%) | +2 | +0.2 | Slow |
| Phase 4 (76-100%) | -30 | -2.5 | Slow |

### Current Velocity

- **Recent Improvement Rate:** -2.5 fitness/generation
- **Acceleration:** -12.7 (positive = speeding up)

### Takeaways

- Velocity mean +5.2 with std 7.1 across phases.

### Warnings

- Recent learning velocity is in the slowest quartile of the run.
- Learning is decelerating faster than typical phase-to-phase variation.

### Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).

## Reward Component Evolution

| Component | Phase 1 | Phase 2 | Phase 3 | Phase 4 | Trend | Status |
|-----------|---------|---------|---------|---------|-------|--------|
| DeathPenalty | -243.9 | -222.3 | -241.3 | -252.5 | ~ -3% | Worsening penalty |
| DistanceBasedKillReward | +49.5 | +84.1 | +57.1 | +34.7 | - -30% | Neutral |
| VelocitySurvivalBonus | +23.4 | +18.9 | +25.8 | +28.2 | + +20% | Learned |
| ExplorationBonus | +19.6 | +15.4 | +21.0 | +20.0 | ~ +2% | Stable |
| TargetLockReward | +14.1 | +17.4 | +13.6 | +12.3 | ~ -13% | Stable |
| ConservingAmmoBonus | +10.4 | +19.5 | +13.1 | +6.5 | - -37% | Neutral |

**Exploration Efficiency (Final Phase):** 0.0451 score/step
- *A higher rate indicates faster map traversal, independent of survival time.*

### Takeaways

- Reward component shifts are modest or mixed across phases.

### Warnings

- DeathPenalty penalty deepened (more negative over time).

### Glossary

- **Reward breakdown:** Per-component average reward contribution per episode.

## Reward Balance Analysis

### Balance Metrics (Latest Generation)

- Reward dominance index (HHI): 0.27
- Reward entropy (normalized): 0.89
- Max component share: 41.7%
- Positive component count: 5

### Takeaways

- Reward mix is broadly stable with no major dominance spikes.

### Warnings

- DeathPenalty remains negative on average (behavior may be over-penalized).
- Penalty ratio is high (2.22), negative rewards dominate.

### Glossary

- **Reward breakdown:** Per-component average reward contribution per episode.
- **Reward dominance index:** HHI-style dominance of positive rewards (higher = more concentrated).
- **Reward entropy:** Normalized entropy of positive reward components (balance proxy).
- **Reward max share:** Share of total positive reward from the largest component.
- **Positive component count:** Number of reward components with positive contribution.

## Population Health Dashboard

### Current Status: Warning

| Metric | Value | Trend (Recent) |
|--------|-------|----------------|
| Diversity Index | 0.44 | Decreasing |
| Elite Gap | 1.40 | Stable |
| Min Fitness Trend | -9.8 | Down |
| Max Fitness Trend | -36.2 | Down |
| IQR (p75-p25) | 78 | Narrowing |

### Takeaways

- Health status is Warning.
- Diversity index at 0.44 with decreasing spread.
- Fitness floor trend -9.8, ceiling trend -36.2.

### Warnings

- Diversity compressed vs run baseline (risk of premature convergence)
- Fitness floor trending down (weakest agents worsening)

### Glossary

- **Fitness std dev:** Standard deviation of fitness across the population (diversity proxy).
- **Average fitness:** Mean fitness across the population for a generation.
- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Minimum fitness:** Lowest fitness in the population for a generation.
- **Fitness p25:** 25th percentile of population fitness.
- **Fitness p75:** 75th percentile of population fitness.

## Stagnation Analysis

- **Current Stagnation:** 24 generations
- **Average Stagnation Period:** 6.8 generations
- **Longest Stagnation:** 24 generations
- **Number of Stagnation Periods:** 6

### Takeaways

- Stagnation periods average 6.8 generations.
- Longest plateau reached 24 generations.

### Warnings

- Current stagnation is in the top 10% of historical plateaus.

### Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).

## Generalization Analysis (Fresh Game)

### Recent Fresh Game Performance

| Gen | Training Fit | Fresh Fit | Accuracy | Ratio | Grade | Cause of Death |
|-----|--------------|-----------|----------|-------|-------|----------------|
| 40 | 95 | -223 | 12.8% | -2.34 | F | asteroid_collision |
| 41 | -42 | 230 | 47.9% | 0.00 | F | asteroid_collision |
| 42 | 65 | 496 | 57.8% | 7.61 | A | completed_episode |
| 43 | 14 | 42 | 46.0% | 3.07 | A | asteroid_collision |
| 44 | 87 | -106 | 35.1% | -1.22 | F | asteroid_collision |
| 45 | 32 | 449 | 57.4% | 14.22 | A | completed_episode |
| 46 | 30 | -217 | 23.1% | -7.13 | F | asteroid_collision |
| 47 | 58 | -155 | 22.5% | -2.68 | F | asteroid_collision |
| 48 | 90 | -87 | 30.8% | -0.96 | F | asteroid_collision |
| 49 | 69 | 361 | 46.8% | 5.22 | A | completed_episode |

### Generalization Summary

- **Average Fitness Ratio:** 3.31
- **Best Ratio:** 14.22
- **Worst Ratio:** 0.01

**Grade Distribution:** A:13 B:1 D:1 F:34 

### Reward Transfer Gap (Fresh vs Training)

| Gen | Share Shift | Largest Share Deltas |
|-----|-------------|----------------------|
| 40 |   43.6% | TargetLockReward +33%, VelocitySurvivalBonus -28%, DistanceBasedKillReward +10% |
| 41 |   20.9% | DistanceBasedKillReward +11%, ExplorationBonus -11%, ConservingAmmoBonus +10% |
| 42 |   49.7% | DistanceBasedKillReward +34%, VelocitySurvivalBonus -27%, ExplorationBonus -16% |
| 43 |   37.1% | VelocitySurvivalBonus -22%, DistanceBasedKillReward +18%, ExplorationBonus -15% |
| 44 |   47.2% | DistanceBasedKillReward +36%, VelocitySurvivalBonus -29%, ExplorationBonus -18% |
| 45 |   26.7% | VelocitySurvivalBonus -16%, ConservingAmmoBonus +15%, ExplorationBonus -11% |
| 46 |   30.8% | TargetLockReward +31%, VelocitySurvivalBonus -14%, DistanceBasedKillReward -9% |
| 47 |    8.1% | ConservingAmmoBonus -6%, VelocitySurvivalBonus +6%, TargetLockReward +2% |
| 48 |    7.3% | DistanceBasedKillReward +5%, ExplorationBonus -3%, VelocitySurvivalBonus -3% |
| 49 |   29.8% | VelocitySurvivalBonus -19%, DistanceBasedKillReward +16%, ExplorationBonus -10% |

### Takeaways

- Average fitness ratio 3.31 (range 0.01 to 14.22).

### Warnings

- Generalization ratios are low relative to peak training performance.
- Some generations show severe generalization drop-off.

### Glossary

- **Fitness ratio:** Fresh-game fitness divided by training fitness for the same generation.
- **Generalization grade:** Letter grade derived from generalization ratios.
- **Reward breakdown:** Per-component average reward contribution per episode.

## Correlation Analysis

### Fitness Correlations

| Metric | Correlation | Strength |
|--------|-------------|----------|
| Kills | +0.98 | Strong |
| Steps Survived | +0.96 | Strong |
| Accuracy | +0.84 | Strong |

### Interpretation

Fitness is most strongly predicted by kills (r=0.98).

### Takeaways

- Strongest fitness driver: kills (r=0.98).

### Glossary

- **Average fitness:** Mean fitness across the population for a generation.
- **Average kills:** Mean kills per episode across the population.
- **Average steps:** Mean steps survived per episode across the population.
- **Accuracy:** Hits divided by shots fired (0 to 1).

## Survival Distribution

### Survival Statistics (Final Phase)

- **Mean Survival:** 447 steps (29.8% of max)
- **Max Survival:** 1159 steps

### Survival Progression (Phase Averages)

| Phase | Mean Steps | Change vs Prior |
|-------|------------|-----------------|
| Phase 1 (0-27%) | 509 |  |
| Phase 2 (27-51%) | 675 | +165 |
| Phase 3 (51-76%) | 531 | -144 |
| Phase 4 (76-100%) | 447 | -83 |

### Takeaways

- Final-phase survival averages 447 steps.
- Best survival reached 1159 steps.

### Warnings

- Average survival remains below half of max steps; survivability is still limited.

### Glossary

- **Average steps:** Mean steps survived per episode across the population.
- **Max steps:** Highest steps survived by any agent in the generation.

## Behavioral Summary (Last 10 Generations)

- **Avg Kills per Agent:** 2.26
- **Avg Steps Survived:** 441
- **Avg Accuracy:** 25.3%
- **Max Kills (Any Agent Ever):** 18.4
- **Max Steps (Any Agent Ever):** 1375.8

### Takeaways

- Recent average kills: 2.26.
- Recent average accuracy: 25.3%.

### Glossary

- **Average kills:** Mean kills per episode across the population.
- **Average steps:** Mean steps survived per episode across the population.
- **Accuracy:** Hits divided by shots fired (0 to 1).

## Learning Progress

| Phase | Gens | Avg Best | Avg Mean | Avg Min |
|-------|------|----------|----------|---------|
| Phase 1 (0-27%) | 1-13 | 96.0 | -126.9 | -235.0 |
| Phase 2 (27-51%) | 14-25 | 214.2 | -67.0 | -223.7 |
| Phase 3 (51-76%) | 26-37 | 160.6 | -110.8 | -231.4 |
| Phase 4 (76-100%) | 38-49 | 59.7 | -150.7 | -244.8 |

### Takeaways

- Best fitness trend: slight regression (low confidence).
- Average fitness trend: slight regression (moderate confidence).

### Warnings

- Both best and average fitness are regressing across phases.

### Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Average fitness:** Mean fitness across the population for a generation.
- **Minimum fitness:** Lowest fitness in the population for a generation.

## Neural & Behavioral Complexity

| Gen | Saturation | Entropy | Control Style |
|-----|------------|---------|---------------|
| 20 |  44.4% |  1.61 | Balanced |
| 21 |  48.5% |  1.52 | Balanced |
| 22 |  50.2% |  1.48 | Binary-leaning |
| 23 |  47.4% |  1.57 | Balanced |
| 24 |  49.4% |  1.52 | Balanced |
| 25 |  52.9% |  1.44 | Binary-leaning / Repetitive |
| 26 |  49.0% |  1.59 | Balanced |
| 27 |  50.7% |  1.52 | Binary-leaning |
| 28 |  49.5% |  1.54 | Balanced |
| 29 |  47.8% |  1.58 | Balanced |
| 30 |  46.2% |  1.66 | Balanced / Exploratory |
| 31 |  46.3% |  1.71 | Balanced / Exploratory |
| 32 |  45.3% |  1.69 | Balanced / Exploratory |
| 33 |  45.6% |  1.66 | Balanced |
| 34 |  44.4% |  1.75 | Balanced / Exploratory |
| 35 |  45.8% |  1.69 | Balanced / Exploratory |
| 36 |  49.1% |  1.59 | Balanced |
| 37 |  45.7% |  1.69 | Balanced / Exploratory |
| 38 |  50.6% |  1.50 | Binary-leaning |
| 39 |  50.6% |  1.56 | Binary-leaning |
| 40 |  53.6% |  1.43 | Binary-leaning / Repetitive |
| 41 |  50.8% |  1.55 | Binary-leaning |
| 42 |  53.1% |  1.45 | Binary-leaning / Repetitive |
| 43 |  53.0% |  1.47 | Binary-leaning |
| 44 |  53.2% |  1.54 | Binary-leaning |
| 45 |  47.3% |  1.79 | Balanced / Exploratory |
| 46 |  46.8% |  1.85 | Balanced / Exploratory |
| 47 |  50.4% |  1.76 | Binary-leaning / Exploratory |
| 48 |  46.6% |  1.89 | Balanced / Exploratory |
| 49 |  44.5% |  1.91 | Balanced / Exploratory |

### Takeaways

- Output saturation trend: stagnation (low confidence (noisy)).
- Action entropy trend: stagnation (low confidence).

### Glossary

- **Output saturation:** Share of NN outputs near 0 or 1 (binary control tendency).
- **Action entropy:** Entropy of action combinations (higher = more varied control).

## Risk Profile Analysis

Analysis of how close agents let asteroids get before reacting or killing them.

| Gen | Avg Min Dist | Fitness | Kills | Archetype |
|-----|--------------|---------|-------|-----------|
| 20 |   16.1px |  -69.7 |  5.4 | Sniper |
| 21 |   15.3px |  -77.4 |  5.3 | Daredevil |
| 22 |   15.2px |  -62.8 |  5.6 | Daredevil |
| 23 |   15.9px |  -78.0 |  5.2 | Balanced |
| 24 |   16.2px |  -65.8 |  5.5 | Sniper |
| 25 |   15.4px |  -44.1 |  6.0 | Balanced |
| 26 |   15.8px |  -72.9 |  5.5 | Balanced |
| 27 |   15.4px |  -92.8 |  4.4 | Balanced |
| 28 |   15.6px |  -74.0 |  4.9 | Balanced |
| 29 |   14.9px | -105.6 |  4.2 | Balanced |
| 30 |   15.4px | -102.0 |  4.2 | Balanced |
| 31 |   15.4px |  -90.2 |  4.5 | Balanced |
| 32 |   15.3px | -122.5 |  3.5 | Balanced |
| 33 |   15.2px | -135.5 |  3.1 | Balanced |
| 34 |   16.0px | -134.8 |  2.6 | Balanced |
| 35 |   16.1px | -128.5 |  2.9 | Balanced |
| 36 |   16.4px | -137.4 |  2.7 | Balanced |
| 37 |   15.1px | -133.0 |  3.1 | Balanced |
| 38 |   16.5px | -136.2 |  2.7 | Balanced |
| 39 |   15.6px | -136.6 |  2.4 | Balanced |
| 40 |   15.3px | -165.4 |  2.0 | Overexposed |
| 41 |   15.6px | -165.6 |  1.8 | Balanced |
| 42 |   16.7px | -168.8 |  1.7 | Cautious Underperformer |
| 43 |   16.2px | -147.1 |  2.2 | Cautious Underperformer |
| 44 |   16.0px | -152.3 |  2.1 | Balanced |
| 45 |   14.9px | -155.4 |  2.3 | Overexposed |
| 46 |   15.5px | -161.3 |  2.1 | Balanced |
| 47 |   15.5px | -143.2 |  2.7 | Balanced |
| 48 |   15.7px | -140.9 |  2.5 | Balanced |
| 49 |   14.5px | -135.9 |  3.1 | Balanced |

### Takeaways

- Min-distance trend: volatile (low confidence (noisy)).
- Danger exposure trend: volatile (low confidence (noisy)).

### Glossary

- **Min asteroid distance:** Closest distance to an asteroid during an episode (pixels).
- **Average asteroid distance:** Mean distance to nearest asteroid over time (pixels).
- **Danger exposure rate:** Fraction of frames with a nearby asteroid inside danger radius.
- **Soft-min TTC:** Weighted time-to-collision proxy that emphasizes the nearest threats (seconds).

## Control Diagnostics

### Control Snapshot (Latest Generation)

| Category | Metric | Value |
|----------|--------|-------|
| Turn | Deadzone Rate | 2.1% |
| Turn | Turn Balance (R-L) | +0.64 |
| Turn | Switch Rate | 22.6% |
| Turn | Avg Streak | 23.5f |
| Turn | Max Streak | 111f |
| Aim | Frontness Avg | 52.3% |
| Aim | Frontness at Shot | 49.3% |
| Aim | Frontness at Hit | 45.0% |
| Aim | Shot Distance | 164.5px |
| Aim | Hit Distance | 92.6px |
| Danger | Exposure Rate | 17.8% |
| Danger | Entries | 3.5 |
| Danger | Reaction Time | 0.0f |
| Danger | Wraps in Danger | 0.3 |
| Movement | Distance Traveled | 1003.8px |
| Movement | Avg Speed | 2.55 |
| Movement | Speed Std | 1.02 |
| Movement | Coverage Ratio | 36.1% |
| Shooting | Shots per Kill | 8.14 |
| Shooting | Shots per Hit | 3.35 |
| Shooting | Cooldown Usage | 29.7% |
| Shooting | Cooldown Ready | 32.5% |
| Stability | Fitness Std (Seeds) | 111.6 |

### Recent Control Trends (Last 10)

| Gen | Deadzone | Turn Bias | Switch | Frontness | Danger | Coverage |
|-----|----------|-----------|--------|-----------|--------|----------|
| 40 |    2.1% |  +0.72 |   14.6% |   52.1% |   15.4% |   35.4% |
| 41 |    1.5% |  +0.73 |   14.4% |   52.0% |   15.1% |   36.1% |
| 42 |    1.5% |  +0.77 |   13.5% |   52.4% |   14.5% |   33.9% |
| 43 |    1.9% |  +0.72 |   17.0% |   52.1% |   17.1% |   35.8% |
| 44 |    1.7% |  +0.70 |   16.4% |   47.2% |   13.9% |   40.7% |
| 45 |    2.2% |  +0.59 |   21.3% |   56.5% |   15.7% |   42.7% |
| 46 |    2.7% |  +0.56 |   25.8% |   54.5% |   14.6% |   40.4% |
| 47 |    1.9% |  +0.66 |   19.5% |   53.5% |   15.5% |   40.4% |
| 48 |    2.2% |  +0.61 |   23.5% |   52.6% |   15.0% |   40.0% |
| 49 |    2.1% |  +0.64 |   22.6% |   52.3% |   17.8% |   36.1% |

### Takeaways

- Turn balance trend: sharp regression (moderate confidence).
- Aim alignment trend: stagnation (low confidence).
- Danger exposure trend: volatile (low confidence (noisy)).

### Warnings

- Turn bias is high vs run baseline (one-direction dominance).

### Glossary

- **Turn deadzone rate:** Fraction of frames where signed turn input is exactly zero (deadzone currently disabled).
- **Turn balance:** Right-turn frames minus left-turn frames divided by total turning.
- **Turn switch rate:** Rate of turn direction switches per signed turn.
- **Average turn streak:** Average consecutive frames turning in the same direction.
- **Max turn streak:** Longest consecutive turn streak per episode (averaged).
- **Frontness average:** Alignment of nearest asteroid with ship heading (1 ahead, 0 behind).
- **Frontness at shot:** Frontness measured at shot times (aim alignment during firing).
- **Frontness at hit:** Frontness measured at hit times (aim alignment on hits).
- **Shot distance:** Distance to nearest asteroid when firing (pixels).
- **Hit distance:** Distance to nearest asteroid when hits occur (pixels).
- **Danger exposure rate:** Fraction of frames with a nearby asteroid inside danger radius.
- **Danger entries:** Average number of entries into the danger zone per episode.
- **Danger reaction time:** Average frames to react after entering danger.
- **Danger wraps:** Screen-wrap count while in danger zones (mobility under threat).
- **Distance traveled:** Total distance traveled per episode (pixels).
- **Average speed:** Mean movement speed per episode.
- **Speed std dev:** Standard deviation of movement speed per episode.
- **Coverage ratio:** Fraction of spatial grid cells visited (0 to 1).
- **Shots per kill:** Shots fired divided by kills (lower is more efficient).
- **Shots per hit:** Shots fired divided by hits (lower is more efficient).
- **Seed fitness std:** Average per-agent fitness std dev across seeds (evaluation noise proxy).

## Convergence Analysis

**Recent 20 Generations Analysis:**

- Average Standard Deviation: 74.30
- Average Range (Best-Min): 331.96
- Diversity Change: -16.4%
- **Status:** Population has balanced diversity

### Takeaways

- Convergence status: balanced.
- Diversity change: -16.4%.

### Glossary

- **Fitness std dev:** Standard deviation of fitness across the population (diversity proxy).
- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Minimum fitness:** Lowest fitness in the population for a generation.

## Behavioral Trends

### Performance Metrics by Quarter

| Period | Avg Kills | Avg Steps | Avg Accuracy | Safe Dist | Max Kills |
|--------|-----------|-----------|--------------|-----------|----------|
| Q1 | 3.23 | 507 | 28.7% | 175.6px | 12.6 |
| Q2 | 5.45 | 661 | 33.0% | 167.6px | 17.2 |
| Q3 | 4.05 | 549 | 29.7% | 175.3px | 18.4 |
| Q4 | 2.37 | 450 | 25.5% | 175.3px | 13.4 |

### Action Distribution & Strategy Evolution

Analysis of how the population's physical behavior has changed over time.

| Period | Thrust % | Turn % | Shoot % | Dominant Strategy |
|--------|----------|--------|---------|-------------------|
| Q1 | 41.2% | 96.8% | 52.0% | **Balanced** |
| Q2 | 25.9% | 96.8% | 71.9% | **Balanced** |
| Q3 | 38.7% | 97.6% | 69.3% | **Balanced** |
| Q4 | 56.6% | 98.1% | 42.1% | **Balanced** |

### Input Control Style

| Period | Thrust Dur | Turn Dur | Shoot Dur | Idle Rate | Wraps |
|--------|------------|----------|-----------|-----------|-------|
| Q1 | 58.3f | 144.8f | 42.9f | 1.0% | 1.0 |
| Q2 | 7.4f | 204.1f | 140.6f | 1.3% | 0.7 |
| Q3 | 10.8f | 173.0f | 162.4f | 0.7% | 1.2 |
| Q4 | 34.3f | 125.5f | 14.9f | 0.5% | 1.1 |

### Takeaways

- Kills trend: slight regression.
- Accuracy trend: stagnation.
- Idle rate trend: stagnation.

### Glossary

- **Average kills:** Mean kills per episode across the population.
- **Average steps:** Mean steps survived per episode across the population.
- **Accuracy:** Hits divided by shots fired (0 to 1).
- **Average asteroid distance:** Mean distance to nearest asteroid over time (pixels).
- **Thrust frames:** Average frames with thrust active per episode.
- **Turn frames:** Average frames with turn input active per episode.
- **Shoot frames:** Average frames with shooting active per episode.
- **Thrust duration:** Average consecutive frames per thrust burst.
- **Turn duration:** Average consecutive frames per turning burst.
- **Shoot duration:** Average consecutive frames per shooting burst.
- **Idle rate:** Fraction of frames with no action input.
- **Screen wraps:** Average number of screen-edge wraps per episode.

### Intra-Episode Score Breakdown

Analysis of when agents earn their reward during an episode (Early vs Late game).

| Quarter | Avg Score | Share of Total | Play Style |
|---------|-----------|----------------|------------|
| Start (0-25%) | 22.7 | -16.7% | Balanced |
| Mid-Game (25-50%) | 26.6 | -19.6% | Balanced |
| Late-Game (50-75%) | 29.7 | -21.9% | Balanced |
| End-Game (75-100%) | -214.9 | 158.1% | Back-loaded |

### Intra-Episode Takeaways

- Highest scoring quarter: Late-Game (50-75%) (-21.9% of episode reward).

### Intra-Episode Glossary

- **Quarterly scores:** Average reward earned in each episode quarter (0-25%, 25-50%, 50-75%, 75-100%).

## Recent Generations (Last 30)

<details>
<summary>Click to expand Recent Generations table</summary>

| Gen   | Best   | Avg    | StdDev | Kills  | Steps  | Acc%   | Stag   |
|-------|--------|--------|--------|--------|--------|--------|--------|
| 20    | 246    | -70    | 91     | 5.4    | 671    | 34     | 0      |
| 21    | 200    | -77    | 88     | 5.3    | 671    | 33     | 1      |
| 22    | 248    | -63    | 105    | 5.6    | 680    | 34     | 0      |
| 23    | 311    | -78    | 108    | 5.2    | 615    | 34     | 0      |
| 24    | 291    | -66    | 123    | 5.5    | 662    | 35     | 1      |
| 25    | 385    | -44    | 127    | 6.0    | 703    | 35     | 0      |
| 26    | 184    | -73    | 100    | 5.5    | 614    | 33     | 1      |
| 27    | 253    | -93    | 98     | 4.4    | 589    | 31     | 2      |
| 28    | 257    | -74    | 110    | 4.9    | 619    | 33     | 3      |
| 29    | 117    | -106   | 91     | 4.2    | 539    | 31     | 4      |
| 30    | 133    | -102   | 89     | 4.2    | 554    | 31     | 5      |
| 31    | 88     | -90    | 85     | 4.5    | 580    | 27     | 6      |
| 32    | 228    | -123   | 90     | 3.5    | 481    | 29     | 7      |
| 33    | 185    | -135   | 99     | 3.1    | 451    | 27     | 8      |
| 34    | 91     | -135   | 84     | 2.6    | 466    | 28     | 9      |
| 35    | 122    | -129   | 84     | 2.9    | 509    | 27     | 10     |
| 36    | 83     | -137   | 80     | 2.7    | 485    | 25     | 11     |
| 37    | 186    | -133   | 88     | 3.1    | 480    | 26     | 12     |
| 38    | 99     | -136   | 72     | 2.7    | 487    | 29     | 13     |
| 39    | 120    | -137   | 71     | 2.4    | 468    | 23     | 14     |
| 40    | 95     | -165   | 74     | 2.0    | 415    | 22     | 15     |
| 41    | -42    | -166   | 50     | 1.8    | 424    | 23     | 16     |
| 42    | 65     | -169   | 58     | 1.7    | 432    | 24     | 17     |
| 43    | 14     | -147   | 63     | 2.2    | 496    | 27     | 18     |
| 44    | 87     | -152   | 62     | 2.1    | 444    | 24     | 19     |
| 45    | 32     | -155   | 63     | 2.3    | 395    | 25     | 20     |
| 46    | 30     | -161   | 65     | 2.1    | 393    | 25     | 21     |
| 47    | 58     | -143   | 66     | 2.7    | 439    | 27     | 22     |
| 48    | 90     | -141   | 67     | 2.5    | 486    | 29     | 23     |
| 49    | 69     | -136   | 76     | 3.1    | 489    | 27     | 24     |

</details>

### Recent Table Takeaways

- Recent table covers 30 generations ending at Gen 49.
- Latest best fitness: 69.2.

### Recent Table Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Average fitness:** Mean fitness across the population for a generation.
- **Minimum fitness:** Lowest fitness in the population for a generation.
- **Median fitness:** Median population fitness (robust central tendency).
- **Fitness std dev:** Standard deviation of fitness across the population (diversity proxy).
- **Best improvement:** Change in best fitness compared to the previous generation.
- **Average improvement:** Change in average fitness compared to the previous generation.
- **Average kills:** Mean kills per episode across the population.
- **Average steps:** Mean steps survived per episode across the population.
- **Accuracy:** Hits divided by shots fired (0 to 1).


## Top 10 Best Generations

<details>
<summary>Click to expand Top 10 Best Generations table</summary>

| Rank | Gen   | Best   | Avg    | Kills  | Steps  | Accuracy |
|------|-------|--------|--------|--------|--------|----------|
| 1    | 25    | 385    | -44    | 18.4   | 1375   | 48.9     |
| 2    | 23    | 311    | -78    | 16.8   | 1224   | 49.0     |
| 3    | 24    | 291    | -66    | 15.8   | 1281   | 43.2     |
| 4    | 28    | 257    | -74    | 15.6   | 1243   | 44.3     |
| 5    | 27    | 253    | -93    | 14.0   | 1376   | 42.1     |
| 6    | 22    | 248    | -63    | 13.0   | 1117   | 41.8     |
| 7    | 20    | 246    | -70    | 17.2   | 1188   | 40.6     |
| 8    | 32    | 228    | -123   | 14.6   | 1153   | 44.9     |
| 9    | 21    | 200    | -77    | 12.6   | 1112   | 39.4     |
| 10   | 14    | 197    | -70    | 12.6   | 1124   | 41.6     |

</details>

### Top Generations Takeaways

- Top generation is Gen 25 with best fitness 384.6.

### Top Generations Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Average fitness:** Mean fitness across the population for a generation.
- **Minimum fitness:** Lowest fitness in the population for a generation.
- **Accuracy:** Hits divided by shots fired (0 to 1).


## Trend Analysis

| Phase | Avg Best | Avg Mean | Avg Min | Improvement |
|-------|----------|----------|---------|-------------|
| Phase 1 (0-27%) | 96.0 | -126.9 | -235.0 |  |
| Phase 2 (27-51%) | 214.2 | -67.0 | -223.7 | +118.2 |
| Phase 3 (51-76%) | 160.6 | -110.8 | -231.4 | -53.5 |
| Phase 4 (76-100%) | 59.7 | -150.7 | -244.8 | -100.9 |

### Takeaways

- Best fitness: slight regression (low confidence).
- Average fitness: slight regression (moderate confidence).
- Minimum fitness: slight regression (moderate confidence).

### Warnings

- Fitness floor is degrading; weakest agents are worsening.

### Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Average fitness:** Mean fitness across the population for a generation.
- **Minimum fitness:** Lowest fitness in the population for a generation.


## Fitness Progression (ASCII Chart)

```
Best Fitness (*) vs Avg Fitness (o) Over Generations

     385 |                                                 
     348 |                        *                        
     311 |                      *                          
     274 |                       *                         
     237 |                   * *    **                     
     200 |                               *                 
     163 |             ** *   *    *      *   *            
     126 |     *  **  *    *           *                   
      89 | *        *       *         *    **  ***       * 
      53 |*  ** **   *   *              *    *     * *  * *
      16 |  *                                         **   
     -21 |                                          *      
     -58 |                oo      o               *        
     -95 |           o ooo  oooooo ooo  o                  
    -132 | o   oooo o o               oo o  o              
    -169 |o ooo    o                      oo oooooooooooooo
         -------------------------------------------------
         Gen 1                                  Gen 49
```

### Takeaways

- Best fitness trend: slight regression (low confidence).
- Average fitness trend: slight regression (moderate confidence).

### Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Average fitness:** Mean fitness across the population for a generation.


---

# Technical Appendix

## System Performance

**Average Duration (Last 10 Generations):** 0.00s
- **Evaluation (Simulation):** 51.33s (0.0%)
- **Evolution (Operators):** 0.1063s (0.0%)

| Phase | Gen Range | Avg Eval Time | Avg Evol Time | Total Time |
|-------|-----------|---------------|---------------|------------|
| Phase 1 (0-27%) | 1-13 | 60.85s | 0.0724s | 0.00s |
| Phase 2 (27-51%) | 14-25 | 89.12s | 0.1078s | 0.00s |
| Phase 3 (51-76%) | 26-37 | 66.89s | 0.1077s | 0.00s |
| Phase 4 (76-100%) | 38-49 | 52.11s | 0.1090s | 0.00s |

### Takeaways

- Evaluation accounts for 0.0% of generation time.
- Evolution accounts for 0.0% of generation time.

### Glossary

- **Evaluation duration:** Wall time spent evaluating a generation.
- **Evolution duration:** Wall time spent evolving a generation.
- **Total generation duration:** Combined evaluation and evolution wall time.

## Genetic Operator Statistics

**Recent Averages (Population: 50)**
- **Crossovers:** 26.9 (53.8%)
- **Mutations:** 42.1 (84.2%)
- **Elites Preserved:** 7.9

### Operator Takeaways

- Recent crossover rate: 53.8%.
- Recent mutation rate: 84.2%.

### Operator Glossary

- **Crossovers:** Number of crossover events per generation.
- **Mutations:** Number of mutation events per generation.
- **Elites:** Individuals preserved without mutation.


## NEAT Speciation & Topology Statistics

**Recent Averages (Last 10 Generations):**
- **Species count:** 7.90
- **Species size (min/median/max):** 1.7 / 6.2 / 10.0
- **Species pruned:** 1.10
- **Topology (avg nodes / avg enabled conns):** 51.74 / 145.53
- **Topology (best nodes / best enabled conns):** 51.40 / 144.40
- **Compatibility (threshold / mean / p10 / p90):** 0.160 / 0.250 / 0.070 / 0.403
- **Structural ops (add-node / add-conn):** 1.60 / 1.50
- **Weight mutations (per-gen counter):** 620.1
- **Innovation survival rate:** 1.00

### NEAT Takeaways

- Species count and compatibility-distance stats indicate whether speciation is separating the population.
- Topology growth (nodes/connections) indicates whether structure is changing, not just weights.

### NEAT Glossary

- **Species count:** Number of species in the population (diversity via speciation).
- **Compatibility distance:** Speciation distance based on excess/disjoint genes and weight differences.
- **Avg nodes/connections:** Mean topology size across the population (growth signal).
- **Innovation survival rate:** Fraction of newly created structural innovations that persist into the next generation.


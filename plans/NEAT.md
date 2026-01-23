# NEAT (NeuroEvolution of Augmenting Topologies)

## Scope / Purpose

NEAT is the topology-growth neuroevolution method for AsteroidsAI. It evolves both network structure and weights so the project can compare fixed-topology methods (GA/ES) against structural innovation under the same environment, state encoder, action interface, reward preset, and analytics pipeline.

## Current Implemented System

### NEAT Method Implementation Status (Implemented)

- Feedforward NEAT is implemented with innovation tracking, speciation, fitness sharing, crossover, and structural mutation.
- NEAT integrates with the shared evaluator via an agent-factory hook so genomes can be evaluated in the headless environment.
- NEAT includes a training entry point that mirrors GA/ES flow (evaluate -> analytics -> playback -> evolve).

### NEAT Core Modules (Implemented)

| Module | File | Granular Responsibility |
|---|---|---|
| Node/connection genes | `ai_agents/neuroevolution/neat/genes.py` | Defines node and connection gene primitives for NEAT genomes. |
| Genome | `ai_agents/neuroevolution/neat/genome.py` | Stores nodes/connections and implements mutations, crossover, and compatibility distance. |
| Feedforward network | `ai_agents/neuroevolution/neat/network.py` | Compiles genomes into a feedforward DAG and executes forward passes. |
| Agent wrapper | `ai_agents/neuroevolution/neat/agent.py` | Implements `BaseAgent` using a compiled NEAT network. |
| Innovation tracker | `training/methods/neat/innovation.py` | Manages global connection innovations and split-connection reuse. |
| Species | `training/methods/neat/species.py` | Holds species members, representative, and stagnation counters. |
| Driver | `training/methods/neat/driver.py` | Owns population, speciation, selection, crossover, mutation, and evolution stats. |

### Training Entry Point & Orchestration (Implemented)

| Component | File | Granular Responsibility |
|---|---|---|
| Training script | `training/scripts/train_neat.py` | Wires encoder/action/reward/driver/analytics/display and runs the NEAT loop. |
| Evaluator hook | `training/core/population_evaluator.py` | Accepts `agent_factory` to evaluate genomes instead of parameter vectors. |
| Display manager | `training/core/display_manager.py` | Plays the best genome in a fresh game and records generalization metrics. |

### NEAT Algorithm Mechanics (Implemented)

- Innovation numbers: Connection innovations are tracked globally and reused across genomes.
- Structural mutations: Add-connection and add-node mutations are implemented with cycle checks.
- Crossover alignment: Genes are aligned by innovation id with excess/disjoint handling.
- Disabled gene inheritance: Disabled genes remain disabled with a configurable probability.
- Speciation: Compatibility distance uses excess/disjoint counts and mean weight deltas.
- Fitness sharing: Adjusted fitness divides by species size to protect novel topologies.
- Species stagnation: Species that do not improve are pruned after a threshold.
- Per-species elitism: Top genome(s) per species are preserved each generation.

### Evaluation & Action Interface (Implemented)

- Encoder: `HybridEncoder` (47 inputs) is the baseline input encoding for NEAT.
- Actions: The NEAT network outputs `[turn, thrust, shoot]` in `[0,1]`.
- Action mapping: `ActionInterface` thresholds thrust/shoot and uses signed turn.

### NEAT Configuration Surface (Implemented)

| Setting | Location | Granular Meaning |
|---|---|---|
| `POPULATION_SIZE` | `training/config/neat.py` | NEAT population size per generation. |
| `NUM_GENERATIONS` | `training/config/neat.py` | Total generations per run. |
| `SEEDS_PER_AGENT` | `training/config/neat.py` | Rollouts per genome (fitness averaged). |
| `USE_COMMON_SEEDS` | `training/config/neat.py` | CRN mode toggle for within-generation noise control. |
| `C1/C2/C3` | `training/config/neat.py` | Compatibility distance coefficients. |
| `COMPATIBILITY_THRESHOLD` | `training/config/neat.py` | Speciation threshold. |
| `ADAPT_COMPATIBILITY_THRESHOLD` | `training/config/neat.py` | Enables automatic threshold adjustment to steer toward a target species count. |
| `TARGET_SPECIES` | `training/config/neat.py` | Desired approximate species count used by adaptive thresholding. |
| `COMPATIBILITY_ADJUST_STEP` | `training/config/neat.py` | Step size applied when adjusting compatibility threshold up/down. |
| `COMPATIBILITY_MIN` | `training/config/neat.py` | Minimum compatibility threshold clamp. |
| `COMPATIBILITY_MAX` | `training/config/neat.py` | Maximum compatibility threshold clamp. |
| `SPECIES_STAGNATION` | `training/config/neat.py` | Generations without improvement before a species is pruned (Reduced to 7). |
| `ELITISM_PER_SPECIES` | `training/config/neat.py` | Champions preserved per species. |
| `WEIGHT_MUTATION_PROB` | `training/config/neat.py` | Per-connection weight mutation probability. |
| `WEIGHT_MUTATION_SIGMA` | `training/config/neat.py` | Gaussian sigma for weight mutation. |
| `ADD_NODE_PROB` | `training/config/neat.py` | Add-node mutation probability. |
| `ADD_CONNECTION_PROB` | `training/config/neat.py` | Add-connection mutation probability. |
| `MAX_NODES` | `training/config/neat.py` | Optional topology guardrail (None = no cap). |
| `MAX_CONNECTIONS` | `training/config/neat.py` | Optional topology guardrail (None = no cap). |
| `ENABLE_NOVELTY` | `training/config/neat.py` | Toggle for novelty bonus integration (off by default). |
| `ENABLE_DIVERSITY` | `training/config/neat.py` | Toggle for diversity bonus integration (off by default). |
| `FITNESS_STD_PENALTY_RATIO` | `training/config/neat.py` | Reliability penalty factor (fitness -= ratio * std_dev). |
| `EARLY_STOPPING_GENERATIONS` | `training/config/neat.py` | Stop training if best fitness doesn't improve for N gens. |

### NEAT Analytics Signals (Implemented)

Operator stats recorded into analytics each generation:

- `species_count`, `species_min_size`, `species_max_size`, `species_median_size`
- `species_pruned`
- `avg_nodes`, `avg_connections`
- `best_nodes`, `best_connections`
- `compatibility_threshold`, `compatibility_mean`, `compatibility_p10`, `compatibility_p90`
- `add_node_events`, `add_connection_events`, `weight_mutation_events`, `crossover_events`
- `innovation_survival_rate`
- `avg_novelty`, `avg_diversity`, `archive_size`

### NEAT Artifacts (Implemented)

- `training_summary_neat.md`: Markdown report produced by the analytics pipeline.
- `training_data_neat.json`: JSON export containing NEAT run data.
- `training/neat_artifacts/gen_XXXX_best.json`: Best genome per generation (JSON).
- `training/neat_artifacts/gen_XXXX_best.dot`: Best genome per generation (DOT graph).
- `training/neat_artifacts/best_overall.json`: Best-of-run genome snapshot (JSON).
- `training/neat_artifacts/best_overall.dot`: Best-of-run genome graph (DOT).

## Implemented Outputs / Artifacts (if applicable)

- NEAT analytics exports and per-generation genome artifacts are produced during `train_neat.py` runs.

## In Progress / Partially Implemented

- [ ] Pareto-driven reproduction: Pareto ordering is used for display selection, but reproduction is still fitness-based.
- [ ] NEAT novelty-first mode: Novelty bonuses are implemented but not enabled by default.
- [ ] Library cross-check: No external NEAT library comparison harness exists yet.
- [ ] XOR sanity harness: No minimal NEAT correctness test exists yet.

## Planned / Missing / To Be Changed

### Adaptive Hyperparameter Roadmap (Planned)

These items describe ways NEAT can move from fixed knobs to **adaptive schedules** (stagnation-aware, diversity-aware, or noise-aware), while keeping runs interpretable via explicit logging.

- [ ] Adaptive weight mutation rate: schedule `WEIGHT_MUTATION_PROB` based on stagnation and species diversity.
- [ ] Adaptive weight mutation magnitude: schedule `WEIGHT_MUTATION_SIGMA` based on stagnation and mutation success rates.
- [ ] Adaptive structural mutation rates: schedule `ADD_NODE_PROB` and `ADD_CONNECTION_PROB` based on innovation survival and stagnation.
- [ ] Adaptive crossover probability: schedule `CROSSOVER_PROB` based on within-species fitness spread and species stability.
- [ ] Adaptive disabled-gene inheritance: schedule `INHERIT_DISABLED_PROB` to control how quickly pruning happens vs reactivation.
- [ ] Adaptive species stagnation threshold: schedule `SPECIES_STAGNATION` based on overall population progress rate.
- [ ] Adaptive seed-noise penalty: schedule `FITNESS_STD_PENALTY_RATIO` based on observed per-genome seed variance.
- [ ] Adaptive evaluation budget: schedule `SEEDS_PER_AGENT` upward when rankings are unstable (seed variance spikes).
- [ ] Adaptive speciation targets: schedule `TARGET_SPECIES` and/or `COMPATIBILITY_ADJUST_STEP` based on collapse risk (species_count trending to 1).

### NEAT Variants (Planned)

- [ ] Recurrent NEAT: Allow recurrent connections and a stable evaluation scheme for cycles.
- [ ] HyperNEAT: Add a CPPN genotype and substrate definition for geometric encodings.
- [ ] Quality-Diversity NEAT: Add a MAP-Elites style archive keyed by behavior descriptors.
- [ ] CoDeepNEAT: Add module/blueprint evolution if deep modular policies become a target.

### Evaluation & Selection Upgrades (Planned)

- [ ] Winner confirmation: Re-evaluate top genomes with extra seeds to reduce seed-luck dominance.
- [ ] CRN-by-default evaluation: Consider making CRN the default for NEAT to stabilize rankings.
- [ ] Pareto-driven selection: Add an optional Pareto mode for reproduction allocation.
- [ ] Complexity penalties: Add soft penalties for runaway topology growth in addition to hard caps.

### Observability & Debugging (Planned)

- [ ] Species-level dashboards: Report best fitness per species and species lifespan.
- [ ] Innovation survival breakdown: Track survival of new add-node vs add-connection innovations separately.
- [ ] Genome provenance: Store genome hashes/ids in analytics for fresh-game provenance.

### Validation & Testing (Planned)

- [ ] XOR sanity harness: Add a small NEAT run that validates speciation/crossover/mutations on XOR.
- [ ] Determinism test: Verify feedforward compilation produces stable output ordering for a fixed genome.
- [ ] Serialization round-trip: Verify genome JSON save/load is lossless.

## Notes / Design Considerations (optional)

- Feedforward-only NEAT is the baseline to keep evaluation deterministic and debuggable.
- `HybridEncoder` keeps the input space compact so topology growth is meaningful early on.
- Fitness sharing provides protection for new structural innovations that would be eliminated under raw-fitness selection.
- Novelty/diversity hooks exist but are intentionally off by default to avoid masking core NEAT issues.

## Discarded / Obsolete / No Longer Relevant

- No NEAT features have been discarded yet; this method is newly implemented.

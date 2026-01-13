# NEAT (NeuroEvolution of Augmenting Topologies)

## Scope / Purpose

NEAT is a planned “topology growth” method for AsteroidsAI. Its purpose is to evolve both neural network structure and weights, enabling comparison between fixed-topology evolution (GA/ES) and structural innovation under the same environment, state/action interfaces, reward presets, and analytics constraints.

## Current Implemented System

### NEAT Method Implementation Status (Implemented)

- No NEAT implementation exists yet: There is no genome/species/innovation logic in the repository today.

### Existing Components NEAT Would Integrate With (Implemented)

| Component | File(s) | What NEAT Can Reuse |
|---|---|---|
| Agent contract | `ai_agents/base_agent.py` | Defines the `BaseAgent` interface (encoded state → action vector). |
| Headless environment | `game/headless_game.py` | Fast seeded rollouts for evaluation throughput and reproducibility. |
| Windowed playback | `Asteroids.py`, `training/core/display_manager.py` | Fresh-game playback and generalization capture (if wired to NEAT). |
| State encoding | `interfaces/StateEncoder.py`, `interfaces/encoders/HybridEncoder.py` | Fixed-size state inputs used by GA today (see `plans/STATE_REPRESENTATION.md`). |
| Action mapping | `interfaces/ActionInterface.py` | Converts action outputs into game inputs and enforces basic validity constraints. |
| Reward composition | `training/config/rewards.py` | Shared reward preset for comparable fitness. |
| Analytics/reporting | `training/analytics/analytics.py` | Storage/report/export pipeline once NEAT supplies generation metrics. |
| Novelty/diversity shaping | `training/components/*`, `training/config/novelty.py` | Optional selection shaping signals (see `plans/SHARED_COMPONENTS.md`). |

### Important Naming Note (Implemented)

- `ai_agents/neuroevolution/nn_agent.py` contains the GA-used `NNAgent` wrapper (fixed-topology MLP). It is not NEAT-specific code.

## Implemented Outputs / Artifacts (if applicable)

- None (no NEAT runs are produced by the repository yet).

## In Progress / Partially Implemented

- [ ] Variable-topology evaluation: Current evaluation utilities are built around fixed-length parameter vectors and a fixed MLP unpacking scheme (via `NNAgent`).

## Planned / Missing / To Be Changed

- [ ] Create NEAT-specific modules (likely under `ai_agents/neuroevolution/` and/or `training/methods/`):
  - [ ] Genome representation (nodes + connections with innovation numbers).
  - [ ] Global innovation registry and structural mutation operators (add node, add connection).
  - [ ] Crossover alignment by innovation number (excess/disjoint gene handling).
  - [ ] Speciation and compatibility distance metrics to protect new structures.
  - [ ] Stagnation and species pruning rules.
- [ ] Add NEAT configuration:
  - [ ] Mutation probabilities for structural and weight mutations.
  - [ ] Compatibility threshold tuning for species separation.
- [ ] Add training entry script:
  - [ ] `training/scripts/train_neat.py` aligned with GA structure (evaluate → evolve → report → fresh-game playback).
- [ ] Add artifacts and observability:
  - [ ] Best-genome visualizations (graph diagrams).
  - [ ] Species fitness/population tracking across generations.

## Notes / Design Considerations (optional)

- NEAT adds bookkeeping overhead (innovation numbers/speciation) that impacts throughput; headless performance constraints still apply.
- To keep method comparisons fair, NEAT should reuse the same reward preset and analytics schema keys where meaningful.

## Discarded / Obsolete / No Longer Relevant

- No NEAT approach has been implemented, so nothing has been discarded yet.

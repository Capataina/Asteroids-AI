# NEAT (NeuroEvolution of Augmenting Topologies)

## Scope / Purpose

NEAT is a planned “topology growth” method for AsteroidsAI. Its purpose is to evolve both neural network structure and weights, enabling the project to compare fixed-topology evolution (GA/ES) against structural innovation under the same environment and evaluation/analytics constraints.

## Current Implemented System

- **No NEAT implementation exists yet**: There is no genome/species/innovation logic in the repository.
- **Existing components NEAT would integrate with**:
  - **Agent contract**: `ai_agents/base_agent.py:BaseAgent` defines the state-to-action interface.
  - **Environment**: `game/headless_game.py:HeadlessAsteroidsGame` supports fast seeded rollouts.
  - **Encoding**: `interfaces/encoders/VectorEncoder.py` provides an initial fixed-size state vector (NEAT could start here before adding alternative encoders).
  - **Action mapping**: `interfaces/ActionInterface.py` maps action outputs to game inputs.
  - **Analytics/reporting**: `training/analytics/analytics.py:TrainingAnalytics` can store/report generation and generalization data if NEAT supplies the same metric keys.
- **Important naming note**:
  - `ai_agents/neuroevolution/nn_agent.py` currently contains the GA-used `NNAgent` wrapper; it is not NEAT-specific code.

## Implemented Outputs / Artifacts

- None (no NEAT runs are produced by the repository yet).

## In Progress / Partially Implemented

- [ ] Variable-topology evaluation: Training/evaluation utilities are currently built around fixed-length parameter vectors and a fixed MLP unpacking scheme.

## Planned / Missing / To Be Changed

- [ ] Create NEAT-specific modules (likely under `ai_agents/neuroevolution/` and/or `training/methods/`):
  - [ ] Genome representation (nodes + connections with innovation numbers).
  - [ ] Global innovation registry and structural mutation operators (add node, add connection).
  - [ ] Crossover alignment by innovation number (excess/disjoint gene handling).
  - [ ] Speciation and distance metrics to protect new structures.
  - [ ] Stagnation and species pruning rules.
- [ ] Add NEAT configuration file:
  - [ ] Mutation probabilities for structural and weight mutations.
  - [ ] Compatibility threshold tuning for species separation.
- [ ] Add training entry script:
  - [ ] `train_neat.py` equivalent to GA entry point (evaluate → evolve → report → fresh-game playback).
- [ ] Add artifact generation:
  - [ ] Genome visualizations (graph diagrams) for best genomes.
  - [ ] Species population/fitness tracking over time.

## Notes / Design Considerations

- NEAT requires additional bookkeeping (innovation numbers, speciation) that will impact evaluation throughput; headless performance constraints still apply.
- To keep method comparisons fair, NEAT evaluation should reuse the same reward preset and analytics schema keys where possible.

## Discarded / Obsolete / No Longer Relevant

- No NEAT approach has been implemented, so nothing has been discarded yet.


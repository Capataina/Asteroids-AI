# Evolution Strategies (ES)

## Scope / Purpose

Evolution Strategies (ES) is a planned optimization method for AsteroidsAI. Its purpose is to benchmark a distribution-based, gradient-estimation approach against the currently implemented GA, while reusing the same environment, state/action interfaces, reward components, and analytics outputs for fair comparison.

## Current Implemented System

- **No ES implementation exists yet**: There is currently no `training/methods/evolution_strategies/` code and no `train_es.py` entry point.
- **Reusable building blocks already exist**:
  - **Environment**: `game/headless_game.py:HeadlessAsteroidsGame` supports seeded RNG per rollout.
  - **State encoding**: `interfaces/encoders/VectorEncoder.py` provides a fixed-size state vector.
  - **Action mapping**: `interfaces/ActionInterface.py` validates and thresholds action vectors.
  - **Rewards**: `interfaces/RewardCalculator.py` + `interfaces/rewards/*` provide composable reward components.
  - **Analytics**: `training/analytics/analytics.py:TrainingAnalytics` can record generations/distributions/fresh-games once ES provides the right inputs.
- **Evaluator reality check**:
  - `training/core/population_evaluator.evaluate_population_parallel(...)` is currently GA-oriented (constructs `NNAgent` and assumes feedforward parameter vectors).

## Implemented Outputs / Artifacts

- None (no ES runs are produced by the repository yet).

## In Progress / Partially Implemented

- [ ] Shared evaluator interface: There is a parallel evaluator, but it is not yet abstracted enough to support non-GA parameterizations/policies.

## Planned / Missing / To Be Changed

- [ ] Create `training/methods/evolution_strategies/`:
  - [ ] Master parameter vector (“mean”) representation.
  - [ ] Noise sampling (Gaussian perturbations) and mirrored/antithetic sampling.
  - [ ] Fitness-weighted update rule (rank-based shaping recommended to reduce outliers).
  - [ ] Sigma/step-size adaptation and learning-rate scheduling.
- [ ] Add `training/config/evolution_strategies.py`:
  - [ ] Population/sample size per update.
  - [ ] Sigma schedule/strategy.
  - [ ] Learning rate / optimizer settings.
- [ ] Add `training/scripts/train_es.py`:
  - [ ] Training loop similar to GA entry point: evaluate → update → report → fresh-game playback.
- [ ] Analytics parity:
  - [ ] Record the same generation-level metrics keys as GA for report compatibility.

## Notes / Design Considerations

- ES relies heavily on rollout throughput; headless performance and parallelism will be the primary scaling constraints.
- If ES uses a different policy representation than `FeedforwardPolicy`, the evaluation layer should accept a generic “policy factory” rather than hard-coding `NNAgent`.

## Discarded / Obsolete / No Longer Relevant

- No ES approach has been implemented, so nothing has been discarded yet.


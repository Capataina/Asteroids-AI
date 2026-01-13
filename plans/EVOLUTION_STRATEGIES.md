# Evolution Strategies (ES)

## Scope / Purpose

Evolution Strategies (ES) is a planned optimization method for AsteroidsAI. Its purpose is to benchmark a distribution-based, gradient-estimation approach against the currently implemented GA while reusing the same environment, state/action interfaces, reward components, and analytics outputs for fair comparison.

## Current Implemented System

### ES Method Implementation Status (Implemented)

- No ES implementation exists yet: There is currently no `training/methods/evolution_strategies/` code and no `training/scripts/train_es.py` entry point.

### Reusable Building Blocks (Implemented)

| Building Block            | File(s)                                                              | What ES Can Reuse                                                                                               |
| ------------------------- | -------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| Headless environment      | `game/headless_game.py`                                              | Seeded rollouts for throughput and reproducibility.                                                             |
| Windowed playback         | `Asteroids.py`, `training/core/display_manager.py`                   | Fresh-game playback and generalization capture (if wired to ES).                                                |
| State encoding            | `interfaces/StateEncoder.py`, `interfaces/encoders/HybridEncoder.py` | Fixed-size vector encoding used by GA today (see `plans/STATE_REPRESENTATION.md`).                              |
| Action mapping            | `interfaces/ActionInterface.py`                                      | Validation/normalization and mapping to `left/right/thrust/shoot`.                                              |
| Reward composition        | `training/config/rewards.py`, `interfaces/RewardCalculator.py`       | Same reward preset used by GA can be used by ES for comparable fitness.                                         |
| Analytics/export          | `training/analytics/analytics.py`                                    | Recording/reporting pipeline once ES provides the same generation-level metric keys.                            |
| Novelty/diversity shaping | `training/components/*`, `training/config/novelty.py`                | Behavior novelty and reward diversity signals for selection/update pressure (see `plans/SHARED_COMPONENTS.md`). |

### Evaluator Reality Check (Implemented)

- `training/core/population_evaluator.evaluate_population_parallel(...)` is currently GA-oriented:
  - It instantiates `NNAgent` and assumes a fixed-length MLP parameter vector representation.
  - It can support ES **only if** ES chooses the same “mean parameter vector + perturbations” representation as GA.

## Implemented Outputs / Artifacts (if applicable)

- None (ES is not implemented, so no ES-specific runs or artifacts are produced).

## In Progress / Partially Implemented

- [ ] Shared evaluator interface: Parallel evaluator exists but is not yet abstracted to accept a generic “policy factory” (instead of hard-coding `NNAgent`).

## Planned / Missing / To Be Changed

- [ ] Create `training/methods/evolution_strategies/`:
  - [ ] Mean parameter vector representation and update rule.
  - [ ] Gaussian noise sampling with antithetic/mirrored sampling.
  - [ ] Fitness shaping (rank-based recommended to reduce outlier sensitivity).
  - [ ] Sigma/step-size strategy and learning-rate scheduling.
- [ ] Add `training/config/evolution_strategies.py`:
  - [ ] Samples per update, sigma strategy, learning rate, and update clipping.
- [ ] Add `training/scripts/train_es.py`:
  - [ ] Training loop aligned with GA: evaluate → update → report → fresh-game playback.
- [ ] Analytics parity:
  - [ ] Record the same generation-level metrics keys as GA where meaningful so existing report sections work.

## Notes / Design Considerations (optional)

- ES relies heavily on rollout throughput; headless performance and parallelism are the primary scaling constraints.
- If ES uses a different policy representation than GA’s fixed MLP, evaluation should accept a generic “policy factory” rather than hard-coding `NNAgent`.

## Discarded / Obsolete / No Longer Relevant

- No ES approach has been implemented, so nothing has been discarded yet.

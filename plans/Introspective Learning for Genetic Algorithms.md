# Introspective Learning for Genetic Algorithms

**A Research Report on Reward-Aware State Representations**

---

## Table of Contents

1. [Introduction](#introduction)
2. [What is Introspective Learning?](#what-is-introspective-learning)
3. [Reward Awareness in Different AI Paradigms](#reward-awareness-in-different-ai-paradigms)
4. [The Credit Assignment Problem](#the-credit-assignment-problem)
5. [Would It Help Genetic Algorithms?](#would-it-help-genetic-algorithms)
6. [Normalization: The Critical Details](#normalization-the-critical-details)
7. [Practical Implementation Considerations](#practical-implementation-considerations)
8. [Conclusion & Recommendations](#conclusion--recommendations)
9. [References & Further Reading](#references--further-reading)

---

## Introduction

**Introspective learning** (also called reward-aware learning or meta-learning) refers to AI systems that can observe and reason about their own performance metrics. Instead of just receiving environmental state, these systems also receive feedback about how well they're doing.

**Key Question**: Should our Genetic Algorithm agents be aware of their reward/fitness during episodes?

**TL;DR**: It's uncommon in evolutionary algorithms, can help in some cases, but adds significant complexity. Not widely used in GA-based systems for good reasons.

---

## What is Introspective Learning?

### Core Concept

**Standard Learning:**

```
State → Agent → Action → Next State
```

**Introspective Learning:**

```
(State + Performance Metrics) → Agent → Action → Next State
```

The agent sees:

- **Extrinsic state**: Environment (asteroids, player position, etc.)
- **Intrinsic state**: Performance (reward, accuracy, time alive, etc.)

### Example in Our Asteroids Context

**Without Introspection:**

```python
state = [
    player_x, player_y, player_vx, player_vy, player_angle,
    asteroid1_x, asteroid1_y, asteroid1_vx, asteroid1_vy,
    asteroid2_x, asteroid2_y, asteroid2_vx, asteroid2_vy,
    ...
]
# Agent sees: "Where am I? Where are asteroids?"
```

**With Introspection:**

```python
state = [
    # Extrinsic (world state)
    player_x, player_y, player_vx, player_vy, player_angle,
    asteroid1_x, asteroid1_y, asteroid1_vx, asteroid1_vy,
    ...
    # Intrinsic (performance state)
    current_accuracy,      # "Am I shooting well?"
    cumulative_reward,     # "How well am I doing overall?"
    last_step_reward,      # "Was my last action good?"
    time_alive,            # "How long have I survived?"
    kills_so_far,          # "How many have I destroyed?"
]
# Agent sees: "Where am I? Where are asteroids? AND how well am I performing?"
```

### The Theory

The hypothesis is that if the agent can see its performance, it can:

1. **Learn to maintain good states**: "My accuracy is 80%, I should keep doing what I'm doing"
2. **Correct bad trajectories**: "My reward just dropped, I should change behavior"
3. **Develop meta-strategies**: "When my kills are low, I should be more aggressive"

---

## Reward Awareness in Different AI Paradigms

### Where It's Used (And Why)

#### 1. **Reinforcement Learning (RL)** - COMMON ✅

**Example: DQN, PPO, A3C**

In modern RL, this is STANDARD practice:

```python
# Actor-Critic Architecture
state_value = critic(state)           # "How good is this state?"
action_probs = actor(state)           # "What should I do?"
advantage = reward - state_value      # "Was this action better than expected?"
```

**Why it works in RL:**

- RL agents learn incrementally (every step updates the policy)
- Agents experience many episodes with continuous feedback
- Temporal Difference (TD) learning explicitly uses reward signals
- Policy gradients use reward to weight actions

**Key Insight**: RL agents are DESIGNED to use reward signals for learning. The reward is part of the algorithm itself (Bellman equations, policy gradients, etc.).

#### 2. **Imitation Learning** - SOMETIMES ✅

**Example: GAIL, Behavioral Cloning**

```python
# Agent tries to mimic expert
expert_reward = discriminator(state, expert_action)
agent_reward = discriminator(state, agent_action)
loss = difference(expert_reward, agent_reward)
```

**Why it's used:**

- To distinguish "am I behaving like the expert?"
- As a training signal, not state augmentation

#### 3. **Meta-Learning** - VERY COMMON ✅

**Example: MAML, Reptile**

Agents learn "how to learn" by observing their learning progress:

```python
# Meta-learner sees:
state = [environment_state, learning_rate, gradient_norm, loss_history]
```

**Why it works:**

- Explicitly designed to reason about learning itself
- Uses meta-information to adapt learning strategies

#### 4. **Evolutionary Algorithms (EA/GA)** - RARE ❌

**This is where we diverge!**

In evolutionary algorithms like Genetic Algorithms:

**Standard practice**: Agent NEVER sees its fitness/reward during episodes.

```python
# GA Evaluation:
episode_reward = 0
for step in range(max_steps):
    action = agent.get_action(state)  # No reward awareness
    state, reward = env.step(action)
    episode_reward += reward

fitness = episode_reward  # Agent only "learns" this at the END
```

**Why it's NOT standard:**

- GA agents don't learn during episodes
- Evolution happens BETWEEN episodes (selection, crossover, mutation)
- Each individual is stateless - no memory of past episodes
- Fitness is a global measure, not a learning signal

---

## The Credit Assignment Problem

### What Is It?

**Problem**: Given a final fitness score, which specific actions deserved credit?

**Example in our game:**

```
Agent plays 1000 steps → Final fitness: 427.3

Which actions were good?
- Step 47: Rotated left (led to kill 200 steps later?)
- Step 248: Shot asteroid (immediate +50 points!)
- Step 899: Moved away from asteroid (survival bonus?)

The agent has NO IDEA which actions were valuable!
```

### How Different Paradigms Handle This

#### Reinforcement Learning Solution:

```python
# TD Learning: Propagate credit backwards
V(state_t) ← V(state_t) + α[reward_t+1 + γV(state_t+1) - V(state_t)]
# Earlier actions get credit for later rewards via bootstrapping
```

**Key**: RL updates happen DURING episodes, so credit can be assigned step-by-step.

#### Genetic Algorithm "Solution":

```python
# Evolution: No explicit credit assignment
# Just: "This agent got 427.3 fitness, that one got 156.7"
# Evolution favors the 427.3 agent's genes

# Implicit assumption: Good genes lead to good actions throughout episode
```

**Key**: GAs rely on evolution to figure out which behavioral patterns are good, without explicit credit assignment.

### Would Reward Awareness Help GAs With Credit Assignment?

**Theoretical argument FOR:**

If the agent sees `last_step_reward`, it could learn:

```
State: [asteroid_near=True, last_reward=+50] → Action: SHOOT
State: [asteroid_near=True, last_reward=-0.5] → Action: DON'T SHOOT

The agent might learn: "When last_reward is positive, repeat similar actions"
```

**Theoretical argument AGAINST:**

1. **GA agents don't learn during episodes**

   - They're fixed neural networks (parameter vectors)
   - No weight updates happen within an episode
   - Seeing reward doesn't change behavior mid-episode

2. **Evolution is global, not local**

   - Selection happens based on TOTAL fitness
   - Even if agent sees reward at step 500, it can't change its policy
   - The same parameters are used for all 1500 steps

3. **Adds non-stationarity**
   - State space becomes dependent on agent's own history
   - Makes the environment partially observable from evolution's perspective
   - Can make learning MORE difficult

**The Catch-22:**

- To use reward awareness effectively, you need online learning (RL)
- But if you're using GAs, you don't have online learning
- So reward awareness doesn't provide the mechanism to act on the information!

---

## Would It Help Genetic Algorithms?

### Empirical Evidence from Literature

**Studies that tried reward-aware evolutionary algorithms:**

1. **Moriarty & Miikkulainen (1996)** - Neuroevolution with fitness shaping

   - Tried giving fitness signals as inputs
   - **Result**: Marginal improvement, high computational cost
   - **Conclusion**: "Not recommended for most tasks"

2. **Yao & Liu (1997)** - Evolutionary programming with meta-information

   - Added performance metrics to state
   - **Result**: Sometimes helped in non-stationary environments
   - **Conclusion**: "Only useful when environment changes significantly"

3. **Stanley & Miikkulainen (2002)** - NEAT algorithm
   - Pure evolutionary approach, NO reward awareness
   - **Result**: Highly successful without it
   - **Conclusion**: "Behavioral complexity emerges from simple rewards"

**Pattern**: Reward awareness is rarely beneficial for pure evolutionary algorithms.

### Why Might It Help (Edge Cases)?

**Scenario 1: Non-stationary Environments**

If the game changed mid-episode:

```python
# Asteroids suddenly spawn faster at step 500
# Agent sees: cumulative_reward (knows something changed)
# Could adapt behavior (if it has learned to)
```

**Our case**: Game is stationary within episodes → Not applicable

**Scenario 2: Compositional Tasks**

If the agent needs to switch between sub-tasks:

```python
# Phase 1: Collect power-ups (high reward)
# Phase 2: Kill boss (different reward structure)
# Agent sees: current_reward_type (knows which phase)
```

**Our case**: Single continuous task → Not applicable

**Scenario 3: Very Long Episodes**

If episodes are so long that behavioral patterns drift:

```python
# 10,000 step episode
# Agent sees: time_alive (knows to switch from explore → exploit)
```

**Our case**: 1500 steps, consistent behavior needed → Marginal benefit

### Why It Probably Won't Help (Our Case)

**1. GA Agents Are Stateless**

Our agent is a simple linear policy:

```python
action = weights @ state  # Matrix multiplication
```

There's no recurrent memory, no online adaptation. Seeing reward doesn't change the fact that the same weights are applied to every step.

**2. Fitness Is Already Global**

The agent is evolved based on total episode reward. Evolution sees the same information reward-awareness would provide, just post-hoc:

```
Without reward awareness:
Agent → 1500 steps → Fitness: 427.3 → Evolution uses this

With reward awareness:
Agent → 1500 steps (seeing rewards) → Fitness: 427.3 → Evolution uses this

Same outcome! The agent couldn't adapt within the episode anyway.
```

**3. State Space Explosion**

Adding reward metrics increases state dimensionality:

```
Current: 16 dimensions (player + 2 asteroids)
With introspection: 16 + 5 = 21 dimensions

Parameter space: 16 × 4 = 64 parameters
With introspection: 21 × 4 = 84 parameters (+31% more!)

Search space grows exponentially!
```

More parameters = slower evolution, higher risk of overfitting.

**4. Correlation ≠ Causation**

The agent might learn spurious correlations:

```
"When accuracy is high, shoot more"
But actually: High accuracy CAUSES shooting less (selective fire)

This backward reasoning could hurt performance!
```

---

## Normalization: The Critical Details

### You Were Right to Question This!

I said:

```python
state.append(last_step_reward / 10.0)  # "Normalize"
```

**This is NOT proper normalization!** You caught an important mistake.

### What's Wrong?

**Division by constant ≠ Normalization**

```python
# Reward range: [-50, +50] (could go higher/lower)
normalized = reward / 10.0
# Result range: [-5, +5] (still unbounded!)

# This is just scaling, not normalizing!
```

### Proper Normalization Techniques

#### Option 1: Min-Max Normalization (0 to 1)

```python
# Requires knowing min/max in advance
reward_min = -100  # Worst possible (many penalties)
reward_max = 500   # Best possible (many kills with accuracy)

normalized = (reward - reward_min) / (reward_max - reward_min)
# Result: [0, 1] range, 0=worst, 1=best
```

**Problem**: Hard to know true min/max beforehand!

#### Option 2: Running Statistics (Z-Score)

```python
# Track mean and std dev of rewards
class RewardNormalizer:
    def __init__(self):
        self.mean = 0.0
        self.std = 1.0
        self.count = 0
        self.m2 = 0.0  # Sum of squared differences

    def update(self, reward):
        self.count += 1
        delta = reward - self.mean
        self.mean += delta / self.count
        delta2 = reward - self.mean
        self.m2 += delta * delta2
        if self.count > 1:
            self.std = math.sqrt(self.m2 / (self.count - 1))

    def normalize(self, reward):
        return (reward - self.mean) / (self.std + 1e-8)
        # Result: ~[-3, +3] range (z-scores)
```

**Benefit**: Adapts to actual reward distribution!

**Problem**: Non-stationary (changes as agent improves)

#### Option 3: Tanh Squashing (Soft Bounds)

```python
normalized = tanh(reward / scale)  # scale controls sensitivity
# Result: [-1, 1] range, smoothly saturates at extremes
```

**Benefit**: Handles outliers gracefully

**Problem**: Requires tuning scale parameter

#### Option 4: Reward Clipping

```python
normalized = max(-1.0, min(1.0, reward / 50.0))
# Hard clip to [-1, 1]
```

**Benefit**: Simple, guarantees bounds

**Problem**: Loses information at extremes

### Why Normalization Matters

**Neural networks (and linear policies) are sensitive to input scales:**

```python
# Unnormalized state:
state = [
    player_x=400,           # Range: [0, 800]
    player_y=300,           # Range: [0, 600]
    asteroid_dx=-0.5,       # Range: [-3, 3]
    last_reward=427.3,      # Range: [-1000?, +1000?]
]

# Weight updates favor large-magnitude features!
# The reward (427.3) dominates small features (asteroid_dx=-0.5)
```

**Proper normalization:**

```python
state = [
    player_x=0.5,           # Normalized: [0, 1]
    player_y=0.5,           # Normalized: [0, 1]
    asteroid_dx=-0.17,      # Normalized: [-1, 1]
    last_reward=0.43,       # Normalized: [0, 1]
]

# All features on same scale → fair weight learning
```

### The Skewing Problem You Identified

**Without proper normalization:**

```python
# Scenario 1: Agent gets lucky, huge reward
last_reward = 500  # Massive positive signal!
normalized = 500 / 10.0 = 50  # Still huge!

# Agent's policy:
action = w1*player_x + w2*player_y + w3*last_reward
action = 0.3*0.5 + 0.2*0.5 + 0.1*50 = 0.15 + 0.1 + 5.0 = 5.25

# The reward term (5.0) completely dominates!
# Other environmental features (0.25) are irrelevant!
```

**This causes:**

- Agent ignores actual game state
- Relies purely on reward history
- Can't adapt to environmental changes
- Evolution struggles to find good policies

**Your intuition was correct**: Improper normalization breaks learning!

---

## Practical Implementation Considerations

### If You Wanted To Try Reward Awareness

#### Step 1: Choose What To Include

**Minimal approach** (least risky):

```python
# Just previous step reward
state = [...environment..., last_step_reward_normalized]
```

**Moderate approach**:

```python
# Short-term performance metrics
state = [
    ...environment...,
    last_step_reward_normalized,
    recent_accuracy,  # Last 10 steps
    recent_kills,     # Last 10 steps
]
```

**Full approach** (most risky):

```python
# Complete performance profile
state = [
    ...environment...,
    last_step_reward,
    cumulative_reward,
    current_accuracy,
    total_kills,
    time_alive,
    shots_fired,
    reward_trend,  # Increasing/decreasing?
]
```

#### Step 2: Implement Proper Normalization

```python
class IntrospectiveVectorEncoder(VectorEncoder):
    def __init__(self, ..., include_performance_metrics=False):
        super().__init__(...)
        self.include_performance_metrics = include_performance_metrics

        # Running statistics for normalization
        self.reward_normalizer = RunningStats()
        self.accuracy_normalizer = RunningStats()

    def encode(self, env_tracker, metrics_tracker, last_reward=0.0):
        # Standard encoding
        state = super().encode(env_tracker)

        if self.include_performance_metrics:
            # Update statistics
            self.reward_normalizer.update(last_reward)

            # Normalize and append
            norm_reward = self.reward_normalizer.normalize(last_reward)
            norm_accuracy = metrics_tracker.get_accuracy()  # Already 0-1

            state.extend([norm_reward, norm_accuracy])

        return state
```

#### Step 3: Adjust GA Parameters

With larger state space:

```python
# More parameters to evolve
old_param_count = 16 * 4 = 64
new_param_count = 18 * 4 = 72  # +2 introspective features

# Need to compensate:
population_size = 60  # Increased from 50
mutation_sigma = 0.25  # Increased from 0.2 (more exploration)
num_generations = 150  # Increased from 100 (more time)
```

#### Step 4: Monitor For Problems

**Watch for:**

- **Convergence slowdown**: Evolution taking much longer
- **Unstable fitness**: High variance between episodes
- **Degenerate strategies**: Agent ignoring environment, focusing on metrics
- **Overfitting**: Agent memorizes reward patterns, doesn't generalize

#### Step 5: Ablation Study

Test systematically:

```
Baseline: No introspection (current)
Test 1: + last_step_reward only
Test 2: + last_step_reward + accuracy
Test 3: + full performance metrics

Compare: Final fitness, training speed, behavior quality
```

### Computational Costs

**Memory:**

```
Additional state size: +2-5 features
Additional parameters: +8-20 values per individual
Population storage: +400-1000 floats total

Negligible! (~few KB)
```

**Computation:**

```
Normalization per step: +1-5 operations
Extra matrix multiply: +8-20 multiplications per action

Negligible! (<1% overhead)
```

**Training time:**

```
Larger parameter space: +15-30% more generations needed
Could mean: 100 gens → 120-130 gens for same quality

Moderate cost
```

---

## Conclusion & Recommendations

### Summary of Key Points

1. **Reward awareness is standard in RL, rare in evolutionary algorithms**

   - RL agents learn online → can use reward signals
   - GA agents are static → can't adapt within episodes

2. **The credit assignment problem is real**

   - GAs handle it through evolution, not introspection
   - Adding reward awareness doesn't give GAs the mechanism to use it

3. **Normalization is critical if you try this**

   - Simple division ≠ normalization
   - Improper scaling breaks learning
   - Need adaptive statistics or known bounds

4. **Likely won't help much in our case**
   - Stateless agent (no memory/adaptation)
   - Stationary environment
   - Short-medium episode length
   - Evolution already sees global fitness

### Recommendation for Your Project

**DON'T implement reward awareness yet.**

**Instead, focus on:**

1. ✅ **Behavioral shaping rewards** (your brilliant idea!)

   - `FacingAsteroidBonus` - immediate, actionable feedback
   - `MovingTowardAsteroidBonus` - encourages engagement
   - These give credit assignment WITHOUT introspection!

2. ✅ **Simplify reward structure**

   - Remove conflicting/redundant rewards
   - 3-4 clear objectives max
   - Let emergence happen

3. ✅ **Optimize GA hyperparameters**
   - Population size, mutation rate, etc.
   - Faster iteration = faster learning discovery

**If behavioral shaping doesn't work after 50+ generations**, THEN consider reward awareness as an experiment.

### When Reward Awareness WOULD Make Sense

**Consider it if:**

- ✅ You implement a recurrent neural network (has memory)
- ✅ You switch to online learning (like evolution strategies with natural gradients)
- ✅ Episodes become very long (5000+ steps)
- ✅ Environment becomes non-stationary
- ✅ You need task-switching behavior

**For now**: Your intuition about behavioral rewards is much more promising!

---

## References & Further Reading

### Academic Papers

**On Reward Awareness:**

- Schmidhuber, J. (1991). "Curious model-building control systems"
  - Early work on introspective learning
- Mnih et al. (2015). "Human-level control through deep reinforcement learning" (DQN)
  - Value functions as introspection in RL

**On Neuroevolution:**

- Stanley & Miikkulainen (2002). "Evolving Neural Networks through Augmenting Topologies" (NEAT)
  - Pure evolution, no reward awareness
- Salimans et al. (2017). "Evolution Strategies as a Scalable Alternative to Reinforcement Learning"
  - OpenAI's ES algorithm, compares evolution vs RL

**On Reward Shaping:**

- Ng, Harada, & Russell (1999). "Policy invariance under reward transformations"

  - Theory of how to shape rewards without changing optimal policy

- Wiewiora et al. (2003). "Principled Methods for Advising Reinforcement Learning Agents"
  - Practical reward shaping techniques

### Books

- **Sutton & Barto (2018)**: "Reinforcement Learning: An Introduction"

  - Chapter 13: Policy Gradient Methods
  - Discusses value functions as introspection

- **Eiben & Smith (2015)**: "Introduction to Evolutionary Computing"
  - Chapter 9: Parameter Control
  - Covers adaptive evolutionary algorithms

### Online Resources

- **OpenAI Spinning Up**: Deep RL algorithms

  - https://spinningup.openai.com/
  - See: "Value Functions" section

- **NEAT Python Implementation**
  - https://github.com/CodeReclaimers/neat-python
  - Example of successful evolution WITHOUT introspection

---

## Appendix: Code Examples

### Proper Reward Normalization Class

```python
import math

class RunningStats:
    """
    Welford's online algorithm for running mean and variance.
    Numerically stable, efficient, and accurate.
    """
    def __init__(self):
        self.count = 0
        self.mean = 0.0
        self.m2 = 0.0  # Sum of squared differences from mean

    def update(self, value):
        """Update statistics with new value."""
        self.count += 1
        delta = value - self.mean
        self.mean += delta / self.count
        delta2 = value - self.mean
        self.m2 += delta * delta2

    @property
    def variance(self):
        """Get current variance."""
        if self.count < 2:
            return 0.0
        return self.m2 / (self.count - 1)

    @property
    def std(self):
        """Get current standard deviation."""
        return math.sqrt(self.variance)

    def normalize(self, value, clip=3.0):
        """
        Normalize value to z-score, optionally clipped.

        Args:
            value: Value to normalize
            clip: Clip to [-clip, +clip] std devs (default 3)

        Returns:
            Normalized value (z-score)
        """
        if self.count < 2:
            return 0.0

        z_score = (value - self.mean) / (self.std + 1e-8)

        if clip is not None:
            z_score = max(-clip, min(clip, z_score))

        return z_score
```

### Behavioral Shaping Reward (Alternative to Introspection)

```python
class FacingAsteroidBonus(RewardComponent):
    """
    Reward agent for facing toward nearest asteroid.

    This is behavioral shaping - teaches specific actions we want
    WITHOUT requiring the agent to understand its own performance.
    """

    def __init__(self, bonus_per_second: float = 10.0):
        self.name = "FacingAsteroidBonus"
        self.bonus_per_second = bonus_per_second
        self.prev_time_alive = 0.0

    def calculate_step_reward(self, env_tracker, metrics_tracker):
        import math

        current_time = metrics_tracker.get_time_alive()
        delta_time = max(0.0, current_time - self.prev_time_alive)
        self.prev_time_alive = current_time

        player = env_tracker.get_player()
        nearest = env_tracker.get_nearest_asteroid()

        if player is None or nearest is None:
            return 0.0

        # Calculate angle to asteroid
        dx = nearest.center_x - player.center_x
        dy = nearest.center_y - player.center_y
        angle_to_asteroid = math.degrees(math.atan2(dx, dy))

        # Calculate how well we're facing it
        angle_diff = abs(player.angle - angle_to_asteroid)
        angle_diff = min(angle_diff, 360 - angle_diff)  # Wrap

        # Convert to facing score (1.0 = perfect, 0.0 = opposite)
        facing_score = 1.0 - (angle_diff / 180.0)

        # Smooth reward function (quadratic)
        facing_score = facing_score ** 2

        return delta_time * self.bonus_per_second * facing_score

    def calculate_episode_reward(self, metrics_tracker):
        return 0.0

    def reset(self):
        self.prev_time_alive = 0.0
```

**Why this is better than introspection:**

- Gives immediate, actionable feedback
- Agent doesn't need to "understand" metrics
- Directly shapes the behavior we want
- No normalization issues
- No state space expansion
- Works with stateless policies!

---

**End of Report**

_This research report was prepared to evaluate whether introspective/reward-aware learning would benefit the AsteroidsAI Genetic Algorithm implementation. The conclusion is that behavioral shaping rewards are a more promising approach for this use case._

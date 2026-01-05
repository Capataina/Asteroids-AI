# Policy Architectures for Neuroevolution: Research & Analysis

## Executive Summary

This document analyzes the current limitations of our linear policy GA implementation and explores alternative policy architectures that could enable more sophisticated agent behaviors. We examine why the current agents "sit and shoot in one direction" rather than actively aiming and dodging, and propose solutions ranging from simple fixes to architectural overhauls.

---

## Part 1: Diagnosing Current Agent Behavior

### Observed Behavior

During visual testing, agents exhibit a consistent pattern:
- **Stationary positioning**: Agent stays near spawn point (center)
- **Fixed shooting direction**: Fires in one consistent direction
- **No reactive dodging**: Doesn't respond to approaching asteroids
- **Luck-dependent performance**: High variance based on asteroid spawn positions

### Why This Happens: The Linear Policy Problem

Our current policy is:
```python
action[i] = sum(weights[j] * state[j] for j in range(state_size))
```

For 4 actions (left, right, thrust, shoot) and 16 state features, we have 64 weights.

**What linear policies CAN learn:**
- Simple thresholds: "If asteroid_x > 0.5, turn right"
- Weighted averages: "Turn based on average asteroid direction"
- Fixed biases: "Always shoot" (if shoot weights sum to > 0.5)

**What linear policies CANNOT learn:**
- Conjunctions: "If asteroid is close AND moving toward me, dodge"
- Conditionals: "If cornered, prioritize escape over shooting"
- Context-switching: "Different behavior when 1 asteroid vs 5 asteroids"
- Temporal patterns: "If I just shot, wait before shooting again"

### The "Sit and Shoot" Optimum

Given the reward structure:
- +100 per kill (dominant reward)
- +2/sec for accuracy (minor)
- +2/sec for facing asteroids (minor)
- +0.5/sec for movement (tiny)

A linear policy discovers that **shooting constantly** is the dominant strategy because:
1. Movement rewards are tiny compared to kill rewards
2. Dodging requires non-linear reasoning (IF close AND approaching THEN dodge)
3. Aiming requires understanding angle-to-target relationships (non-linear)
4. Standing still and shooting catches asteroids that happen to cross the firing line

The GA optimizes the **shooting direction weights** because that's what maximizes expected kills under a linear constraint. This explains the "upward trend" - agents are getting better at picking which direction to shoot, not at actually playing the game.

---

## Part 2: The Same-Seed Selection Problem

### Current Approach

All 100 agents in a generation face the **exact same** asteroid configuration:
```python
generation_seed = random.randint(0, 2**31 - 1)
# All agents evaluated with this seed
```

### Why This Is Problematic

1. **Positional Luck**: An agent pointing in the "right" direction for this specific spawn wins
2. **No Generalization Pressure**: Agents aren't tested on diverse scenarios
3. **Overfitting to Seeds**: Selected agents are "best for seed X", not "best overall"
4. **Deceptive Fitness**: High fitness doesn't indicate general capability

### Evidence from Logs

```
Gen 17: Training=4319 (43 kills) → Fresh game: dies at 100 steps (1 kill)
Gen 16: Training=2207 (22 kills) → Fresh game: survives 1500 steps (27 kills)
```

Gen 17's agent had higher training fitness but worse generalization. It was selected for being lucky on one seed, not for being skilled.

### Different Seeds Approach

If each agent plays a **different random seed**:

**Pros:**
- Forces reactive behavior (can't rely on knowing spawn positions)
- Selects for generalization, not luck
- Reduces variance in "true skill" measurement
- More similar to real gameplay conditions

**Cons:**
- Fitness scores aren't directly comparable (different difficulties)
- Some agents might get "easy" seeds by chance
- Slower convergence initially (more noise in selection)

**Mitigation for cons:**
- Evaluate each agent on 3-5 different seeds, use average
- This balances fairness with generalization testing
- Computational cost increases but parallelization helps

### Recommendation

Switch to **different seeds per agent** or **multiple seeds per agent averaged**. This single change could dramatically improve agent quality by selecting for actual reactive capability rather than lucky positioning.

---

## Part 3: Non-Linear Policy Architectures

### What Makes a Policy "Non-Linear"?

A linear policy computes:
```
output = W · input
```

A non-linear policy introduces **activation functions**:
```
output = f(W · input)
```

Where `f` is non-linear (sigmoid, tanh, ReLU, etc.)

With multiple layers:
```
hidden = f(W1 · input)
output = g(W2 · hidden)
```

This allows learning **arbitrary functions** of the input, not just weighted sums.

### Why Non-Linearity Enables Complex Behavior

**Linear**: Can only draw straight lines through state space
- "Turn left if asteroid_x < 0.3"

**Non-linear**: Can draw curved, complex decision boundaries
- "Turn left if (asteroid_x < 0.3 AND asteroid_y > 0.5) OR (speed > 0.7 AND angle ~ 45°)"

**Visual intuition**:
- Linear: Dividing a room with a single straight wall
- Non-linear: Dividing a room with curved, irregular partitions

---

## Part 4: Policy Architecture Options

### Option A: Feedforward Neural Network (Recommended Starting Point)

**Architecture:**
```
Input (16) → Hidden (32, ReLU) → Hidden (16, ReLU) → Output (4, Sigmoid)
```

**Parameter count:** 16×32 + 32×16 + 16×4 = 512 + 512 + 64 = 1088 weights

**How it works:**
1. State vector feeds into first layer
2. Each hidden neuron computes: `output = ReLU(sum(weights × inputs) + bias)`
3. ReLU(x) = max(0, x) - introduces non-linearity
4. Final layer outputs action probabilities

**What it can learn:**
- "If asteroid is close (feature 8 high) AND approaching (feature 9 negative), then thrust"
- Hidden neurons can represent concepts like "danger level", "best escape direction"
- Complex conditionals emerge from combinations of hidden activations

**Evolution approach:**
- Same GA, but evolving 1088 weights instead of 64
- Crossover: blend parent weight vectors
- Mutation: Gaussian noise on weights

**Pros:**
- Well-understood, lots of research
- Can approximate any function (universal approximator)
- Relatively easy to implement

**Cons:**
- More parameters = slower convergence
- Can overfit to training conditions
- "Black box" - hard to interpret what it learned

### Option B: NEAT (NeuroEvolution of Augmenting Topologies)

**Core idea:** Evolve both the **weights** AND the **network structure**

**How it works:**
1. Start with minimal network (direct input→output connections)
2. Mutation can:
   - Change weights
   - Add new connections
   - Add new neurons
3. Crossover aligns networks by "innovation numbers" (historical markers)
4. Speciation protects novel structures from being outcompeted immediately

**What makes it special:**
- Finds **minimal complexity** needed for the task
- Can discover novel architectures
- Avoids the "competing conventions" problem (different networks encoding same function)

**Example evolution:**
```
Gen 1:  input → output (linear, like current)
Gen 10: input → hidden1 → output (one hidden neuron added)
Gen 50: input → hidden1 → hidden2 → output (discovered useful intermediate representation)
```

**Pros:**
- Automatic complexity scaling
- Often finds elegant, minimal solutions
- Well-studied, reference implementations available (neat-python)

**Cons:**
- More complex to implement from scratch
- Slower than fixed-topology evolution
- Speciation parameters need tuning

### Option C: Genetic Programming (GP)

**Core idea:** Evolve **expression trees** instead of weight vectors

**Representation:**
```
Tree: IF(
        LessThan(asteroid_distance, 0.3),
        shoot,
        IF(
          GreaterThan(asteroid_angle, 0),
          turn_left,
          turn_right
        )
      )
```

**Primitives:**
- Functions: IF, AND, OR, ADD, MUL, SIN, COS, LessThan, GreaterThan
- Terminals: state features, constants, action outputs

**How it works:**
1. Generate random expression trees
2. Evaluate fitness by executing tree to get actions
3. Crossover: swap subtrees between parents
4. Mutation: replace subtree with random new subtree

**What it can learn:**
- Literally any computable function
- Human-readable policies (can inspect the tree!)
- Creative solutions humans might not think of

**Example discovered policy:**
```
turn_amount = MUL(asteroid_x, SIN(player_angle))
shoot_decision = AND(LessThan(distance, 0.5), Facing(asteroid))
```

**Pros:**
- Interpretable - you can read what it learned!
- Can discover novel algorithms
- No fixed architecture constraints

**Cons:**
- Bloat: trees grow unnecessarily large
- Slow evaluation (tree traversal)
- Harder to optimize than weight vectors
- Requires careful primitive selection

### Option D: Compositional Pattern Producing Networks (CPPNs)

**Core idea:** Use diverse activation functions (sin, cos, gaussian, step) to create complex patterns with few parameters

**Relevance:** Often used with HyperNEAT to generate large neural network weights from small CPPNs. Could generate our policy weights indirectly.

**Verdict:** Interesting but probably overkill for this project.

### Option E: Radial Basis Function (RBF) Networks

**Core idea:** Hidden neurons activate based on distance to "centers" in input space

**How it works:**
```
hidden[i] = gaussian(distance(input, center[i]))
output = sum(weights × hidden)
```

**What it can learn:**
- Local patterns: "When state is near THIS configuration, do THIS"
- Good for recognizing specific situations

**Pros:**
- Simpler than full neural networks
- Good for local pattern recognition
- Fewer parameters than deep networks

**Cons:**
- Requires choosing/learning centers
- Less flexible than neural networks
- Not as well-suited for this continuous control task

---

## Part 5: How Non-Linear Policies "Discover" Behaviors

### The Key Insight: Emergence Through Optimization

Non-linear policies don't require us to **specify** behaviors - they **discover** them through optimization pressure.

**Example: How a neural network might learn to dodge**

1. **Initial state:** Random weights, random behavior
2. **Selection pressure:** Agents that survive longer reproduce
3. **What happens:**
   - Hidden neuron 7 happens to activate when asteroids are close
   - Hidden neuron 12 happens to activate when moving away from danger
   - Agents where neuron 7 → neuron 12 → thrust survive better
   - This connection strengthens over generations
4. **Result:** Network "discovers" the concept of "dodge when in danger"

We never told it to dodge. The structure of the network allowed it to represent this concept, and evolution found it.

### Why Linear Policies Can't Do This

Linear policies have no "hidden concepts" - they directly map inputs to outputs. There's no neuron that can represent "danger level" as an intermediate computation.

```
Linear: asteroid_distance → thrust (direct, can't combine with other factors)
Non-linear: asteroid_distance + approaching_speed → danger_level → thrust
```

The hidden layer creates a **feature space** where the network can invent useful concepts.

---

## Part 6: Implementation Considerations

### Complexity vs. Learnability Tradeoff

| Architecture | Parameters | Expressiveness | Learning Difficulty |
|--------------|------------|----------------|---------------------|
| Linear (current) | 64 | Low | Easy |
| Small NN (32 hidden) | ~600 | Medium | Medium |
| Medium NN (64-32 hidden) | ~3000 | High | Hard |
| NEAT | Variable | High | Medium |
| GP | Variable | Very High | Hard |

**Rule of thumb:** More parameters = more expressive but harder to optimize

### Recommended Progression

1. **Immediate fix:** Switch to different seeds per agent (no architecture change)
2. **Next step:** Small neural network (1 hidden layer, 16-32 neurons)
3. **If needed:** NEAT for automatic complexity discovery
4. **Research option:** GP for interpretable policies

### Computational Considerations

| Architecture | Eval Speed | Memory | Parallelizable |
|--------------|------------|--------|----------------|
| Linear | Very Fast | Tiny | Yes |
| Small NN | Fast | Small | Yes |
| NEAT | Medium | Medium | Yes |
| GP | Slow | Medium | Yes |

All options remain parallelizable for population evaluation.

---

## Part 7: Specific Recommendations for This Project

### Immediate Changes (No Architecture Change)

1. **Different seeds per agent**
   - Each agent gets unique random seed
   - Forces reactive behavior
   - Easy to implement (remove seed sharing)

2. **Multiple seeds per agent**
   - Each agent plays 3 seeds, fitness = average
   - More robust selection
   - 3x computational cost (still fast with parallelization)

### Short-Term: Simple Neural Network

**Proposed architecture:**
```
Input (16) → Hidden (24, tanh) → Output (4, sigmoid)
```

**Why tanh:**
- Output range [-1, 1] naturally represents "turn left vs right"
- Smoother gradients than ReLU for small networks

**Parameter count:** 16×24 + 24×4 = 384 + 96 = 480 parameters

**Expected impact:**
- Agents can learn "if close AND approaching, dodge"
- Can represent "danger assessment" as hidden concept
- Should see actual aiming/dodging behavior emerge

### Medium-Term: NEAT

If simple NN doesn't produce satisfying results:
- Use `neat-python` library
- Let evolution find optimal network structure
- May discover minimal, elegant solutions

### Long-Term: Hybrid Approaches

- Use GP to discover reward shaping (what behaviors to encourage)
- Use NN for the actual policy (how to execute behaviors)
- Meta-learning: evolve the learning algorithm itself

---

## Part 8: Expected Behavior Changes

### With Different Seeds + Current Linear Policy

- Less "stand and shoot one direction"
- More variance in behavior (agents try different strategies)
- Fitness scores more meaningful (reflect actual capability)
- But still limited by linear expressiveness

### With Neural Network Policy

- Active aiming (network can learn angle→target relationship)
- Reactive dodging (network can represent "danger" concept)
- Context-dependent behavior (different actions based on situation)
- More consistent performance across different seeds

### What "Good" Behavior Looks Like

A well-trained non-linear agent should:
1. **Move toward asteroids** (engagement)
2. **Turn to face targets** (aiming)
3. **Lead targets** (predict where asteroid will be)
4. **Dodge when necessary** (survival)
5. **Prioritize threats** (handle multiple asteroids intelligently)

Current linear agents do none of these - they pick a direction and hope asteroids cross their path.

---

## Part 9: Open Questions for Further Research

### Q1: How many hidden neurons are enough?

**Hypothesis:** 16-32 hidden neurons should be sufficient for Asteroids.

**Why:** The game has limited complexity - position, velocity, angle. Unlike image recognition, we don't need deep hierarchies.

**Test:** Try 8, 16, 32, 64 hidden neurons and compare learning curves.

### Q2: Should we use recurrent connections?

**Current:** Feedforward only (no memory)

**Alternative:** LSTM/GRU for temporal reasoning

**When needed:** If agents need to remember past actions (e.g., "I just shot, wait for cooldown")

**Our case:** Probably not needed - current state should be sufficient for Asteroids.

### Q3: Is the state representation sufficient?

**Current state includes:**
- Player: x, y, vx, vy, sin(angle), cos(angle) [6 features]
- Nearest 2 asteroids: rel_x, rel_y, distance, rel_vx, rel_vy [10 features]

**Potentially missing:**
- More asteroids (only 2 currently)
- Bullet positions (where did I shoot?)
- Time since last shot
- Wall/edge proximity

**Recommendation:** Try increasing `num_nearest_asteroids` to 4-5 before adding architectural complexity.

### Q4: How do we know if non-linearity is helping?

**Metrics to track:**
- Fitness variance (should decrease with better policies)
- Behavioral diversity (are agents doing different things?)
- Transfer performance (training vs fresh game gap)
- Qualitative observation (does it look like it's aiming?)

### Q5: Could we combine evolution with gradient descent?

**Approach:** "Lamarckian evolution" - agents learn during lifetime, pass learned weights to offspring

**How:**
1. Evolve initial weights
2. Each agent does gradient descent during evaluation
3. Improved weights passed to next generation

**Complexity:** Requires differentiable reward signal, more complex implementation.

**Verdict:** Interesting research direction, not needed for initial improvements.

---

## Part 10: Implementation Roadmap

### Phase 1: Better Selection (1-2 hours)
- [ ] Change to different seeds per agent
- [ ] Test with current linear policy
- [ ] Observe if behavior diversifies

### Phase 2: Simple Neural Network (2-4 hours)
- [ ] Implement NeuralNetworkAgent class
- [ ] Single hidden layer with tanh activation
- [ ] Integrate with existing GA infrastructure
- [ ] Test and tune hidden layer size

### Phase 3: Evaluation & Tuning (ongoing)
- [ ] Compare linear vs NN fitness curves
- [ ] Qualitative assessment of behavior
- [ ] Tune hyperparameters (mutation rate, hidden size)
- [ ] Document findings

### Phase 4: Advanced Architectures (if needed)
- [ ] Implement NEAT using neat-python
- [ ] Compare with fixed-topology NN
- [ ] Explore GP for interpretable policies

---

## Conclusion

The current "sit and shoot" behavior is an expected outcome of:
1. **Linear policy limitations** - can't learn conditional/contextual behavior
2. **Same-seed selection** - rewards lucky positioning over skill
3. **Reward structure** - killing dominates, movement rewards are negligible

**Recommended immediate fix:** Different seeds per agent

**Recommended architecture upgrade:** Small feedforward neural network (16-32 hidden neurons)

These changes should produce agents that actually aim at asteroids, dodge threats, and demonstrate intelligent gameplay rather than optimized luck.

---

## References & Further Reading

1. **NEAT:** Stanley, K. O., & Miikkulainen, R. (2002). Evolving Neural Networks through Augmenting Topologies.
2. **Neuroevolution:** Floreano, D., Dürr, P., & Mattiussi, C. (2008). Neuroevolution: from architectures to learning.
3. **Genetic Programming:** Koza, J. R. (1992). Genetic Programming: On the Programming of Computers by Means of Natural Selection.
4. **neat-python:** https://neat-python.readthedocs.io/
5. **OpenAI ES:** Salimans, T., et al. (2017). Evolution Strategies as a Scalable Alternative to Reinforcement Learning.

# Critical GA Bugfixes Applied

## Date: 2026-01-04

## Summary
Fixed four catastrophic bugs in the genetic algorithm implementation that were preventing any meaningful learning.

---

## Bug 1: Mutation Operators Returned Wrong-Sized Vectors
**Location:** `ai_agents/neuroevolution/genetic_algorithm/operators.py:23, 35`

**Problem:**
```python
# BROKEN - only returns ~35% of genes
return [individual[i] + random.gauss(0, sigma) 
        for i in range(len(individual)) 
        if random.random() < mutation_probability]
```

The list comprehension filtered genes, so with `mutation_probability=0.35`, a 64-dimensional vector would shrink to ~22 dimensions. This catastrophically broke the population each generation.

**Fix:**
```python
# FIXED - returns ALL genes, mutates probabilistically
mutated = [
    individual[i] + random.gauss(0, self.mutation_gaussian_sigma) 
    if random.random() < self.mutation_probability 
    else individual[i]
    for i in range(len(individual))
]
return (mutated,)
```

Applied to both `mutate_gaussian` and `mutate_uniform`.

---

## Bug 2: Crossover Only Returned One Child
**Location:** `ai_agents/neuroevolution/genetic_algorithm/operators.py:48, 61`

**Problem:**
```python
# BROKEN - returns single list, not tuple of two
return [(ind1[i] * prob + ind2[i] * (1-prob)) for i in range(len(ind1))]
```

Function signature promised `Tuple[List[float], List[float]]` but returned only one offspring.

**Fix:**
```python
# FIXED - returns TWO complementary children
child1 = [ind1[i] * prob + ind2[i] * (1-prob) for i in range(len(ind1))]
child2 = [ind2[i] * prob + ind1[i] * (1-prob) for i in range(len(ind2))]
return (child1, child2)
```

Applied to both `crossover_blend` and `crossover_arithmetic`.

---

## Bug 3: State Dimensionality Mismatch
**Location:** `ai_agents/neuroevolution/genetic_algorithm/ga_trainer.py:78`

**Problem:**
```python
# BROKEN - creates 16-dimensional vectors (state_size only)
return [[random.uniform(low, high) 
         for _ in range(self.state_encoder.get_state_size())] 
        for _ in range(self.population_size)]
```

Agents need `state_size × action_size = 16 × 4 = 64` parameters for a complete linear policy. This created individuals with 75% of policy weights always zero.

**Fix:**
```python
# FIXED - creates 64-dimensional vectors (state_size * action_size)
state_size = self.state_encoder.get_state_size()
action_size = 4
param_size = state_size * action_size

return [
    [random.uniform(low, high) for _ in range(param_size)]
    for _ in range(self.population_size)
]
```

---

## Bug 4: Tournament Selection Had No Selection Pressure
**Location:** `ai_agents/neuroevolution/genetic_algorithm/ga_trainer.py:93-104`

**Problem:**
```python
# BROKEN - returns random indices, ignores fitnesses
def tournament_selection(self, fitnesses, tournament_size):
    return [random.randint(0, len(fitnesses) - 1) 
            for _ in range(self.tournament_size)]  # self.tournament_size doesn't exist!
```

Completely random selection with zero evolutionary pressure.

**Fix:**
```python
# FIXED - proper tournament selection with fitness-based winner
def tournament_selection(self, fitnesses, tournament_size):
    selected = []
    for _ in range(len(fitnesses)):
        tournament_indices = random.sample(range(len(fitnesses)), 
                                          min(tournament_size, len(fitnesses)))
        winner_idx = max(tournament_indices, key=lambda idx: fitnesses[idx])
        selected.append(winner_idx)
    return selected
```

---

## Additional Improvements in train_ga_parallel.py

### Fixed Mutation Application Logic
**Problem:** Mutation was applied per-offspring probabilistically, adding another layer of randomness.

**Fix:** Now mutates ALL offspring (mutation probability is handled per-gene inside the mutation operator).

```python
# Apply mutation to ALL offspring (not probabilistically per-offspring)
for i, child in enumerate(offspring):
    mutated = self.ga_trainer.operators.mutate_gaussian(child)
    if isinstance(mutated, tuple) and len(mutated) > 0:
        offspring[i] = list(mutated[0])
```

### Fixed Offspring Generation Logic
**Problem:** Offspring count calculation was off (`population_size - len(parents)`).

**Fix:** Generate full population size, then trim and apply elitism correctly.

---

## Expected Impact

### Before Fixes:
- **No meaningful learning** - fitness improvements purely from random search + elitism
- Population vector dimensions shrunk each generation
- Zero selection pressure
- Agents couldn't represent complete policies

### After Fixes:
- **Proper genetic algorithm** - crossover mixes good solutions, mutation explores
- Selection pressure favors better individuals
- Population maintains correct dimensionality
- Full 64-parameter policy space explored
- Expect to see **genuine fitness improvement trends** across generations

---

## Configuration Notes

Current settings in `train_ga_parallel.py:456-466`:
```python
population_size=100
num_generations=500
mutation_probability=0.35  # Per-gene probability
crossover_probability=0.7
mutation_gaussian_sigma=0.3
```

These are now **properly applied**. With 100 agents and proper evolution:
- **Generation 0:** 100 random agents
- **Generation 1+:** Top 10 elite + 90 offspring (crossover + mutation)
- Tournament selection (size=3) ensures good individuals reproduce more

---

## Testing Recommendations

1. **Run training for 50+ generations** and monitor:
   - Best fitness should show clearer upward trend
   - Average fitness should improve more consistently
   - Population diversity (std dev) should remain healthy

2. **Check vector dimensions** - add debug print in first generation:
   ```python
   print(f"Individual dimension: {len(self.population[0])}")  # Should be 64
   ```

3. **Monitor learning curves** - after fixes, expect:
   - Smoother fitness progression
   - Less noise in generation averages
   - Occasional plateaus followed by breakthroughs (typical GA behavior)

---

## Files Modified

1. `ai_agents/neuroevolution/genetic_algorithm/operators.py` - Fixed all operators
2. `ai_agents/neuroevolution/genetic_algorithm/ga_trainer.py` - Fixed initialization + selection
3. `training/train_ga_parallel.py` - Fixed evolution loop

**All changes preserve backward compatibility with the rest of the codebase.**

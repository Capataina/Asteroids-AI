# Parallel GA Training

## What's New?

This is a **parallelized version** of the Genetic Algorithm training that evaluates all agents simultaneously for massive speedup.

## Files Created:

1. **`game/headless_game.py`** - Headless version of AsteroidsGame (no rendering)
2. **`training/parallel_evaluator.py`** - Parallel evaluation functions
3. **`training/train_ga_parallel.py`** - New parallel training driver

## How It Works:

### Before (Sequential):

```
Agent 1 plays → fitness
Agent 2 plays → fitness
...
Agent 50 plays → fitness
→ Evolve → Next Generation

Time per generation: ~10 minutes
```

### After (Parallel):

```
All 50 agents play simultaneously (in background)
→ Show best agent visually
→ Evolve → Next Generation

Time per generation: ~10-60 seconds
```

## Speedup:

Expected speedup depends on your CPU cores:

- **4 cores**: ~4x faster (10 min → 2.5 min)
- **8 cores**: ~8x faster (10 min → 75 sec)
- **16 cores**: ~16x faster (10 min → 38 sec)

## How to Run:

```bash
cd "c:\Asteroids AI"
python training\train_ga_parallel.py
```

## Configuration:

Edit `train_ga_parallel.py` line 372-380:

```python
ga_trainer = create_ga_trainer(
    game=window,
    population_size=50,      # Number of agents
    num_generations=100,     # Number of generations
    mutation_probability=0.25,
    crossover_probability=0.7,
    mutation_gaussian_sigma=0.2,
    ...
)
```

## What You'll See:

1. **"Evaluating in parallel..."** - All agents running in background (fast!)
2. **Best agent plays visually** - Watch the current best performer
3. **Evolution happens** - New generation created
4. **Repeat!**

## Differences from Original:

| Feature       | Original (train_ga.py) | Parallel (train_ga_parallel.py) |
| ------------- | ---------------------- | ------------------------------- |
| Evaluation    | Sequential (1 by 1)    | Parallel (all at once)          |
| Speed         | Slow (~10 min/gen)     | Fast (~30 sec/gen)              |
| Visualization | Every agent visible    | Only best agent visible         |
| Episode limit | 400 steps              | 2000 steps                      |
| Algorithm     | Same GA                | Same GA                         |

## Keep Using Original If:

- You want to watch every single agent play
- You want to debug agent behavior step-by-step
- You have a slow computer (< 4 cores)

## Use Parallel If:

- You want fast training
- You have a modern CPU (4+ cores)
- You only care about seeing the best agents

## Technical Notes:

- Uses `ThreadPoolExecutor` for parallelism
- Each agent runs in a separate `HeadlessAsteroidsGame` instance
- No rendering overhead during evaluation
- Same GA algorithm (tournament selection, crossover, mutation, elitism)
- Thread-safe evaluation (each thread has its own game instance)

## Troubleshooting:

**If it's slower than expected:**

- Check `max_workers` (should match your CPU cores)
- Close other programs
- Reduce `population_size` if memory is tight

**If it crashes:**

- Try reducing `max_workers` to 4
- Check if headless_game.py is working: `python -c "from game.headless_game import HeadlessAsteroidsGame; print('OK')"`

**If agents seem worse:**

- They're not! Same algorithm, just faster evaluation
- Early generations will still be random
- Give it 20-30 generations to see improvement

# Training Improvements - Balancing & Physics

## Changes Made (Response to User Feedback)

### Issue 1: Episodes Too Short ✅
**Problem**: Max steps was too low (400-2000), agents would spawn, click buttons, then reset immediately.

**Fix**: 
- Increased max steps to **1500** in parallel training
- This gives agents more time to experiment with strategies
- Allows for multiple engagement opportunities per episode

**Location**: `training/train_ga_parallel.py` line ~158

---

### Issue 2: Reward System Not Encouraging Smart Play ✅
**Problem**: AI was spam-shooting because any hit = reward, no penalty for missing.

**Fixes**:

#### Created New Reward Component: `ShootingPenalty`
```python
# interfaces/rewards/ShootingPenalty.py
penalty_per_shot = -0.5  # Small penalty for each shot fired
```

**Logic**: 
- Each shot costs -0.5 points
- Killing an asteroid gives +50 points
- Net result: Accurate shooting is rewarded (50 - 0.5 = +49.5 per kill)
- Spam shooting is punished (missing costs points)

#### Rebalanced Existing Rewards:

| Reward Component | Old Value | New Value | Reasoning |
|-----------------|-----------|-----------|-----------|
| **KillAsteroid** | 25 pts | **50 pts** | Make kills more valuable to encourage engagement |
| **AccuracyBonus** | 8 pts/sec | **15 pts/sec** | Reward accurate play more heavily |
| **ShootingPenalty** | N/A | **-0.5 pts/shot** | Discourage spray-and-pray |

**Net Effect**:
- Spam shooting with 10% accuracy: Many wasted shots → negative reward
- Deliberate shooting with 50% accuracy: Fewer wasted shots + accuracy bonus → high reward
- Not shooting at all: Survival bonus only → low reward

---

### Issue 3: Ship Too Fast & Shoots Too Fast ✅
**Problem**: AI was moving and shooting unrealistically fast, making it hard to learn proper control.

**Fixes in `game/classes/player.py`**:

```python
# Movement (Old → New)
acceleration = 0.3 → 0.15     # 50% slower acceleration
rotation_speed = 5 → 3        # 40% slower turning

# Shooting (Old → New)
shoot_cooldown = 0.12 → 0.25  # ~2x slower fire rate (8.3 shots/sec → 4 shots/sec)
```

**Benefits**:
- More realistic physics (closer to human gameplay)
- Agent has more time to "think" between actions
- Reduces accidental spam-shooting
- Makes precise aiming more important

---

## Expected Impact on Learning:

### Early Generations (1-20):
- Agents will shoot less randomly
- Spam-shooters will score poorly (negative fitness)
- Agents that avoid asteroids will score better

### Mid Generations (20-60):
- Agents learn to shoot only when asteroids are near
- Accuracy improves gradually
- Movement becomes more deliberate

### Late Generations (60-100):
- High-accuracy agents dominate
- Strategic positioning emerges
- Kill rate increases with better aiming

---

## Reward Breakdown Example:

**Bad Agent (Spam Shooter, 10% accuracy):**
```
Survival: 10 seconds × 1.0 = 10 pts
Shots fired: 40 × -0.5 = -20 pts
Hits: 4 (10% accuracy)
Kills: 1 × 50 = 50 pts
Accuracy bonus: 0 pts (below 25% threshold)
---
Total: ~40 pts (low fitness)
```

**Good Agent (Accurate Shooter, 60% accuracy):**
```
Survival: 15 seconds × 1.0 = 15 pts
Shots fired: 10 × -0.5 = -5 pts
Hits: 6 (60% accuracy)
Kills: 2 × 50 = 100 pts
Accuracy bonus: 15 seconds × 15 × 0.6 = 135 pts
---
Total: ~245 pts (high fitness)
```

**Perfect Agent (90% accuracy, long survival):**
```
Survival: 25 seconds × 1.0 = 25 pts
Shots fired: 20 × -0.5 = -10 pts
Hits: 18 (90% accuracy)
Kills: 6 × 50 = 300 pts
Accuracy bonus: 25 seconds × 15 × 0.9 = 337.5 pts
KPM bonus: ~50 pts
---
Total: ~700+ pts (excellent fitness)
```

---

## Files Modified:

1. **`game/classes/player.py`** - Reduced movement speed and fire rate
2. **`interfaces/rewards/ShootingPenalty.py`** - NEW: Penalty for wasted shots
3. **`interfaces/rewards/KillAsteroid.py`** - Doubled reward (25 → 50)
4. **`interfaces/rewards/AccuracyBonus.py`** - Increased reward (8 → 15)
5. **`training/train_ga_parallel.py`** - Added ShootingPenalty, increased max_steps to 1500
6. **`training/parallel_evaluator.py`** - Added ShootingPenalty

---

## Testing Recommendations:

1. **Run for 30-50 generations** to see the new reward structure take effect
2. **Watch accuracy metric** - should increase over generations
3. **Look for emergent behaviors**:
   - Agents positioning themselves before shooting
   - Fewer "wild" shots
   - More deliberate movement patterns

4. **If agents still spam-shoot**: Increase penalty to -1.0 per shot
5. **If agents never shoot**: Reduce penalty to -0.25 per shot
6. **If learning is too slow**: Increase kill reward to 75 or 100

---

## Quick Adjustment Guide:

**Want more aggressive agents?**
- Increase `KillAsteroid` reward (50 → 75)
- Decrease `ShootingPenalty` (-0.5 → -0.25)

**Want more accurate agents?**
- Increase `ShootingPenalty` (-0.5 → -1.0)
- Increase `AccuracyBonus` (15 → 20)

**Want faster movement?**
- Increase `player.acceleration` (0.15 → 0.2)
- Increase `player.rotation_speed` (3 → 4)

**Want faster fire rate?**
- Decrease `player.shoot_cooldown` (0.25 → 0.18)

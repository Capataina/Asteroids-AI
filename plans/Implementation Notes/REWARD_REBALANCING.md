# Reward Rebalancing for Long Episodes

## Problem Identified

With 1500-step episodes (~25 seconds at 60 FPS), the per-second reward rates were way too high, causing fitness scores to balloon into the tens of thousands even for mediocre performance.

### Original Values (Scaled for ~5 second episodes)
- **KillAsteroid**: 50 points per kill
- **AccuracyBonus**: 15 points/second
- **FacingAsteroidBonus**: 15 points/second  
- **MaintainingMomentumBonus**: 3 points/second

### Problem Example
An agent surviving 481 steps (~8 seconds) with 1 kill and 11% accuracy was scoring **18,166 points**, when it should have scored around **150-200 points**.

**Why this happened:**
- Time-based rewards dominate: 15 pts/sec × 25 sec = **375 points** just for facing asteroids
- Kills became insignificant: 50 points is nothing compared to 10,000+ points from time rewards
- AI had no incentive to take risks or be aggressive

## New Balanced Values (for 1500-step episodes)

### Core Philosophy
1. **Kills should be the primary reward** - riskier, more valuable actions
2. **Behavioral shaping should guide, not dominate** - helpful hints, not the goal
3. **Scale appropriately** - rewards should match episode length

### New Reward Structure

#### Primary Rewards (High Value)
- **KillAsteroid**: **100 points** per kill (doubled from 50)
  - Most important metric
  - Encourages risk-taking and aggression
  - 5 kills = 500 points baseline

#### Secondary Rewards (Supporting Behaviors)
- **AccuracyBonus**: **2 points/second** (reduced from 15)
  - Max ~50 points for full episode at 100% accuracy
  - Still encourages careful aiming
  - Doesn't dominate the score

- **FacingAsteroidBonus**: **2 points/second** (reduced from 15)
  - Max ~50 points for full episode if constantly facing asteroids
  - Guides agents toward engagement
  - Not rewarded more than actually killing

- **MaintainingMomentumBonus**: **0.5 points/second** (reduced from 3), **-1 penalty** (from -3)
  - Max ~12 points for full episode
  - Small nudge to keep moving
  - Penalty for sitting still more noticeable

## Expected Fitness Ranges

### Good Performance (1500 steps)
- 5 kills: **500 points** (kills)
- 50% accuracy: **25 points** (accuracy bonus)
- 50% facing time: **25 points** (facing bonus)
- Constant movement: **12 points** (momentum)
- **Total: ~560 points**

### Great Performance (1500 steps)
- 10 kills: **1000 points** (kills)
- 70% accuracy: **35 points**
- 70% facing time: **35 points**
- Constant movement: **12 points**
- **Total: ~1080 points**

### Mediocre Performance (481 steps as shown)
- 1 kill: **100 points** (kills)
- 11% accuracy: **0 points** (below 25% threshold)
- 50% facing: **8 points** (8 seconds × 2 × 0.5)
- Some movement: **4 points** (8 seconds × 0.5)
- **Total: ~112 points** ✅ Much more reasonable!

## Migration Notes

- Old fitness scores are NOT comparable to new scores
- Expect initial generation fitness to be in the **100-500 range** now
- Good agents should reach **1000-2000 points** after training
- The all-time best from old runs (35,957) would translate to maybe **3,000-4,000** in new system

## Benefits of This Change

1. ✅ **Kills are now the primary goal** - AI will learn aggressive play
2. ✅ **Behavioral shaping provides guidance** - still useful but not dominant
3. ✅ **Fitness scores are interpretable** - you can reason about what they mean
4. ✅ **Risk/reward balance** - taking risks (attacking) pays off more than playing safe
5. ✅ **Comparable across different episode lengths** - more stable learning signal

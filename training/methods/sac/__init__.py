"""
SAC (Soft Actor-Critic) with GNN backbone for AsteroidsAI.

This module implements:
- GNN backbone for graph state encoding
- Stochastic actor with continuous turn/thrust and discrete shoot
- Twin Q-critics for SAC
- Replay buffer for off-policy learning
- SAC learner with automatic entropy tuning
"""

from training.methods.sac.networks import GNNBackbone, Actor, TwinCritics
from training.methods.sac.replay_buffer import ReplayBuffer, Transition
from training.methods.sac.learner import SACLearner

__all__ = [
    'GNNBackbone',
    'Actor',
    'TwinCritics',
    'ReplayBuffer',
    'Transition',
    'SACLearner',
]

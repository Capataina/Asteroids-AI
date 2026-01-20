"""
Configuration for GNN-SAC training.

Hyperparameters are exposed as class attributes for consistency
with other training configs (GAConfig, ESConfig, NEATConfig).
"""


class SACConfig:
    """Configuration for GNN-SAC training."""

    # === Training Duration ===
    TOTAL_STEPS = 500_000           # Total environment steps
    MAX_EPISODE_STEPS = 1500        # Max steps per episode
    FRAME_DELAY = 1.0 / 60.0        # Fixed time step (60 FPS)

    # === SAC Hyperparameters ===
    GAMMA = 0.99                    # Discount factor
    TAU = 0.005                     # Target network update rate (Polyak averaging)
    BATCH_SIZE = 256                # Minibatch size for updates
    REPLAY_SIZE = 100_000           # Replay buffer capacity
    LEARN_START_STEPS = 5_000       # Steps before learning begins
    UPDATES_PER_STEP = 1            # Gradient updates per environment step

    # === Learning Rates ===
    ACTOR_LR = 3e-4                 # Actor (and GNN) learning rate
    CRITIC_LR = 3e-4                # Critic learning rate
    ALPHA_LR = 3e-4                 # Entropy temperature learning rate

    # === Entropy Tuning ===
    AUTO_ENTROPY = True             # Enable automatic entropy tuning
    INIT_ALPHA = 0.2                # Initial entropy temperature
    TARGET_ENTROPY = -3.0           # Target entropy (typically -dim(action))

    # === GNN Architecture ===
    GNN_HIDDEN_DIM = 64             # Hidden dimension for GNN layers
    GNN_NUM_LAYERS = 2              # Number of GNN message passing layers
    GNN_HEADS = 4                   # Number of attention heads
    GNN_DROPOUT = 0.0               # Dropout probability

    # === Actor/Critic Architecture ===
    ACTOR_HIDDEN_DIM = 256          # Hidden dimension for actor MLP
    CRITIC_HIDDEN_DIM = 256         # Hidden dimension for critic MLPs

    # === Stability ===
    GRAD_CLIP_NORM = 10.0           # Gradient clipping threshold

    # === Graph Encoder ===
    MAX_ASTEROIDS = None            # Maximum asteroids in graph (None = all)

    # === Logging & Display ===
    LOG_EVERY_STEPS = 1_000         # Log metrics every N steps
    DISPLAY_EVERY_STEPS = 10_000    # Display best policy every N steps
    SAVE_EVERY_STEPS = 50_000       # Save checkpoint every N steps

    # === Single-Process Simulation ===
    TRAIN_STEPS_PER_FRAME = 2       # Headless training steps per render frame (simulate script)

    # === Evaluation / Best Tracking ===
    EVAL_EVERY_EPISODES = 5         # Evaluate current policy every N episodes
    EVAL_SEEDS = [1001, 1002, 1003, 1004, 1005]  # Fixed evaluation seeds
    BEST_CHECKPOINT_PATH = "training/sac_checkpoints/best_sac.pt"

    # === Viewer / Playback ===
    VIEWER_MAX_STEPS = 1500         # Max steps per visible episode
    VIEWER_SEED_MODE = "increment"  # increment | random
    VIEWER_SEED_START = 200000
    VIEWER_SEED_RANGE = (200000, 900000)

    # === Seeds ===
    SEED = 42                       # Random seed for reproducibility

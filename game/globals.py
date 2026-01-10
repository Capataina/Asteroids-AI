"""
Global constants for the Asteroids game.
Acts as a single source of truth for physics, dimensions, and game rules
to ensure parity between the visual game and the headless simulation.
"""

# Screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Asteroids Basic"

# Player Physics
PLAYER_SCALE = 0.5
PLAYER_ACCELERATION = 0.15  # Pixels per frame^2
PLAYER_ROTATION_SPEED = 3.0  # Degrees per frame
PLAYER_FRICTION = 0.99      # Velocity multiplier per frame
PLAYER_RADIUS = 5.0        # Collision radius (pixels)

# Weapon
BULLET_SCALE = 0.8
BULLET_SPEED = 10.0         # Pixels per frame
BULLET_LIFETIME = 60        # Frames
BULLET_COOLDOWN = 0.25      # Seconds
BULLET_RADIUS = 2.0         # Collision radius (pixels)

# Asteroids
ASTEROID_SPAWN_INTERVAL = 0.75  # Seconds between spawns

# Asteroid Sizes (Scale factors)
ASTEROID_SCALE_LARGE = 1.25
ASTEROID_SCALE_MEDIUM = 0.75
ASTEROID_SCALE_SMALL = 0.50

# Base radius for a scale=1.0 asteroid (approximate from sprite)
# Actual sprite is ~64x64, so radius 32 is a good baseline
ASTEROID_BASE_RADIUS = 16.0

# Calculated radii for collision
ASTEROID_RADIUS_LARGE = ASTEROID_BASE_RADIUS * ASTEROID_SCALE_LARGE   # 40.0
ASTEROID_RADIUS_MEDIUM = ASTEROID_BASE_RADIUS * ASTEROID_SCALE_MEDIUM # 24.0
ASTEROID_RADIUS_SMALL = ASTEROID_BASE_RADIUS * ASTEROID_SCALE_SMALL   # 16.0

# Asteroid Physics
ASTEROID_SPEED_LARGE = 1.0
ASTEROID_SPEED_MEDIUM = 2.0
ASTEROID_SPEED_SMALL = 3.0

ASTEROID_HP_LARGE = 3
ASTEROID_HP_MEDIUM = 2
ASTEROID_HP_SMALL = 1

# Collision Logic
COLLISION_DEBUG_ENABLED = False  # Default debug state

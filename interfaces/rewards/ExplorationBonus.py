from typing import Set, Tuple
from interfaces.RewardCalculator import RewardComponent
from interfaces.EnvironmentTracker import EnvironmentTracker
from interfaces.MetricsTracker import MetricsTracker

class ExplorationBonus(RewardComponent):
    """
    Rewards the agent for exploring the game world.
    The screen is divided into a grid, and a one-time bonus is awarded
    for entering each grid cell for the first time in an episode.
    """
    def __init__(self, screen_width: int, screen_height: int, grid_rows: int = 3, grid_cols: int = 4, bonus_per_cell: float = 50.0):
        """
        Args:
            screen_width: The width of the game screen.
            screen_height: The height of the game screen.
            grid_rows: How many rows to divide the screen into.
            grid_cols: How many columns to divide the screen into.
            bonus_per_cell: The one-time bonus for entering a new cell.
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.grid_rows = grid_rows
        self.grid_cols = grid_cols
        self.bonus_per_cell = bonus_per_cell
        
        self.cell_width = screen_width / grid_cols
        self.cell_height = screen_height / grid_rows
        
        self.visited_cells: Set[Tuple[int, int]] = set()

    def calculate_step_reward(self, env_tracker: EnvironmentTracker, metrics_tracker: MetricsTracker, debug: bool = False) -> float:
        player = env_tracker.get_player()
        if not player:
            return 0.0
            
        # Determine the player's current grid cell
        col = int(player.center_x // self.cell_width)
        row = int(player.center_y // self.cell_height)
        
        current_cell = (row, col)
        
        # If the cell has not been visited yet in this episode
        if current_cell not in self.visited_cells:
            self.visited_cells.add(current_cell)
            if debug:
                print(f"ExplorationBonus: Entered new cell {current_cell}. "
                      f"Reward: {self.bonus_per_cell}. Total visited: {len(self.visited_cells)}")
            return self.bonus_per_cell
            
        return 0.0

    def calculate_episode_reward(self, metrics_tracker: MetricsTracker) -> float:
        return 0.0

    def reset(self):
        """Called at the start of a new episode."""
        self.visited_cells.clear()

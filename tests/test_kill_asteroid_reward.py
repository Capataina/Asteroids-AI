"""
Comprehensive tests for KillAsteroid reward component.

Tests cover:
- Normal operation (single and multiple kills)
- Edge cases (no kills, reset behavior, state tracking)
- Configurable reward amounts
- Episode-level rewards
- State persistence across multiple steps
"""

import unittest
from unittest.mock import Mock
from interfaces.rewards.KillAsteroid import KillAsteroid
from interfaces.EnvironmentTracker import EnvironmentTracker
from interfaces.MetricsTracker import MetricsTracker


class TestKillAsteroidReward(unittest.TestCase):
    """Test suite for KillAsteroid reward component."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create mock trackers that will be reused across tests
        self.mock_env_tracker = Mock(spec=EnvironmentTracker)
        self.mock_metrics_tracker = Mock(spec=MetricsTracker)
        
        # Default mock behavior - no kills initially
        self.mock_metrics_tracker.get_total_kills.return_value = 0

    def test_initial_state_no_kills(self):
        """Test that initial state with no kills returns zero reward."""
        reward_component = KillAsteroid(reward_per_asteroid=10.0)
        
        reward = reward_component.calculate_step_reward(
            self.mock_env_tracker,
            self.mock_metrics_tracker
        )
        
        self.assertEqual(reward, 0.0, "Should return 0.0 when no kills have occurred")
        self.assertEqual(reward_component.prev_kills, 0, "prev_kills should remain 0")

    def test_single_kill_rewards_correctly(self):
        """Test that a single kill rewards the correct amount."""
        reward_per_asteroid = 10.0
        reward_component = KillAsteroid(reward_per_asteroid=reward_per_asteroid)
        
        # First step: no kills
        self.mock_metrics_tracker.get_total_kills.return_value = 0
        reward1 = reward_component.calculate_step_reward(
            self.mock_env_tracker,
            self.mock_metrics_tracker
        )
        self.assertEqual(reward1, 0.0)
        
        # Second step: one kill
        self.mock_metrics_tracker.get_total_kills.return_value = 1
        reward2 = reward_component.calculate_step_reward(
            self.mock_env_tracker,
            self.mock_metrics_tracker
        )
        
        self.assertEqual(reward2, reward_per_asteroid, 
                        f"Should reward {reward_per_asteroid} for one kill")
        self.assertEqual(reward_component.prev_kills, 1, 
                        "prev_kills should be updated to 1")

    def test_multiple_kills_single_step(self):
        """Test that multiple kills in one step are rewarded correctly."""
        reward_per_asteroid = 10.0
        reward_component = KillAsteroid(reward_per_asteroid=reward_per_asteroid)
        
        # First step: no kills
        self.mock_metrics_tracker.get_total_kills.return_value = 0
        reward_component.calculate_step_reward(
            self.mock_env_tracker,
            self.mock_metrics_tracker
        )
        
        # Second step: 3 kills (e.g., multiple asteroids destroyed)
        self.mock_metrics_tracker.get_total_kills.return_value = 3
        reward = reward_component.calculate_step_reward(
            self.mock_env_tracker,
            self.mock_metrics_tracker
        )
        
        expected_reward = 3 * reward_per_asteroid
        self.assertEqual(reward, expected_reward, 
                        f"Should reward {expected_reward} for 3 kills")
        self.assertEqual(reward_component.prev_kills, 3,
                        "prev_kills should be updated to 3")

    def test_multiple_kills_across_multiple_steps(self):
        """Test that kills across multiple steps are tracked correctly."""
        reward_per_asteroid = 10.0
        reward_component = KillAsteroid(reward_per_asteroid=reward_per_asteroid)
        
        # Step 1: no kills
        self.mock_metrics_tracker.get_total_kills.return_value = 0
        reward1 = reward_component.calculate_step_reward(
            self.mock_env_tracker,
            self.mock_metrics_tracker
        )
        self.assertEqual(reward1, 0.0)
        
        # Step 2: one kill
        self.mock_metrics_tracker.get_total_kills.return_value = 1
        reward2 = reward_component.calculate_step_reward(
            self.mock_env_tracker,
            self.mock_metrics_tracker
        )
        self.assertEqual(reward2, reward_per_asteroid)
        
        # Step 3: still one kill (no new kills)
        self.mock_metrics_tracker.get_total_kills.return_value = 1
        reward3 = reward_component.calculate_step_reward(
            self.mock_env_tracker,
            self.mock_metrics_tracker
        )
        self.assertEqual(reward3, 0.0, "Should return 0.0 when kills haven't increased")
        
        # Step 4: two more kills (total 3)
        self.mock_metrics_tracker.get_total_kills.return_value = 3
        reward4 = reward_component.calculate_step_reward(
            self.mock_env_tracker,
            self.mock_metrics_tracker
        )
        expected_reward = 2 * reward_per_asteroid  # Delta is 2 (3 - 1)
        self.assertEqual(reward4, expected_reward,
                        f"Should reward {expected_reward} for 2 new kills")
        self.assertEqual(reward_component.prev_kills, 3)

    def test_custom_reward_amount(self):
        """Test that custom reward_per_asteroid values work correctly."""
        custom_reward = 25.5
        reward_component = KillAsteroid(reward_per_asteroid=custom_reward)
        
        # No kills initially
        self.mock_metrics_tracker.get_total_kills.return_value = 0
        reward_component.calculate_step_reward(
            self.mock_env_tracker,
            self.mock_metrics_tracker
        )
        
        # One kill with custom reward
        self.mock_metrics_tracker.get_total_kills.return_value = 1
        reward = reward_component.calculate_step_reward(
            self.mock_env_tracker,
            self.mock_metrics_tracker
        )
        
        self.assertEqual(reward, custom_reward,
                        f"Should reward {custom_reward} for one kill")

    def test_default_reward_amount(self):
        """Test that default reward_per_asteroid is 10.0."""
        reward_component = KillAsteroid()  # Use default
        
        self.assertEqual(reward_component.reward_per_asteroid, 10.0,
                        "Default reward_per_asteroid should be 10.0")

    def test_reset_clears_state(self):
        """Test that reset() properly clears the previous kills state."""
        reward_component = KillAsteroid(reward_per_asteroid=10.0)
        
        # Accumulate some kills
        self.mock_metrics_tracker.get_total_kills.return_value = 0
        reward_component.calculate_step_reward(
            self.mock_env_tracker,
            self.mock_metrics_tracker
        )
        
        self.mock_metrics_tracker.get_total_kills.return_value = 5
        reward_component.calculate_step_reward(
            self.mock_env_tracker,
            self.mock_metrics_tracker
        )
        self.assertEqual(reward_component.prev_kills, 5,
                        "prev_kills should be 5 before reset")
        
        # Reset should clear state
        reward_component.reset()
        self.assertEqual(reward_component.prev_kills, 0,
                        "prev_kills should be 0 after reset")
        
        # After reset, new kills should be rewarded from 0
        self.mock_metrics_tracker.get_total_kills.return_value = 2
        reward_after_reset = reward_component.calculate_step_reward(
            self.mock_env_tracker,
            self.mock_metrics_tracker
        )
        expected_reward = 2 * 10.0
        self.assertEqual(reward_after_reset, expected_reward,
                        "Should reward from 0 after reset")
        self.assertEqual(reward_component.prev_kills, 2)

    def test_episode_reward_returns_zero(self):
        """Test that calculate_episode_reward always returns 0.0."""
        reward_component = KillAsteroid(reward_per_asteroid=10.0)
        
        # Set up metrics tracker with some kills
        self.mock_metrics_tracker.get_total_kills.return_value = 10
        
        episode_reward = reward_component.calculate_episode_reward(
            self.mock_metrics_tracker
        )
        
        self.assertEqual(episode_reward, 0.0,
                        "Episode reward should always return 0.0 for KillAsteroid")

    def test_kills_decreasing_handled_gracefully(self):
        """Test behavior when kills decrease (shouldn't happen normally but test robustness)."""
        reward_component = KillAsteroid(reward_per_asteroid=10.0)
        
        # Step 1: 5 kills
        self.mock_metrics_tracker.get_total_kills.return_value = 5
        reward_component.calculate_step_reward(
            self.mock_env_tracker,
            self.mock_metrics_tracker
        )
        self.assertEqual(reward_component.prev_kills, 5)
        
        # Step 2: kills decrease to 3 (shouldn't happen, but test robustness)
        self.mock_metrics_tracker.get_total_kills.return_value = 3
        reward = reward_component.calculate_step_reward(
            self.mock_env_tracker,
            self.mock_metrics_tracker
        )
        
        # Current implementation: if kills decrease, it should still calculate
        # delta = 3 - 5 = -2, so reward would be negative
        # This tests the actual behavior (may want to add guards later)
        expected_reward = (3 - 5) * 10.0  # -20.0
        self.assertEqual(reward, expected_reward,
                        "Should handle decreasing kills (may produce negative reward)")
        self.assertEqual(reward_component.prev_kills, 3,
                        "prev_kills should be updated to current value even if decreased")

    def test_kills_unchanged_returns_zero(self):
        """Test that unchanged kill count returns zero reward."""
        reward_component = KillAsteroid(reward_per_asteroid=10.0)
        
        # Set up initial state with 2 kills
        self.mock_metrics_tracker.get_total_kills.return_value = 2
        reward_component.calculate_step_reward(
            self.mock_env_tracker,
            self.mock_metrics_tracker
        )
        self.assertEqual(reward_component.prev_kills, 2)
        
        # Same kill count
        self.mock_metrics_tracker.get_total_kills.return_value = 2
        reward = reward_component.calculate_step_reward(
            self.mock_env_tracker,
            self.mock_metrics_tracker
        )
        
        self.assertEqual(reward, 0.0, "Should return 0.0 when kills unchanged")
        self.assertEqual(reward_component.prev_kills, 2,
                        "prev_kills should remain unchanged")

    def test_zero_reward_per_asteroid(self):
        """Test behavior with zero reward_per_asteroid."""
        reward_component = KillAsteroid(reward_per_asteroid=0.0)
        
        # No kills initially
        self.mock_metrics_tracker.get_total_kills.return_value = 0
        reward_component.calculate_step_reward(
            self.mock_env_tracker,
            self.mock_metrics_tracker
        )
        
        # One kill with zero reward
        self.mock_metrics_tracker.get_total_kills.return_value = 1
        reward = reward_component.calculate_step_reward(
            self.mock_env_tracker,
            self.mock_metrics_tracker
        )
        
        self.assertEqual(reward, 0.0, "Should return 0.0 when reward_per_asteroid is 0.0")

    def test_negative_reward_per_asteroid(self):
        """Test behavior with negative reward_per_asteroid (punishment for kills)."""
        reward_component = KillAsteroid(reward_per_asteroid=-5.0)
        
        # No kills initially
        self.mock_metrics_tracker.get_total_kills.return_value = 0
        reward_component.calculate_step_reward(
            self.mock_env_tracker,
            self.mock_metrics_tracker
        )
        
        # One kill with negative reward (punishment)
        self.mock_metrics_tracker.get_total_kills.return_value = 1
        reward = reward_component.calculate_step_reward(
            self.mock_env_tracker,
            self.mock_metrics_tracker
        )
        
        self.assertEqual(reward, -5.0, "Should return -5.0 when reward_per_asteroid is -5.0")

    def test_very_large_kill_count(self):
        """Test behavior with very large kill counts."""
        reward_component = KillAsteroid(reward_per_asteroid=10.0)
        
        # No kills initially
        self.mock_metrics_tracker.get_total_kills.return_value = 0
        reward_component.calculate_step_reward(
            self.mock_env_tracker,
            self.mock_metrics_tracker
        )
        
        # Very large number of kills
        large_count = 1000000
        self.mock_metrics_tracker.get_total_kills.return_value = large_count
        reward = reward_component.calculate_step_reward(
            self.mock_env_tracker,
            self.mock_metrics_tracker
        )
        
        expected_reward = large_count * 10.0
        self.assertEqual(reward, expected_reward,
                        "Should handle very large kill counts correctly")

    def test_metrics_tracker_called_correctly(self):
        """Test that get_total_kills() is called on metrics_tracker."""
        reward_component = KillAsteroid(reward_per_asteroid=10.0)
        
        self.mock_metrics_tracker.get_total_kills.return_value = 0
        
        reward_component.calculate_step_reward(
            self.mock_env_tracker,
            self.mock_metrics_tracker
        )
        
        # Verify get_total_kills was called
        self.mock_metrics_tracker.get_total_kills.assert_called()

    def test_consecutive_identical_steps(self):
        """Test multiple consecutive steps with identical kill counts."""
        reward_component = KillAsteroid(reward_per_asteroid=10.0)
        
        # Multiple steps with same kill count
        for _ in range(5):
            self.mock_metrics_tracker.get_total_kills.return_value = 0
            reward = reward_component.calculate_step_reward(
                self.mock_env_tracker,
                self.mock_metrics_tracker
            )
            self.assertEqual(reward, 0.0, "Should return 0.0 for consecutive identical steps")
        
        # Then one kill
        self.mock_metrics_tracker.get_total_kills.return_value = 1
        reward = reward_component.calculate_step_reward(
            self.mock_env_tracker,
            self.mock_metrics_tracker
        )
        self.assertEqual(reward, 10.0, "Should reward after consecutive zero steps")


if __name__ == '__main__':
    unittest.main()


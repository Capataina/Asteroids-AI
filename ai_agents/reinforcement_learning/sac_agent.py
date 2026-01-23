from typing import Any, List, Optional
import torch

from ai_agents.base_agent import BaseAgent
from interfaces.encoders.GraphEncoder import GraphPayload
from training.config.sac import SACConfig
from training.methods.sac.learner import SACLearner
from training.methods.sac.replay_buffer import ReplayBuffer


class SACAgent(BaseAgent):
    """Inference-only SAC agent wrapper for playback."""
    def __init__(self, learner: SACLearner, device: Optional[torch.device] = None):
        self.learner = learner
        self.device = device or learner.device
        self.prev_action: Optional[List[float]] = None

    def get_action(self, state: Any) -> List[float]:
        if not isinstance(state, GraphPayload):
            raise ValueError("SACAgent expects GraphPayload state from GraphEncoder.")

        graph_tensors = ReplayBuffer.collate_graphs([state], self.device)
        action_tensor, _ = self.learner.select_action(graph_tensors, deterministic=True)

        action = action_tensor.squeeze(0).detach().cpu().tolist()
        if SACConfig.ACTION_SMOOTHING_ENABLED:
            if self.prev_action is None:
                smoothed = action
            else:
                alpha = SACConfig.ACTION_SMOOTHING_ALPHA
                smoothed = [
                    alpha * self.prev_action[0] + (1.0 - alpha) * action[0],
                    alpha * self.prev_action[1] + (1.0 - alpha) * action[1],
                    alpha * self.prev_action[2] + (1.0 - alpha) * action[2],
                ]
            smoothed = [
                max(-1.0, min(1.0, float(smoothed[0]))),
                max(0.0, min(1.0, float(smoothed[1]))),
                max(0.0, min(1.0, float(smoothed[2]))),
            ]
            self.prev_action = smoothed
            action = smoothed

        # Map turn from [-1, 1] to [0, 1] for ActionInterface compatibility.
        turn = (action[0] + 1.0) * 0.5
        thrust = max(0.0, min(1.0, action[1]))
        shoot = max(0.0, min(1.0, action[2]))

        return [turn, thrust, shoot]

    def reset(self) -> None:
        # Stateless for now; no RNN hidden state.
        self.prev_action = None

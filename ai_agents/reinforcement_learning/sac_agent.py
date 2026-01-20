from typing import Any, List, Optional
import torch

from ai_agents.base_agent import BaseAgent
from interfaces.encoders.GraphEncoder import GraphPayload
from training.methods.sac.learner import SACLearner
from training.methods.sac.replay_buffer import ReplayBuffer


class SACAgent(BaseAgent):
    """Inference-only SAC agent wrapper for playback."""
    def __init__(self, learner: SACLearner, device: Optional[torch.device] = None):
        self.learner = learner
        self.device = device or learner.device

    def get_action(self, state: Any) -> List[float]:
        if not isinstance(state, GraphPayload):
            raise ValueError("SACAgent expects GraphPayload state from GraphEncoder.")

        graph_tensors = ReplayBuffer.collate_graphs([state], self.device)
        action_tensor, _ = self.learner.select_action(graph_tensors, deterministic=True)

        action = action_tensor.squeeze(0).detach().cpu().tolist()
        # Map turn from [-1, 1] to [0, 1] for ActionInterface compatibility.
        turn = (action[0] + 1.0) * 0.5
        thrust = max(0.0, min(1.0, action[1]))
        shoot = max(0.0, min(1.0, action[2]))

        return [turn, thrust, shoot]

    def reset(self) -> None:
        # Stateless for now; no RNN hidden state.
        pass

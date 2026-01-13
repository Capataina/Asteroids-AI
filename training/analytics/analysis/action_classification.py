"""
Behavioral classification logic for agents.

Analyzes action metrics to assign descriptive labels to agent strategies.
"""

from typing import Dict, Any

def get_action_rates(metrics: Dict[str, Any]) -> Dict[str, float]:
    """Calculate normalized action rates per step.
    
    Args:
        metrics: Dictionary containing 'avg_thrust_frames', 'avg_turn_frames', 
                 'avg_shoot_frames', and 'avg_steps_survived' (or similar best_agent keys)
                 
    Returns:
        Dictionary with 'thrust_rate', 'turn_rate', 'shoot_rate'
    """
    # Handle both population average keys and best agent keys
    steps = metrics.get('avg_steps') or metrics.get('best_agent_steps', 1)
    if steps == 0: steps = 1
    
    thrust = metrics.get('avg_thrust_frames') or metrics.get('best_agent_thrust', 0)
    turn = metrics.get('avg_turn_frames') or metrics.get('best_agent_turn', 0)
    shoot = metrics.get('avg_shoot_frames') or metrics.get('best_agent_shoot', 0)
    
    return {
        'thrust_rate': thrust / steps,
        'turn_rate': turn / steps,
        'shoot_rate': shoot / steps
    }

def classify_behavior(metrics: Dict[str, Any]) -> str:
    """Classify agent behavior based on action patterns.
    
    Args:
        metrics: Dictionary containing action counts and steps
        
    Returns:
        String label describing the behavior (e.g., "Turret", "Dogfighter")
    """
    rates = get_action_rates(metrics)
    thrust = rates['thrust_rate']
    turn = rates['turn_rate']
    shoot = rates['shoot_rate']
    
    # Thresholds
    HIGH_SHOOT = 0.15  # Shooting > 15% of frames
    LOW_SHOOT = 0.02
    
    HIGH_MOVE = 0.10   # Thrusting > 10% of frames
    LOW_MOVE = 0.01
    
    HIGH_TURN = 0.30   # Turning > 30% of frames
    
    label = "Unknown"
    
    if shoot > HIGH_SHOOT:
        if thrust > HIGH_MOVE:
            label = "Dogfighter"  # Moves and shoots
        elif turn > HIGH_TURN:
            label = "Spinner"     # Spins and shoots (spray & pray)
        elif thrust < LOW_MOVE:
            label = "Turret"      # Sits and shoots
        else:
            label = "Aggressive"  # General shooter
            
    elif shoot < LOW_SHOOT:
        if thrust > HIGH_MOVE:
            label = "Runner"      # Moves but doesn't shoot
        elif thrust < LOW_MOVE and turn < HIGH_TURN:
            label = "Drifter"     # Doesn't do much
        else:
            label = "Passive"
            
    else:
        # Moderate shooting
        if thrust > HIGH_MOVE:
            label = "Skirmisher"
        elif thrust < LOW_MOVE:
            label = "Sniper" if metrics.get('avg_accuracy', 0) > 0.3 else "Camper"
        else:
            label = "Balanced"
            
    return label

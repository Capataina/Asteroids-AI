import random
from typing import List

def tournament_selection(population: List[List[float]], fitnesses: List[float], tournament_size: int = 3) -> List[List[float]]:
    """
    Select parents using tournament selection.
    
    Args:
        population: List of parameter vectors
        fitnesses: List of fitness scores corresponding to population
        tournament_size: Number of individuals in each tournament
        
    Returns:
        List of selected parent parameter vectors (same size as population)
    """
    parents = []
    pop_size = len(population)
    for _ in range(pop_size):
        tournament_indices = random.sample(range(pop_size), min(tournament_size, pop_size))
        tournament_fitnesses = [fitnesses[i] for i in tournament_indices]
        winner_idx = tournament_indices[tournament_fitnesses.index(max(tournament_fitnesses))]
        parents.append(population[winner_idx].copy())
    return parents

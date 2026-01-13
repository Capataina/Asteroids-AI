import random
import time
from typing import List, Dict, Optional
from training.config.genetic_algorithm import GAConfig
from training.methods.genetic_algorithm.operators import GAGeneticOperators
from training.methods.genetic_algorithm.selection import tournament_selection

class GADriver:
    """
    Manages the Genetic Algorithm population and evolution process.
    """
    def __init__(self, param_size: int):
        self.param_size = param_size
        self.population_size = GAConfig.POPULATION_SIZE
        
        self.operators = GAGeneticOperators(
            mutation_probability=GAConfig.MUTATION_PROBABILITY,
            crossover_probability=GAConfig.CROSSOVER_PROBABILITY,
            mutation_gaussian_sigma=GAConfig.MUTATION_GAUSSIAN_SIGMA,
            mutation_uniform_low=GAConfig.MUTATION_UNIFORM_LOW,
            mutation_uniform_high=GAConfig.MUTATION_UNIFORM_HIGH,
            crossover_alpha=GAConfig.CROSSOVER_ALPHA
        )
        
        self.population = self._initialize_population()
        self.last_evolution_stats = {}
        self.last_evolution_duration = 0.0

    def _initialize_population(self) -> List[List[float]]:
        return [
            [random.uniform(
                GAConfig.MUTATION_UNIFORM_LOW,
                GAConfig.MUTATION_UNIFORM_HIGH
            ) for _ in range(self.param_size)]
            for _ in range(self.population_size)
        ]

    def evolve(self, fitnesses: List[float], best_individual: Optional[List[float]] = None, stagnation: int = 0):
        """
        Evolve the population to the next generation.
        
        Args:
            fitnesses: List of fitness scores for current population.
            best_individual: All-time best individual (for elitism/preservation).
            stagnation: Number of generations without improvement (for adaptive mutation).
        """
        start_time = time.time()
        crossover_count = 0
        mutation_count = 0
        
        # Adaptive Mutation
        self._adapt_mutation(stagnation)

        # Tournament selection
        parents = tournament_selection(self.population, fitnesses)
        
        # Create offspring through crossover
        offspring = []
        while len(offspring) < self.population_size:
            if len(parents) >= 2:
                parent1 = random.choice(parents).copy()
                parent2 = random.choice(parents).copy()
                
                if random.random() < self.operators.crossover_probability:
                    result = self.operators.crossover_blend(parent1, parent2)
                    crossover_count += 1
                    if isinstance(result, tuple) and len(result) == 2:
                        child1 = list(result[0])
                        child2 = list(result[1])
                        offspring.extend([child1, child2])
                    else:
                        offspring.extend([parent1, parent2])
                else:
                    offspring.extend([parent1, parent2])
            else:
                offspring.append(random.choice(parents).copy())
        
        # Trim offspring to correct size
        offspring = offspring[:self.population_size]
        
        # Apply mutation to ALL offspring
        for i, child in enumerate(offspring):
            mutated = self.operators.mutate_gaussian(child)
            mutation_count += 1
            if isinstance(mutated, tuple) and len(mutated) > 0:
                offspring[i] = list(mutated[0])
        
        # Elitism
        sorted_pop = sorted(zip(self.population, fitnesses), key=lambda x: x[1], reverse=True)
        elite_count = max(2, self.population_size // 10)  # 10% elitism
        elite = [ind.copy() for ind, fit in sorted_pop[:elite_count]]

        # Preserve all-time best if not stagnant too long
        if best_individual is not None and stagnation < 30:
            best_in_elite = any(
                all(abs(a - b) < 1e-9 for a, b in zip(best_individual, ind))
                for ind in elite
            )
            if not best_in_elite:
                elite[-1] = best_individual.copy()

        # New population: elite + best offspring
        self.population = elite + offspring[:self.population_size - len(elite)]
        self.population = self.population[:self.population_size]
        
        self.last_evolution_duration = time.time() - start_time
        self.last_evolution_stats = {
            'crossover_events': crossover_count,
            'mutation_events': mutation_count,
            'elite_count': len(elite)
        }
    
    def _adapt_mutation(self, stagnation: int):
        """Adjust mutation parameters based on stagnation."""
        stagnation_threshold = 10
        if stagnation > stagnation_threshold:
            stagnation_severity = min((stagnation - stagnation_threshold) / 40.0, 1.0)
            prob_multiplier = 2.0 + stagnation_severity * 2.0
            sigma_multiplier = 1.5 + stagnation_severity * 1.5

            adapted_prob = min(GAConfig.MUTATION_PROBABILITY * prob_multiplier, 0.8)
            adapted_sigma = GAConfig.MUTATION_GAUSSIAN_SIGMA * sigma_multiplier

            self.operators.mutation_probability = adapted_prob
            self.operators.mutation_gaussian_sigma = adapted_sigma
            print(f"  Stagnation={stagnation} gens. Mutation boosted to prob={adapted_prob:.2f}, sigma={adapted_sigma:.3f}")
        else:
            # Reset to defaults
            self.operators.mutation_probability = GAConfig.MUTATION_PROBABILITY
            self.operators.mutation_gaussian_sigma = GAConfig.MUTATION_GAUSSIAN_SIGMA

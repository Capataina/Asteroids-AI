"""
NEAT XOR Sanity Test

This test verifies that the NEAT implementation can solve the classic XOR problem.
XOR is non-linearly separable, requiring at least one hidden node to solve.
If NEAT can't solve XOR, there's likely a bug in the implementation.

XOR Truth Table:
    Input A | Input B | Output
    --------|---------|-------
        0   |    0    |   0
        0   |    1    |   1
        1   |    0    |   1
        1   |    1    |   0

Success criteria:
- NEAT should solve XOR within ~150 generations with reasonable probability
- "Solved" means all 4 outputs are correct (threshold 0.5)
"""

import os
import sys
import random

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from ai_agents.neuroevolution.neat.genome import Genome
from training.methods.neat.innovation import InnovationTracker


# XOR dataset
XOR_INPUTS = [
    [0.0, 0.0],
    [0.0, 1.0],
    [1.0, 0.0],
    [1.0, 1.0],
]
XOR_OUTPUTS = [0.0, 1.0, 1.0, 0.0]


def evaluate_xor(genome: Genome, cycle_counter: dict = None) -> float:
    """
    Evaluate a genome on the XOR problem.

    Args:
        genome: The genome to evaluate
        cycle_counter: Optional dict to track cycle occurrences. If provided,
                      increments cycle_counter['count'] when a cycle is detected.

    Returns:
        Fitness score (higher is better). Max fitness = 4.0 (all correct).
    """
    try:
        network = genome.build_network()
    except ValueError as e:
        # Cycle detected - this should NOT happen after the crossover fix
        if "Cycle detected" in str(e):
            if cycle_counter is not None:
                cycle_counter['count'] = cycle_counter.get('count', 0) + 1
            # Return zero fitness but don't crash - we want to count all occurrences
            return 0.0
        raise

    fitness = 0.0

    for inputs, expected in zip(XOR_INPUTS, XOR_OUTPUTS):
        outputs = network.activate(inputs)
        actual = outputs[0]  # Single output

        # Fitness is based on how close the output is to expected
        error = abs(expected - actual)
        fitness += (1.0 - error) ** 2  # Squared to reward being very close

    return fitness


def evaluate_xor_accuracy(genome: Genome) -> tuple:
    """
    Evaluate a genome on XOR and return accuracy info.

    Returns:
        Tuple of (num_correct, outputs_list)
    """
    try:
        network = genome.build_network()
    except ValueError as e:
        if "Cycle detected" in str(e):
            return 0, [0.5, 0.5, 0.5, 0.5]  # Invalid genome
        raise

    correct = 0
    outputs = []

    for inputs, expected in zip(XOR_INPUTS, XOR_OUTPUTS):
        actual = network.activate(inputs)[0]
        outputs.append(actual)

        # Threshold at 0.5
        predicted = 1.0 if actual > 0.5 else 0.0
        if predicted == expected:
            correct += 1

    return correct, outputs


class SimpleNEATDriver:
    """
    Simplified NEAT driver for XOR testing.
    Uses the same core components as the full driver but stripped down.
    """

    def __init__(
        self,
        population_size: int = 150,
        compatibility_threshold: float = 3.0,
        c1: float = 1.0,
        c2: float = 1.0,
        c3: float = 0.4,
        weight_mutation_prob: float = 0.8,
        weight_mutation_sigma: float = 0.5,
        add_connection_prob: float = 0.05,
        add_node_prob: float = 0.03,
        crossover_prob: float = 0.75
    ):
        self.population_size = population_size
        self.compatibility_threshold = compatibility_threshold
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        self.weight_mutation_prob = weight_mutation_prob
        self.weight_mutation_sigma = weight_mutation_sigma
        self.add_connection_prob = add_connection_prob
        self.add_node_prob = add_node_prob
        self.crossover_prob = crossover_prob

        # XOR: 2 inputs, 1 output
        self.input_ids = [0, 1]
        self.bias_id = 2
        self.output_ids = [3]

        self.innovation_tracker = InnovationTracker(start_innovation=0, start_node_id=4)

        # Create initial population
        self.population = [
            Genome.create_minimal(
                self.input_ids,
                self.output_ids,
                self.bias_id,
                self.innovation_tracker,
                weight_range=(-1.0, 1.0)
            )
            for _ in range(population_size)
        ]

    def evolve(self, fitnesses: list) -> None:
        """Run one generation of evolution."""
        # Sort population by fitness
        paired = list(zip(self.population, fitnesses))
        paired.sort(key=lambda x: x[1], reverse=True)

        # Elitism: keep top 10%
        elite_count = max(1, self.population_size // 10)
        new_population = [genome.copy() for genome, _ in paired[:elite_count]]

        # Fill rest with offspring
        while len(new_population) < self.population_size:
            # Tournament selection
            parent1 = self._tournament_select(paired)

            if random.random() < self.crossover_prob:
                parent2 = self._tournament_select(paired)
                child = self._crossover(parent1, parent2, fitnesses)
            else:
                child = parent1.copy()

            # Mutate
            self._mutate(child)
            new_population.append(child)

        self.population = new_population[:self.population_size]

    def _tournament_select(self, paired: list, k: int = 3) -> Genome:
        """Tournament selection."""
        tournament = random.sample(paired, min(k, len(paired)))
        winner = max(tournament, key=lambda x: x[1])
        return winner[0]

    def _crossover(self, parent1: Genome, parent2: Genome, fitnesses: list) -> Genome:
        """Simple crossover - use NEAT's crossover method."""
        idx1 = self.population.index(parent1) if parent1 in self.population else 0
        idx2 = self.population.index(parent2) if parent2 in self.population else 0
        fit1 = fitnesses[idx1] if idx1 < len(fitnesses) else 0
        fit2 = fitnesses[idx2] if idx2 < len(fitnesses) else 0

        return Genome.crossover(parent1, parent2, fit1, fit2, inherit_disabled_prob=0.75)

    def _mutate(self, genome: Genome) -> None:
        """Apply mutations to a genome."""
        # Weight mutation
        genome.mutate_weights(self.weight_mutation_prob, self.weight_mutation_sigma)

        # Structural mutations
        if random.random() < self.add_node_prob:
            genome.mutate_add_node(self.innovation_tracker)

        if random.random() < self.add_connection_prob:
            genome.mutate_add_connection(self.innovation_tracker, weight_range=(-1.0, 1.0))


def run_xor_test(
    max_generations: int = 150,
    population_size: int = 150,
    target_fitness: float = 3.9,
    verbose: bool = True
) -> dict:
    """
    Run NEAT on the XOR problem.

    Args:
        max_generations: Maximum generations to run
        population_size: Size of population
        target_fitness: Fitness threshold to consider "solved" (max is 4.0)
        verbose: Print progress

    Returns:
        Dict with results: {
            'solved': bool,
            'generation': int (generation solved, or max if not solved),
            'best_fitness': float,
            'best_accuracy': int (0-4),
            'best_outputs': list,
            'cycles_detected': int (should be 0 after bug fix)
        }
    """
    driver = SimpleNEATDriver(population_size=population_size)

    best_ever_fitness = 0.0
    best_ever_genome = None
    solved_generation = None
    cycle_counter = {'count': 0}  # Track cycles detected

    for gen in range(max_generations):
        # Evaluate population (with cycle tracking)
        fitnesses = [evaluate_xor(genome, cycle_counter) for genome in driver.population]

        # Track best
        best_idx = fitnesses.index(max(fitnesses))
        best_fitness = fitnesses[best_idx]
        best_genome = driver.population[best_idx]

        if best_fitness > best_ever_fitness:
            best_ever_fitness = best_fitness
            best_ever_genome = best_genome.copy()

        # Check if solved
        accuracy, outputs = evaluate_xor_accuracy(best_genome)

        if verbose and (gen % 10 == 0 or accuracy == 4):
            cycle_msg = f" [cycles: {cycle_counter['count']}]" if cycle_counter['count'] > 0 else ""
            print(f"Gen {gen:3d}: Best fitness = {best_fitness:.4f}, Accuracy = {accuracy}/4{cycle_msg}")
            if accuracy == 4 or gen % 50 == 0:
                print(f"         Outputs: {[f'{o:.3f}' for o in outputs]}")
                print(f"         Expected: {XOR_OUTPUTS}")

        if best_fitness >= target_fitness and accuracy == 4:
            solved_generation = gen
            if verbose:
                print(f"\nSOLVED at generation {gen}!")
                print(f"Network has {best_genome.num_nodes()} nodes, {best_genome.num_enabled_connections()} connections")
            break

        # Evolve
        driver.evolve(fitnesses)

    # Final evaluation
    final_accuracy, final_outputs = evaluate_xor_accuracy(best_ever_genome)

    return {
        'solved': solved_generation is not None,
        'generation': solved_generation if solved_generation else max_generations,
        'best_fitness': best_ever_fitness,
        'best_accuracy': final_accuracy,
        'best_outputs': final_outputs,
        'best_genome': best_ever_genome,
        'cycles_detected': cycle_counter['count']
    }


def run_cycle_stress_test(
    num_generations: int = 100,
    population_size: int = 200,
    num_trials: int = 5,
    verbose: bool = True
) -> dict:
    """
    Stress test to verify that crossover no longer produces cycles.

    This test runs multiple trials with large populations and many generations
    to maximize the chance of triggering the cycle bug if it still exists.

    Args:
        num_generations: Generations per trial
        population_size: Population size (larger = more crossovers)
        num_trials: Number of independent trials
        verbose: Print progress

    Returns:
        Dict with results: {
            'total_cycles': int (should be 0),
            'total_evaluations': int,
            'passed': bool
        }
    """
    total_cycles = 0
    total_evaluations = 0

    if verbose:
        print(f"Running cycle stress test: {num_trials} trials x {num_generations} generations x {population_size} pop")
        print("=" * 60)

    for trial in range(num_trials):
        result = run_xor_test(
            max_generations=num_generations,
            population_size=population_size,
            verbose=False
        )
        cycles = result['cycles_detected']
        evals = num_generations * population_size
        total_cycles += cycles
        total_evaluations += evals

        if verbose:
            status = "PASS" if cycles == 0 else f"FAIL ({cycles} cycles)"
            print(f"  Trial {trial + 1}/{num_trials}: {status}")

    passed = total_cycles == 0

    if verbose:
        print("=" * 60)
        print(f"Total evaluations: {total_evaluations}")
        print(f"Total cycles detected: {total_cycles}")
        print(f"Result: {'PASSED - No cycles detected!' if passed else 'FAILED - Cycles still occurring'}")

    return {
        'total_cycles': total_cycles,
        'total_evaluations': total_evaluations,
        'passed': passed
    }


def run_multiple_trials(num_trials: int = 10, **kwargs) -> dict:
    """
    Run multiple trials and report statistics.

    Args:
        num_trials: Number of independent trials
        **kwargs: Arguments passed to run_xor_test

    Returns:
        Dict with aggregate statistics
    """
    results = []

    print(f"Running {num_trials} trials...\n")

    for trial in range(num_trials):
        print(f"=== Trial {trial + 1}/{num_trials} ===")
        result = run_xor_test(**kwargs)
        results.append(result)
        print()

    # Aggregate
    solved_count = sum(1 for r in results if r['solved'])
    generations = [r['generation'] for r in results]
    fitnesses = [r['best_fitness'] for r in results]
    accuracies = [r['best_accuracy'] for r in results]

    print("=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(f"Solved: {solved_count}/{num_trials} ({100*solved_count/num_trials:.1f}%)")
    print(f"Average generations (when solved): {sum(g for g, r in zip(generations, results) if r['solved']) / max(1, solved_count):.1f}")
    print(f"Average best fitness: {sum(fitnesses)/len(fitnesses):.4f}")
    print(f"Average accuracy: {sum(accuracies)/len(accuracies):.2f}/4")

    return {
        'num_trials': num_trials,
        'solved_count': solved_count,
        'solve_rate': solved_count / num_trials,
        'avg_generations_when_solved': sum(g for g, r in zip(generations, results) if r['solved']) / max(1, solved_count),
        'avg_fitness': sum(fitnesses) / len(fitnesses),
        'avg_accuracy': sum(accuracies) / len(accuracies),
        'results': results
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Test NEAT implementation on XOR problem")
    parser.add_argument("--trials", type=int, default=1, help="Number of trials to run")
    parser.add_argument("--generations", type=int, default=150, help="Max generations per trial")
    parser.add_argument("--population", type=int, default=150, help="Population size")
    parser.add_argument("--quiet", action="store_true", help="Reduce output verbosity")
    parser.add_argument("--stress-test", action="store_true",
                        help="Run cycle stress test to verify crossover bug fix")

    args = parser.parse_args()

    # Cycle stress test mode
    if args.stress_test:
        print("=" * 60)
        print("NEAT CYCLE BUG STRESS TEST")
        print("=" * 60)
        print("This test verifies that crossover no longer creates cycles.")
        print()

        stress_result = run_cycle_stress_test(
            num_generations=args.generations,
            population_size=args.population,
            num_trials=max(args.trials, 5),  # At least 5 trials for stress test
            verbose=not args.quiet
        )

        if stress_result['passed']:
            print("\nCycle bug fix VERIFIED - crossover is safe!")
            sys.exit(0)
        else:
            print(f"\nCycle bug NOT FIXED - {stress_result['total_cycles']} cycles detected!")
            sys.exit(1)

    # Normal XOR test mode
    elif args.trials == 1:
        result = run_xor_test(
            max_generations=args.generations,
            population_size=args.population,
            verbose=not args.quiet
        )

        print("\n" + "=" * 50)
        print("RESULT")
        print("=" * 50)
        print(f"Solved: {result['solved']}")
        print(f"Generation: {result['generation']}")
        print(f"Best Fitness: {result['best_fitness']:.4f}")
        print(f"Best Accuracy: {result['best_accuracy']}/4")
        print(f"Cycles Detected: {result['cycles_detected']}")

        if result['cycles_detected'] > 0:
            print(f"\nWARNING: {result['cycles_detected']} cycles were detected!")
            print("The cycle bug may not be fully fixed.")
            sys.exit(1)
        elif result['solved']:
            print("\nNEAT implementation PASSED XOR sanity test!")
            sys.exit(0)
        else:
            print("\nNEAT implementation FAILED XOR sanity test.")
            print("This may indicate a bug, or the test needs more generations.")
            sys.exit(1)
    else:
        stats = run_multiple_trials(
            num_trials=args.trials,
            max_generations=args.generations,
            population_size=args.population,
            verbose=not args.quiet
        )

        # Check for cycles across all trials
        total_cycles = sum(r.get('cycles_detected', 0) for r in stats['results'])

        if total_cycles > 0:
            print(f"\nWARNING: {total_cycles} cycles detected across trials!")
            sys.exit(1)
        elif stats['solve_rate'] >= 0.7:
            print("\nNEAT implementation PASSED XOR sanity test (>=70% solve rate)!")
            sys.exit(0)
        else:
            print(f"\nNEAT implementation has LOW solve rate ({stats['solve_rate']*100:.1f}%).")
            print("This may indicate a bug in the implementation.")
            sys.exit(1)

import math
import random
import statistics
import time
from typing import Dict, List, Optional, Tuple

from ai_agents.neuroevolution.neat.genome import Genome
from training.components.archive import BehaviorArchive
from training.components.novelty import compute_population_novelty
from training.components.selection import compute_selection_score
from training.config.neat import NEATConfig
from training.config.novelty import NoveltyConfig
from training.methods.neat.innovation import InnovationTracker
from training.methods.neat.species import Species


class NEATDriver:
    """
    NEAT population manager: speciation, crossover, mutation, and reproduction.
    """
    def __init__(self, input_size: int, output_size: int = 3, novelty_config: Optional[NoveltyConfig] = None):
        self.input_ids = list(range(input_size))
        self.bias_id = input_size
        self.output_ids = list(range(input_size + 1, input_size + 1 + output_size))
        start_node_id = self.output_ids[-1] + 1 if self.output_ids else self.bias_id + 1

        self.innovation_tracker = InnovationTracker(start_innovation=0, start_node_id=start_node_id)
        self.population_size = NEATConfig.POPULATION_SIZE
        self._species_id_counter = 0
        self.compatibility_threshold = float(NEATConfig.COMPATIBILITY_THRESHOLD)

        self.population = [
            Genome.create_minimal(
                self.input_ids,
                self.output_ids,
                self.bias_id,
                self.innovation_tracker,
                weight_range=NEATConfig.INITIAL_WEIGHT_RANGE
            )
            for _ in range(self.population_size)
        ]

        self.species: List[Species] = []
        self._speciate(self.population)
        self._species_id_counter = len(self.species)

        self.novelty_config = novelty_config or NoveltyConfig()
        self.behavior_archive = BehaviorArchive(
            max_size=self.novelty_config.archive_max_size,
            novelty_threshold=self.novelty_config.archive_novelty_threshold,
            k_nearest=self.novelty_config.k_nearest
        )

        self.last_evolution_stats: Dict[str, float] = {}
        self.last_evolution_duration = 0.0
        self.last_generation_new_innovations: Optional[set] = None

    def evolve(self, fitnesses: List[float], per_agent_metrics: Optional[List[Dict]] = None) -> None:
        start_time = time.time()

        fitness_map = {id(genome): fitnesses[i] for i, genome in enumerate(self.population)}
        effective_fitnesses = list(fitnesses)

        novelty_scores = [0.0 for _ in fitnesses]
        diversity_scores = [0.0 for _ in fitnesses]

        if per_agent_metrics is not None and (NEATConfig.ENABLE_NOVELTY or NEATConfig.ENABLE_DIVERSITY):
            behavior_vectors = [m.get('behavior_vector', [0.0] * 11) for m in per_agent_metrics]
            diversity_scores = [m.get('reward_diversity', 0.0) for m in per_agent_metrics]
            if NEATConfig.ENABLE_NOVELTY:
                novelty_scores = compute_population_novelty(
                    behavior_vectors,
                    self.behavior_archive.get_behaviors(),
                    self.novelty_config.k_nearest
                )
                self.behavior_archive.add_batch(behavior_vectors, novelty_scores)

            effective_fitnesses = [
                compute_selection_score(
                    fitnesses[i],
                    novelty_scores[i],
                    diversity_scores[i],
                    self.novelty_config
                )
                for i in range(len(fitnesses))
            ]

        effective_fitness_map = {id(genome): effective_fitnesses[i] for i, genome in enumerate(self.population)}

        species_list, compat_distances = self._speciate(self.population)
        species_stats = self._species_size_stats(species_list)

        adjusted_fitness: Dict[int, float] = {}
        for species in species_list:
            size = max(1, len(species.members))
            for genome in species.members:
                adjusted_fitness[id(genome)] = effective_fitness_map[id(genome)] / size

        pruned_species, pruned_count = self._prune_stagnant_species(species_list, fitness_map)
        species_list = pruned_species

        offspring_counts = self._allocate_offspring(species_list, adjusted_fitness)

        mutation_counts = {
            "add_node": 0,
            "add_connection": 0,
            "weight_mutation": 0,
            "crossover": 0
        }
        mutated_genomes = 0
        elite_total = 0
        new_innovations = set()

        new_population: List[Genome] = []
        for species in species_list:
            count = offspring_counts.get(species.species_id, 0)
            if count <= 0:
                continue

            members = species.members
            sorted_members = sorted(members, key=lambda g: fitness_map[id(g)], reverse=True)
            elite_count = min(NEATConfig.ELITISM_PER_SPECIES, len(sorted_members), count)
            elite_total += elite_count
            for i in range(elite_count):
                new_population.append(sorted_members[i].copy())

            remaining = count - elite_count
            for _ in range(remaining):
                parent1 = self._select_parent(members, adjusted_fitness)
                child = None
                if random.random() < NEATConfig.CROSSOVER_PROB and len(members) > 1:
                    parent2 = self._select_parent(members, adjusted_fitness)
                    child = Genome.crossover(
                        parent1,
                        parent2,
                        fitness_map[id(parent1)],
                        fitness_map[id(parent2)],
                        NEATConfig.INHERIT_DISABLED_PROB
                    )
                    mutation_counts["crossover"] += 1
                else:
                    child = parent1.copy()

                self._mutate_genome(child, mutation_counts, new_innovations)
                mutated_genomes += 1
                new_population.append(child)

        while len(new_population) < self.population_size:
            genome = random.choice(self.population).copy()
            self._mutate_genome(genome, mutation_counts, new_innovations)
            mutated_genomes += 1
            new_population.append(genome)

        new_population = new_population[:self.population_size]

        best_index = fitnesses.index(max(fitnesses)) if fitnesses else 0
        best_genome = self.population[best_index] if self.population else None

        avg_nodes = sum(genome.num_nodes() for genome in self.population) / len(self.population)
        avg_connections = sum(genome.num_enabled_connections() for genome in self.population) / len(self.population)

        survival_rate = self._compute_innovation_survival_rate()
        self.last_generation_new_innovations = new_innovations

        compat_stats = self._compatibility_stats(compat_distances)

        self.last_evolution_stats = {
            "species_count": len(species_list),
            "species_min_size": species_stats.get("min", 0),
            "species_max_size": species_stats.get("max", 0),
            "species_median_size": species_stats.get("median", 0),
            "species_pruned": pruned_count,
            "avg_nodes": avg_nodes,
            "avg_connections": avg_connections,
            "best_nodes": best_genome.num_nodes() if best_genome else 0,
            "best_connections": best_genome.num_enabled_connections() if best_genome else 0,
            "compatibility_threshold": self.compatibility_threshold,
            "compatibility_mean": compat_stats.get("mean", 0.0),
            "compatibility_p10": compat_stats.get("p10", 0.0),
            "compatibility_p90": compat_stats.get("p90", 0.0),
            "add_node_events": mutation_counts["add_node"],
            "add_connection_events": mutation_counts["add_connection"],
            "weight_mutation_events": mutation_counts["weight_mutation"],
            "crossover_events": mutation_counts["crossover"],
            "innovation_survival_rate": survival_rate if survival_rate is not None else 0.0,
            "avg_novelty": sum(novelty_scores) / len(novelty_scores) if novelty_scores else 0.0,
            "avg_diversity": sum(diversity_scores) / len(diversity_scores) if diversity_scores else 0.0,
            "archive_size": self.behavior_archive.size(),
            "elite_count": elite_total,
            "mutation_events": mutated_genomes
        }

        self._adapt_compatibility_threshold(len(species_list))

        self.population = new_population
        self.species, _ = self._speciate(self.population)

        self.last_evolution_duration = time.time() - start_time

    def _mutate_genome(self, genome: Genome, counters: Dict[str, int], new_innovations: set) -> None:
        if NEATConfig.MAX_NODES is None or genome.num_nodes() < NEATConfig.MAX_NODES:
            if random.random() < NEATConfig.ADD_NODE_PROB:
                result = genome.mutate_add_node(self.innovation_tracker)
                if result is not None:
                    _, innov1, innov2 = result
                    new_innovations.update([innov1, innov2])
                    counters["add_node"] += 1

        if NEATConfig.MAX_CONNECTIONS is None or genome.num_connections() < NEATConfig.MAX_CONNECTIONS:
            if random.random() < NEATConfig.ADD_CONNECTION_PROB:
                innov = genome.mutate_add_connection(
                    self.innovation_tracker,
                    weight_range=NEATConfig.INITIAL_WEIGHT_RANGE
                )
                if innov is not None:
                    new_innovations.add(innov)
                    counters["add_connection"] += 1

        mutated = genome.mutate_weights(NEATConfig.WEIGHT_MUTATION_PROB, NEATConfig.WEIGHT_MUTATION_SIGMA)
        counters["weight_mutation"] += mutated

    def _select_parent(self, members: List[Genome], adjusted_fitness: Dict[int, float]) -> Genome:
        total = sum(max(0.0, adjusted_fitness[id(genome)]) for genome in members)
        if total <= 0:
            return random.choice(members)
        pick = random.uniform(0.0, total)
        running = 0.0
        for genome in members:
            running += max(0.0, adjusted_fitness[id(genome)])
            if running >= pick:
                return genome
        return members[-1]

    def _speciate(self, population: List[Genome]) -> Tuple[List[Species], List[float]]:
        for species in self.species:
            species.reset(species.representative)

        species_list = [s for s in self.species]
        distances: List[float] = []

        for genome in population:
            assigned = False
            for species in species_list:
                distance = Genome.compatibility_distance(
                    genome,
                    species.representative,
                    NEATConfig.C1,
                    NEATConfig.C2,
                    NEATConfig.C3
                )
                distances.append(distance)
                if distance < self.compatibility_threshold:
                    species.add(genome)
                    assigned = True
                    break
            if not assigned:
                species_id = self._next_species_id()
                new_species = Species(species_id, genome)
                new_species.add(genome)
                species_list.append(new_species)

        species_list = [s for s in species_list if s.members]
        for species in species_list:
            species.representative = random.choice(species.members)
        self.species = species_list
        return species_list, distances

    def _adapt_compatibility_threshold(self, species_count: int) -> None:
        if not NEATConfig.ADAPT_COMPATIBILITY_THRESHOLD:
            return
        target = int(NEATConfig.TARGET_SPECIES)
        step = float(NEATConfig.COMPATIBILITY_ADJUST_STEP)
        if species_count < target:
            self.compatibility_threshold -= step
        elif species_count > target:
            self.compatibility_threshold += step
        self.compatibility_threshold = max(float(NEATConfig.COMPATIBILITY_MIN), self.compatibility_threshold)
        self.compatibility_threshold = min(float(NEATConfig.COMPATIBILITY_MAX), self.compatibility_threshold)

    def _next_species_id(self) -> int:
        species_id = self._species_id_counter
        self._species_id_counter += 1
        return species_id

    def _prune_stagnant_species(self, species_list: List[Species], fitness_map: Dict[int, float]) -> Tuple[List[Species], int]:
        pruned = []
        for species in species_list:
            best = max(fitness_map[id(genome)] for genome in species.members)
            if best > species.best_fitness:
                species.best_fitness = best
                species.stagnation = 0
            else:
                species.stagnation += 1
            pruned.append(species)

        candidates = [s for s in pruned if s.stagnation < NEATConfig.SPECIES_STAGNATION]
        if not candidates:
            best_species = max(pruned, key=lambda s: s.best_fitness)
            return [best_species], len(pruned) - 1

        pruned_count = len(pruned) - len(candidates)
        return candidates, pruned_count

    def _allocate_offspring(self, species_list: List[Species], adjusted_fitness: Dict[int, float]) -> Dict[int, int]:
        species_fitness = {}
        total = 0.0
        for species in species_list:
            score = sum(adjusted_fitness[id(genome)] for genome in species.members)
            species_fitness[species.species_id] = score
            total += score

        if total <= 0.0:
            base = self.population_size // max(1, len(species_list))
            counts = {s.species_id: base for s in species_list}
            remainder = self.population_size - base * len(species_list)
            for species in species_list:
                if remainder <= 0:
                    break
                counts[species.species_id] += 1
                remainder -= 1
            return counts

        expected = {}
        for species in species_list:
            expected_count = (species_fitness[species.species_id] / total) * self.population_size
            expected[species.species_id] = expected_count

        counts = {sid: int(math.floor(val)) for sid, val in expected.items()}
        remainder = self.population_size - sum(counts.values())
        if remainder > 0:
            fractions = sorted(
                expected.items(),
                key=lambda item: item[1] - math.floor(item[1]),
                reverse=True
            )
            for sid, _ in fractions:
                if remainder <= 0:
                    break
                counts[sid] += 1
                remainder -= 1
        return counts

    def _species_size_stats(self, species_list: List[Species]) -> Dict[str, float]:
        if not species_list:
            return {"min": 0, "max": 0, "median": 0}
        sizes = sorted(len(s.members) for s in species_list)
        return {
            "min": sizes[0],
            "max": sizes[-1],
            "median": statistics.median(sizes)
        }

    def _compatibility_stats(self, distances: List[float]) -> Dict[str, float]:
        if not distances:
            return {"mean": 0.0, "p10": 0.0, "p90": 0.0}
        distances_sorted = sorted(distances)
        n = len(distances_sorted)
        p10 = distances_sorted[int(0.1 * (n - 1))]
        p90 = distances_sorted[int(0.9 * (n - 1))]
        return {
            "mean": sum(distances_sorted) / n,
            "p10": p10,
            "p90": p90
        }

    def _compute_innovation_survival_rate(self) -> Optional[float]:
        if not self.last_generation_new_innovations:
            return None
        if not self.population:
            return None
        current_innovations = set()
        for genome in self.population:
            current_innovations.update(genome.connections.keys())
        survived = self.last_generation_new_innovations.intersection(current_innovations)
        return len(survived) / max(1, len(self.last_generation_new_innovations))

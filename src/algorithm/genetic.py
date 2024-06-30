import random
import copy
import time
from builder.timetable import TimetableBuilder

class GeneticTimetable(TimetableBuilder):
    """
    Class that builds timetable using genetic algorithm.

    ### Args:
    - rooms (list): List of `Room` objects.
    - courses (list): List of `CourseClass` objects.
    - timeslots (list): List of `Timeslot` objects.
    - population_size (int): Size of the population.
    - num_generations (int): Number of generations.

    ### Attributes:
    - rooms (list): List of `Room` objects.
    - courses (list): List of `CourseClass` objects.
    - timeslots (list): List of `Timeslot` objects.
    - population_size (int): Size of the population.
    - num_generations (int): Number of generations.
    """
    def __init__(self, rooms: list, courses: list, timeslots: list, population_size: int, num_generations: int):
        super().__init__(rooms, courses, timeslots)
        self.population_size = population_size
        self.num_generations = num_generations

    def perform_crossover(self, parent_1: dict, parent_2: dict) -> dict:
        """
        Perform crossover between two timetables. This will return an offspring as a new timetable
        and be used for the next generation.
        """
        offspring = {}
        for course in self.courses:
            if random.random() < 0.5:
                offspring[course] = copy.deepcopy(parent_1[course])
            else:
                offspring[course] = copy.deepcopy(parent_2[course])
        return offspring
    
    def perform_mutation(self, timetable: dict) -> dict:
        """
        Get a mutated version of the timetable (solution). This mutated version is based
        on probability (20%) of each course being mutated.
        """
        mutated_solution = copy.deepcopy(timetable)
        course = random.choice(self.courses)
        mutated_solution[course]['room'] = random.choice(self.rooms)
        mutated_solution[course]['timeslot'] = random.choice(self.timeslots)
        return mutated_solution
    
    def run(self, *args, **kwargs) -> tuple[dict, int]:
        print("----------------------------GENETIC ALGORITHM----------------------------")
        start_time = time.time()
        population = [copy.deepcopy(self.timetable) for _ in range(self.population_size)]
        counter = 0

        while counter < self.num_generations:
            checkpoint_time = time.time()

            # Break immediately if the current population has a solution with 0 conflicts.
            if (self.evaluate(min(population, key=lambda timetable: self.evaluate(timetable, *args, **kwargs)), *args, **kwargs) == 0
                or checkpoint_time - start_time > 180): break

            # Calculate the fitness score of each solution (Timetable) in the population.
            fitness_scores = [self.evaluate(timetable, *args, **kwargs) for timetable in population]
            sorted_fitness_scores = sorted(fitness_scores)

            # Select parents to perform crossover.
            parent_1 = population[fitness_scores.index(sorted_fitness_scores[0])]
            parent_2 = population[fitness_scores.index(sorted_fitness_scores[1])]

            # Perform crossover and mutation for new population.
            new_population = [self.perform_crossover(parent_1, parent_2) for _ in range(self.population_size)]
            new_population = [self.perform_mutation(i) if random.random() < 0.2 else i for i in new_population]
            population = new_population
            counter += 1
        
        time_taken = time.time() - start_time
        if time_taken > 180: print('GENETIC ALGORITHM exceeds 3 mins, stopping...')
        if counter == self.num_generations: print("GENETIC ALGORITHM iterations ended.")
        print("Time taken (Genetic Algorithm):", time_taken, "seconds.")
        best_solution = min(population, key=lambda timetable: self.evaluate(timetable, *args, **kwargs))
        best_score = self.evaluate(best_solution, *args, **kwargs)
        print(best_solution, '=> Score:', best_score)
        return best_solution, best_score
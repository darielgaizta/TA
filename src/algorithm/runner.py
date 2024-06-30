from . import genetic, tabu_search

class Runner:
    """Class that runs algorithms."""
    
    @staticmethod
    def run_genetic(rooms, courses, timeslots, population_size, num_generations, *args, **kwargs):
        timetable = genetic.GeneticTimetable(
            rooms=rooms,
            courses=courses,
            timeslots=timeslots,
            population_size=population_size,
            num_generations=num_generations)
        return timetable.run(*args, **kwargs)
    
    @staticmethod
    def run_tabu_search(rooms, courses, timeslots, tabu_list_size, max_iterations, *args, **kwargs):
        timetable = tabu_search.TabuSearchTimetable(
            rooms=rooms,
            courses=courses,
            timeslots=timeslots,
            tabu_list_size=tabu_list_size,
            max_iterations=max_iterations)
        return timetable.run(*args, **kwargs)
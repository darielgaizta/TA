import time
import copy
from builder.timetable import TimetableBuilder

class TabuSearchTimetable(TimetableBuilder):
    """
    Class that builds timetable using tabu search.

    ### Args:
    - rooms (list): List of `Room` objects.
    - courses (list): List of `CourseClass` objects.
    - timeslots (list): List of `Timeslot` objects.
    - tabu_list_size (int): tabu tenure
    - max_iterations (int): number of iterations.

    ### Attributes:
    - rooms (list): List of `Room` objects.
    - courses (list): List of `CourseClass` objects.
    - timeslots (list): List of `Timeslot` objects.
    - tabu_list_size (int): tabu tenure
    - max_iterations (int): number of iterations.
    """

    def __init__(self, rooms, courses, timeslots, tabu_list_size, max_iterations):
        super().__init__(rooms, courses, timeslots)
        self.tabu_list = []
        self.tabu_list_size = tabu_list_size
        self.max_iterations = max_iterations
    
    def get_neighbors(self, timetable: dict):
        """Search all neighbors of current solution."""
        neighbors = []
        for course in timetable.keys():
            for room in self.rooms:
                for timeslot in self.timeslots:
                    neighbor = copy.deepcopy(timetable)
                    neighbor[course]['room'] = room
                    neighbor[course]['timeslot'] = timeslot
                    neighbors.append(neighbor)
        return neighbors
        
    def is_tabu(self, timetable: dict) -> bool:
        """Check if current timetable (solution) is (in) tabu (list)."""
        return timetable in self.tabu_list
    
    def update_tabu(self, timetable: dict, tabu_tenure: int):
        self.tabu_list.append(timetable)
        if len(self.tabu_list) > tabu_tenure: self.tabu_list.pop(0)
    
    def run(self, *args, **kwargs) -> tuple[dict, int]:
        print("----------------------------TABU SEARCH----------------------------")
        start_time = time.time()
        current_solution = copy.deepcopy(self.timetable)
        current_score = self.evaluate(current_solution, *args, **kwargs)

        best_solution, best_score = current_solution, current_score
        counter = 0

        while counter < self.max_iterations:
            checkpoint_time = time.time()
            if best_score == 0 or checkpoint_time - start_time > 300:
                break

            best_neighbor = None
            best_neighbor_score = float('inf')
            neighbors = self.get_neighbors(current_solution)

            for neighbor in neighbors:
                if not self.is_tabu(neighbor):
                    neighbor_score = self.evaluate(neighbor, *args, **kwargs)
                    if neighbor_score < best_neighbor_score:
                        best_neighbor = neighbor
                        best_neighbor_score = neighbor_score
            
            if best_neighbor != None:
                current_solution = best_neighbor
                current_score = best_neighbor_score
                if current_score < best_score:
                    best_solution = current_solution
                    best_score = current_score
            
            self.update_tabu(current_solution, self.tabu_list_size)
            counter += 1

        time_taken = time.time() - start_time
        if time_taken > 300: print('TABU SEARCH exceeds 5 mins, stopping...')
        if counter == self.max_iterations: print("TABU SEARCH iterations ended.")
        print("Time taken (Tabu Search):", time_taken, "seconds.")
        print(best_solution, '=> Score:', best_score)
        return best_solution, best_score
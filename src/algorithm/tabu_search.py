import time
import copy
from builder.timetable import TimetableBuilder

class TabuSearchTimetable(TimetableBuilder):
    def __init__(self, rooms, courses, timeslots):
        super().__init__(rooms, courses, timeslots)
        self.tabu_list = []
    
    def get_neighbors(self, timetable: dict):
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
        return timetable in self.tabu_list
    
    def update_tabu(self, timetable: dict, tabu_tenure: int):
        self.tabu_list.append(timetable)
        if len(self.tabu_list) > tabu_tenure: self.tabu_list.pop(0)
    
    def run(self, tabu_list_size: int, max_iterations: int) -> tuple[dict, int]:
        print("----------------------------TABU SEARCH----------------------------")
        start_time = time.time()
        current_solution = copy.deepcopy(self.timetable)
        current_score = self.evaluate(current_solution)

        best_solution, best_score = current_solution, current_score
        counter = 0

        while counter < max_iterations:
            checkpoint_time = time.time()
            if best_score == 0 or checkpoint_time - start_time > 180:
                break

            best_neighbor = None
            best_neighbor_score = float('inf')
            neighbors = self.get_neighbors(current_solution)

            for neighbor in neighbors:
                if not self.is_tabu(neighbor):
                    neighbor_score = self.evaluate(neighbor)
                    if neighbor_score < best_neighbor_score:
                        best_neighbor = neighbor
                        best_neighbor_score = neighbor_score
            
            if best_neighbor != None:
                current_solution = best_neighbor
                current_score = best_neighbor_score
                if current_score < best_score:
                    best_solution = current_solution
                    best_score = current_score
            
            self.update_tabu(current_solution, tabu_list_size)
            counter += 1

        if counter == max_iterations: print("TABU SEARCH timed out.")
        print("Time taken (Tabu Search):", time.time() - start_time, "seconds.")
        return best_solution, best_score
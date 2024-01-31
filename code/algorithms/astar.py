from queue import PriorityQueue
import copy
from ..game.rush_hour import RushHour, Vehicle
from bfs import RushHourBFS
import pandas as pd
import time



class RushHourAStar:
    """
    In this method we initialize the variables needed later.
    """
 
    def __init__(self, initial_state):
        # Initial state and number of states
        self.initial_state = initial_state
        self.num_of_states = 0
        
        
    def a_star(self):
        """
        The AStar algorithm is implemented, it returns the time, number of states and the goal state.
        """
        # Print text and show board
        print("Starting A*...")
        print("Initial Board:")
        self.initial_state.display_board()
        
        # Save visited states
        visited = set()
        
        # Keep track of time
        start_time = time.time()
        
        # Queue to manage AStar frontier
        priority_queue = PriorityQueue()
        
        # Initial state with heuristic added to queue
        priority_queue.put((self.heuristics(self.initial_state), self.initial_state))
        visited.add(self.initial_state.get_state_hashable())
        
        # Dictionary to store the predecessor of each state
        predecessors = {self.initial_state.get_state_hashable(): None}
        
        # Dictionary to store g scores 
        g_scores = {self.initial_state.get_state_hashable(): 0}

        while not priority_queue.empty():
            
            # Dequeue the next state
            current_state = priority_queue.get()[1]

            # Check if current state is the goal state
            if self.check_win(current_state):
                print("Winning state found!")
                print(time.time() - start_time)
                print(self.num_of_states)
                current_state.display_board()
                
                # Return the path to the solution
                return self.backtrack_path(current_state, predecessors)
            
            # Generate and enqueue all possible next states from the current state
            for next_state in self.generate_next_states(current_state):
                state_hash = next_state.get_state_hashable()
                
                # Get g scores
                tentative_g_score = g_scores[current_state.get_state_hashable()] + 1
                
                if state_hash not in visited or tentative_g_score < g_scores[state_hash]:
                    visited.add(state_hash)
                    g_scores[state_hash] = tentative_g_score
                    priority_queue.put((tentative_g_score + self.heuristics(next_state), next_state))
                    predecessors[state_hash] = current_state
                    self.num_of_states += 1 

        print("No solution found.")
        return None

    
    def heuristics(self, state):
        """
        Heuristic function: Number of cars blocking the red car, 
        total distance from blocking vehicles to red car and red car's distance to  exit.

        Parameters:
        state (RushHour): The state to evaluate.

        Returns:
        int: Heuristic value.
        """
        red_car = state.vehicles.get('X')

        # Calculate the red car's distance to exit
        distance_to_exit = state.board_size - (red_car.col + red_car.length)
        
        # Check for deadlock patterns
        deadlock_penalty = self.check_deadlock_patterns(state)
        
        # Get number of blocking cars in row and initialize weight
        blocking_cars_in_row = sum(
        1 for vehicle in state.vehicles.values() if vehicle.row == red_car.row and vehicle.col > red_car.col + vehicle.length)
        weight = 100 # This factor can be changed
        
        # Dynamic component, increases as number of states increaases
        dynamic_component = self.num_of_states * 0.0001 # This factor can be changed
        
        # Indirect blocking cars
        indirect_blocking_cars = self.indirect_blocking_cars_heuristic(state)

        return (distance_to_exit + deadlock_penalty + blocking_cars_in_row * weight + indirect_blocking_cars + dynamic_component)
    
    
    def indirect_blocking_cars_heuristic(self, state):
        """
        Calculate the number of cars that are indirectly blocking the
        red car's path to the exit.

        Parameters:
        state (RushHour): The current state of the game.

        Returns:
        int: The number of indirectly blocking cars."""
        red_car = state.vehicles.get('X')
        if not red_car or red_car.orientation != 'H':
            return float('inf')

        indirect_blocking_cars = 0
        red_car_end_col = red_car.col + red_car.length

        # Check each column between the red car and the exit
        for col in range(red_car_end_col, state.board_size):
            if state.board[red_car.row][col] != '.':
                blocking_vehicle = state.vehicles[state.board[red_car.row][col]]
                if blocking_vehicle.orientation == 'V':
                    if self.is_vehicle_blocked(blocking_vehicle, state):
                        indirect_blocking_cars += 1
        return indirect_blocking_cars

    
    def is_vehicle_blocked(self, vehicle, state):
        """
        Check if a vehicle is blocked on both sides.
        
        Parameters:
        vehicle (Vehicle): The vehicle to check.
        state (RushHour): The current state of the game.

        Returns:
        bool: True if the vehicle is blocked on both sides, False otherwise.
        """
        if vehicle.orientation == 'H':
            return not state.is_move_valid(vehicle, vehicle.row, vehicle.col - 1) and \
                   not state.is_move_valid(vehicle, vehicle.row, vehicle.col + vehicle.length)
        else:
            return not state.is_move_valid(vehicle, vehicle.row - 1, vehicle.col) and \
                   not state.is_move_valid(vehicle, vehicle.row + vehicle.length, vehicle.col)


    def check_deadlock_patterns(self, state):
        """
        Check for deadlock patterns on the game board.

        Parameters:
        state (RushHour): The state to evaluate.

        Returns:
        int: Deadlock penalty (negative value if a deadlock pattern is detected).
        """
        deadlock_penalty = 0

        # Check for completely blocked rows and columns
        for row in range(state.board_size):
            if all(cell != '.' for cell in state.board[row]):
                deadlock_penalty -= 1  # Penalize, this factor can be changed

        for col in range(state.board_size):
            if all(row[col] != '.' for row in state.board):
                deadlock_penalty -= 1  # Penalize, this factor can be changed

        return deadlock_penalty
    

    
    def check_win(self, state):
        """
        Check if the given state is a winning state.

        Parameters:
        state (RushHour): The state to check.

        Returns:
        bool: True if it's a winning state, False otherwise.
        """

        red_car = state.vehicles.get('X')
        if not red_car:
            return False  # Red car not found in the state

        # Check if red car is horizontal and at the rightmost position
        if red_car.orientation == 'H' and red_car.col + red_car.length == state.board_size:
            return True

        return False
    
    
    def generate_next_states(self, current_state):
        """
        Generate all possible next states from the current state.

        Parameters:
        current_state (State): The current state of the game.

        Returns:
        list of State: A list of all possible next states.
        """

        # List of states
        next_states = []


        for vehicle_name, vehicle in current_state.vehicles.items():

            # Try moving each vehicle one step forward and backward
            for distance in [1, -1]:

                # Calculate new position
                new_row, new_col = self.calculate_new_position(vehicle, distance)

                if current_state.is_move_valid(vehicle, new_row, new_col):
                    # Make a copy of the current state and apply the move
                    new_state = clone_rush_hour_state(current_state)
                    new_state.move_vehicle(vehicle_name, distance)

                    next_states.append(new_state)

        if not next_states:
            print("No new states generated")

        return next_states


    def calculate_new_position(self, vehicle, distance):
        if vehicle.orientation == 'H':
            return vehicle.row, vehicle.col + distance
        else:        
            return vehicle.row + distance, vehicle.col



    def backtrack_path(self, goal_state, predecessors):
        """
        Backtrack from the goal state to the initial state to find the solution path.

        Parameters:
        goal_state (State): The goal state from which to start backtracking.

        Returns:
        list of State: The path from the initial state to the goal state.
        """
        # Store the path
        path = []
        current_state = goal_state
        while current_state:
            path.append(current_state)
            current_state = predecessors.get(current_state.get_state_hashable())
        # Reverse the path to start from the initial state
        return path[::-1]
    
    
def read_all_vehicles_bfs(file_path):
    """
    In this method we read the input-file and create the variables
    for the vehicles such as name, orientation, length, starting column
    and starting row. Furthermore we add the vehicle instance to the dictionary.
    """
    rush_hour_file = pd.read_csv(file_path)
    vehicles = {}

    # Loops through the csv file and assigns the values to variables
    for car in rush_hour_file.values:
        name = car[0]
        orientation = car[1]

        # We substract 1 because of indexing
        start_col = car[2] - 1
        start_row = car[3] - 1
        length = car[4]

        # Adds the vehicle to dictionary and places it on the board
        vehicle = (Vehicle(name, length, orientation, start_row, start_col))
        vehicles[name] = vehicle

    return vehicles

def clone_rush_hour_state(rush_hour_state):
    """
    Create a deep copy of the given RushHour game state.

    Parameters:
    rush_hour_state (RushHour): The RushHour instance to clone.

    Returns:
    RushHour: A new RushHour object with the same state as the input state.
    """
    # Create a new RushHour instance without starting the game
    cloned_game = RushHour(start_game=False, board_size=rush_hour_state.board_size, board=[row[:] for row in rush_hour_state.board])

    # Deep copy each vehicle
    cloned_game.vehicles = {}
    for name, vehicle in rush_hour_state.vehicles.items():
        cloned_vehicle = Vehicle(vehicle.name, vehicle.length, vehicle.orientation, vehicle.row, vehicle.col)
        cloned_game.vehicles[name] = cloned_vehicle

    return cloned_game
    
    
    
if __name__ == "__main__":
    rush_hour_game = RushHour()
    solver = RushHourAStar(rush_hour_game)
    solution_path = solver.a_star()
    if solution_path:
        print(f"Solution found in {len(solution_path) - 1} moves!")
    else:
        print("No solution found.")
        
        
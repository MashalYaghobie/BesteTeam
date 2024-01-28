from queue import PriorityQueue
import copy
from rush_hour import RushHour, Vehicle
import time


class RushHourBFS:
    def __init__(self, initial_state, distance_heuristic=False, direct_blocking_heuristic=False, indirect_blocking_heuristic=False, distance_weight=1, direct_blocking_weight=1, indirect_blocking_weight=1):

        self.initial_state = initial_state

        # heuristic settings
        self.distance_heuristic = distance_heuristic
        self.direct_blocking_heuristic = direct_blocking_heuristic
        self.indirect_blocking_heuristic = indirect_blocking_heuristic
        self.distance_weight = distance_weight
        self.direct_blocking_weight = direct_blocking_weight
        self.indirect_blocking_weight = indirect_blocking_weight

        # print(f"Initial state: {self.initial_state.get_state_hashable()}")
        #
        # print("Initial Board:")
        # self.initial_state.display_board()

    def bfs(self):
        """
        Perform the breadth-first search algorithm to find a solution to the Rush Hour game.
        Uses heuristic to prioritise certain states

        Returns:
        list of State: The path from the initial state to the goal state, if a solution is found.
        """

        print("Starting BFS...")
        print("Initial Board:")
        self.initial_state.display_board()

        # save visited states
        visited = set()
        # priority queue for heuristics
        queue = PriorityQueue()
        
        initial_g = 0  # cost from initial state to current state
        
        initial_heuristic = self.combined_heuristics(self.initial_state)
        
        initial_f = initial_g + initial_heuristic
        
        # add the initial state to the queue
        #queue.put((initial_heuristic, self.initial_state))
        queue.put((initial_f, self.initial_state, initial_g))
        
        
        visited.add(self.initial_state.get_state_hashable())

        # Dictionary to store the predecessor of each state
        predecessors = {self.initial_state.get_state_hashable(): (None, 0)}

        # debugging
        print("Starting BFS...")

        while not queue.empty():
            # dequeue the next state (with the lowest heuristic value)
            _, current_state, g_value = queue.get()

            # debugging
            #print(f"Current state: {current_state}")

            # check if current state is the goal state
            if self.check_win(current_state):

                # debugging
                print("Winning state found!")
                current_state.display_board()

                # return the path to the solution
                solution_path = self.backtrack_path(current_state, predecessors)

                # process the solution path to get the sequence of moves
                moves = self.calculate_moves(solution_path)

                return moves

            # generate and enqueue all possible next states from the current state
            for next_state in self.generate_next_states(current_state):
                state_hash = next_state.get_state_hashable()
                if state_hash not in visited:
                    visited.add(state_hash)
                    
                    next_g = g_value + 1
                    
                    # update queue with heuristic value of each state
                    heuristic_value = self.combined_heuristics(next_state)
                    
                    next_f = next_g + heuristic_value
                    
                    queue.put((next_f, next_state, next_g))

                    # Record the predecessor of the next_state
                    predecessors[state_hash] = (current_state, next_g)

        print("No solution found.")
        return None

    def calculate_moves(self, solution_path):
        """
        Calculate the sequence of moves from the solution path.

        Parameters:
        solution_path (list): List of states representing the solution path.

        Returns:
        list: List of moves that lead to the solution.
        """
        moves = []
        for i in range(1, len(solution_path)):
            previous_state = solution_path[i - 1]
            current_state = solution_path[i]
            move = state_to_move(previous_state, current_state)
            if move:
                moves.append(move)
        return moves

    def generate_next_states(self, current_state):
        """
        Generate all possible next states from the current state.

        Parameters:
        current_state (State): The current state of the game.

        Returns:
        list of State: A list of all possible next states.
        """
        #print(f"Generating next states for: {current_state.get_state_hashable()}")

        # list of states
        next_states = []


        for vehicle_name, vehicle in current_state.vehicles.items():

            #print(f"Trying to move vehicle: {vehicle_name}")

            # try moving each vehicle one step forward and backward
            for distance in [1, -1]:

                # calculate new position
                new_row, new_col = self.calculate_new_position(vehicle, distance)

                #print(f"Attempting to move {vehicle_name} to Row: {new_row}, Col: {new_col}")

                if current_state.is_move_valid(vehicle, new_row, new_col):
                    #print("Move is valid, generating new state")
                    # make a copy of the current state and apply the move
                    new_state = clone_rush_hour_state(current_state)
                    new_state.move_vehicle(vehicle_name, distance)

                    next_states.append(new_state)


                    # debugging
                    #print(f"Generated new state by moving {vehicle_name} {distance} step(s):")
                    #new_state.display_board()
                #else:
                    #print(f"Move not valid for vehicle {vehicle_name}")

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
        # store the path
        path = []
        current_state = goal_state
        while current_state:
            path.append(current_state)
            current_state, _ = predecessors.get(current_state.get_state_hashable(), (None, None))
        # reverse the path to start from the initial state
        return path[::-1]

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

    def distance_to_exit_heuristic(self, state):
        """
        Calculate the distance from the red car to the exit.

        Parameters:
        state (RushHour): The current state of the game.

        Returns:
        int: The number of steps the red car needs to reach the exit.
        """
        red_car = state.vehicles.get('X')
        # in case the red car is not found
        if not red_car:
            return float('inf')

        distance_to_exit = state.board_size - (red_car.col + red_car.length)
        return distance_to_exit

    def direct_blocking_cars_heuristic(self, state):
        """
        Calculate the number of cars directly blocking the red car's path to the exit.

        Parameters:
        state (RushHour): The current state of the game.

        Returns:
        int: The number of cars directly blocking the red car.
        """
        red_car = state.vehicles.get('X')
        # in case the red car is not find or it's orientation is not horizontal
        if not red_car or red_car.orientation != 'H':
            return float('inf')

        blocking_cars = 0
        # find the nose of the red car
        red_car_end_col = red_car.col + red_car.length

        # iterate trough each column between the red car and the exit
        for col in range(red_car_end_col, state.board_size):
            if any(state.board[red_car.row][col] != '.' for row in range(state.board_size)):
                blocking_cars += 1

        return blocking_cars

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

        # check each column between the red car and the exit
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


    def combined_heuristics(self, state):
        """For easy implementation in the bfs method."""
        heuristic_value = 0
        if self.distance_heuristic:
             heuristic_value += self.distance_weight * self.distance_to_exit_heuristic(state)
        if self.direct_blocking_heuristic:
            heuristic_value += self.direct_blocking_weight * self.direct_blocking_cars_heuristic(state)
        if self.indirect_blocking_heuristic:
            heuristic_value += self.indirect_blocking_weight * self.indirect_blocking_cars_heuristic(state)
        return heuristic_value









def state_to_move(previous_state, current_state):
    """
    Convert a state into a move by comparing it with its predecessor.

    Parameters:
    previous_state (RushHour): The previous state of the game.
    current_state (RushHour): The current state of the game.

    Returns:
    tuple: A tuple containing the vehicle name and the distance moved.
    """
    for vehicle_name, current_vehicle in current_state.vehicles.items():
        previous_vehicle = previous_state.vehicles[vehicle_name]
        if current_vehicle.row != previous_vehicle.row:
            # Vertical movement
            distance = current_vehicle.row - previous_vehicle.row
            return (vehicle_name, distance)
        elif current_vehicle.col != previous_vehicle.col:
            # Horizontal movement
            distance = current_vehicle.col - previous_vehicle.col
            return (vehicle_name, distance)

    return None  # No move detected

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
    initial_state = rush_hour_game.get_state_hashable()
    #print(f"Initial state for BFS: {initial_state_hash}")
    solver = RushHourBFS(rush_hour_game, direct_blocking_heuristic=True, indirect_blocking_heuristic=True, indirect_blocking_weight=5)

    start_time = time.time()
    solution_path = solver.bfs()
    end_time = time.time()
    if solution_path:
        print("Solution sequence of moves:")
        for move in solution_path:
            print(move)
        print(f"Solution found in {len(solution_path)} moves!")

        elapsed_time = end_time - start_time
        print(f"Time taken to solve the board: {elapsed_time:.2f} seconds")
    else:
        print("No solution found.")

from queue import Queue
import copy
from rush_hour import RushHour, Vehicle
import time


class RushHourBFS:
    def __init__(self, initial_state):

        self.initial_state = initial_state

        self.states_visited = 0

        # print(f"Initial state: {self.initial_state.get_state_hashable()}")
        #
        # print("Initial Board:")
        # self.initial_state.display_board()

    def bfs(self):
        """
        Perform the breadth-first search algorithm to find a solution to the Rush Hour game.

        Returns:
        list of State: The path from the initial state to the goal state, if a solution is found.
        """

        print("Starting BFS...")
        print("Initial Board:")
        self.initial_state.display_board()

        # save visited states
        visited = set()
        # queue to manage BFS frontier
        queue = Queue()
        # add the initial state to the queue
        queue.put(self.initial_state)
        visited.add(self.initial_state.get_state_hashable())

        # Dictionary to store the predecessor of each state
        predecessors = {self.initial_state.get_state_hashable(): None}

        # debugging
        print("Starting BFS...")

        while not queue.empty():
            # dequeue the next state
            current_state = queue.get()

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

                print(f"Number of states visited: {self.states_visited}")

                return moves

            # generate and enqueue all possible next states from the current state
            for next_state in self.generate_next_states(current_state):
                state_hash = next_state.get_state_hashable()
                if state_hash not in visited:
                    visited.add(state_hash)
                    queue.put(next_state)
                    # Record the predecessor of the next_state
                    predecessors[state_hash] = current_state

                    self.states_visited += 1

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
            current_state = predecessors.get(current_state.get_state_hashable())
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
    initial_state_hash = rush_hour_game.get_state_hashable()
    #print(f"Initial state for BFS: {initial_state_hash}")

    solver = RushHourBFS(rush_hour_game)

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

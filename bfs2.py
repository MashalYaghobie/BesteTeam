from queue import Queue
import copy
from rush_hour import RushHour, Vehicle
import pandas as pd


class RushHourBFS:
    def __init__(self, initial_state):

        self.initial_state = initial_state

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
                return self.backtrack_path(current_state, predecessors)

            # generate and enqueue all possible next states from the current state
            for next_state in self.generate_next_states(current_state):
                state_hash = next_state.get_state_hashable()
                if state_hash not in visited:
                    visited.add(state_hash)
                    queue.put(next_state)

                    # Record the predecessor of the next_state
                    predecessors[state_hash] = current_state



        # debugging
        print("No solution found.")
        return None

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
    #rush_hour_game.start_game()
    initial_state_hash = rush_hour_game.get_state_hashable()
    #print(f"Initial state for BFS: {initial_state_hash}")
    solver = RushHourBFS(rush_hour_game)
    solution_path = solver.bfs()
    if solution_path:
        print(f"Solution found in {len(solution_path) - 1} moves!")
    else:
        print("No solution found.")

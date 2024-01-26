from queue import Queue
import copy
from rush_hour import RushHour, Vehicle
import pandas as pd

class RushHourDFS:
    """
    In this class we will define some methods to create a depth first
    search algorithm that can solve our rush hour problem.
    """

    def __init__(self, initial_state):
        """
        In this method we will define the starting state 
        """
        self.initial_state = initial_state

    def dfs(self):
        """
        In this method we run the depth first search algorithm
        and try to solve our rush hour problem. We will save all of our
        gamestates from the initial to the final board.
        """

        print("Starting the DFS algorithm")
        print("This is the initial board:")
        self.initial_state.display_board()

        # save the visited states in a set
        visited = set()

        # Create a dictionary to store the predecessor for each state
        predecessor_states = {self.initial_state.get_state_hashable(): None}

        # We start DFS recursion from the initial / starting state
        solution_path = self.dfs_recursive(self.initial_state, visited, predecessor_states)

        # Print the number of moves if we found a path
        if solution_path:
            print(f"Solution found in {len(solution_path) - 1} moves!")
        else:
            print("No solution found.")

        # return the paht with our solution
        return solution_path

    def dfs_recursive(self, current_state, visited, predecessor_states):
        """
        In this method we define a recursive method for our depth 
        first search method. This method makes sure that we take a state from
        the game as input and explores all the possible moves untill
        we find a solution or reach a dead end.
        """

        # We add the current state to the states we visited
        visited.add(current_state.get_state_hashable())

        # Check if we have won the game
        if self.check_win(current_state):
            return [current_state]

        # Then we create next states and explore further down the path
        for next_state in self.generate_next_states(current_state):

            # create the next state
            state_hash = next_state.get_state_hashable()

            # check if we have not seen this state before
            if state_hash not in visited:

                # save the state to the list with all previous states
                predecessor_states[state_hash] = current_state

                # we explore further down the path
                solution_path = self.dfs_recursive(next_state, visited, predecessor_states)
                
                # if we have found a solution we return the entire path
                if solution_path:
                    return [current_state] + solution_path

        return None

    def generate_next_states(self, current_state):
        """
        In this method we create the new states from the state
        we are currently on.
        """

        # create an empty list for new / next states
        next_states = []

        # loop thourgh the vehicles
        for vehicle_name, vehicle in current_state.vehicles.items():

            # this distance is a move in a direction
            for distance in [1, -1]:

                # we get the new position for the vehicle
                new_row, new_col = self.calculate_new_position(vehicle, distance)

                # we check if the move is valid
                if current_state.is_move_valid(vehicle, new_row, new_col):

                    # we create the new / next game state
                    new_state = self.clone_rush_hour_state(current_state)

                    # and we move the vehicle and append the new state to the list
                    new_state.move_vehicle(vehicle_name, distance)
                    next_states.append(new_state)

        return next_states

    def calculate_new_position(self, vehicle, distance):
        """
        In this method we calculte the new position for our vehicle
        based on the distance we input.
        """

        # if the vehicle is horizontal oriented
        if vehicle.orientation == 'H':

            # we only move the column placement it is in
            return vehicle.row, vehicle.col + distance

        # if the vehicle is vertical oriented
        else:

            # we only move the row placement it is in
            return vehicle.row + distance, vehicle.col

    def check_win(self, state):
        """
        In this method we check if the new state 
        is a solution to solve the game.
        """

        # get our red car from the vehicles
        red_car = state.vehicles.get('X')

        # make sure we have a red car
        if not red_car:
            return False

        # car must be horizontal oriented and at the most right column for a win
        if red_car.orientation == 'H' and red_car.col + red_car.length == state.board_size:
            return True

        return False

    def clone_rush_hour_state(self, rush_hour_state):
        """
        In this method we create a deep copy using .clone
        for an inputed game state of the rush hour board/game.
        Create a deep copy of the given RushHour game state.
        """

        # create a new rush hour instance without starting the game again
        cloned_game = RushHour(start_game=False, board_size=rush_hour_state.board_size, board=[row[:] for row in rush_hour_state.board])

        # make a deepcopy of each vehicle
        cloned_game.vehicles = {}
        for name, vehicle in rush_hour_state.vehicles.items():
            cloned_vehicle = Vehicle(vehicle.name, vehicle.length, vehicle.orientation, vehicle.row, vehicle.col)
            cloned_game.vehicles[name] = cloned_vehicle

        return cloned_game

if __name__ == "__main__":
    rush_hour_game = RushHour()
    rush_hour_game.start_game()
    initial_state_hash = rush_hour_game.get_state_hashable()

    solver = RushHourDFS(rush_hour_game)
    solution_path = solver.dfs()

    if solution_path:
        print("Initial State:")
        rush_hour_game.display_board()

        print("Final State:")
        solution_path[-1].display_board()

        print(f"Number of moves to solve the board: {len(solution_path) - 1}")
    else:
        print("No solution found.")
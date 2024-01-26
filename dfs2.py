import time
from rush_hour import RushHour, Vehicle

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
        self.visited = set()
        self.solution_path = []

    def depth_first_search(self):
        """
        In this method we run the depth first search algorithm
        and try to solve our rush hour problem. We will save all of our
        gamestates from the initial to the final board.
        """

        # start the timer when we run the algorithm
        start_time = time.time()

        # add the initial state to the visited set
        self.visited.add(self.initial_state.get_state_hashable())

        # create a stack for our iterative depth first search
        stack = [self.initial_state]

        # loop if the stack is not empty
        while stack:

            # get the top from the stack
            current_state = stack.pop()

            # append the top of the stack to the solution path
            self.solution_path.append(current_state)
            
            # stop condition - check if we have won
            if self.check_win(current_state):

                # get out of the loop if we have found a solution
                break

            # create next states
            for next_state in self.generate_next_states(current_state):
                state_hash = next_state.get_state_hashable()

                # check if those states are new states    
                if state_hash not in self.visited:
                    self.visited.add(state_hash)

                    # put the state on the stack
                    stack.append(next_state)

        # print the number of moves if we found a path
        if self.solution_path:
            print(f"Solution found in {len(self.solution_path) - 1} moves!")
        else:
            print("No solution found.")

        # print the time it took to solve
        print(f"Solving time: {time.time() - start_time} seconds")

        # return the paht with our solution
        return self.solution_path

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

    solver = RushHourDFS(rush_hour_game)
    solution_path = solver.depth_first_search()

    if solution_path:
        print("Initial State:")
        rush_hour_game.display_board()

        print("Final State:")
        solution_path[-1].display_board()

        print(f"Number of moves to solve the board: {len(solution_path) - 1}")
    else:
        print("No solution found.")
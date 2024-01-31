from queue import Queue
import copy
from code.game.rush_hour import RushHour, Vehicle
import time


class RushHourBFS:
    """
    In this class we will define methods to perform the breadth first search
    algorithm for our rush hour gameboards.
    """

    def __init__(self, initial_state):
        """
        In this method we define some initial starting variables.
        """

        # we set the initial state
        self.initial_state = initial_state

        # create a counter for the states visited
        self.states_visited = 0


    def bfs(self):
        """
        In this method we perform the breadth-first search algorithm for our
        rush hour case. We will try to find the path from the initial state
        to the solution state, which we will call the solution path.
        """

        print("Starting BFS...")
        print("Initial Board:")
        self.initial_state.display_board()

        # save unique visited states
        visited = set()

        # queue to manage BFS frontier
        queue = Queue()

        # add the initial state to the queue
        queue.put(self.initial_state)

        # and to the visited set
        visited.add(self.initial_state.get_state_hashable())

        # create a dctionary to store the predecessor for each state
        predecessors = {self.initial_state.get_state_hashable(): None}

        # debugging
        print("Starting BFS...")

        # condition to keep on running our algorithm
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

                # print the number of states we visited
                print(f"Number of states visited: {self.states_visited}")

                # return all the moves we have done to get to the solution
                return moves

            # generate and enqueue all possible next states from the current state
            for next_state in self.generate_next_states(current_state):
                state_hash = next_state.get_state_hashable()

                # check if it is a unique state
                if state_hash not in visited:

                    # add it to the visited set
                    visited.add(state_hash)

                    # and put it in the queue
                    queue.put(next_state)

                    # save/record the predecessor of the next_state
                    predecessors[state_hash] = current_state

                    # increase the counter
                    self.states_visited += 1

        print("No solution found.")
        return None

    def calculate_moves(self, solution_path):
        """
        In this method we will calculate the order of the moves done
        to get from our initial state to the solution state. So
        we will find all the moves from our solution path
        """

        # create an empty list for the moves
        moves = []

        # loop through all the states in the solution path
        for i in range(1, len(solution_path)):

            # get the previous state and the current state
            previous_state = solution_path[i - 1]
            current_state = solution_path[i]

            # find the move that has been done and append it to the list
            move = state_to_move(previous_state, current_state)
            if move:
                moves.append(move)

        return moves

    def generate_next_states(self, current_state):
        """
        In this method we will generate all the possible next states from
        the current state we are in.
        """

        # create an empty list for the next states
        next_states = []

        # loop through all vehicles in the gameboards current state
        for vehicle_name, vehicle in current_state.vehicles.items():


            # try to move each unique vehicle one step
            for distance in [1, -1]:

                # calculate the new position for the vehicle
                new_row, new_col = self.calculate_new_position(vehicle, distance)

                # check if this move is possible/valid
                if current_state.is_move_valid(vehicle, new_row, new_col):

                    # make a copy of the current state
                    new_state = clone_rush_hour_state(current_state)

                    # apply the move to the board
                    new_state.move_vehicle(vehicle_name, distance)

                    # append the new state to the list
                    next_states.append(new_state)

        # check if we generated new states
        if not next_states:
            print("No new states generated")

        return next_states


    def calculate_new_position(self, vehicle, distance):
        """
        In this method we will calculate the new position for
        a vehicle based on its orientation.
        """

        # if the vehicle is horizontal oriented
        if vehicle.orientation == 'H':

            # increase the column position by the move distance
            return vehicle.row, vehicle.col + distance

        # if the vehicle is vertical oriented
        else:

            # increase the row position by the move distance
            return vehicle.row + distance, vehicle.col


    def backtrack_path(self, goal_state, predecessors):
        """
        In this method we will backtrack from the solution state/goal state to
        the initial state/starting state to find the solution path.
        """

        # create an empty list for the path
        path = []

        # set that the current state is the goal state
        current_state = goal_state

        while current_state:
            path.append(current_state)

            # get all the predecessor states from the goal state
            current_state = predecessors.get(current_state.get_state_hashable())

        # reverse the path to start from the initial state
        return path[::-1]

    def check_win(self, state):
        """
        In this method we will apply a check to see
        if the game has been won.
        """

        # get the position of the red car
        red_car = state.vehicles.get('X')

        # if there is no red car
        if not red_car:

            # return False, since the car is not in the state
            return False

        # check if red car is horizontal and at winning position
        if red_car.orientation == 'H' and red_car.col + red_car.length == state.board_size:

            # return True, since the game has been won
            return True

        # otherwise return False
        return False

def state_to_move(previous_state, current_state):
    """
    In this method we convert a given state to a move by comparing
    the current state with its previous state.
    """

    # loop through all the vehicles in the gameboards current state
    for vehicle_name, current_vehicle in current_state.vehicles.items():

        # get the previous position of the vehicle
        previous_vehicle = previous_state.vehicles[vehicle_name]

        # check if the vehicle is not in the same position (vertical movement)
        if current_vehicle.row != previous_vehicle.row:

            # get the distance from the move that has been done
            distance = current_vehicle.row - previous_vehicle.row
            return (vehicle_name, distance)

        # check if the vehicle is not in the same position (horizontal movement)
        elif current_vehicle.col != previous_vehicle.col:

            # get the distance from the move that has been done
            distance = current_vehicle.col - previous_vehicle.col
            return (vehicle_name, distance)

    # return None if we have not detected any move
    return None

def clone_rush_hour_state(rush_hour_state):
    """
    In this method we will create a deep copy/clone from
    an inputed game state of the rush hour case.
    """

    # create a cloned rush hour instance without starting the game
    cloned_game = RushHour(start_game=False, board_size=rush_hour_state.board_size, board=[row[:] for row in rush_hour_state.board])

    # make a deep copy of each vehicle
    cloned_game.vehicles = {}
    for name, vehicle in rush_hour_state.vehicles.items():
        cloned_vehicle = Vehicle(vehicle.name, vehicle.length, vehicle.orientation, vehicle.row, vehicle.col)
        cloned_game.vehicles[name] = cloned_vehicle

    # return the cloned game state
    return cloned_game

if __name__ == "__main__":

    # create an instance of the rush hour game
    rush_hour_game = RushHour()

    # get the initial state from the game
    initial_state_hash = rush_hour_game.get_state_hashable()

    solver = RushHourBFS(rush_hour_game)

    # create the start time
    start_time = time.time()

    # find the solution path
    solution_path = solver.bfs()

    # create the end time
    end_time = time.time()

    # if we have found a solution path
    if solution_path:
        print("Solution sequence of moves:")
        for move in solution_path:
            print(move)
        print(f"Solution found in {len(solution_path)} moves!")

        elapsed_time = end_time - start_time
        print(f"Time taken to solve the board: {elapsed_time:.2f} seconds")

    else:
        print("No solution found.")

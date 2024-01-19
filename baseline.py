# baseline.py
import random
from rush_hour import RushHour
import matplotlib.pyplot as plt

class RushHourSolver:
    """
    In this class we add some methods to solve our rushhour boards/game randomly.
    """

    # this method initializes the game
    def __init__(self, game):
        self.game = game

    def get_possible_moves(self, vehicle):
        """
        In this method we generate / get all the possible moves for any
        vehicle and add those moves to a list.
        """

        board_size = len(self.game.board)
        print(board_size)
        # create a list where we will store all moves
        moves = []

        # check if the vehicle is oriented horizontally
        if vehicle.orientation == 'H':

            # loop over the columns
            for col in range(6 - vehicle.length + 1): # TODO: avoid hardcoding these values

                # check if the vehicle is allowed to move there
                if self.game.is_move_valid(vehicle, vehicle.row, col):

                    # calculate the distance for the move
                    distance = col - vehicle.col

                    # exclude moves with 0 distance
                    if distance != 0:

                        # add the move to the list
                        moves.append((vehicle.row, col))

        # for all the vehicles that are vertically oriented
        else:

            # loop over the rows
            for row in range(6 - vehicle.length + 1): # TODO: avoid hardcoding these values

                # check if the vehicle is allowed to move here
                if self.game.is_move_valid(vehicle, row, vehicle.col):

                    # calculate the distance for the move
                    distance = row - vehicle.row

                    # exclude moves with 0 distance
                    if distance != 0:

                        # add the move to the list
                        moves.append((row, vehicle.col))

        # return the list with all the possible moves
        return moves


    def solve_randomly(self, max_iterations=1000000000):
        """
        In this method we create an algorithm that is capable
        of solving the rush hour board by repeatedly doing random moves
        untill the red vehicle is at the desired exit spot.
        """

        # Count total moves made
        moves_counter = 0

        # we loop through our set maximum iterations
        for iteration in range(max_iterations):

            # choose a random vehicle from the game
            vehicle_name = random.choice(list(self.game.vehicles.keys()))
            vehicle = self.game.vehicles[vehicle_name]

            # check if the vehicle is allowed to move
            possible_moves = self.get_possible_moves(vehicle)

            # if the vehicle can't move, choose a different vehicle
            if not possible_moves:
                continue

            # choose a random move from the possible moves
            new_row, new_col = random.choice(possible_moves)

            # calculate the distance for the move
            distance = new_col - vehicle.col if vehicle.orientation == 'H' else new_row - vehicle.row

            # move the vehicle to the new place on the board
            self.game.move_vehicle(vehicle_name, distance)

            # Count total moves
            moves_counter += 1

            #Print the current/new state of the board
            print(f"Iteration: {iteration + 1}, Move: {moves_counter}\nVehicle {vehicle_name} by {distance} units")
            self.game.display_board()

            # check for win condition
            if self.game.check_win():
                print(f"Puzzle solved in {moves_counter} moves!")
                self.game.display_board()
                return moves_counter
        return None
        print("Failed to solve the puzzle within the maximum number of iterations.")

    def perform_experiments(self, num_experiments = 10000, max_iterations = 100000):
        results = []
        for game in range(num_experiments):
            # reset game for each experiment
            self.game.reset()
            result = self.solve_randomly(max_iterations)
            if result is not None:
                results.append(result)

        return results

if __name__ == "__main__":
    game = RushHour()

    solver = RushHourSolver(game)

    solver.solve_randomly()

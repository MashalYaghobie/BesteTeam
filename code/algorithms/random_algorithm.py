import random
import time
from code.game.rush_hour import RushHour
import matplotlib.pyplot as plt

class RushHourSolver:
    """
    In this class we add some methods to solve our rushhour boards/game
    by applying random moves.
    """

    def __init__(self, game, visualizer=None):
        """
        In this method we define some starting/intial variables.
        """

        # creating/initializing the variables
        self.game = game
        self.visualizer = visualizer

        
    def get_possible_moves(self, vehicle):
        """
        In this method we generate / get all the possible moves for any
        vehicle and add those moves to a list.
        """

        board_size = len(self.game.board)
        
        # create a list where we will store all moves
        moves = []

        # check if the vehicle is oriented horizontally
        if vehicle.orientation == 'H':

            # loop over the columns
            for col in range(board_size - vehicle.length + 1): 

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
            for row in range(board_size - vehicle.length + 1): 

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
        
        # count the total moves made
        moves_counter = 0

        # create the starting time
        start_time = time.time()
        
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

            # visualizer
            if self.visualizer:
                self.visualizer.update_board(vehicle_name)

            # increase the total moves done
            moves_counter += 1

            # print the current/new state of the board
            print(f"Iteration: {iteration + 1}, Move: {moves_counter}\nVehicle {vehicle_name} by {distance} units")
            self.game.display_board()

            # check for win condition
            if self.game.check_win():
                print(f"Puzzle solved in {moves_counter} moves! Time needed: {time.time() - start_time}")
                self.game.display_board()
                return moves_counter

        return None
        print("Failed to solve the puzzle within the maximum number of iterations.")

        
    def perform_experiments(self, num_experiments = 10000, max_iterations = 100000):
        """
        In this method we will create a way to let the algorithm run num_experiments
        amount of times. And set a limit at max_iterations amount of moves.
        """

        # create an empty list to store the results
        results = []

        # loop through our number of experiments/number of games
        for game in range(num_experiments):

            # reset game for each experiment
            self.game.reset()

            # save the results
            result = self.solve_randomly(max_iterations)
            if result is not None:
                results.append(result)

        return results

    
if __name__ == "__main__":
    
    # create a rush hour game
    game = RushHour()
    
    # start the game
    game.start_game()
    
    solver = RushHourSolver(game)
    
    solver.solve_randomly()
    

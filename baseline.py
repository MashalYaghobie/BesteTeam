# baseline.py
import random
from rush_hour import RushHour

class RushHourSolver:
    def __init__(self, game):
        self.game = game


    def get_possible_moves(self, vehicle):
        """Generate all possible moves for a given vehicle."""
        # store the moves in a list
        moves = []
        if vehicle.orientation == 'H':
            # loop over the columns
            for col in range(6 - vehicle.length + 1):
                # check if the vehicle can move there
                if self.game.is_move_valid(vehicle, vehicle.row, col):
                    # add the move to the list
                    moves.append((vehicle.row, col))
        else:
            for row in range(6 - vehicle.length + 1):
                if self.game.is_move_valid(vehicle, row, vehicle.col):
                    moves.append((row, vehicle.col))
        return moves


    def solve_randomly(self, max_iterations=1000):
        """Attempt to solve the puzzle with random moves."""
        for _ in range(max_iterations):
            # choose a random vehicle
            vehicle_name = random.choice(list(self.game.vehicles.keys()))
            vehicle = self.game.vehicles[vehicle_name]
            # check if the vehicle can move
            possible_moves = self.get_possible_moves(vehicle)
            if not possible_moves: # if it can't move, choose a different vehicle
                continue
            # choose a random move
            new_row, new_col = random.choice(possible_moves)
            # calculate the distance
            distance = new_col - vehicle.col if vehicle.orientation == 'H' else new_row - vehicle.row
            # move the vehicle
            self.game.move_vehicle(vehicle_name, distance)
            # check for win condition
            if self.game.check_win():
                print(f"Puzzle solved in {_ + 1} iterations!")
                self.game.display_board()
                return
        print("Failed to solve the puzzle within the maximum number of iterations.")


if __name__ == "__main__":
    game = RushHour('gameboards/Rushhour6x6_1.csv')
    
    solver = RushHourSolver(game)
    solver.solve_randomly()

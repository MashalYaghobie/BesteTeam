from rush_hour import RushHour
from baseline import RushHourSolver

from collections import deque
import time
import copy


class BFS:
    
    def __init__(self, game):
        self.game = game
        
    def get_possible_moves(self, vehicle):
        moves = []
        board_size = len(self.game.board)

        if vehicle.orientation == 'H':
            for col in range(board_size - vehicle.length + 1):
                if self.game.is_move_valid(vehicle, vehicle.row, col):
                    distance = col - vehicle.col
                    if distance != 0:
                        moves.append((vehicle.name, distance))
        else:
            for row in range(board_size - vehicle.length + 1):
                if self.game.is_move_valid(vehicle, row, vehicle.col):
                    distance = row - vehicle.row
                    if distance != 0:
                        moves.append((vehicle.name, distance))

        return moves
    
    
    def breadth_First_Search(game):
        
        # get current time
        start_time = time.time()

        # initialize
        boardsQueue = deque()
        archive = {}
        number = 0

        # put initial gameboard in queue
        initial_board = Gameboard(copy.deepcopy(game))
        boardsQueue.appendleft(initial_board)

        # add initial gameboard to archive
        archive[initial_board.get_state()] = 0

        while len(boardsQueue) != 0:
            # pop new board and path
            current_board = boardsQueue.pop()

            number += 1
            # if board is solved, return result
            if current_board.game.check_win():
                print("found board")
                return {"solvetime": time.time() - start_time, "nodes_popped": number, "archive": archive, "solution": current_board.game}

            # else add all possible boards to queue, if they're not in archive
            else:
                for vehicle_id, distance in current_board.get_possible_moves(current_board.game.vehicles[vehicle_id]):
                    new_rush_hour = copy.deepcopy(current_board.game)
                    new_vehicle = new_rush_hour.vehicles[vehicle_id]
                    new_rush_hour.move_vehicle(vehicle_id, distance)

                    new_state = new_rush_hour.get_state()
                    if new_state in archive:
                        pass
                    else:
                        new_board = Gameboard(new_rush_hour)
                        boardsQueue.appendleft(new_board)
                        archive[new_state] = current_board.get_state()
                    
                    
# Example usage:
if __name__ == "__main__":
    # initialize and set up the game
    game = RushHour()

    # Start and play the game
    game.start_game()

    # Run breadth-first search
    result = breadth_First_Search(game)
    print(result)

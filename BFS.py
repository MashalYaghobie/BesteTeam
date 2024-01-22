# BFS.py

import queue
import copy

# # no deeper than 'depth'
# depth = 3
# queue = queue.Queue()

# # add begin state to queue
# queue.put("")

# while not queue.empty():

#     # get first from queue
#     state = queue.get()
#     print(state)

#     # stop condition
#     if len(state) < depth:

#         # for each possible action
#         for i in ['L', 'R']:

#             # deepcopy the state
#             child = copy.deepcopy(state)

#             # make new child
#             child += i

#             # add new child
#             queue.put(child)

from rush_hour import RushHour
from collections import deque

class RusHourBFS(RushHour):
    """Extends the Rush Hour game class with BFS algorithm to solve this puzzle"""

    def solve_with_bfs(self):
        """Solves the Rush Hour puzzle using the BFS algorithm"""
        # deque allows fast appends and pops from both ends
        queue = deque([(self.get_state(), None, None)])
        # save visited states
        visited = set()
        # dictionary for tracking the path
        parents = {}
        # while there are states in the queue
        while queue:
            # remove leftmost item from the queue, which is the next state to explore
            current_state, parent_state, move_made = queue.popleft()
            # check if current state is winning
            if self.check_win():
                # call backtrack method and build path to the winning state
                return self.reconstruct_path(parents, current_state)
            # add current state to visited
            visited.add(current_state)
            # if current state has a parent, it's added to 'parents' with the move that led to it
            if parent_state:
                parents[current_state] = (parent_state, move_made)

            # get all possible moves from current state
                for vehicle_id, distance in self.get_all_possible_moves()
                # apply move and check new state
                if self.move_vehicle(vehicle_id, distance):
                    new_state = self.get_state()
                    # revert move after getting the state
                    self.move_vehicle(vehicle_id, -distance)

                    # if new state not visited, add it to the queue
                    if new_state not in visisted:
                        queue.append((new_state, current_state, (vehicle_id, distance)))

    def get_all_possible_moves(self):
        """Generate all possible valid moves from the current state"""
        moves = []
        for vehicle_id, vehicle in self.vehicles.items():
            # check possible moves in both directions
            for distance in [-1, 1]:
                if self.is_move_valid(vehicle, vehicle.row + (distance if vehicle.orientation == 'V' else 0),
                                      vehicle.col + (distance if vehicle.orientation == 'H' else 0)):
                    moves.append((vehicle_id, distance))
        return moves

    def reconstruct_path(self, parents, state):
        """Reconstructs the path from the initial state to the winning state."""
        path = []
        while state in parents:
            parent_state, move = parents[state]
            path.append(move)
            state = parent_state
        path.reverse()
        return path















from queue import Queue
import copy
from rush_hour import RushHour
from rush_hour import Vehicle

class breadth_first_search:

    def play_breadth_first_search(self):
        """
        In this method we use Breadth First Search to win a game of Rush Hour
        and find its winning state.
        """

        # Set up the queue for breadth first search
        queue_bfs = Queue()

        # Add the startin
        starting_state = self.get_state()
        queue_bfs.put(starting_state)

        # Keep track of all the states we have already visited
        already_visited_states = set()
        already_visited_states.add(starting_state)

        # Implement breadth first search
        while not queue_bfs.empty():

            # Get the current state from the bfs queue
            current_state = queue_bfs.get()

            # We can show the current state of the board
            # print("Current State:")
            # self.display_board()

            # Check if we have won / finished the game
            if self.check_win():
                print(f"Congratulations! You've won!")
                return

            # Create possible moves
            for vehicle_id, vehicle in self.vehicles.items():
                for distance in [-1, 1]:

                    # Try to move the vehicle to both sides
                    new_state = self.get_new_state_after_move(vehicle_id, distance)

                    # Make sure the new state is valid and that we have not visited it yet
                    if new_state is not None and new_state not in visited_states:
                        queue_bfs.put(new_state)
                        visited_states.add(new_state)

        print(f"We have not found a solution.")

    def get_new_state_after_move(self, vehicle_id, distance):
        """
        In this method we get the new state after a move for a vehicle_id and a distance.
        If the move is not valid we will return None
        """
        # Deepcopy the game state
        copy_of_game = copy.deepcopy(self)

        # Try to move the vehicle
        if vehicle_id in copy_of_game.vehicles:
            copy_of_game.move_vehicle(vehicle_id, distance)

            # and get the new game state after the move
            return copy_of_game.get_state()

            # if the move is invalid we return None
        else:
            return None


if __name__ == "__main__":
    # initialize and set up the game
    game = RushHour()

    # start and play the game with our breadth first search algorithm
    game.start_game()
    game.play_breadth_first_search()






    def breadth_First_Search(gameboard):
    # get current time
    start_time = time.time()
    # initialize
    boardsQueue = deque()
    archive  = {}
    archive[gameboard] = 0
    number = 0

    # put intial gameboard in queue
    boardsQueue.appendleft(gameboard)

    # add initial gameboard to archive
    archive[gameboard] = 0
    while len(boardsQueue) != 0 :
        # pop new board and path
        new_board = boardsQueue.pop()

        number += 1
        # if board is solved, return result
        if new_board.hasSolved():
            print ("found board")
            return {"solvetime": time.time() - start_time, "nodes_popped": number, "archive": archive, "solution": new_board}

        # else add all possible boards to queue, if they're not in archive
        else:
            for move in new_board.checkformoves():
                newgameboard = Gameboard(move)
                if newgameboard in archive:
                    pass
                else:
                    boardsQueue.appendleft(newgameboard)
                    archive[newgameboard] = new_board

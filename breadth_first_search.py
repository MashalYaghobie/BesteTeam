from queue import Queue
import copy
from rush_hour import RushHour, Vehicle


class BreadthFirstSearch:
    
    
    def __init__(self, game):
        self.game = game
    
    
    def play_breadth_first_search(self):
        """
        In this method we use Breadth First Search to win a game of Rush Hour
        and find its winning state.
        """

        # Set up the queue for breadth first search
        queue_bfs = Queue()

        # Add the starting state
        starting_state = self.game.get_state()
        queue_bfs.put(starting_state)

        # Keep track of all the states we have already visited
        already_visited_states = set()
        already_visited_states.add(starting_state)

        # Implement breadth first search
        while not queue_bfs.empty():

            # Get the current state from the bfs queue
            current_state = queue_bfs.get()

            # Check if we have won / finished the game
            if self.game.check_win():
                print(f"Congratulations! You've won!")
                return

            # Create possible moves
            for vehicle_id, vehicle in self.game.vehicles.items():
                for distance in [-1, 1]:

                    # Try to move the vehicle to both sides
                    new_state = self.get_new_state_after_move(vehicle_id, distance)

                    # Make sure the new state is valid and that we have not visited it yet
                    if new_state is not None and new_state not in already_visited_states:
                        queue_bfs.put(new_state)
                        already_visited_states.add(new_state)

        print(f"We have not found a solution.")

    def get_new_state_after_move(self, vehicle_id, distance):
        """
        In this method we get the new state after a move for a vehicle_id and a distance.
        If the move is not valid we will return None
        """
        # Deepcopy the game state
        copy_of_game = copy.deepcopy(self)

        # Try to move the vehicle
        if vehicle_id in copy_of_game.game.vehicles:
            copy_of_game.game.move_vehicle(vehicle_id, distance)

            # and get the new game state after the move
            return copy_of_game.game.get_state()

            # if the move is invalid we return None
        else:
            return None


if __name__ == "__main__":
    # initialize and set up the game
    game = RushHour()

    # start and play the game with our breadth first search algorithm
    game.start_game()
    
    bfs = BreadthFirstSearch(game)
    
    bfs.play_breadth_first_search()

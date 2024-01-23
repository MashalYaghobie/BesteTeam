from rush_hour import RushHour
from baseline import RushHourSolver

from collections import deque
import time
import copy


def breadth_first_search(game):

    #Initialize the queue for BFS
    queue = deque([(game.get_state(), 0)])

    # Set to keep track of visited states
    visited_states = set()

    
    
    while queue:
        # Dequeue the current state and its depth
        current_state, depth = queue.popleft()

        # Load the current state into the game
        game.load_state(current_state)

        # Check if the current state is the goal state
        if game.check_win():
            print("BFS found a solution with depth:", depth)
            game.display_board()
            return

        # Add the current state to the set of visited states
        visited_states.add(current_state)

        # Generate possible moves for all vehicles on the board
        for vehicle_id, vehicle in game.vehicles.items():
            possible_moves = game.get_possible_moves(vehicle)
            
            print(possible_moves)
            
            for move in possible_moves:
                
                print(f"Trying move {move} for vehicle {vehicle_id}")
                
                # Make a copy of the current game state
                new_game = game.copy()
                
                
                # ADDING CODE
                new_row, new_col = move
                distance = new_col - vehicle.col if vehicle.orientation == 'H' else new_row - vehicle.row
                print(distance)
                print(f"Checking validity: {new_game.is_move_valid(vehicle, new_row, new_col)}")
                ############
                
                
                # Move the vehicle in thew new game state
                new_game.move_vehicle(vehicle_id, distance)

                # Get the new state of the game
                new_state = new_game.get_state()
                
                new_game.display_board()
                
               
                # Check if the new state has not been visited
                if new_state not in visited_states:
                    
                    # Enqueue the new state and its depth
                    queue.append((new_state, depth + 1))
                    visited_states.add(new_state)

       
    print("BFS did not find a solution.")

if __name__ == "__main__":
    # Initialize and set up the game
    game = RushHour()

    # Start and play the game
    game.start_game()

    # Use BFS to find a solution
    breadth_first_search(game)
    
    
    
    
    
    

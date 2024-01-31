import time

from code.algorithms.astar import RushHourAStar
from code.algorithms.astar2 import RushHourAStar2
from code.algorithms.bfs import RushHourBFS
from code.algorithms.dfs import RushHourDFS
from code.algorithms.random_algorithm import RushHourSolver

from code.game.rush_hour import RushHour, Vehicle


def run_algorithm(choice):
    """
    Runs algorithm based off of the user's choice. Input is an integer between 1 and 5.
    """
    # ----------------------------------------------------- Random ------------------------------------------------------
    if choice == '1':
        game = RushHour()
        solver = RushHourSolver(game)
        solver.solve_randomly()
    
    
    # ----------------------------------------------------- AStar -------------------------------------------------------
    # The best possible heuristics combinations I could find are in this algorithm. It solves the 6x6 boards and the first 
    # 9x9 board in around 20 seconds with the shortest path as well. It keeps on running when trying a different board.
    elif choice == '2':
        rush_hour_game = RushHour()
        solver = RushHourAStar(rush_hour_game)
        solution_path = solver.a_star()
        if solution_path:
            print(f"Solution found in {len(solution_path) - 1} moves!")
        else:
            print("No solution found.")
               
                
    # --------------------------------------- AStar, with heuristics as parameters --------------------------------------
    elif choice == '3':
        rush_hour_game = RushHour()
        initial_state = rush_hour_game.get_state_hashable()

        solver = RushHourAStar2(rush_hour_game, use_distance_heuristic=True, use_direct_blocking_heuristic=True, use_indirect_blocking_heuristic=True, use_car_mobility_heuristic=True, use_deadlock_penalty=True, distance_weight=6, direct_blocking_weight=3, indirect_blocking_weight=2, car_mobility_weight=4)
        start_time = time.time()
        solution_path = solver.bfs()
        end_time = time.time()

        if solution_path:
            print("Solution sequence of moves:")
            for move in solution_path:
                print(move)
            print(f"Solution found in {len(solution_path)} moves!")

            elapsed_time = end_time - start_time
            print(f"Time taken to solve the board: {elapsed_time:.2f} seconds")
        else:
            print("No solution found.")

            
    # ----------------------------------------------- Breadth-First Search ----------------------------------------------
    elif choice == '4':
        rush_hour_game = RushHour()
        initial_state_hash = rush_hour_game.get_state_hashable()
        solver = RushHourBFS(rush_hour_game)
        start_time = time.time()
        solution_path = solver.bfs()

        end_time = time.time()

        if solution_path:
            print("Solution sequence of moves:")
            for move in solution_path:
                print(move)
            print(f"Solution found in {len(solution_path)} moves!")

            elapsed_time = end_time - start_time
            print(f"Time taken to solve the board: {elapsed_time:.2f} seconds")

        else:
            print("No solution found.")

            
    # ----------------------------------------------- Depth-First Search ----------------------------------------------
    elif choice == '5':
        rush_hour_game = RushHour()
        start_time = time.time()
        solver = RushHourDFS(rush_hour_game)
        solution_path = solver.depth_first_search()
        end_time = time.time()

        if solution_path:
            print("Initial State:")
            rush_hour_game.display_board()

            print("Final State:")
            solution_path[-1].display_board()

            print(f"Number of moves to solve the board: {len(solution_path) - 1}")

            # this is the time the algorithm has been running
            elapsed_time = end_time - start_time
            print(f"Time taken to solve the board: {elapsed_time:.2f} seconds")

        else:
            print("No solution found.")

            
            
if __name__ == "__main__":
    print("Choose an algorithm:")
    print("1. Random Algorithm")
    print("2. A* Algorithm")
    print("3. A* Algorithm with customizable heuristics")
    print("4. Breadth-First Search")
    print("5. Depth-First Search")

    user_choice = input("Enter the number of the algorithm you want to run: ")
    run_algorithm(user_choice)

        
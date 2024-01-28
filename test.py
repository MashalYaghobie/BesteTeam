import cProfile
from astar import RushHourAStar, RushHour

if __name__ == "__main__":
    rush_hour_game = RushHour()
    solver = RushHourAStar(rush_hour_game)

    # Wrap the A* search function in cProfile
    cProfile.run('solution_path = solver.a_star()', sort='cumulative')

    if solution_path:
        print(f"Solution found in {len(solution_path) - 1} moves!")
    else:
        print("No solution found.")

    

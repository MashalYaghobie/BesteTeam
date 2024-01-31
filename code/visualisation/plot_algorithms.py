import matplotlib.pyplot as plt
import numpy as np

def plot_moves_and_states(puzzle_names, moves_data, states_data, total_state_space):
    # data for number of moves and states visited for each algorithm
    bfs, dfs, astar = moves_data
    bfs_states, dfs_states, astar_states = states_data

    # prepare plotting
    pos = list(range(len(puzzle_names)))
    width = 0.15

    # plotting bar chart for num moves
    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax1.bar([p - 1.5*width for p in pos], bfs, width, alpha=0.5, label='Breadth-First-Search')
    ax1.bar([p - 0.5*width for p in pos], dfs, width, alpha=0.5, label='Depth-First-Search')
    ax1.bar([p + 0.5*width for p in pos], astar, width, alpha=0.5, label='A*')
    ax1.set_ylabel('Number of Moves')
    ax1.set_title('Performance of Algorithms in Rush Hour Puzzle')
    ax1.set_xticks([p for p in pos])
    ax1.set_xticklabels(puzzle_names)
    ax1.legend(loc='upper left')
    ax1.grid()

    # plotting line chart for the states visited and total state space
    ax2 = ax1.twinx()
    ax2.plot(puzzle_names, bfs_states, color='blue', label='States visited - Breadth-First-Search', marker='o')
    ax2.plot(puzzle_names, dfs_states, color='red', label='States visited - Depth-First-Search', marker='o')
    ax2.plot(puzzle_names, astar_states, color='green', label='States visited - A*', marker='o')
    ax2.plot(puzzle_names, total_state_space, color='purple', label='Total State Space', marker='x', linestyle='--')
    ax2.set_ylabel('Number of states')
    ax2.legend(loc='upper right')

    plt.show()


puzzle_names = ['6x6-1', '6x6-2', '6x6-3']
bfs = [35, 29, 83]
dfs = [187, 219, 2050]
astar = [35, 29, 85]
moves_data = [bfs, dfs, astar]

states_bfs = [650, 4223, 8752]
states_dfs = [397, 861, 5711]
states_astar = [291, 1244, 7362]
states_data = [states_bfs, states_dfs, states_astar]


total_state_space = [818, 13841, 11252]

plot_moves_and_states(puzzle_names, moves_data, states_data, total_state_space)

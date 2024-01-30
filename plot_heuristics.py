import matplotlib.pyplot as plt
import numpy as np

def plot_heuristics_performance(heuristics, moves_data, states_data):
    # Prepare plotting
    pos = list(range(len(heuristics)))
    width = 0.35

    # Plotting the bar chart for the number of moves
    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax1.bar(pos, moves_data, width, alpha=0.5, color='blue')
    ax1.set_ylabel('Number of Moves')
    ax1.set_title('Performance of Different Heuristic Combinations in Rush Hour Puzzle on 6x6-3 Board')
    ax1.set_xticks([p for p in pos])
    ax1.set_xticklabels(heuristics, rotation=45, ha='right')
    ax1.grid()

    # Plotting the bar chart for the time
    ax2 = ax1.twinx()
    ax2.bar([p + width for p in pos], states_data, width, alpha=0.5, color='green')
    ax2.set_ylabel('States visited')

    plt.show()

heuristics = ['Dist+Dir+Ind', 'Dist+Ind+Car Mov', 'Dir+Ind',
              'Dist+Car Mov', 'Dist+Ind', 'Dir+Car Mov',
              'Dist+Dir+Ind+Car Mov', 'Dir+Ind+Car Mov']


moves_data = [85, 88, 87, 88, 85, 88, 90, 92]
states_data = [7362, 8654, 8686, 8699, 8426, 8715, 8563, 8649]

plot_heuristics_performance(heuristics, moves_data, states_data)

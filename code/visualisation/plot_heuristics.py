import matplotlib.pyplot as plt
import numpy as np

def plot_heuristics_performance(heuristics, moves_data, states_data):
    # Prepare plotting
    pos = list(range(len(heuristics)))
    width = 0.35

    # Plotting the bar chart for the number of moves
    fig, ax1 = plt.subplots(figsize=(12, 6))
    bars1 = ax1.bar(pos, moves_data, width, alpha=0.5, color='blue')
    ax1.set_ylabel('Number of Moves')
    ax1.set_title('Performance of Different Heuristic Combinations on a 9x9 Board')
    ax1.set_xticks([p for p in pos])
    ax1.set_xticklabels(heuristics, rotation=45, ha='right')
    ax1.grid()

    # Plotting the bar chart for the states
    ax2 = ax1.twinx()
    bars2 = ax2.bar([p + width for p in pos], states_data, width, alpha=0.5, color='green')
    ax2.set_ylabel('States visited')

    plt.legend([bars1, bars2], ['Number of Moves', 'States Visited'], loc='upper left')

    plt.show()

heuristics = ['Dist+Dir+CarMob', 'Ind+DeadPen+Dist', 'CarMob+DeadPen',
              'Dir+Ind+Dist+CarMob', 'DeadPen+Dist+Dir', 'CarMob+Dir+Ind',
               'Dist+DeadPen', 'Ind+CarMob+DeadPen+Dist', 'Dir+CarMob',
               'Dist+Ind+DeadPen'
               ]


moves_data = [57, 52, 60, 57, 51, 60, 52, 58, 60, 52]
states_data = [110075, 96869, 348300, 83366, 84980, 60168, 115603, 96922, 94022, 96896]

plot_heuristics_performance(heuristics, moves_data, states_data)

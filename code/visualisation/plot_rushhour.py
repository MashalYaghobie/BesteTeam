import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from code.game.rush_hour import RushHour
from code.algorithms.random_algorithm import RushHourSolver

def plot_histogram(data, num_bins=None):
    plt.figure(figsize=(10, 6))
    if num_bins is None:
        num_bins = int(len(data) ** 0.5)
    plt.hist(data, bins=num_bins, edgecolor='black')
    plt.xlabel('Number of Moves')
    plt.ylabel('Frequency')
    plt.title('Histogram of Moves in 10,000 Experiments')
    plt.grid(True)
    plt.show()

def plot_boxplot(data):
    plt.figure(figsize=(10, 6))
    plt.boxplot(data)
    plt.title('Box Plot of Moves in 10.000 Experiments')
    plt.ylabel('Number of Moves')
    plt.grid(True)
    plt.show()

def plot_densityplot(data):
    plt.figure(figsize=(10, 6))
    sns.kdeplot(data, bw_adjust=0.5)
    plt.title('Density Plot of Moves in 10.000 Experiments')
    plt.xlabel('Number of Moves')
    plt.grid(True)
    plt.show()

def plot_cdf(data):
    plt.figure(figsize=(10, 6))
    sorted_data = np.sort(data)
    yvals = np.arange(len(sorted_data)) / float(len(sorted_data))
    plt.plot(sorted_data, yvals)
    plt.title('CDF of Moves in 10.000 Experiments')
    plt.xlabel('Number of Moves')
    plt.ylabel('Cumulative Probability')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    game= RushHour('gameboards/Rushhour6x6_1.csv')
    solver = RushHourSolver(game)
    results = solver.perform_experiments(num_experiments=10000)

    # plotting
    plot_boxplot(results)
    plot_densityplot(results)
    plot_cdf(results)

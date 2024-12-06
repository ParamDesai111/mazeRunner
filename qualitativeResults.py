import matplotlib.pyplot as plt
from main import parse_grievers
from mazeParser import load_maze, load_dynamic_walls
from qlearning import MazeRunner
import numpy as np

def run_simulation_with_metrics(maze_file, dynamic_file, episodes=10000):
    maze = load_maze(maze_file)
    dynamic_walls = load_dynamic_walls(dynamic_file)

    start = None
    goal = None
    for i in range(maze.shape[0]):
        for j in range(maze.shape[1]):
            if maze[i, j] == 'S':
                start = (i, j)
            if maze[i, j] == 'E':
                goal = (i, j)

    maze_numeric = np.where(maze == 'S', 0, maze)
    maze_numeric = np.where(maze_numeric == 'E', 0, maze_numeric)
    maze_numeric = np.where(maze_numeric == 'G', -1, maze_numeric)

    grievers = parse_grievers(maze_numeric)

    runner = MazeRunner(maze_numeric.astype(int), start, goal)
    runner.initialize_q_table()
    metrics = runner.train(episodes=episodes, dynamic_walls=dynamic_walls, grievers=grievers)

    return metrics

import pandas as pd
import matplotlib.pyplot as plt

def visualize_metrics(metrics):
    """Visualize the metrics collected and display them in a table."""
    configurations = list(metrics.keys())
    success_rates = [metrics[config]["success_count"] / metrics[config]["runs"] * 100 for config in configurations]
    avg_steps = [metrics[config]["total_steps"] / metrics[config]["success_count"] for config in configurations]
    avg_rewards = [metrics[config]["total_rewards"] / metrics[config]["runs"] for config in configurations]
    penalties = [metrics[config]["penalties"] for config in configurations]
    wall_triggers = [1,3,2]

    # Create a DataFrame for tabular display
    data = {
        "Configuration": configurations,
        "Success Rate (%)": success_rates,
        "Average Steps": avg_steps,
        "Average Reward": avg_rewards,
        "Total Penalties": penalties,
        "Dynamic Wall Triggers": wall_triggers,
    }
    results_df = pd.DataFrame(data)
    
    # Display the table
    print("\nSimulation Metrics Summary:")
    print(results_df.to_string(index=False))
    
    # Visualize each metric as a bar chart
    x = range(len(configurations))

    # Success Rate
    plt.figure(figsize=(10, 6))
    plt.bar(x, success_rates, color="green", alpha=0.7)
    plt.xticks(x, configurations)
    plt.title("Success Rate Across Configurations")
    plt.xlabel("Configuration")
    plt.ylabel("Success Rate (%)")
    plt.show()

    # Average Steps
    plt.figure(figsize=(10, 6))
    plt.bar(x, avg_steps, color="blue", alpha=0.7)
    plt.xticks(x, configurations)
    plt.title("Average Steps Across Configurations")
    plt.xlabel("Configuration")
    plt.ylabel("Average Steps")
    plt.show()

    # Average Rewards
    plt.figure(figsize=(10, 6))
    plt.bar(x, avg_rewards, color="orange", alpha=0.7)
    plt.xticks(x, configurations)
    plt.title("Average Rewards Across Configurations")
    plt.xlabel("Configuration")
    plt.ylabel("Average Reward")
    plt.show()

    # Penalties
    plt.figure(figsize=(10, 6))
    plt.bar(x, penalties, color="red", alpha=0.7)
    plt.xticks(x, configurations)
    plt.title("Total Penalties Across Configurations")
    plt.xlabel("Configuration")
    plt.ylabel("Total Penalties")
    plt.show()

    # Dynamic Wall Triggers
    plt.figure(figsize=(10, 6))
    plt.bar(x, wall_triggers, color="purple", alpha=0.7)
    plt.xticks(x, configurations)
    plt.title("Dynamic Wall Triggers Across Configurations")
    plt.xlabel("Configuration")
    plt.ylabel("Dynamic Wall Triggers")
    plt.show()


def main():
    maze_files = {
        "Simple": "Results/simple_maze.csv",
        "Moderate": "Results/moderate_maze.csv",
        "Complex": "Results/complex_maze.csv",
    }
    dynamic_files = {
        "Simple": "Results/simple_dynamic.txt",
        "Moderate": "Results/moderate_dynamic.txt",
        "Complex": "Results/complex_dynamic.txt",
    }

    results = {}
    for config in maze_files:
        print(f"Running simulation for {config} configuration...")
        results[config] = run_simulation_with_metrics(maze_files[config], dynamic_files[config])

    visualize_metrics(results)

if __name__ == "__main__":
    main()

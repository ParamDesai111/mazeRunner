import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors  # Import the colors module from matplotlib
import numpy as np

# def load_maze(csv_file):
#     """Load maze from a CSV file."""
#     maze = pd.read_csv(csv_file, header=None)
#     return maze.values

def load_maze(csv_file):
    """Load maze from a CSV file."""
    maze = pd.read_csv(csv_file, header=None)
    return maze.applymap(lambda x: x.strip() if isinstance(x, str) else x).values


def load_dynamic_walls(dynamic_file):
    """Load dynamic walls from a text file."""
    dynamic_walls = {}
    with open(dynamic_file, 'r') as file:
        for line in file:
            coord, behavior = line.strip().split(':')
            x, y = eval(coord.strip())
            dynamic_walls[(x, y)] = behavior.strip()
    return dynamic_walls

def visualize_maze(maze, dynamic_walls=None):
    """Visualize the maze with dynamic walls highlighted."""
    fig, ax = plt.subplots()
    colors = {'S': 'green', 'E': 'red', '0': 'white', '1': 'black', 'G': 'blue'}
    dynamic_color = 'yellow'
    
    # Create a color grid
    color_grid = np.zeros_like(maze, dtype=object)
    for i in range(maze.shape[0]):
        for j in range(maze.shape[1]):
            cell = maze[i, j]
            color_grid[i, j] = colors.get(cell, 'white')
    
    # Highlight dynamic walls
    if dynamic_walls:
        for (x, y) in dynamic_walls.keys():
            color_grid[x, y] = dynamic_color
    
    # Convert colors to RGBA
    rgba_grid = [[mcolors.to_rgba(c) for c in row] for row in color_grid]

    # Display the maze
    ax.imshow(rgba_grid, aspect='equal')
    ax.set_xticks(np.arange(-0.5, maze.shape[1], 1), minor=True)
    ax.set_yticks(np.arange(-0.5, maze.shape[0], 1), minor=True)
    ax.grid(which='minor', color='black', linestyle='-', linewidth=0.5)
    ax.tick_params(which='minor', size=0)
    plt.show()

# # Example Usage
# csv_file = "csv/maze.csv"
# dynamic_file = "csv/dynamic_walls.txt"

# maze = load_maze(csv_file)
# dynamic_walls = load_dynamic_walls(dynamic_file)
# visualize_maze(maze, dynamic_walls)

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.colors import ListedColormap

def load_maze_from_csv(filename):
    maze_data = pd.read_csv(filename)
    maze = {}
    
    max_row = maze_data['row'].max()
    max_col = maze_data['col'].max()
    rows, cols = max_row + 1, max_col + 1

    for _, row in maze_data.iterrows():
        position = (row['row'], row['col'])
        maze[position] = {
            'type': row['type'],
            'dynamic_change': row.get('dynamic_change', 'static')
        }
    return maze, rows, cols

def visualize_maze(maze, rows, cols):
    # Define the grid and color mapping
    grid = np.zeros((rows, cols), dtype=int)
    
    # Assign values for each type of cell
    for (r, c), cell_info in maze.items():
        cell_type = cell_info['type']
        if cell_type == 'wall':
            grid[r, c] = 2  # Black for walls
        elif cell_type == 'path':
            grid[r, c] = 1  # White for paths
        elif cell_type == 'start':
            grid[r, c] = 3  # Green for start
        elif cell_type == 'goal':
            grid[r, c] = 4  # Blue for goal
        elif cell_type == 'griever':
            grid[r, c] = 5  # Red for grievers

    # Define a color map for each type
    cmap = ListedColormap(['white', 'black', 'white', 'green', 'blue', 'red'])
    
    # Plot the grid with the custom color map
    plt.imshow(grid, cmap=cmap)
    plt.colorbar(ticks=[1, 2, 3, 4, 5], label="Cell Types")  # Optional colorbar with labels
    plt.show()

# Load maze and visualize with custom color mapping
maze, rows, cols = load_maze_from_csv("csv/file.csv")
visualize_maze(maze, rows, cols)

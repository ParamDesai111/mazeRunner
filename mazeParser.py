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
            trigger, target = line.strip().split(':')
            trigger = eval(trigger.strip())  # Convert to tuple
            target = eval(target.strip())   # Convert to tuple
            dynamic_walls[trigger] = target
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

def apply_dynamic_wall_changes(maze, dynamic_walls, visited_cells, triggered_walls):
    """
    Apply dynamic wall changes based on the runner's visited cells.
    
    :param maze: Current maze as a NumPy array.
    :param dynamic_walls: Dictionary with trigger and target positions for dynamic walls.
    :param visited_cells: Set of cells visited by the runner.
    :param triggered_walls: Set of already moved walls to avoid re-triggering.
    :return: Updated maze.
    """
    changes_made = False  # Track if any changes are made
    for trigger, target in dynamic_walls.items():
        if trigger in visited_cells and trigger not in triggered_walls:
            tx, ty = target
            # Ensure the target position is valid and unoccupied
            if maze[tx, ty] == 0:  # Target must be walkable
                print(f"Moving wall from {trigger} to {target}")
                maze[tx, ty] = 1   # Move the wall to the target
                triggered_walls.add(trigger)  # Mark this wall as triggered
                changes_made = True  # Indicate that a change was made
    return maze, changes_made



# # Example Usage
# csv_file = "csv/maze.csv"
# dynamic_file = "csv/dynamic_walls.txt"

# maze = load_maze(csv_file)
# dynamic_walls = load_dynamic_walls(dynamic_file)
# visualize_maze(maze, dynamic_walls)

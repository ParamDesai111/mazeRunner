import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors  # Import the colors module from matplotlib
import numpy as np
import pandas as pd
import pygame
import numpy as np
import time

# def load_maze(csv_file):
#     """Load maze from a CSV file."""
#     maze = pd.read_csv(csv_file, header=None)
#     return maze.values

def load_maze(csv_file):
    """Load maze from a CSV file."""
    maze = pd.read_csv(csv_file, header=None)
    return maze.applymap(lambda x: x.strip() if isinstance(x, str) else x).values


# def load_dynamic_walls(dynamic_file):
#     """Load dynamic walls from a text file."""
#     dynamic_walls = {}
#     with open(dynamic_file, 'r') as file:
#         for line in file:
#             trigger, target = line.strip().split(':')
#             trigger = eval(trigger.strip())  # Convert to tuple
#             target = eval(target.strip())   # Convert to tuple
#             dynamic_walls[trigger] = target
#     return dynamic_walls

def load_dynamic_walls(dynamic_file):
    """Load dynamic walls from a text file with support for multiple targets."""
    dynamic_walls = {}
    with open(dynamic_file, 'r') as file:
        for line in file:
            trigger, targets = line.strip().split(':')
            trigger = eval(trigger.strip())  # Convert to tuple
            targets = eval(targets.strip())  # Convert to list of tuples
            
            # Ensure the targets are stored as a list
            if not isinstance(targets, list):
                targets = [targets]
            
            # Add the trigger and its targets to the dictionary
            if trigger not in dynamic_walls:
                dynamic_walls[trigger] = []
            dynamic_walls[trigger].extend(targets)
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

# def apply_dynamic_wall_changes(maze, dynamic_walls, visited_cells, triggered_walls):
#     """
#     Apply dynamic wall changes based on the runner's visited cells.
    
#     :param maze: Current maze as a NumPy array.
#     :param dynamic_walls: Dictionary with trigger and target positions for dynamic walls.
#     :param visited_cells: Set of cells visited by the runner.
#     :param triggered_walls: Set of already moved walls to avoid re-triggering.
#     :return: Updated maze.
#     """
#     changes_made = False  # Track if any changes are made
#     for trigger, target in dynamic_walls.items():
#         if trigger in visited_cells and trigger not in triggered_walls:
#             tx, ty = target
#             # Ensure the target position is valid and unoccupied
#             if maze[tx, ty] == 0:  # Target must be walkable
#                 print(f"Moving wall from {trigger} to {target}")
#                 maze[tx, ty] = 1   # Move the wall to the target
#                 triggered_walls.add(trigger)  # Mark this wall as triggered
#                 changes_made = True  # Indicate that a change was made
#     return maze, changes_made
def apply_dynamic_wall_changes(maze, dynamic_walls, visited_cells, triggered_walls):
    """
    Apply dynamic wall changes based on the runner's visited cells.
    
    :param maze: Current maze as a NumPy array.
    :param dynamic_walls: Dictionary with triggers and lists of target positions for dynamic walls.
    :param visited_cells: Set of cells visited by the runner.
    :param triggered_walls: Set of already moved walls to avoid re-triggering.
    :return: Updated maze and a flag indicating if changes were made.
    """
    changes_made = False  # Track if any changes are made
    for trigger, targets in dynamic_walls.items():
        if trigger in visited_cells and trigger not in triggered_walls:
            for target in targets:
                tx, ty = target
                # Ensure the target position is valid and unoccupied
                if maze[tx, ty] == 0:  # Check if target is walkable
                    print(f"Moving wall from {trigger} to {target}")
                    maze[tx, ty] = 1   # Place the wall at the target location
                    # changes_made = True  # Indicate that a change was made
            triggered_walls.add(trigger)  # Mark this trigger as processed
    return maze, changes_made


# # Example Usage
# csv_file = "csv/maze.csv"
# dynamic_file = "csv/dynamic_walls.txt"

# maze = load_maze(csv_file)
# dynamic_walls = load_dynamic_walls(dynamic_file)
# visualize_maze(maze, dynamic_walls)

# Define colors for visualization
COLORS = {
    'S': (0, 255, 0),  # Start - Green
    'E': (0, 0, 255),  # End - Red
    '0': (255, 255, 255),  # Walkable - White
    '1': (0, 0, 0),  # Wall - Black
    'G': (255, 0, 0),  # Griever - Blue
    'PATH': (255, 255, 0),  # Path - Yellow
    'DYNAMIC': (255, 165, 0)  # Dynamic change - Orange
}

# Maze visualization settings
CELL_SIZE = 30
MARGIN = 2
FPS = 2  # Frames per second for animation speed
def visualize_maze_live(maze, path, dynamic_walls=None):
    """
    Visualize the maze in real-time with images, simulating the agent's path.
    
    :param maze: 2D NumPy array representing the maze.
    :param path: List of tuples representing the agent's path.
    :param dynamic_walls: Dictionary of dynamic walls (optional).
    """
    rows, cols = maze.shape
    window_width = cols * (CELL_SIZE + MARGIN)
    window_height = rows * (CELL_SIZE + MARGIN)

    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Maze Runner Simulation with Images")
    clock = pygame.time.Clock()
    running = True

    # Load images
    agent_img = pygame.transform.scale(pygame.image.load("images/agent.png"), (CELL_SIZE, CELL_SIZE))
    wall_img = pygame.transform.scale(pygame.image.load("images/wall.png"), (CELL_SIZE, CELL_SIZE))
    griever_img = pygame.transform.scale(pygame.image.load("images/griever.png"), (CELL_SIZE, CELL_SIZE))
    start_img = pygame.transform.scale(pygame.image.load("images/start.png"), (CELL_SIZE, CELL_SIZE))
    end_img = pygame.transform.scale(pygame.image.load("images/goal.png"), (CELL_SIZE, CELL_SIZE))
    floor_img = pygame.transform.scale(pygame.image.load("images/start.png"), (CELL_SIZE, CELL_SIZE))
    path_highlight_img = pygame.transform.scale(pygame.image.load("images/path_highlight.png"), (CELL_SIZE, CELL_SIZE))
    dynamic_wall_img = pygame.transform.scale(pygame.image.load("images/dynamic_wall.png"), (CELL_SIZE, CELL_SIZE))

    # Mapping maze characters to images
    image_mapping = {
        'S': start_img,
        'E': end_img,
        '0': floor_img,
        '1': wall_img,
        'G': griever_img,
    }

    # Helper function to draw the maze
    def draw_maze(current_position=None, completed=False):
        screen.fill((0, 0, 0))  # Black background
        for i in range(rows):
            for j in range(cols):
                rect = pygame.Rect(
                    j * (CELL_SIZE + MARGIN),
                    i * (CELL_SIZE + MARGIN),
                    CELL_SIZE,
                    CELL_SIZE
                )
                cell_type = str(maze[i, j])
                image = image_mapping.get(cell_type, floor_img)  # Default to floor image

                # # Highlight dynamic walls
                # if dynamic_walls and (i, j) in [t for sublist in dynamic_walls.keys() for t in sublist]:
                #     image = dynamic_wall_img
                if dynamic_walls and (i, j) in dynamic_walls.keys():
                    image = dynamic_wall_img
                
                # Highlight the completed path
                if completed and (i, j) in path:
                    image = path_highlight_img
                elif current_position == (i, j):
                    image = agent_img
                
                screen.blit(image, rect.topleft)
        
        pygame.display.flip()

    # Simulate the path
    for step, (x, y) in enumerate(path):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Check for dynamic wall triggers
        if dynamic_walls and (x, y) in dynamic_walls:
            targets = dynamic_walls[(x, y)]
            for tx, ty in targets:
                if maze[tx, ty] == 0:  # Ensure the target is a valid cell
                    print(f"Dynamic wall triggered at ({tx}, {ty}).")
                    maze[tx, ty] = 1  # Place the wall at the target location
            del dynamic_walls[(x, y)]  # Remove the trigger to avoid re-triggering

        # Draw the maze with the agent's current position
        draw_maze(current_position=(x, y))
        clock.tick(FPS)  # Control animation speed
        
        if not running:
            break

    # Highlight the entire path after completion
    draw_maze(completed=True)

    # Keep the window open until the user closes it
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        pygame.display.flip()
        clock.tick(30)  # Run at 30 FPS to minimize CPU usage

    pygame.quit()



import pandas as pd
import pygame
import numpy as np
import time

# Define colors for visualization
COLORS = {
    'S': (0, 255, 0),  # Start - Green
    'E': (0, 0, 255),  # End - Red
    '0': (255, 255, 255),  # Walkable - White
    '1': (0, 0, 0),  # Wall - Black
    'G': (255, 0, 0),  # Griever - Blue
    'PATH': (255, 255, 0),  # Path - Yellow
    'DYNAMIC': (255, 165, 0)  # Dynamic Wall - Orange
}

# Maze visualization settings
CELL_SIZE = 30
MARGIN = 2
FPS = 2  # Frames per second for animation speed

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


def visualize_maze_live(maze, path, dynamic_walls=None):
    """
    Visualize the maze in real-time, simulating the agent's path.
    
    :param maze: 2D NumPy array representing the maze.
    :param path: List of tuples representing the agent's path.
    :param dynamic_walls: Dictionary of dynamic walls (optional).
    """
    rows, cols = maze.shape
    window_width = cols * (CELL_SIZE + MARGIN)
    window_height = rows * (CELL_SIZE + MARGIN)

    # Add a new color for the completed path
    COLORS['PATH_COMPLETED'] = (0, 255, 255)  # Cyan

    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Maze Runner Simulation")
    clock = pygame.time.Clock()
    running = True

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
                color = COLORS.get(cell_type, (255, 255, 255))  # Default: White
                
                # Highlight dynamic walls
                if dynamic_walls and (i, j) in dynamic_walls.keys():
                    color = COLORS['DYNAMIC']
                
                # Highlight the current position or completed path
                if completed and (i, j) in path:
                    color = COLORS['PATH_COMPLETED']
                elif current_position == (i, j):
                    color = COLORS['PATH']
                
                pygame.draw.rect(screen, color, rect)
        
        pygame.display.flip()

    # Simulate the path
    for step, (x, y) in enumerate(path):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
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
            if maze[tx, ty] == '0':  # Target must be walkable
                print(f"Moving wall from {trigger} to {target}")
                maze[tx, ty] = '1'   # Move the wall to the target
                triggered_walls.add(trigger)  # Mark this wall as triggered
                changes_made = True  # Indicate that a change was made
    return maze, changes_made
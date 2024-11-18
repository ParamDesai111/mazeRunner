import numpy as np
from mazeParser import load_maze, load_dynamic_walls, visualize_maze, apply_dynamic_wall_changes
from qlearning import MazeRunner
from astar import AStar


def hybrid_navigation(maze, start, goal, dynamic_walls):
    """
    Hybrid navigation strategy combining Q-Learning and A* Search.
    
    :param maze: The maze grid.
    :param start: The starting position.
    :param goal: The goal position.
    :param dynamic_walls: Dictionary of dynamic wall triggers and target positions.
    :return: Path taken by the agent to reach the goal.
    """
    # Initialize components
    runner = MazeRunner(maze, start, goal)
    astar = AStar(maze, start, goal)
    runner.initialize_q_table()

    # Maintain partial observability
    visited_cells = set()
    triggered_walls = set()

    # Start hybrid navigation
    state = start
    path = []
    max_steps = len(maze) * len(maze[0]) * 2  # Prevent infinite loops

    for step in range(max_steps):
        path.append(state)
        visited_cells.add(state)

        # Apply dynamic changes to the maze
        maze, changes_made = apply_dynamic_wall_changes(maze, dynamic_walls, visited_cells, triggered_walls)
        if changes_made:
            print("Dynamic wall changes applied. Recalculating paths...")

        # Decide whether to use Q-Learning or A* based on the environment's state
        if len(visited_cells) > 0.5 * (len(maze) * len(maze[0])) or changes_made:
            # If the environment is dynamic or partially observable, use Q-Learning
            action = runner.choose_action(state)
            next_state = runner.get_next_state(state, action)
            reward = runner.get_reward(state, next_state)
            runner.update_q_value(state, action, reward, next_state)
        else:
            # Use A* for precise pathfinding in known areas
            astar_path = astar.a_star_with_dynamic_changes(dynamic_walls, visited_cells)
            if astar_path is not None:
                return astar_path

        # Update state
        state = next_state
        if state == goal:
            path.append(goal)
            break

    return path


def test_astar(maze, start, goal):
    """Test A* search on the maze."""
    astar = AStar(maze, start, goal)
    path = astar.a_star_search()
    print("Path found by A* search:", path)

def main():
    # Load the maze and dynamic walls
    csv_file = "csv/maze.csv"
    dynamic_file = "csv/dynamic_walls.txt"

    maze = load_maze(csv_file)
    dynamic_walls = load_dynamic_walls(dynamic_file)

    # Find the start ('S') and goal ('E') positions
    start = None
    goal = None
    for i in range(maze.shape[0]):
        for j in range(maze.shape[1]):
            if maze[i, j] == 'S':  # Start position
                start = (i, j)
            if maze[i, j] == 'E':  # Goal position
                goal = (i, j)

    if start is None or goal is None:
        print("Error: Start ('S') or Goal ('E') position not defined in the maze.")
        return

    # Convert maze to numeric format
    maze_numeric = np.where(maze == 'S', 0, maze)
    maze_numeric = np.where(maze_numeric == 'E', 0, maze_numeric)
    maze_numeric = np.where(maze_numeric == 'G', -1, maze_numeric)  # Griever is -1

    # Run the hybrid navigation strategy
    path = hybrid_navigation(maze_numeric.astype(int), start, goal, dynamic_walls)
    print("Hybrid Path:", path)

if __name__ == "__main__":
    main()

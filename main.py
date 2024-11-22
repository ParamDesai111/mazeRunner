import numpy as np
from mazeParser import load_maze, load_dynamic_walls, visualize_maze, visualize_maze_live
from qlearning import MazeRunner
from astar import AStar

def test_astar(maze, start, goal):
    """Test A* search on the maze."""
    astar = AStar(maze, start, goal)
    path = astar.a_star_search()
    print("Path found by A* search:", path)

def parse_grievers(maze):
    """Identify the initial positions of grievers in the maze."""
    grievers = []
    for i in range(maze.shape[0]):
        for j in range(maze.shape[1]):
            if maze[i, j] == -1:  # Griever positions are marked as -1
                grievers.append((i, j))
    return grievers



def main():
    # csv_file = "csv/maze3.csv"
    # dynamic_file = "csv/dynamic_walls3.txt"
    csv_file = "csv/maze.csv"
    dynamic_file = "csv/dynamic_walls.txt"

    maze = load_maze(csv_file)
    dynamic_walls = load_dynamic_walls(dynamic_file)
    print("dynamic_walls:", dynamic_walls)

    visualize_maze(maze, dynamic_walls)

    start = None
    goal = None
    for i in range(maze.shape[0]):
        for j in range(maze.shape[1]):
            if maze[i, j] == 'S':
                start = (i, j)
            if maze[i, j] == 'E':
                goal = (i, j)

    if start is None or goal is None:
        print("Error: Start ('S') or Goal ('E') position not defined in the maze.")
        return

    maze_numeric = np.where(maze == 'S', 0, maze)
    maze_numeric = np.where(maze_numeric == 'E', 0, maze_numeric)
    maze_numeric = np.where(maze_numeric == 'G', -1, maze_numeric)

    print("Maze:" + str(maze_numeric))
    grievers = parse_grievers(maze_numeric)
    print("Grievers:", grievers)
    runner = MazeRunner(maze_numeric.astype(int), start, goal)
    runner.initialize_q_table()
    runner.train(episodes=1000, dynamic_walls=dynamic_walls, grievers=grievers)
    path = runner.find_path()
    print("Path found by Q-Learning:", path)
    # Visualize the maze with the Q-Learning path
    visualize_maze_live(maze, path, dynamic_walls, grievers)

    # # A* with dynamic adjustments
    # print("Testing A* with Dynamic Walls:")
    # astar = AStar(maze_numeric.astype(int), start, goal)
    # visited_cells = set()
    # astar_path = astar.a_star_with_dynamic_changes(dynamic_walls, visited_cells)
    # # astar_path = test_astar(maze_numeric.astype(int), start, goal)
    # print("Path found by A*:", astar_path)

if __name__ == "__main__":
    main()
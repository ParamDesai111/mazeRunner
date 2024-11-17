import numpy as np
from mazeParser import load_maze, load_dynamic_walls, visualize_maze
from qlearning import MazeRunner
from astar import AStar

def test_astar(maze, start, goal):
    """Test A* search on the maze."""
    astar = AStar(maze, start, goal)
    path = astar.a_star_search()
    print("Path found by A* search:", path)

import numpy as np
from mazeParser import load_maze, load_dynamic_walls, visualize_maze
from qlearning import MazeRunner
from astar import AStar

def main():
    # Load the maze and dynamic walls
    csv_file = "csv/mazeDynamic.csv"
    dynamic_file = "csv/dynamic_walls.txt"

    maze = load_maze(csv_file)
    dynamic_walls = load_dynamic_walls(dynamic_file)

    # Visualize the maze
    visualize_maze(maze, dynamic_walls)

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

    # Convert maze to numeric format for Q-learning and A*
    maze_numeric = np.where(maze == 'S', 0, maze)
    maze_numeric = np.where(maze_numeric == 'E', 0, maze_numeric)
    maze_numeric = np.where(maze_numeric == 'G', -1, maze_numeric)  # Griever is -1

    # # Q-Learning with dynamic adjustments
    print("Testing Q-Learning with Dynamic Walls:")
    runner = MazeRunner(maze_numeric.astype(int), start, goal)
    runner.initialize_q_table()
    runner.train(episodes=1000, dynamic_walls=dynamic_walls)
    qlearning_path = runner.find_path()
    print("Path found by Q-Learning:", qlearning_path)

    # A* with dynamic adjustments
    print("Testing A* with Dynamic Walls:")
    astar = AStar(maze_numeric.astype(int), start, goal)
    visited_cells = set()
    astar_path = astar.a_star_with_dynamic_changes(dynamic_walls, visited_cells)
    # astar_path = test_astar(maze_numeric.astype(int), start, goal)
    print("Path found by A*:", astar_path)

if __name__ == "__main__":
    main()


# TODO: add more test cases to see both of the algos running
# TODO: add dynamic walls to the maze, and test the algorithms with dynamic walls
    # ! Dynamic walls are a little bit tricky with how to implement them so we might need to go back to the drawing board
    # ! and think about how to implement them in some way that makes sense
# TODO: we need to combine the both searches after to find the most optimal path after the dynamic changes, rn they both
    # run independently with the same output.
# TODO: we will need to change the visualizer to pygame or tkinter cuz i checked and matplotlib is not good for real time updates when we show the runner moving
# TODO: Grievers will only have one thing (if close to the runner reward -1000 so it never takes that path)

# TODO: add more test cases to see both of the algos running
# TODO: add dynamic walls to the maze, and test the algorithms with dynamic walls
    # ! Dynamic walls are a little bit tricky with how to implement them so we might need to go back to the drawing board
    # ! and think about how to implement them in some way that makes sense
# TODO: we need to combine the both searches after to find the most optimal path after the dynamic changes, rn they both
    # run independently with the same output.
# TODO: we will need to change the visualizer to pygame or tkinter cuz i checked and matplotlib is not good for real time updates when we show the runner moving
# TODO: Grievers will only have one thing (if close to the runner reward -1000 so it never takes that path)
import numpy as np
from mazeParser import load_maze, load_dynamic_walls, visualize_maze, visualize_maze_live
from qlearning import MazeRunner
import tkinter as tk
from tkinter import filedialog, messagebox

def parse_grievers(maze):
    grievers = []
    for i in range(maze.shape[0]):
        for j in range(maze.shape[1]):
            if maze[i, j] == -1:
                grievers.append((i, j))
    return grievers

class FileSelectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Runner File Selector")
        self.root.geometry("800x800")
        self.root.resizable(False, False)

        # Labels and buttons
        self.maze_label = tk.Label(root, text="Maze File: Not Selected", wraplength=300, anchor="w")
        self.maze_label.pack(pady=10, fill="x")

        self.maze_button = tk.Button(root, text="Select Maze CSV", command=self.select_maze_file, width=20)
        self.maze_button.pack(pady=5)

        self.dynamic_label = tk.Label(root, text="Dynamic Walls File: Not Selected", wraplength=300, anchor="w")
        self.dynamic_label.pack(pady=10, fill="x")

        self.dynamic_button = tk.Button(root, text="Select Dynamic Walls File", command=self.select_dynamic_file, width=20)
        self.dynamic_button.pack(pady=5)

        self.run_button = tk.Button(root, text="Run Simulation", command=self.run_simulation, state="disabled", width=20)
        self.run_button.pack(pady=20)

        # Variables to store file paths
        self.maze_file = None
        self.dynamic_file = None

    def select_maze_file(self):
        """Select the maze CSV file."""
        file_path = filedialog.askopenfilename(
            title="Select Maze CSV File",
            filetypes=[("CSV Files", "*.csv")]
        )
        if file_path:
            self.maze_file = file_path
            self.maze_label.config(text=f"Maze File: {file_path}")
            self.check_ready()

    def select_dynamic_file(self):
        """Select the dynamic walls file."""
        file_path = filedialog.askopenfilename(
            title="Select Dynamic Walls File",
            filetypes=[("Text Files", "*.txt")]
        )
        if file_path:
            self.dynamic_file = file_path
            self.dynamic_label.config(text=f"Dynamic Walls File: {file_path}")
            self.check_ready()

    def check_ready(self):
        """Enable the Run Simulation button if both files are selected."""
        if self.maze_file and self.dynamic_file:
            self.run_button.config(state="normal")
    def run_simulation(self):
        try:
            maze = load_maze(self.maze_file)
            dynamic_walls = load_dynamic_walls(self.dynamic_file)
            print("dynamic_walls:", dynamic_walls)

            # visualize_maze(maze, dynamic_walls)

            start = None
            goal = None
            for i in range(maze.shape[0]):
                for j in range(maze.shape[1]):
                    if maze[i, j] == 'S':
                        start = (i, j)
                    if maze[i, j] == 'E':
                        goal = (i, j)

            if start is None or goal is None:
                messagebox.showerror("Error", "Start ('S') or Goal ('E') position not defined in the maze.")
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
            runner.train(episodes=10000, dynamic_walls=dynamic_walls, grievers=grievers)
            path = runner.find_path()
            print("Path found by Q-Learning:", path)
            # Visualize the maze with the Q-Learning path
            visualize_maze_live(maze, path, dynamic_walls, grievers)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            print(e)

def main():
    root = tk.Tk()
    app = FileSelectorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
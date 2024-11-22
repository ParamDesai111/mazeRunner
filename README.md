
# Maze Runner Project: README

## Overview
The Maze Runner project is a Python-based application to solve dynamic mazes using artificial intelligence techniques. It employs Q-learning, artificial life for dynamic wall updates, and rule-based systems for moving obstacles (grievers) to challenge the maze-solving capabilities of an agent.

---

## Files and Their Purpose

1. **`mazeParser.py`**:
   - **Purpose**: 
     - Handles loading, parsing, and visualizing mazes.
     - Manages dynamic wall changes during the simulation.
   - **Key Functions**:
     - `load_maze`: Loads a maze from a CSV file.
     - `load_dynamic_walls`: Loads dynamic wall configurations.
     - `visualize_maze`: Visualizes the static maze.
     - `apply_dynamic_wall_changes`: Updates maze structure based on dynamic walls.

2. **`qlearning.py`**:
   - **Purpose**: Implements the Q-learning algorithm to train the agent to solve the maze.
   - **Key Classes**:
     - `MazeRunner`:
       - Initializes and trains a Q-table for decision-making.
       - Simulates agent movements and computes rewards based on maze dynamics.
     - Key methods include:
       - `train`: Trains the agent using Q-learning with dynamic wall and griever interactions.
       - `find_path`: Extracts the optimal path after training.

3. **`main.py`**:
   - **Purpose**: Acts as the entry point for the application.
   - **Key Features**:
     - Provides a GUI for selecting input files (maze and dynamic walls).
     - Runs the simulation by integrating maze visualization, Q-learning, and live updates.
     - Combines and executes functionalities from other modules.

4. **`grievers.py`**:
   - **Purpose**: Handles the behavior of moving obstacles (grievers) in the maze with rule based systems.
   - **Key Function**:
     - `update_griever_positions`: Dynamically updates griever positions while ensuring valid moves within the maze.

---

## Setting Up the Environment (macOS)

1. **Prerequisites**:
   - Python 3.8 or newer.
   - `pip` for package management.


2. **Install Required Libraries**:
   Open a terminal and run the following commands
   - `brew install python-tk@3.12`
     - To install tkinter
     - Run `python -m tkinter` to check if tkinter is installed
   - `pip install -r requirements.txt`
     - To install all of the dependencies for the application

3. **Running the Application**:
   - Open the terminal and navigate to the directory containing the project files:
     ```bash
     cd /path/to/main.py
     ```
   - Start the application:
     ```bash
     python main.py
     ```
   - Use the GUI to select the maze and dynamic walls input files.

---

## Artificial Intelligence Techniques Used

1. **Q-Learning**:
   - A model-free reinforcement learning algorithm.
   - Updates a Q-table with state-action pairs to learn an optimal policy.
   - Exploits a reward system to guide the agent towards the goal while avoiding grievers and walls.

2. **Artificial Life**:
   - Simulates dynamic walls that change the maze structure during the simulation based on triggers.
   - Creates evolving and adaptive behaviors in the environment.

3. **Rule-Based Systems**:
   - Governs the movement of grievers using predefined rules.
   - Ensures grievers move in a predictable yet dynamic fashion within the maze.

4. **Exploration vs. Exploitation**:
   - Implements an epsilon-greedy strategy to balance exploring new paths and exploiting known rewards.

5. **Pathfinding Assistance**:
   - Employs heuristic rewards to encourage movements closer to the goal.

---

This project demonstrates the integration of reinforcement learning with artificial life and rule-based systems, making it suitable for exploring AI techniques in adaptive environments. Enjoy the challenge of solving dynamic mazes!

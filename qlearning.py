import numpy as np
import random
from mazeParser import apply_dynamic_wall_changes
from astar import AStar
from grievers import update_griever_positions


class MazeRunner:
    def __init__(self, maze, start, goal):
        self.maze = maze
        self.start = start
        self.goal = goal
        self.q_table = {}
        self.actions = ['up', 'down', 'left', 'right']
        self.alpha = 0.01  # Learning rate
        self.gamma = 0.9  # Discount factor
        self.epsilon = 0.2  # Exploration rate

    def is_valid_move(self, state, action):
        """Check if the move is valid."""
        x, y = state
        if action == 'up': x -= 1
        elif action == 'down': x += 1
        elif action == 'left': y -= 1
        elif action == 'right': y += 1

        # Check boundaries and ensure the cell is not a wall
        if 0 <= x < self.maze.shape[0] and 0 <= y < self.maze.shape[1]:
            if self.maze[x, y] != 1:  # Walls are explicitly excluded
                return True
        return False

    def get_next_state(self, state, action):
        """Get the next state based on the action."""
        x, y = state
        if action == 'up': x -= 1
        elif action == 'down': x += 1
        elif action == 'left': y -= 1
        elif action == 'right': y += 1
        if self.is_valid_move(state, action):  # Ensure the move is valid
            return (x, y)
        return state  # Return the current state if the move is invalid

    def get_reward(self, state, next_state):
        """Reward function for the agent."""
        if next_state == self.goal:
            return 100  # Reached goal
        elif self.maze[next_state] == -1:  # Griever penalty
            return -40
        elif self.maze[next_state] == 1:  # Wall penalty
            return -50
        else:
            # Encourage moving closer to the goal
            dist_before = abs(state[0] - self.goal[0]) + abs(state[1] - self.goal[1])
            dist_after = abs(next_state[0] - self.goal[0]) + abs(next_state[1] - self.goal[1])
            return 15 if dist_after < dist_before else -1  # Reward closer moves, penalize further ones

    def initialize_q_table(self):
        """Initialize the Q-table."""
        for i in range(self.maze.shape[0]):
            for j in range(self.maze.shape[1]):
                if self.maze[i, j] != 1:  # Not a wall
                    self.q_table[(i, j)] = {action: 0 for action in self.actions}

    def choose_action(self, state):
        """Choose an action using epsilon-greedy strategy."""
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(self.actions)  # Explore
        return self.choose_best_action(state)  # Exploit

    # def choose_best_action(self, state):
    #     """Choose the best action based on the learned Q-values."""
    #     return max(self.q_table[state], key=self.q_table[state].get)
    def choose_best_action(self, state):
        """Choose the best action based on the learned Q-values."""
        if state not in self.q_table:
            print(f"State {state} not in Q-table. Choosing random action.")
            return random.choice(self.actions)  # Fall back to exploration
        return max(self.q_table[state], key=self.q_table[state].get)


    def update_q_value(self, state, action, reward, next_state):
        """Update the Q-value for the given state-action pair."""
        max_next_q = max(self.q_table[next_state].values()) if next_state in self.q_table else 0
        self.q_table[state][action] += self.alpha * (reward + self.gamma * max_next_q - self.q_table[state][action])

    # def train(self, episodes, dynamic_walls):
    #     """Train the agent using Q-learning with dynamic wall updates."""
    #     visited_cells = set()
    #     triggered_walls = set()
        
    #     for episode in range(episodes):
    #         state = self.start
    #         steps = 0
    #         self.epsilon = max(0.1, 1 - episode / episodes)  # Gradually decrease exploration rate
            
    #         while state != self.goal:
    #             visited_cells.add(state)

    #             # Apply dynamic changes based on visited cells
    #             self.maze, changes_made = apply_dynamic_wall_changes(
    #                 self.maze, dynamic_walls, visited_cells, triggered_walls
    #             )
    #             if changes_made:
    #                 print(f"Episode {episode}: Maze updated due to dynamic walls.")
    #                 # Reinitialize Q-values for affected states
    #                 for i, j in dynamic_walls.values():
    #                     if (i, j) in self.q_table:
    #                         del self.q_table[(i, j)]

    #             # Ensure Q-values exist for the current state
    #             if state not in self.q_table:
    #                 self.q_table[state] = {action: 0 for action in self.actions}

    #             action = self.choose_action(state)
    #             if not self.is_valid_move(state, action):
    #                 continue

    #             next_state = self.get_next_state(state, action)

    #             if next_state == state:  # Detect stuck state
    #                 break

    #             reward = self.get_reward(state, next_state)
    #             self.update_q_value(state, action, reward, next_state)

    #             state = next_state
    #             steps += 1

    #             # Prevent infinite loops by limiting steps per episode
    #             if steps > 1000:
    #                 print(f"Episode {episode}: Too many steps. Ending episode.")
    #                 break

    def train(self, episodes, dynamic_walls, grievers):
        """Train the agent using Q-learning with dynamic wall and griever updates."""
        visited_cells = set()
        triggered_walls = set()

        for episode in range(episodes):
            state = self.start
            steps = 0
            self.epsilon = max(0.1, 1 - episode / episodes)  # Gradually decrease exploration rate

            while state != self.goal:
                visited_cells.add(state)

                # Apply dynamic wall changes
                self.maze, changes_made = apply_dynamic_wall_changes(
                    self.maze, dynamic_walls, visited_cells, triggered_walls
                )
                if changes_made:
                    print(f"Episode {episode}: Maze updated due to dynamic walls.")

                # Update griever positions
                grievers = update_griever_positions(grievers, self.maze)

                # Ensure Q-values exist for the current state
                if state not in self.q_table:
                    self.q_table[state] = {action: 0 for action in self.actions}

                action = self.choose_action(state)
                next_state = self.get_next_state(state, action)

                # Avoid states with grievers
                if next_state in grievers:
                    continue  # Retry a different action if next state is occupied by a griever

                reward = self.get_reward(state, next_state)
                self.update_q_value(state, action, reward, next_state)

                state = next_state
                steps += 1

                # Prevent infinite loops by limiting steps per episode
                if steps > 1000:
                    print(f"Episode {episode}: Too many steps. Ending episode.")
                    break


    def find_path(self):
        """Find the optimal path using the learned Q-table."""
        path = []
        state = self.start
        steps = 0

        while state != self.goal:
            path.append(state)

            if state not in self.q_table:
                print(f"State {state} not in Q-table. No path found.")
                return "No path found."

            action = self.choose_best_action(state)
            next_state = self.get_next_state(state, action)

            if next_state == state:  # Detect stuck state
                print(f"Stuck at {state}. No further moves possible.")
                return "No path found."

            state = next_state
            steps += 1

            # Prevent infinite loops
            if steps > 1000:
                print("Too many steps. No path found.")
                return "No path found."

        path.append(self.goal)
        return path


# Example Usage
# maze = np.array([
#     ['S', 0, 1, 1, 1, 0, 0],
#     [1, 0, 1, 'G', 0, 1, 1],
#     [1, 0, 0, 0, 0, 1, 0],
#     [1, 1, 1, 0, 1, 1, 0],
#     [0, 0, 1, 0, 0, 0, 'E']
# ])

# maze = np.array([
#     [0, 0, 1, 1, 1, 0, 0],  # Use integers for walls (1) and paths (0)
#     [1, 0, 1, -1, 0, 1, 1],  # Use -1 for grievers
#     [1, 0, 0, 0, 0, 1, 0],
#     [1, 1, 1, 0, 0, 1, 0],
#     [0, 0, 1, -1, 0, 0, 0]    # Goal is at (4, 6)
# ])

# start = (0, 1)  # Starting position
# goal = (4, 6)  # Goal position

# maze = np.array([
#     [1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0],
#     [1, 0, 1, -1, 0, 1, 1, 1, 0, 1, 1, 1, 0],
#     [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
#     [1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
#     [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1],
#     [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0],
#     [0, 0, 0, 0, 0, 1, 0, -1, 0, 0, 0, 0, 0],
#     [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0],
#     [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
#     [1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
# ])

# start = (1, 1)  # Starting position
# goal = (11, 12)  # Goal position


# runner = MazeRunner(maze, start, goal)
# runner.initialize_q_table()
# runner.train(episodes=100000)

# path = runner.find_path()
# print("Path taken by the Maze Runner:", path)
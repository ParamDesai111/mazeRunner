import numpy as np
import random
from mazeParser import apply_dynamic_wall_changes

class MazeRunner:
    def __init__(self, maze, start, goal):
        self.maze = maze
        self.start = start
        self.goal = goal
        self.q_table = {}
        self.actions = ['up', 'down', 'left', 'right']
        self.alpha = 0.1  # Learning rate
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
            return -100
        elif self.maze[next_state] == 1:  # Wall penalty
            return -10
        else:
            # Encourage moving closer to the goal
            dist_before = abs(state[0] - self.goal[0]) + abs(state[1] - self.goal[1])
            dist_after = abs(next_state[0] - self.goal[0]) + abs(next_state[1] - self.goal[1])
            return 10 if dist_after < dist_before else -1  # Reward closer moves, penalize further ones

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

    def choose_best_action(self, state):
        """Choose the best action based on the learned Q-values."""
        return max(self.q_table[state], key=self.q_table[state].get)

    def update_q_value(self, state, action, reward, next_state):
        """Update the Q-value for the given state-action pair."""
        max_next_q = max(self.q_table[next_state].values()) if next_state in self.q_table else 0
        self.q_table[state][action] += self.alpha * (reward + self.gamma * max_next_q - self.q_table[state][action])

    # def train(self, episodes):
    #     """Train the agent using Q-learning."""
    #     for episode in range(episodes):
    #         state = self.start
    #         while state != self.goal:
    #             action = self.choose_action(state)
    #             if not self.is_valid_move(state, action):
    #                 continue
    #             next_state = self.get_next_state(state, action)
    #             reward = self.get_reward(state, next_state)
    #             self.update_q_value(state, action, reward, next_state)
    #             state = next_state
    def train(self, episodes, dynamic_walls):
        """Train the agent using Q-learning with dynamic wall updates."""
        visited_cells = set()  # Track visited cells
        triggered_walls = set()  # Track triggered walls to prevent re-triggering

        for episode in range(episodes):
            state = self.start
            while state != self.goal:
                visited_cells.add(state)  # Mark the cell as visited
                
                # Apply dynamic changes based on visited cells
                self.maze, changes_made = apply_dynamic_wall_changes(
                    self.maze, dynamic_walls, visited_cells, triggered_walls
                )
                if changes_made:
                    print(f"Episode {episode}: Maze updated due to dynamic walls.")

                action = self.choose_action(state)
                if not self.is_valid_move(state, action):
                    continue

                next_state = self.get_next_state(state, action)
                reward = self.get_reward(state, next_state)
                self.update_q_value(state, action, reward, next_state)
                state = next_state

                # Debugging log for the current state, action, and reward
                # print(f"Episode {episode}: State {state}, Action {action}, Reward {reward}")



    def find_path(self):
        """Find the optimal path using the learned Q-table."""
        path = []
        state = self.start
        while state != self.goal:
            path.append(state)
            action = self.choose_best_action(state)  # Exploit learned Q-values
            next_state = self.get_next_state(state, action)
            if next_state == state:  # Stuck, no valid moves
                break
            state = next_state
        if state == self.goal:
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

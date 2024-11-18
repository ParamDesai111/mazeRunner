import numpy as np

class Griever:
    def __init__(self, position):
        """
        Initialize a griever at the given position.
        :param position: Tuple (x, y) indicating the griever's starting position.
        """
        self.position = position

    def detect_agent(self, agent_position):
        """
        Check if the agent is within a one-block radius of the griever.
        :param agent_position: Tuple (x, y) of the agent's position.
        :return: True if the agent is within a one-block radius, else False.
        """
        ax, ay = agent_position
        gx, gy = self.position
        # print(f"Agent at {agent_position}, Griever at {self.position}")
        # print(f"Distance: {abs(ax - gx)}, {abs(ay - gy)}")
        return abs(ax - gx) <= 1 and abs(ay - gy) <= 1

    def move(self, maze):
        """
        Move the griever one block left or right if there's open space.
        :param maze: The maze grid.
        """
        x, y = self.position
        # Try to move right
        if y + 1 < maze.shape[1] and maze[x, y + 1] == 0:
            self.position = (x, y + 1)
            # print(f"Griever moved to {self.position}")
        # Else, try to move left
        elif y - 1 >= 0 and maze[x, y - 1] == 0:
            self.position = (x, y - 1)
            # print(f"Griever moved to {self.position}")

    def apply_penalty(self, agent_position, reward):
        """
        Apply a penalty if the agent is within range.
        :param agent_position: Tuple (x, y) of the agent's position.
        :param reward: Current reward of the agent.
        :return: Updated reward.
        """
        if self.detect_agent(agent_position):
            print(f"Griever detected agent at {agent_position}. Applying penalty.")
            reward -= 1000  # Penalty value
        return reward

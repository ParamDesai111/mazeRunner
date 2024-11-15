import heapq

class AStar:
    def __init__(self, maze, start, goal):
        self.maze = maze
        self.start = start
        self.goal = goal
        self.rows = maze.shape[0]
        self.cols = maze.shape[1]

    def is_valid_move(self, x, y):
        """Check if the move is valid (within bounds and not a wall)."""
        return 0 <= x < self.rows and 0 <= y < self.cols and self.maze[x, y] != 1

    def get_neighbors(self, node):
        """Get valid neighbors of the current node."""
        x, y = node
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
        neighbors = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if self.is_valid_move(nx, ny):
                neighbors.append((nx, ny))
        return neighbors

    def heuristic(self, node):
        """Calculate the Manhattan distance heuristic."""
        x, y = node
        gx, gy = self.goal
        return abs(x - gx) + abs(y - gy)

    def a_star_search(self):
        """Perform A* search to find the shortest path."""
        open_set = []
        heapq.heappush(open_set, (0 + self.heuristic(self.start), 0, self.start))  # (f, g, node)
        came_from = {}  # To reconstruct the path
        g_score = {self.start: 0}
        f_score = {self.start: self.heuristic(self.start)}

        while open_set:
            _, current_g, current = heapq.heappop(open_set)

            if current == self.goal:
                return self.reconstruct_path(came_from, current)

            for neighbor in self.get_neighbors(current):
                tentative_g_score = g_score[current] + 1  # Assuming uniform cost for each move
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor)
                    heapq.heappush(open_set, (f_score[neighbor], tentative_g_score, neighbor))

        return None  # No path found

    def reconstruct_path(self, came_from, current):
        """Reconstruct the path from the start to the goal."""
        path = []
        while current in came_from:
            path.append(current)
            current = came_from[current]
        path.append(self.start)
        path.reverse()
        return path

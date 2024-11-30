import random

def update_griever_positions(grievers, maze):
    new_positions = []
    for griever in grievers:
        x, y = griever
        possible_moves = []
        if y > 0 and maze[x, y - 1] == 0:  # Check if left is walkable
            possible_moves.append((x, y - 1))
        if y < maze.shape[1] - 1 and maze[x, y + 1] == 0:  # Check if right is walkable
            possible_moves.append((x, y + 1))
        
        if possible_moves:
            # Randomly choose between left and right
            new_position = random.choice(possible_moves)
            maze[x, y] = 0  # Clear old position
            maze[new_position] = -1  # Mark new position
            new_positions.append(new_position)
        else:
            # Stay in place if no valid moves
            new_positions.append((x, y))
    
    return new_positions


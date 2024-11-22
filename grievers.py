import random

def update_griever_positions(grievers, maze):
    directions = ['left', 'right']
    new_positions = []
    for griever in grievers:
        x, y = griever
        random.shuffle(directions)
        moved = False
        for direction in directions:
            nx, ny = x, y
            if direction == 'left': ny -= 1
            elif direction == 'right': ny += 1
            
            # Ensure new position is valid and walkable (not a wall or another griever)
            if (
                0 <= nx < maze.shape[0]
                and 0 <= ny < maze.shape[1]
                and maze[nx, ny] == 0  # Walkable space
            ):
                new_positions.append((nx, ny))
                maze[x, y] = 0  # Clear old position
                maze[nx, ny] = -1  # Mark new position with griever value (-1)
                moved = True
                print(f"Griever at position {griever} moved to ({nx}, {ny})")
                break
        if not moved:  # If no valid moves, stay in place
            new_positions.append(griever)
            print(f"Griever at position {griever} is stuck!")
    return new_positions

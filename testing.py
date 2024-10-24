import random
from collections import deque

def generate_bomb_positions(width, height, num_bombs):
    # Calculate number of empty cells
    num_empty = width * height - num_bombs
    
    # Initialize grid with all cells set to bombs (-1)
    grid = [[-1 for _ in range(width)] for _ in range(height)]

    # Start from a random central point
    start_row, start_col = height // 2, width // 2
    grid[start_row][start_col] = 0  # Mark as empty

    # BFS to expand empty cells outwards
    queue = deque([(start_row, start_col)])
    empty_cells = [(start_row, start_col)]
    
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    
    while queue and len(empty_cells) < num_empty:
        row, col = queue.popleft()
        
        # Shuffle directions to maintain randomness
        random.shuffle(directions)
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < height and 0 <= new_col < width and grid[new_row][new_col] == -1:
                grid[new_row][new_col] = 0  # Mark as empty
                empty_cells.append((new_row, new_col))
                queue.append((new_row, new_col))
                if len(empty_cells) >= num_empty:
                    break

    # Gather bomb positions
    bomb_positions = [(r, c) for r in range(height) for c in range(width) if grid[r][c] == -1]
    
    # Shuffle bomb positions to ensure randomness
    random.shuffle(bomb_positions)

    return grid

def print_board(grid):
    # Print the board with `.` for empty cells and `B` for bombs
    for row in grid:
        row_str = ""
        for cell in row:
            if cell == -1:
                row_str += " B"
            else:
                row_str += " ."
        print(row_str)
    print()  # Add an empty line for better readability

# Example usage
width, height, num_bombs = 5, 5, 10
grid = generate_bomb_positions(width, height, num_bombs)
print_board(grid)

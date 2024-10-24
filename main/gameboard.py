class Gameboard:
    def __init__(self, width, height, num_bombs, default_value):
        self.width = width
        self.height = height
        self.num_bombs = num_bombs
        self.board = [[default_value.copy() for _ in range(width)] for _ in range(height)]

    def _validate_pos(self, pos: tuple):
        if len(pos) != 2 or not isinstance(pos, tuple):
            raise ValueError(f"Invalid Position Format: {pos}")
        x, y = pos
        if not (0 <= x < self.width) or not (0 <= y < self.height):
            raise IndexError(f"Position Out of Bounds: {pos}")
        return True

    def __getitem__(self, pos: tuple):
        self._validate_pos(pos)
        x, y = pos
        return self.board[y][x]

    def __setitem__(self, pos: tuple, value):
        self._validate_pos(pos)
        x, y = pos
        self.board[y][x] = value

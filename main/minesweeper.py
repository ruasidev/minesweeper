import random
from gameboard import Gameboard

class Minesweeper:
    def __init__(self):
        self.gameboard = None
        self.seed = None
        self.bomb_val = 9
        self.cell_struct = {"value": 0, "visibility": False, "flagged": False} # data structure of each cell
    
    # indices for each cell for readability
    VALUE, VISIBILITY, FLAGGED = 0, 1, 2


    # ----------------------------- BOARD GENERATION -----------------------------
    # assign values to self.gameboard (no return)
    # if not seed, generate with normal generation methods
    # already happens in constructor, but used if you need to regenerate the board
    def generate_board(self, width=0, height=0, num_bombs=0, seed=None) -> None: 
        if seed:
            raise NotImplementedError
            self._decompile_seed(seed) 
            return
        self.gameboard = Gameboard(width, height, num_bombs, list(self.cell_struct.values()))


    # TODO: This method sucks really bad rn
    # {exclude} should exclude a bomb position from being generated (not implemented)
    # called by generate_board internally
    # returns list of random bomb positions [(x1, y1), (x2, y2), (x3, y3)...]
    # this should be as efficient as possible
    def _generate_bomb_positions(self, exclude: tuple = None, exclude_adjacent = False) -> list:
        gameboard_area = self.gameboard.height*self.gameboard.width
        available_bomb_spaces = gameboard_area-self.gameboard.num_bombs
        exclusions = []
        def convert_to_sample(pos):
            return self.gameboard.width*pos[1] + pos[0]
        if exclude_adjacent and not exclude:
            print(f"_generate_bomb_positions({exclude}, {exclude_adjacent}) : Missing initial exclusion position")
        if exclude_adjacent: exclusions = [convert_to_sample(pos) for pos in self._get_adjacent_relatives(exclude)]
        if exclude: exclusions.append(convert_to_sample(exclude))

        if available_bomb_spaces < 0:
            print(f"_generate_bomb_positions({exclude}) : Bomb count exceeds available bomb cells")
            return []
        population = [value for value in range(gameboard_area) if value not in exclusions]
        positions = []
        # if the range is like 20 and exclude is 5, sample should be of range()
        random_position_sample = random.sample(population, self.gameboard.num_bombs) # list

        for value in random_position_sample:
            x_pos = value % self.gameboard.width
            y_pos = value // self.gameboard.width
            positions.append((x_pos, y_pos))
        return positions
    
    # assigns ALL bombs on the board via positions given by generate_bomb_positions()
    def place_bombs(self, exclude=None, exclude_adjacent=False) -> None:
        positions = self._generate_bomb_positions(exclude, exclude_adjacent)
        for pos in positions:
            self.gameboard[pos][self.VALUE] = self.bomb_val
    
    # generates and assigns the values for all cells based on bomb adjacency 
    # called by generate_board() internally
    def assign_vals(self, validate=False) -> None:
        for y in range(self.gameboard.height):
            for x in range(self.gameboard.width):
                pos = (x, y)
                if self.get_cell_value(pos) == self.bomb_val:    # skip bomb cells
                    continue
                num_adj_bombs = len(self._get_adjacent_relatives(pos, self.bomb_val))
                self.gameboard[pos][self.VALUE] = num_adj_bombs
                if validate:
                    num_adj_cells = len(self._get_adjacent_relatives(pos))
                    if num_adj_cells == num_adj_bombs:
                        print(f"[WARN] Detected surrounded safe cell at {pos}")
    
    # TODO
    # generates and returns a unique seed based on:
    # - values of the bomb positions
    # - width and height of the board (order matters)
    # - number of bombs
    # allows us to compact a board into a seed and regenerate based on that
    # this will require a lot of thought and math
    def _compile_seed(self) -> int:
        raise NotImplementedError
        pass
    
    # generates a board based on a required seed (just do in generate_board?)
    def _decompile_seed(self, seed: int):
        raise NotImplementedError
        if not seed:
            print(f"The seed value has not been generated yet! seed: {seed}")
            return None
        

    # ----------------------------- BOARD ACTIONS -----------------------------

    # processes like the user revealed a cell at pos
    # different from board.reveal() in that the game ends if (x, y)
    # performs cascade reveal if pos value is 0
    def click(self, pos: tuple, opening=False) -> None:
        if opening: 
            self.place_bombs(exclude=pos, exclude_adjacent=True)
            self.assign_vals(validate=True)
        if self.get_cell_value(pos) == 0:
            print(f"Cascading from {pos}")
            self._cascade(pos)
        else:
            self.reveal(pos)
    
    # sets the cell at {pos} to visible
    def reveal(self, pos: tuple) -> None:
        if not self.in_bounds(pos):
            print(f"reveal({pos}) : Position is out of bounds")
            return
        self.gameboard[pos][self.VISIBILITY] = True
    

    # sets the cell at {pos} to hidden
    def hide(self, pos: tuple) -> None:
        if not self.in_bounds(pos):
            print(f"hide({pos}) : Position is out of bounds")
            return
        self.gameboard[pos][self.VISIBILITY] = False

    # sets the cell at {pos} to flagged, or not flagged if already flagged
    def flag(self, pos: tuple) -> None:
        self.gameboard[pos][self.FLAGGED] = True if not self.is_flagged(pos) else False


    # ----------------------------- CLASS TOOLS -----------------------------

    # returns a list of the positions of adjacent cells to {pos}
    # if a target is assigned, returns only positions of adjacent cells that match target
    # if no target is assigned, return all positions of all adjacent cells
    def _get_adjacent_relatives(self, pos: tuple, target=None) -> list:
        if not self._is_valid_pos(pos, feedback=False):
            print(f"_get_adjacent_relatives({pos}, {target}) : Invalid Position Argument {pos}")
            return
        ADJACENTS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        adjacent_targets = []
        for a in ADJACENTS:
            adj_pos = (pos[0] + a[0], pos[1] + a[1])
            target_matched = self.in_bounds(adj_pos) and ((self.gameboard[adj_pos][self.VALUE] == target) or target == None)
            if target_matched:
                adjacent_targets.append(adj_pos)
        return adjacent_targets

    # TODO
    # modifies self.gameboard in place
    # if self.gameboard.cell(x, y)
    # cascading cell revealing from cell (x, y)
    # uses _get_adjacent_relatives for this
    # recursive
    def _cascade(self, pos: tuple) -> None:
        if self.is_visible(pos): return
        self.reveal(pos)
        if self.get_cell_value(pos) == 0:
            for position in self._get_adjacent_relatives(pos):
                self._cascade(position)

    # updates the value of a cell at {pos} based on number of bomb cells adjacent
    def update_cell_value(self, pos):
        if self.cell_value(pos) == self.bomb_val:
            return
        self.gameboard[pos][self.VALUE] = len(self._get_adjacent_relatives(pos, self.bomb_val)) 

    # sets the value of a cell at {pos} to {value}
    def set_cell_value(self, pos, value):
        if not self.in_bounds(pos): 
            print(f"set_cell_value({pos}, {value}) : Position not in bounds")
            return
        self.gameboard[pos][self.VALUE] = value

    # returns the value of a given position
    def get_cell_value(self, pos):
        if self.in_bounds(pos):
            return self.gameboard[pos][self.VALUE]
        else:
            print(f"cell_value({pos}) : Position out of bounds")
            return None
    
    # TODO: Works, but structure sucks since _validate_pos() exists in Gameboard
    def _is_valid_pos(self, pos: tuple, feedback=True):
        if len(pos) != 2 or not isinstance(pos, tuple):
            if feedback: print(f"pos {pos} must be a tuple of length 2")
            return False
        if not ((isinstance(pos[0], int) and isinstance(pos[1], int))):
            if feedback: print(f"Expected values x, y in pos to be int. Got: {type(pos[0]), type(pos[1])}")
            return False
        return True

    # True if {pos} exists in self.gameboard, else False
    def in_bounds(self, pos: tuple):
        try:
            self.gameboard[pos]
        except IndexError:
            return False
        return True
    
    # True if cell at {pos} is flagged, else False
    def is_flagged(self, pos: tuple) -> bool:
        return self.gameboard[pos][self.FLAGGED]
    
    # True if cell at {pos} is visible, else False
    def is_visible(self, pos: tuple) -> bool:
        return self.gameboard[pos][self.VISIBILITY]

    # ----------------------------- DEV TOOLS -----------------------------

    # TODO: args aren't implemented yet because i don't feel like it
    def print_board(self, all_visible=False) -> None:
        for y in range(self.gameboard.height):
            for x in range(self.gameboard.width):
                if all_visible:
                    print(self.gameboard[(x, y)][self.VALUE], end=' ')
                else:
                    if not self.gameboard[(x, y)][self.VISIBILITY]:
                        print('-', end=' ')
                    else:
                        print(self.gameboard[(x, y)][self.VALUE], end=' ')
            print()
    
    def print_board_raw(self):
        for row in self.gameboard.board:
            print(row)

    # assigns ONE cell on the board to self.bomb_val
    def place_bomb(self, pos):
        if not self.in_bounds(pos): 
            print(f"place_bomb({pos}) : Position not in bounds")
            return
        self.set_cell_value(pos, self.bomb_val)
        self.update_cell_value(pos)

    # sets the {attribute} of all cells to {value}
    # very open, can set any attribute to whatever you want (can break stuff)
    def set_all_cells(self, attribute, value):
        try:
            for row in self.gameboard.board:
                for col in row:
                    col[attribute] = value
        except IndexError:
            print(f"set_all_cells({attribute}, {value}) : Attribute index {attribute} not found in cells")
        
    # sets all cells to visible
    def reveal_all(self) -> None:
        self.set_all_cells(attribute=self.VISIBILITY, value=True)

    # sets all cells to hidden
    def hide_all(self) -> None:
        self.set_all_cells(attribute=self.VISIBILITY, value=False)

    # ----- for later -----
    # get_state(self) for a serialized version of the board with only the data 
    #   the user should see (don't send clues over the air!)
    # 
    # to_dict() or to_json() for easy integration with front-end API 

# Tools:
# generate_board(width, height, num_bombs)
# click(pos)
# reveal(pos)
# hide(pos)
# flag(pos)
# is_visible(pos)
# is_flagged(pos)

# place_bomb(pos)
# set_all_cells(attribute, value)
# reveal_all()
# hide_all()

# _get_adjacent_relatives(pos, target)
# update_cell_value(pos)
# set_cell_value(pos, value)
# get_cell_value(pos)
# _is_valid_pos(pos)
# in_bounds(pos)

minesweeper = Minesweeper()

print(f'''
MINESWEEPER
Choose a difficulty:
    1: Beginner (8x8)
    2: Intermediate (16x16)
    3: Advanced (16x30)      
''')
level = int(input())
while level not in range(1, 4):
    print('''
Invalid difficulty. Try again.

    1: Beginner (8x8)
    2: Intermediate (16x16)
    3: Advanced (16x30)           
''')

match level:
    case 1:
        minesweeper.generate_board(width=8, height=8, num_bombs=10)
    case 2:
        minesweeper.generate_board(width=16, height=16, num_bombs=40)
    case 3:
        minesweeper.generate_board(width=30, height=16, num_bombs=99)
minesweeper.print_board()
print()
print('Good luck!! Choose a coordinate to make your first move.')
dead = False
opening = True
while not dead:
    x, y = int(input("x: ")), int(input("y: "))
    minesweeper.click((x, y), opening=opening)
    if minesweeper.get_cell_value((x, y)) == minesweeper.bomb_val:
        dead = True
        break
    opening = False
    minesweeper.print_board()
    print()
minesweeper.print_board(all_visible=True)
print(f"\nYou died!!!")


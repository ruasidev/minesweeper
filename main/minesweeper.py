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

        self.place_bombs()
        self.assign_vals(validate=True)

    # TODO: This method sucks really bad rn
    # {exclude} should exclude a bomb position from being generated (not implemented)
    # called by generate_board internally
    # returns list of random bomb positions [(x1, y1), (x2, y2), (x3, y3)...]
    # this should be as efficient as possible
    def _generate_bomb_positions(self, exclude=None) -> list:
        if exclude != None:
            raise NotImplementedError
        positions = []
        # if the range is like 20 and exclude is 5, sample should be of range()
        random_position_sample = random.sample(range(self.gameboard.height * self.gameboard.width), self.gameboard.num_bombs) # list
        
        # fix later:
        #   absolutely fucking horrendous way of implementing this but idc rn (idek if it works)
        if exclude != None and isinstance(exclude, int) and 0 < exclude < self.gameboard.height * self.gameboard.width:
            while exclude in random_position_sample or len(random_position_sample) != self.gameboard.num_bombs:
                random_position_sample[random_position_sample.index(exclude)] = random.choice(self.gameboard.height*self.gameboard.width)

        for value in random_position_sample:
            x_pos = value % self.gameboard.width
            y_pos = value // self.gameboard.width
            positions.append((x_pos, y_pos))
        return positions
    
    # assigns ALL bombs on the board via positions given by generate_bomb_positions()
    def place_bombs(self, exclude=None) -> None:
        positions = self._generate_bomb_positions(exclude)
        for pos in positions:
            self.gameboard[pos][self.VALUE] = self.bomb_val
    
    # generates and assigns the values for all cells based on bomb adjacency 
    # called by generate_board() internally
    def assign_vals(self, validate=False) -> None:
        for y in range(self.gameboard.height):
            for x in range(self.gameboard.width):
                pos = (x, y)
                if self._get_cell_value(pos) == self.bomb_val:    # skip bomb cells
                    continue
                num_adj_bombs = len(self._adjacent_relatives(pos, self.bomb_val))
                self.gameboard[pos][self.VALUE] = num_adj_bombs
                if validate:
                    num_adj_cells = len(self._adjacent_relatives(pos))
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
    def click(self, pos: tuple) -> None:
        pass

    # sets the cell at {pos} to visible
    def reveal(self, pos: tuple) -> None:
        if self.gameboard[pos][self.VISIBILITY]: 
            print(f"reveal({pos}) : Cell already visible")
        self.gameboard[pos][self.VISIBILITY] = True

    # sets the cell at {pos} to hidden
    def hide(self, pos: tuple) -> None:
        if not self._in_bounds(pos):
            print(f"hide({pos}) : Position is out of bounds")
            return
        if not self.gameboard[pos][self.VISIBILITY]:
            print(f"hide({pos}) : Cell already hidden")
            return
        self.gameboard[pos][self.VISIBILITY] = False

    # sets the cell at {pos} to flagged, or not flagged if already flagged
    def flag(self, pos: tuple) -> None:
        self.gameboard[pos][self.FLAGGED] = True if not self.gameboard[pos][self.FLAGGED] else False


    # ----------------------------- CLASS TOOLS -----------------------------

    # returns a list of the positions of adjacent cells to {pos}
    # if a target is assigned, returns only positions of adjacent cells that match target
    # if no target is assigned, return all positions of all adjacent cells
    def _adjacent_relatives(self, pos: tuple, target=None) -> list:
        if not self._is_valid_pos(pos, feedback=False):
            print(f"_adjacent_relatives({pos}, {target}) : Invalid Position Argument {pos}")
            return
        ADJACENTS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        adjacent_targets = []
        for a in ADJACENTS:
            adj_pos = (pos[0] + a[0], pos[1] + a[1])
            target_matched = self._in_bounds(adj_pos) and ((self.gameboard[adj_pos][self.VALUE] == target) or target == None)
            if target_matched:
                adjacent_targets.append(adj_pos)
        return adjacent_targets

    # TODO
    # modifies self.gameboard in place
    # if self.gameboard.cell(x, y)
    # cascading cell revealing from cell (x, y)
    # uses _adjacent_relatives for this
    # recursive
    def _cascade(self, pos: tuple) -> None:
        pass

    # updates the value of a cell at {pos} based on number of bomb cells adjacent
    def _update_cell_value(self, pos):
        if self.cell_value(pos) == self.bomb_val:
            return
        self.gameboard[pos][self.VALUE] = len(self._adjacent_relatives(pos, self.bomb_val)) 

    # sets the value of a cell at {pos} to {value}
    def _set_cell_value(self, pos, value):
        if not self._in_bounds(pos): 
            print(f"_set_cell_value({pos}, {value}) : Position not in bounds")
            return
        self.gameboard[pos][self.VALUE] = value

    # returns the value of a given position
    def _get_cell_value(self, pos):
        if self._in_bounds(pos):
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
    def _in_bounds(self, pos: tuple):
        try:
            self.gameboard[pos]
        except IndexError:
            return False
        return True
    
    # True if cell at {pos} is flagged, else False
    def _is_flagged(self, pos: tuple) -> bool:
        return self.gameboard[pos][self.FLAGGED]
    
    # True if cell at {pos} is visible, else False
    def _is_visible(self, pos: tuple) -> bool:
        return self.gameboard[pos][self.VISIBILITY]

    # ----------------------------- DEV TOOLS -----------------------------

    # TODO: args aren't implemented yet because i don't feel like it
    def print_board(self, all_visible=True, all_vals=False, raw=False) -> None:
        if raw:
            for row in self.gameboard.board:
                print(row)
        else:
            for y in range(self.gameboard.height):
                for x in range(self.gameboard.width):
                    print(self.gameboard[(x, y)][self.VALUE], end=' ')
                print()

    # assigns ONE cell on the board to self.bomb_val
    def place_bomb(self, pos):
        if not self._in_bounds(pos): 
            print(f"place_bomb({pos}) : Position not in bounds")
            return
        self._set_cell_value(pos, self.bomb_val)
        self._update_cell_value(pos)

    # sets the {attribute} of all cells to {value}
    # very open, can set any attribute to whatever you want (can break stuff)
    def set_all_cells(self, attribute, value):
        try:
            for row in self.gameboard.board:
                for col in row:
                    col[attribute] = value
        except IndexError:
            print(f"_set_all_cells({attribute}, {value}) : Attribute index {attribute} not found in cells")
        
    # sets all cells to visible
    def reveal_all(self) -> None:
        self._set_all_cells(attribute=self.VISIBILITY, value=True)

    # sets all cells to hidden
    def hide_all(self) -> None:
        self._set_all_cells(attribute=self.VISIBILITY, value=False)

    # ----- for later -----
    # get_state(self) for a serialized version of the board with only the data 
    #   the user should see (don't send clues over the air!)
    # 
    # to_dict() or to_json() for easy integration with front-end API 

# Tools:
# generate_board(width, height, num_bombs)
# click(pos) (not implemeneted)
# reveal(pos)
# hide(pos)
# flag(pos)
# _is_visible(pos)
# _is_flagged(pos)

# place_bomb(pos)
# set_all_cells(attribute, value)
# reveal_all()
# hide_all()

# _adjacent_relatives(pos, target)
# _update_cell_value(pos)
# _set_cell_value(pos, value)
# _get_cell_value(pos)
# _is_valid_pos(pos)
# _in_bounds(pos)

minesweeper = Minesweeper()
minesweeper.generate_board(width=5, height=5, num_bombs=5)
minesweeper._set_cell_value((4, 4), '*')
minesweeper.print_board()
print(minesweeper._adjacent_relatives(pos=(4, 4), target=9))

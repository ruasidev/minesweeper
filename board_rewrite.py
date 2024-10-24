import random
from gameboard import Gameboard

class Minesweeper:
    def __init__(self):
        self.gameboard = None
        self.seed = None
        self.bomb_val = 9
        # each cell = [0, False, False] -> Hidden unflagged cell with value 0
        self.cell_struct = {"value": 0, "visibility": False, "flagged": False} 
    
    # indices for each cell for readability
    VALUE, VISIBILITY, FLAGGED = 0, 1, 2

    def print_board(self, all_visible=True, all_vals=False, raw=False) -> None:
        # args aren't implemented yet because i don't feel like it
        if raw:
            for row in self.gameboard.board:
                print(row)
        else:
            for y in range(self.gameboard.height):
                for x in range(self.gameboard.width):
                    print(self.gameboard[(x, y)][self.VALUE], end=' ')
                print()
    
    # pls use for all methods with pos parameter <3
    # raises an exception if the position is out of the board dimensions or is invalid
    # if pos[0] < 0 or pos[0] > self.gameboard.width:  out of bounds on x axis
    # if pos[1] < 0 or pos[1] > self.gameboard.height: out of bounds on y axis ... etc.
    def _valid_pos(self, pos: tuple, feedback=True):
        if len(pos) != 2 or not isinstance(pos, tuple):
            if feedback: print(f"pos {pos} must be a tuple of length 2")
            return False
        if not ((isinstance(pos[0], int) and isinstance(pos[1], int))):
            if feedback: print(f"Expected values x, y in pos to be int. Got: {type(pos[0]), type(pos[1])}")
            return False
        return True

    # similar to _valid_pos, but a value is returned with no exceptions
    def _in_bounds(self, pos: tuple):
        try:
            self.gameboard[pos]
        except IndexError:
            return False
        return True

    # must be updated if cell values change
    # modifies self.gameboard in place
    # sets the value of cell {attribute} to {value} for all cells on self.gameboard
    # attribute must be VALUE, VISIBILITY, or FALGGED (0, 1, or 2)
    # i would never in a million years let this be global even tho its idiot proofed (im an idiot)
    def _set_all_cells(self, attribute, value):
        # ------ idiot-proofing ------
        # validate attribute
        if attribute not in (self.VALUE, self.VISIBILITY, self.FLAGGED):
            print(f"set_all_cells({attribute}, {value}) : Invalid attribute `{attribute}`")
            return
        # validate VALUE
        if attribute == self.VALUE and len(value) != 1:
            print(f"set_all_cells({attribute}, {value}) : Value {value} must be of length 1")
            return
        # validate VISIBILITY
        if attribute == self.VISIBILITY and not isinstance(value, bool):
            print(f"set_all_cells({attribute}, {value}) : Invalid visibility {value}")
            return
        # validate FLAGGED
        if attribute == self.FLAGGED and not isinstance(value, bool):
            print(f"set_all_cells({attribute}, {value}) : Invalid flag {value}")
            return
        
        for row in self.gameboard.board:
            for col in row:
                col[attribute] = value
        


    # modifies self.gameboard in place
    # sets all cells to visible
    def reveal_all(self):
        # --- if set_all_cells method doesn't work for some reason ---
        #   for row in self.gameboard:
        #       for col in row:
        #           col[self.VISIBILITY] = True
        # ---                                                      ---

        self._set_all_cells(attribute=self.VISIBILITY, value=True)




    # modifies self.gameboard in place
    # sets all cells to hidden
    def hide_all(self):
        # --- if set_all_cells method doesn't work for some reason ---
        #   for row in self.gameboard:
        #       for col in row:
        #           col[self.VISIBILITY] = False
        # ---                                                      ---

        self._set_all_cells(attribute=self.VISIBILITY, value=False)
    
    # modifies self.gameboard[cell] in place
    # set cell at pos[1][0] to visible
    def reveal(self, pos: tuple) -> None:
        if self.gameboard[pos][self.VISIBILITY]: 
            print(f"reveal({pos}) : Cell already visible")
        self.gameboard[pos][self.VISIBILITY] = True

    # modifies self.gameboard[cell] in place
    def hide(self, pos: tuple) -> None:
        if not self._in_bounds(pos):
            print(f"hide({pos}) : Position is out of bounds")
            return
        if not self.gameboard[pos][self.VISIBILITY]:
            print(f"hide({pos}) : Cell already hidden")
            return
        self.gameboard[pos][self.VISIBILITY] = False

    # modifies self.gameboard[cell] in place
    # sets pos[1][0] to flagged, or unflagged if already flagged
    def flag(self, pos: tuple) -> None:
        self.gameboard[pos][self.FLAGGED] = True if not self.gameboard[pos][self.FLAGGED] else False

    # assign values to self.gameboard (no return)
    # if not seed, generate with normal generation methods
    # already happens in constructor, but used if you need to regenerate the board
    def generate_board(self, width=0, height=0, num_bombs=0, seed=None): 
        if seed:
            self._decompile_seed(seed)
            return
        self.gameboard = Gameboard(width, height, num_bombs, list(self.cell_struct.values()))
        
        # generate board based on seed
        self.place_bombs()
        self.assign_vals()

    # generates a board based on a required seed (just do in generate_board?)
    def _decompile_seed(self, seed: int):
        if not seed:
            print(f"The seed value has not been generated yet! seed: {seed}")
            return None

    # generates and returns a unique seed based on:
    # - values of the bomb positions
    # - width and height of the board (order matters)
    # - number of bombs
    # allows us to compact a board into a seed and regenerate based on that
    # this is gonna require a lot of thought and math
    def _compile_seed(self) -> int:
        pass
    
    # private
    # generates bomb positions for self.gameboard
    # {exclude} excludes a bomb position from being generated
    # called by generate_board internally
    # returns list of 'pos' style tuple positions [(x1, y1), (x2, y2), (x3, y3)...]
    # this is the hard part
    # retro style generation
    # this should be as efficient as possible (ironic)
    def _generate_bomb_positions(self, exclude=None) -> list:
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

    # should work globally
    # places bombs onto self.gameboard
    # relies on generate_bomb_positions() to generate values    
    def place_bombs(self, exclude=None) -> None:
        positions = self._generate_bomb_positions(exclude)
        for pos in positions:
            self.gameboard[pos][self.VALUE] = self.bomb_val
        pass

    # private
    # tool for cascade() and assign_vals() to check adjacent cells
    # target is the value we want to return the positions of
    # returns list of tuples [(x1, y1), (x2, y2), (x3, y3)...]
    def _adjacent_relatives(self, pos: tuple, target) -> list:
        if not self._valid_pos(pos, feedback=False):
            print(f"_adjacent_relatives({pos}, {target}) : Invalid Position Argument {pos}")
            return
        # ADJACENTS = [(adj_x, adj_y) for adj_x in range(-1, 2) for adj_y in range(-1, 2) if not (adj_x == 0 and adj_y == 0)]
        ADJACENTS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        adjacent_targets = []
        for a in ADJACENTS:
            adj_pos = (pos[0] + a[0], pos[1] + a[1])
            if self._in_bounds(adj_pos) and self.gameboard[adj_pos][self.VALUE] == target:
                adjacent_targets.append(adj_pos)
        return adjacent_targets
            
    # modifies self.gameboard in place
    # should work globally
    # generates and assigns the values for all cells based on bomb adjacency 
    # uses _adjacent_relatives for this
    # called by generate_board internally
    def assign_vals(self) -> None:

        pass

    # modifies self.gameboard in place
    # if self.gameboard.cell(x, y)
    # cascading cell revealing from cell (x, y)
    # uses _adjacent_relatives for this
    # recursive
    def _cascade(self, pos: tuple) -> None:
        pass

    # modifies self.gameboard in place
    # if flagged(pos)
    # processes like the user revealed a cell at pos = (x, y)
    # different from board.reveal() in that the game ends if (x, y)
    # is a bomb, and performs cascade reveal if its a 0
    def click(self, pos: tuple) -> None:
        pass

    def _flagged(self, pos: tuple) -> bool:
        return self.gameboard[pos][self.FLAGGED]

    # ----- for later -----
    # get_state(self) for a serialized version of the board with only the data 
    #   the user should see (don't send clues over the air!)
    # 
    # to_dict() or to_json() for easy integration with front-end API 

minesweeper = Minesweeper()
minesweeper.generate_board(width=5, height=5, num_bombs=5)

cell = minesweeper.gameboard[(0, 0)]
cell[minesweeper.VALUE] = '*'
minesweeper.gameboard[(0, 0)] = cell
minesweeper.print_board()
print(minesweeper._adjacent_relatives(pos=(0, 0), target=9))

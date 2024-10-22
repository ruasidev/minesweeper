import random

class Board:
    def __init__(self, width, height, num_bombs):
        self.width = width
        self.height = height
        self.num_bombs = num_bombs
        self.flag_val = 'F'
        self.bomb_val = 9
        self.zero_val = '-'
        # each cell = [0, False, False] -> Hidden unflagged cell with value 0
        self.cell_struct = {"value": 0, "visibility": False, "flagged": False} 
        self.gameboard = [[list(self.cell_struct.values()) for _ in range(self.width)] for _ in range(self.height)]
        self.seed = None
    
    # indices for each cell for readability
    VALUE, VISIBILITY, FLAGGED = 0, 1, 2

    # idk if this works yet but:
    # allows us to access cell positions with gameboard[(x, y)] == gameboard[y][x]
    def __getitem__(self, pos: tuple):
        self._validate_pos(pos)
        return self.gameboard[pos[1]][pos[0]]

    def print_board(self, all_visible=True, all_vals=False, raw=False) -> None:
        # piece = col if all_vals else col[0]
        # if not raw:
        #     for row in self.gameboard:
        #         for col in row:
        #             print(piece, end=' ')
        #         print()
        # else:
        #     for row in self.gameboard:
        #         for col in row:
        #             print(piece)
        pass
    
    # pls use for all methods with pos parameter <3
    # raises an exception if the position is out of the board dimensions or is invalid
    # if pos[0] < 0 or pos[0] > self.width:  out of bounds on x axis
    # if pos[1] < 0 or pos[1] > self.height: out of bounds on y axis ... etc.
    def _validate_pos(self, pos: tuple):
        pass

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
        
        for row in self.gameboard:
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

        self.set_all_cells(attribute=self.VISIBILITY, value=True)




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
    # set cell at pos[1][0] to hidden
    def hide(self, pos: tuple) -> None:
        if not self.gameboard[pos][self.VISIBILITY]:
            print(f"hide({pos}) : Cell already hidden")
        self.gameboard[pos][self.VISIBILITY] = False

    # modifies self.gameboard[cell] in place
    # sets pos[1][0] to flagged, or unflagged if already flagged
    def flag(self, pos: tuple) -> None:
        cell_flag = self.gameboard[pos][self.FLAGGED]
        cell_flag = True if not cell_flag else False

    # assign values to self.gameboard (no return)
    # if not seed, generate with normal generation methods
    # already happens in constructor, but used if you need to regenerate the board
    def generate_board(self, seed=None): 
        if seed:
            self._decompile_seed(seed)
            return
        
        self.gameboard = [[list(self.cell_struct.values()) for _ in range(self.width)] for _ in range(self.height)]
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
        random_position_sample = random.sample(range(self.height * self.width), self.nbombs) # list
        
        # fix later:
        #   absolutely fucking horrendous way of implementing this but idc rn (idek if it works)
        if exclude != None and isinstance(exclude, int) and 0 < exclude < self.height * self.width:
            while exclude in random_position_sample or len(random_position_sample) != self.num_bombs:
                random_position_sample[random_position_sample.index(exclude)] = random.choice(self.height*self.width)

        for value in random_position_sample:
            x_pos = value % self.width
            y_pos = value // self.width
            positions.append((x_pos, y_pos))
        return positions

    # should work globally
    # places bombs onto self.gameboard
    # relies on generate_bomb_positions() to generate values    
    def place_bombs(self, exclude=None) -> None:
        positions = self._generate_bomb_positions(exclude)
        for pos in positions:
            self.gameboard.set_cell(pos, self.bomb_val) # still implement set_cell pls
        pass

    # private
    # tool for cascade() and assign_vals() to check adjacent cells
    # target is the value we want to return the positions of
    # returns list of tuples [(x1, y1), (x2, y2), (x3, y3)...]
    def _check_adjacent(self, pos: tuple, target) -> list:
        pass

    # modifies self.gameboard in place
    # should work globally
    # generates and assigns the values for all cells based on bomb adjacency 
    # uses check_adjacent for this
    # called by generate_board internally
    def assign_vals(self) -> None:
        pass

    # modifies self.gameboard in place
    # if self.gameboard.cell(x, y)
    # cascading cell revealing from cell (x, y)
    # uses check_adjacent for this
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

minesweeper = Board.generate_board()

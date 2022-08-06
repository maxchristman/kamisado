board_size = 8
valid_colors = ['brown', 'green', 'red', 'yellow', 'pink', 'purple', 'blue', 'orange']
valid_players = ['black', 'white']

class Tower:
    def __init__(self, player, color, starting_tile):
        if color not in valid_colors or player not in valid_players:
            raise Exception("Error: invalid tile or player color.")

        self.is_sumo = False
        self.player = player
        self.color = color
        self.tile = starting_tile
    
    def move_forwards(self, test=False):
        if self.player == 'black':
            in_front = self.tile.north_tile
        elif self.player == 'white':
            in_front = self.tile.south_tile
        
        if in_front.tower_on != None:
            print("Notice: forwards movement blocked by piece")
            return False

        if (self.player == 'black' and self.tile.north_tile == None) or (self.player == 'white' and self.tile.south_tile == None):
            print("Notice: cannot move forwards off the board")
            return False

        if not test:
            self.tile.tower_on = None
            self.tile = in_front 
            in_front.tower_on = self
        return True

    def move_diag_left(self, test=False):
        if self.player == 'black':
            diag_left = self.tile.nw_tile
        elif self.player == 'white':
            diag_left = self.tile.se_tile
        
        if diag_left.tower_on != None:
            print("Notice: diagonal left movement blocked by piece")
            return False

        if (self.player == 'black' and self.tile.nw_tile == None) or (self.player == 'white' and self.tile.se_tile == None):
            print("Notice: cannot move diagonally left off the board")
            return False

        if not test:
            self.tile.tower_on = None
            self.tile = diag_left
            diag_left.tower_on = self
        return True

    def move_diag_right(self, test=False):
        if self.player == 'black':
            diag_right = self.tile.ne_tile
        elif self.player == 'white':
            diag_right = self.tile.sw_tile
        
        if diag_right.tower_on != None:
            print("Notice: diagonal right movement blocked by piece")
            return False

        if (self.player == 'black' and self.tile.ne_tile == None) or (self.player == 'white' and self.tile.sw_tile == None):
            print("Notice: cannot move diagonally right off the board")
            return False

        if not test:
            self.tile.tower_on = None
            self.tile = diag_right
            diag_right.tower_on = self
        return True
    
    def move_to(self, x, y, test=False):
        if x <= self.tile.x:
            print("Error: towers cannot be moved sideways or backwards.")
            return False
        if x >= board_size or y < 0 or y >= board_size:
            print("Error: towers cannot be moved off the board")
            return False
        if y != self.tile.y and abs(y-self.tile.y) != abs(x-self.tile.x):
            print("Error: diagonal moves must have equal x and y components")
            return False
        
        initial_tile = self.tile

        if y == self.tile.y:
            while not (self.tile.x == x and self.tile.y == y) and self.move_forwards(test=True):
                self.move_forwards()
        elif y < self.tile.y:
            while not (self.tile.x == x and self.tile.y == y) and self.move_diag_left(test=True):
                self.move_diag_left()
        elif y > self.tile.y:
            while not (self.tile.x == x and self.tile.y == y) and self.move_diag_right(test=True):
                self.move_diag_right()
        
        success = (self.tile.x == x and self.tile.y == y)
        
        if success and not test:
            print("Notice: Tower was successfully moved.")
            return True
        
        # Move the tower back
        self.tile.tower_on = None
        self.tile = initial_tile

        if not test:
            print("Notice: Tower was not successfully moved.")

        if success:
            print("Notice: tower can be moved to this location.")
            return True
        
        print("Notice: this move is blocked by other towers.")
        return False

class Tile:
    def __init__(self, x, y, color):
        if color not in valid_colors:
            raise Exception("Error: invalid tile color.")

        self.x = x
        self.y = y
        self.color = color
    
        self.north_tile = None
        self.nw_tile = None
        self.ne_tile = None
        self.south_tile = None
        self.se_tile = None
        self.sw_tile = None

        self.is_empty = True
        self.tower_on = None
    
class Board:
    def __init__(self):
        self.__layout = [
            ['brown', 'green', 'red', 'yellow', 'pink', 'purple', 'blue', 'orange'],
            ['purple', 'brown', 'yellow', 'blue', 'green', 'pink', 'orange', 'red'],
            ['blue', 'yellow', 'brown', 'purple', 'red', 'orange', 'pink', 'green'],
            ['yellow', 'red', 'green', 'brown', 'orange', 'blue', 'purple', 'pink'],
            ['pink', 'purple', 'blue', 'orange', 'brown', 'green', 'red', 'yellow'],
            ['green', 'pink', 'orange', 'red', 'purple', 'brown', 'yellow', 'blue'],
            ['red', 'orange', 'pink', 'green', 'blue', 'yellow', 'brown', 'purple'],
            ['orange', 'blue', 'purple', 'pink', 'yellow', 'red', 'green', 'brown']
            ]
        
        self.tiles = []

        for x, row in enumerate(self.__layout):
            new_row = []
            for y, color in enumerate(row):
                new_tile = Tile(x, y, color)
                new_row.append(new_tile)
            self.tiles.append(new_row)
        
        for x, row in enumerate(self.tiles):
            for y, tile in enumerate(row):
                if x+1 < board_size:
                    tile.north_tile = self.tiles[x+1][y]
                if x-1 >= 0:
                    tile.south_tile = self.tiles[x-1][y]

                if x+1 < board_size and y+1 < board_size:
                    tile.ne_tile = self.tiles[x+1][y+1]
                if x+1 < board_size and y-1 >= 0:
                    tile.nw_tile = self.tiles[x+1][y-1]

                if x-1 >= 0 and y+1 < board_size:
                    tile.se_tile = self.tiles[x-1][y+1]
                if x-1 >= 0 and y-1 >= 0:
                    tile.sw_tile = self.tiles[x-1][y-1]
            
        self.towers = []
        
        for player in valid_players:
            for y, color in enumerate(valid_colors):
                if player == 'black':
                    starting_tile = self.tiles[0][y]
                elif player == 'white':
                    starting_tile = self.tiles[-1][len(self.tiles)-y-1]

                new_tower = Tower(player, color, starting_tile)

                if player == 'black':
                    self.tiles[0][y].tower_on = new_tower
                elif player == 'white':
                    self.tiles[-1][len(self.tiles)-y-1].tower_on = new_tower
                self.towers.append(new_tower)

class Player:
    def __init__(self, color):
        self.score = 0
        self.color = color

class BoardView:
    def __init__(self, board):
        self.board = board
        self.update()

    def update(self):
        # Reverse rows for displaying
        for row in self.board.tiles[::-1]:
            row_string = ""
            for tile in row:
                if tile.tower_on == None:
                    row_string += self.get_display_string('x', tile.color)
                    continue
                row_string += self.get_display_string(tile.tower_on.player, tile.tower_on.color)
            print(row_string)

    def colored(self, text, r, g, b):
        return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)

    def get_display_string(self, player, color):
        c = player[0]
        match color:
            case 'red':
                return self.colored(c, 255, 0, 0)
            case 'blue':
                return self.colored(c, 0, 0, 255)
            case 'green':
                return self.colored(c, 0, 255, 0)
            case 'yellow':
                return self.colored(c, 255, 255, 0)
            case 'pink':
                return self.colored(c, 255, 20, 147)
            case 'purple':
                return self.colored(c, 148, 0, 211)
            case 'brown':
                return self.colored(c, 115, 97, 77)
            case 'orange':
                return self.colored(c, 255, 137, 0)


class Game:
    def __init__(self, game_length, reset_mode):
        self.game_length = game_length
        self.reset_mode = reset_mode

        black = Player('black')
        white = Player('white')

        board = Board()
        bv = BoardView(board)
        for tower in board.towers:
            if tower.color == 'orange':
                tower.move_to(x=6, y=1, test=False)
                break
        bv.update()
        
    


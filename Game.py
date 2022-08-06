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
            return False

        if (self.player == 'black' and self.tile.north_tile == None) or (self.player == 'white' and self.tile.south_tile == None):
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
            return False

        if (self.player == 'black' and self.tile.nw_tile == None) or (self.player == 'white' and self.tile.se_tile == None):
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
            return False

        if (self.player == 'black' and self.tile.ne_tile == None) or (self.player == 'white' and self.tile.sw_tile == None):
            return False

        if not test:
            self.tile.tower_on = None
            self.tile = diag_right
            diag_right.tower_on = self
        return True
    
    def move_to(self, x, y, test=False):
    
        if (x <= self.tile.x and self.player == 'black') or (x >= self.tile.x and self.player == 'white'):
            return False
        if x >= board_size or y < 0 or y >= board_size:
            return False
        if y != self.tile.y and abs(y-self.tile.y) != abs(x-self.tile.x):
            return False
        
        initial_tile = self.tile

        if y == self.tile.y:
            while not (self.tile.x == x and self.tile.y == y) and self.move_forwards(test=True):
                self.move_forwards()
        elif (y < self.tile.y and self.player == 'black') or (y > self.tile.y and self.player == 'white'):
            while not (self.tile.x == x and self.tile.y == y) and self.move_diag_left(test=True):
                self.move_diag_left()
        elif (y > self.tile.y and self.player == 'black') or (y < self.tile.y and self.player == 'white'):
            while not (self.tile.x == x and self.tile.y == y) and self.move_diag_right(test=True):
                self.move_diag_right()
        
        success = (self.tile.x == x and self.tile.y == y)
        
        if success and not test:
            print("Notice: tower was successfully moved.")
            return True
        
        # Move the tower back
        self.tile.tower_on = None
        self.tile = initial_tile

        if not test:
            print("Notice: tower was not successfully moved.")

        if success:
            return True
        
        return False
    
    def get_possible_moves(self):
        possible_moves = []
        for x in range(board_size):
            for y in range(board_size):
                if self.move_to(x, y, test=True):
                    possible_moves.append([x, y])
        return possible_moves

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
    def __init__(self, color, towers):
        self.score = 0
        self.color = color
        self.towers = towers
    
    def get_tower(self, color):
        tower = None
        for t in self.towers:
            if t.color == color:
                tower = t
                break
        return tower
    
    def move_tower(self, color, x, y):
        tower = self.get_tower(color)
        status = tower.move_to(x, y, test=False)
        return status, tower.tile.color
    
    def get_possible_moves(self, color):
        return self.get_tower(color).get_possible_moves()

class BoardView:
    def __init__(self, board):
        self.board = board
        print("Welcome to Kamisado!")
        self.update()

    def update(self):
        row_strings = []
        for x, row in enumerate(self.board.tiles):
            row_string = str(x) + ' '
            for tile in row:
                if tile.tower_on == None:
                    row_string += self.get_display_string('o', tile.color)
                    continue
                row_string += self.get_display_string(tile.tower_on.player, tile.tower_on.color)
            row_strings.append(row_string)

        # Reverse rows for displaying
        row_strings = row_strings[::-1] 
        horizontal_label = '  '
        for y in range(board_size):
            horizontal_label += str(y) + ' '
        row_strings.append(horizontal_label)
        for rs in row_strings:
            print(rs)

    def colored(self, text, r, g, b):
        return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)

    def get_display_string(self, player, color):
        if player != 'o':
            c = player[0].upper()
        else:
            c = player
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

        self.board = Board()
        self.bv = BoardView(self.board)

        black_towers, white_towers = [], []
        for tower in self.board.towers:
            if tower.player == 'black':
                black_towers.append(tower)
            elif tower.player == 'white':
                white_towers.append(tower)

        self.black = Player('black', black_towers)
        self.white = Player('white', white_towers)
        self.active_player = self.black

    def start(self):
        while True:
            ready = input("Are you ready to play? ")
            if 'y' not in ready.lower():
                continue
            break
            
        self.first_move()

        while not self.take_turn():
            continue
    
    def first_move(self):
        print("Black makes the first move.")
            
        while True:
            try:
                color_to_move = input("Which piece would you like to move? ") 
                x_to_move = int(input("Please enter the desired x coordinate. "))
                y_to_move = int(input("Please enter the desired y coordinate. "))
                status, next_color = self.active_player.move_tower(color_to_move, x_to_move, y_to_move)
                if not status:
                    print("Warning: invalid move")
                    continue
                self.next_color = next_color
                break
            except Exception:
                print("Error: I didn't understand that. Please try again.")
                continue
        self.bv.update()
        self.active_player = self.white
    
    def check_win(self):
        for tower in self.board.towers:
            if (tower.tile.x == 0 and tower.player == 'white'):
                print("Congrats, white won the game!")
                self.winner = self.active_player
                self.active_player.score += 1
                return True
            if (tower.tile.x == board_size - 1 and tower.player == 'black'):
                print("Congrats, black won the game!")
                self.winner = self.active_player
                self.active_player.score += 1
                return True
        return False
    
    def take_turn(self):
        print("Current turn:", self.active_player.color)
        while True:
            try:
                print("You must move your", self.next_color, 'tower') 
                possible_moves = self.active_player.get_possible_moves(self.next_color)
                if len(possible_moves) == 0:
                    print("Warning: your piece is stuck.")
                    self.next_color = self.active_player.get_tower(self.next_color).tile.color
                    if self.active_player.color == 'white':
                        self.active_player = self.black
                    elif self.active_player.color == 'black':
                        self.active_player = self.white
                    print("Current turn:", self.active_player.color)
                    print("You must move your", self.next_color, 'tower') 
                    self.bv.update()
                x_to_move = int(input("Please enter the desired x coordinate. "))
                y_to_move = int(input("Please enter the desired y coordinate. "))
                status, next_color = self.active_player.move_tower(self.next_color, x_to_move, y_to_move)
                if not status:
                    print("Warning: invalid move")
                    continue
                self.next_color = next_color
                break
            except Exception:
                print("Error: I didn't understand that. Please try again.")
                continue

        self.bv.update()
        if self.check_win():
            return True
        if self.active_player.color == 'white':
            self.active_player = self.black
        elif self.active_player.color == 'black':
            self.active_player = self.white
        return False

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
    
    def can_move_forwards(self):
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

        return True
    
    # def move_to(self, x, y):
    #     if x <= self.tile.x:
    #         raise Exception("Warning: towers may only be moved forwards, either straight or diagonally.")
        
    #     # Moving straight forwards
    #     if y == self.tile.y:


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

class Game:
    def __init__(self, game_length, reset_mode):
        self.game_length = game_length
        self.reset_mode = reset_mode

        black = Player('black')
        white = Player('white')

        board = Board()
        for tower in board.towers:
            print(tower.player, tower.color)
            for _ in range(7):
                tower.move_forwards()
            break

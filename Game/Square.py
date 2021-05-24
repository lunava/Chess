import re
board_size = 8
total_squares = board_size ** 2
pattern = re.compile('([a-h][1-8])')

class Square(object):
    
    def __init__(self, col, row):
        self.col = col
        self.row = row
        self.index = (self.row << 3) + self.col
    def __str__(self):
        return "{0}{1}".format(chr(ord('a') + self.col), 1 + self.row)
    def get_row(self):
        return self.row
    def get_col(self):
        return self.col
    def get_index(self):
        return self.index
    #Checks if the square that I am moving to is a valid square
    def valid_sq_move(self, square):
        return self != square and \
            (self.row == square.get_row() or  \
            self.col == square.get_col() or \
            self.row + self.col == square.get_col() + square.get_row() or \
            self.row - self.col == square.get_row() - self.get_row())

#TODO TEST
#Functions for squares
def distance(square_f , square_t):
    return  int(max(abs(square_f.get_row() - square_t.get_row()), 
            abs(square_f.get_col() - square_t.get_col())))

#TODO TEST
#Checks if the square exists with the given coordinates
def square_exist(col, row):
    return col < board_size and col >= 0 and \
        row < board_size and row >= 0

#TODO: TEST
#returns a square with the given string position
def square_string(posn):
    if pattern.match(posn):
    
        return get_square(ord(posn[0]) - ord('a'), ord(posn[1]) - ord('1'))
    else:
        return None

#TODO: TEST
#returns a square with the given coordinates:
def get_square(col, row):
    if (not square_exist(col, row)):
        ValueError('Rows or Columns out of bounds')
    else:
        return SQUARES[col][row]

#TODO: Test
#returns the direction of square FROM to square TO
def direction(square_f, square_t):
    dc = 0 if square_f.get_col() > square_t.get_col() else \
         1 if square_f.get_col() == square_t.get_col() else 2
    dr = 0 if square_f.get_row() > square_t.get_row() else \
         1 if square_f.get_row() == square_t.get_row() else 2
    return DIST_TO_DIR[dc][dr]

#Returns square from given direction and distanec from Square sq
def dir_distance(sq, dir, dist):
    col = sq.get_col() + DC[dir] * dist
    row = sq.get_row() + DR[dir] * dist
    if (dir > 7 or dir < 0 or dist <= 0  or \
        not square_exist(col, row) ):
        return None
    return get_square(col, row)

#Returns square adjecent from given Square sq
def dir_adj(sq, dir):
    return dir_distance(sq, dir, 1)

#TODO: Direction func, adj_Square_inDirection func, 


#Misc

ALL_SQUARES = [None] * total_squares
SQUARES = [[None] * board_size] * board_size
DC = [0,  1,  1,  1,  0, -1, -1, -1]
DR = [1,  1,  0, -1, -1, -1,  0,  1 ]
DIST_TO_DIR = [[5, 6, 7], [ 4, -1, 0 ], [3, 2, 1]]

#Direction based on coordinate in unit-circle. i.e. North (direction = 0) =[0,1] 
DIRECTION_COR = [[ 0, 1 ], [1, 1 ], [1, 0 ], [ 1, -1 ],
                 [ 0, -1 ], [ -1, -1 ], [ -1, 0 ], [ -1, 1 ]]

#TODO: MIGHT NEED FIXING
#Generate all possible squares in the board
SQUARES = [[Square(c,r) for r in range(8)] for c in range(8)]


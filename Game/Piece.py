from Game.Square import *

"""
Class representation of a Chess Piece
Square encapsulate Piece class.
Squares are represented as [a-h][1-8] denoting columns and rows
"""
class Piece(object):
    #Pieces are represented by their color and type

    def __init__(self, color, piece_type):
        self.color = color
        assert color == 'black' or color == 'white' or color == None
        self.piece_type = piece_type

    def __str__(self):
        if (self.color == None):
            return 'EMP'
        else:
            return self.color + " " + self.piece_type
    def get_color(self):
        return self.color

    def get_piece_type(self):
        return self.piece_type

    def abbrev(self):
        if (self.color == None):
            return '- '
        else:
            return self.color[0] + self.piece_type[0]

    def is_valid_move(self, move):
        return move.dist == 1

# Specific pieces with certain move types
class Knight(Piece):
    def __init__(self, color):
        super().__init__(color, 'night')

    def is_valid_move(self, move):
        return (abs(move.y1 - move.y2) == 2 and abs(move.x1 - move.x2) == 1) or \
                (abs(move.y1 - move.y2) == 1 and abs(move.x1 - move.x2) == 2)


class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color, 'pawn')
        self.intial_move = True
        #possible diagonals based on the piece color
        self.diag1, self.diag2 = 0, 0
        if (self.color == 'white'):
            self.diag1, self.diag2 = 1, 7
        else:
            self.diag1, self.diag2 = 3, 5

    def is_valid_move(self, move):
        if (move.x1 != move.x2 
            and not self.pawn_diag(move)):
            return False
        elif (self.color == 'white' and
             (move.dy == 1 or
             (move.y1 == 1 and move.dy == 2 ))):
              return True
        elif (self.color == 'black' and
              (move.dy == -1 or 
               move.y1 == 6 and move.dy == -2)):
               return True
        return False

    #Checks if the pawn is able to move diag
    def pawn_diag(self, move):
        return dir_adj(move.square_f, self.diag1) == move.square_t or \
           dir_adj(move.square_f, self.diag2) == move.square_t
    #Checks if the valid pawn capture move diagonal

class King(Piece):

    def __init__(self, color):
        super().__init__(color, 'king')
        #Special attribute for castling
        self.has_moved = False
        self.rooks = [] # Pointers to the rooks, [0] = queen rook [1] = king rook

    def is_valid_move(self, move):
        return super().is_valid_move(move)

class Queen(Piece):
    def __init__(self, color):
        super().__init__(color, 'queen')

    def is_valid_move(self, move):
        #TODO
        return (abs(move.x1 - move.x2) == abs(move.y1 - move.y2)) or \
                (move.x1 == move.x2 or move.y1 == move.y2)

class Rook(Piece):
    def __init__(self, color):
        super().__init__(color, 'rook')
        #Special attribute for castling
        self.has_moved = False

    def is_valid_move(self, move):
        return move.x1 == move.x2 or move.y1 == move.y2

class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color, 'bishop')

    def is_valid_move(self, move):
        return abs(move.x1 - move.x2) == abs(move.y1 - move.y2) 

class Empty(Piece):
    def __init__(self):
        super().__init__(None, None)
    def is_valid_move(self, move):
        return False
 
#Returns true if the move is a diagonal pawn capture

#Returns piece based on piece type and color
def get_p(piece_type, color=None):
    return {
            'night': Knight(color),
            'king': King(color),
            'bishop': Bishop(color),
            'queen': Queen(color),
            'pawn': Pawn(color),
            'rook': Rook(color), 
            'empty': Empty()
    }[piece_type]
#Generate a row of Piece piece_type and color Color
def generate_row(piece_type, color=None):
    p = get_p(piece_type, color)
    return [p for x in range(8)]

#Generate King's row based on color
def generate_king_row(color):
    king = King(color)
    rook1 = Rook(color)
    rook2 = Rook(color)
    king.rooks.append(rook1)
    king.rooks.append(rook2)
    return [rook1, Knight(color), Bishop(color), Queen(color), 
            king, Bishop(color), Knight(color), rook2]
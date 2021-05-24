"""
Data Stucture for Moves,
Encapsulates Squares and Pieces
Move is represented as [a-h][1-8]-[a-h][1-8] (a1-a3)
"""
import re
from Game.Piece import *
from Game.Square import *
pattern = re.compile("[a-h][1-8]-[a-h][1-8]\\b.*")
class Move(object):
    #by default move is NOT a capture move
    def __init__(self, square_f, square_t, is_capture=False):
        self.square_f = square_f
        self.square_t = square_t
        self.is_capture = is_capture
        self.capture_move = self if is_capture else Move(square_f, square_t, True)
        self.length = distance(square_f, square_t)
        self.x1 = self.square_f.col
        self.y1 = self.square_f.row
        self.x2 = self.square_t.col
        self.y2 = self.square_t.row
        self.dx = self.x2 - self.x1
        self.dy = self.y2 - self.y1
        self.dist = distance(square_f, square_t)
        self.dir = direction(square_f, square_t)
        self.captured_piece = None
    #String representation of move
    def __str__(self):
        return "{0}-{1}".format(self.square_f, self.square_t)

    @staticmethod
    def move_str(s, is_capture=False):
        move = s.strip()
        if pattern.match(move):
            sq1 = square_string(move[0:2])
            sq2 = square_string(move[3:5])
            return Move(sq1, sq2, is_capture)

    #No capture version of move_str
    @staticmethod
    def move_str_nc(s):
        return move_str(s, False)


#The set of all possible moves
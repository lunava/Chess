import unittest
from Game.Piece import *
from Game.Square import *
from Game.Board import *
from Game.Move import *


night = Knight('black')
king = King('black')
pawn = Pawn('black')
queen = Queen('black')
rook = Rook('black')
empty = Empty()
a1 = square_string('a1')
a2 = square_string('a2')
b = Board()

def test_prop(piece, color, abbrev, piece_type):
    return piece.get_color() == color and \
            piece.abbrev() == abbrev and \
            piece.get_piece_type() == piece_type
def test_sq(sq1, col, row, sq2, is_valid, dist, dir):
    return sq1.get_col() == col and \
            sq1.get_row() == row and \
            sq1.valid_sq_move(sq2) == is_valid and \
            distance(sq1, sq2) == dist and \
            direction(sq1, sq2) == dir
class TestPiece(unittest.TestCase):
    def test_piece_properties(self):
        self.assertTrue(test_prop(night, 'black', 'bn', 'night'))
    def test_square(self):
        self.assertTrue(test_sq(a1, 0, 0, a2, True, 1, 0))


class TestBoard(unittest.TestCase):
    def test_legal(self):
        b.reset()
        for _ in range(7):
            b.make_move(b.generate_legalmoves()[0])
        m = Move.move_str('a8-a1')
        piece = b.get_piece(m.square_f)
        self.assertFalse(b.is_legal(m, piece))

if __name__ == '__ main__':
    unittest.main()
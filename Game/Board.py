import re
from Game.Square import *
from Game.Piece import *
from Game.Move import *
from copy import deepcopy
from random import randrange as rr

#Standard set for chess board
INITIAL_SETUP = [generate_king_row('white'),
                generate_row('pawn', 'white'),
                generate_row('empty'),
                generate_row('empty') ,
                generate_row('empty'),
                generate_row('empty'),
                generate_row('pawn', 'black'),
                generate_king_row('black')   
                ]
"""
Rules for Castling:
    - King is not under attack
    - Move is not blocked
    - King and Rook must have previously not moved
    - Cannot castle through a check or land in a check
"""
#returns the opposide color
def opposite(side):
    return 'white' if side == 'black' else 'white'
# 0 denotes queenside castling, 1 represents kingside castling
#TODO functions and attribute

#Checks if the king of color Color is under attack
def is_check(board, color):
    king_square = None
    for c in range(8):
        for r in range(8):
            piece = board.get_piece(get_square(c,r))
            if isinstance(piece, King) and piece.color == color:
                king_square = get_square(c, r)
                break
        if king_square != None:
            break
    assert king_square != None # King square has to exist
    
    board.change_turn() # Change the color of board to the 
    enemy_pseudo =  board.generate_pseudo_legalmoves()
    for move in enemy_pseudo:
        if (move.square_t == king_square):
            return True
    return False

"""
Class Representation of a Board.
Used abbreviation based on chess.com
 * br/wr = "black/white rook"
 * br/wn = "black/white knight"
 * bb/wb = "black/white bishop"
 * bq/wq = "black/white queen"
 * bk/wk = "black/white king"
 * bp/wp = "black/white pawn"
"""
class Board(object):
    #TODO RESET function
    #Regex for chess row and col
    ROW_COL = re.compile("^[a-h][1-8]$")

    def __init__(self,intial_content=INITIAL_SETUP, turn='white'):
        self.pieces = [None for _ in range(64)]
        self.moves = []
        self.turn = turn
        index = 0
        self.contents = intial_content
        for  i in range(8):
            for j in range(8):
                self.pieces[index] = self.contents[i][j]
                index +=1
        self.winner = ''
        self.winner_known = False
        #All possible Legal moves from this position

    def __str__(self):
       out = "=== \n"
       for r in range(board_size - 1, -1, -1):
           out += "   "
           for c in range(board_size):
               p = self.get_piece(get_square(c, r))
               abbrev = p.abbrev()
               out += abbrev + ' '
           out += '\n'
       out += "=== \n"
       out += 'Next move: {}'.format(self.turn)
       return out
    #arbitary function for just changing turns of the board
    def change_turn(self):
        if (self.turn == 'white'):
            self.turn = 'black'
        else:
            self.turn = 'white'

    # Set the contents of Square sq to Piece and change turn
    def set_piece_turn(self, sq, piece, next_turn):
        if (next_turn != None):
            self.turn = next_turn
        self.pieces[sq.get_index()] = piece

    # Set the contents of Square sq to Piece without changing the turn
    def set_piece(self, sq, piece):
        self.set_piece_turn(sq, piece, None)

    # Get the piece content of the Square
    def get_piece(self, sq):
        return self.pieces[sq.get_index()]

    #Checks if the Square sq is Empty
    def is_empty(self, sq):
        return isinstance(self.get_piece(sq), Empty)

    # Reset the board to standard set up
    def reset(self):
        self.__init__()
    
    #Checks if the game ends in a tie
    #TODO
    def is_tie(self):
        return False 
    
    #Checks the number of pieces left in side Side
    #TODO
    def num_pieces(self, side):
        total = 0
        for piece in self.pieces:
            if piece.color == side:
                total +=1
        return total

    #Returns the number of moves made
    def moves_made(self):
        return len(self.moves)

    #prototype function just for checking that king is gone
    def game_over(self):
        total_kings = []
        for piece in self.pieces:
            if isinstance(piece, King):
                total_kings.append(piece)
        if len(total_kings) < 2:
            self.winner_known = True
            self.winner = total_kings[0].color
            return self.winner_known
        return False
    
    #checks The move squares exists and are not the same squares
    def is_legal(self, move, piece):
        can_jump = isinstance(piece, Knight)

        return  move.square_f != move.square_t and \
                (piece.is_valid_move(move) if not isinstance(piece, Pawn) 
                    else (piece.is_valid_move(move) and self.is_capture(move) and piece.pawn_diag(move) or 
                          piece.is_valid_move(move) and not self.is_capture(move) and not piece.pawn_diag(move)) )and \
                piece.color == self.turn and \
                not self.is_empty(move.square_f) and \
                (not self.blocked(move) if not can_jump else 
                    self.get_piece(move.square_t).color !=  self.turn) and \
                not self.winner_known
    #Checks if the any of the squares in the move are blocked by a piece
    def blocked(self, move):
        square_f = move.square_f
        dir = move.dir
        dist = move.dist
        adj = dir_adj(square_f, dir)
        while (dist > 0 and adj != None):
            if (adj != None and not self.is_empty(adj)):
                return True
            dist -=1 
            adj = dir_adj(adj, dir)
        return False

    #Checks if the following move is a valid capture move
    def is_capture(self, move):
        return not self.is_empty(move.square_t) and \
               self.get_piece(move.square_f).color != self.get_piece(move.square_t).color

    #Make a move on this Board
    def make_move(self, move):
        piece = self.get_piece(move.square_f)
        if not self.is_legal(move, piece):
            print( 'Last State: {}, move; {}, piece {}'.format(self, move, piece))
            print('last move made: {}'.format(self.moves[-1]))
        assert self.is_legal(move, piece)

        if (self.is_capture(move)):
            move = move.capture_move
            move.captured_piece = self.get_piece(move.square_t)

        self.set_piece(move.square_t, self.pieces[move.square_f.get_index()])
        self.set_piece(move.square_f, get_p('empty'))
        self.moves.append(move)
        #Account for ability to not castle after making move
        if (isinstance(piece, King) 
            or isinstance(piece, Rook)):
            piece.has_moved = True

        self.game_over()
        if (self.winner_known == True):
            print('Winner : {}'.format(self.winner))

        self.change_turn()


    #Generates all possible legal moves from this position ignoring special treatment for king
    def generate_pseudo_legalmoves(self):
        ##possible = [[[None for _ in range(2) for _ in range (total_squares)] for _ in range(total_squares)]]
        possible = []
        for c in range(board_size):
            for r in range(board_size):
                f = get_square(c, r)
                if (self.is_empty(f) or 
                self.get_piece(f).color != self.turn):
                    continue
                for x in range(board_size):
                    for y in range(board_size):
                         t = get_square(x, y)
                         piece = self.get_piece(f)
                         move = Move(f, t)
                         if self.is_legal(move, piece):
                             possible.append(move)
        return possible
    
    #Generate all legal moves that would account for checking:
    def generate_legalmoves(self):
        legalmoves = []
        for move in self.generate_pseudo_legalmoves():
            b_copy = deepcopy(self)
            b_copy.make_move(move)
            if not is_check(b_copy, self.turn):
                legalmoves.append(move)
        return legalmoves

    #function to castle king to queenside to kingside rook
    # 0 Corresponds with queenside castling, 1 corresponds with kingside
    def castle(self, king, side, color):
        sq_k = None
        sq_r = None
        rook = king.rooks[side]
        if (color == 'white'):
           sq_k = square_string('e1')
           sq_r = square_string('a1') if side == 0 else square_string('h1')
        elif (color == 'black'):
           sq_k = square_string('e8')
           sq_r = square_string('a8') if side == 0 else square_string('h8')
        #Replace king square with rook and vice versa
        self.set_piece(sq_k, rook)
        self.set_piece(sq_r, king)

    #Returns True if checkmate, only possible if in check and no legal moves
    def is_checkmate(self):
        if not is_check(self, self.color):
            return False
        else:
            if len(self.generate_pseudo_legalmoves()) > 0:
                return False
            return True

    #Check if the current move made the pawn reach other side of board
    
    def can_pawn_promo(self):
        king_row = self.contents[-1] if self.turn == 'white' else self.contents[0]
        if any(isinstance(piece, Pawn) and piece.color == self.turn for piece in king_row):
            return True
        return False    #Check if the current move made the pawn reach other side of board

    #TODO
    #Once pawn reaches to other side of board, they are promoted
    def pawn_promotion(self, new_piece):
        assert not isinstance(new_piece, Pawn)
        col = 7 if self.turn == 'white' else 0
        for row in range(8):
            sq = get_square(col, row)
            piece = self.get_piece(sq)
            if (isinstance(piece, Pawn) and piece.color == self.turn):
                self.set_piece(sq, new_piece)
                assert not isinstance(self.get_piece(sq), Pawn)
                break;

    def can_castle(self, piece, side):
        if (isinstance(piece, King) and
            not piece.has_moved and 
            not piece.rooks[side].has_moved):
            sq_k = ''
            sq_r = ''
            if (piece.color == 'white'):
                sq_k = 'e1'
                sq_r = 'b1' if side == 0 else 'g1' #  make sure that squares between are empty
            elif (piece.color == 'black'):
                sq_k = 'e8'
                sq_r = 'b8' if side == 0 else 'g8'
            assert sq_r != ''
            assert sq_k != ''

            return not self.blocked(Move.move_str('{}-{}'.format(sq_k, sq_r)))

        return False

    #Retracts the last move made
    def retract_move(self):
        assert self.moves_made() > 0
        last_move = self.moves[-1]
        sq_f = last_move.square_f
        sq_t = last_move.square_t
        temp = self.get_piece(sq_t)

        if (last_move.is_capture):
            self.set_piece(sq_t, last_move.captured_piece)
            last_move.captured_piece = None

        else:
            self.set_piece(sq_t, get_p('empty'))
        self.set_piece(sq_f, temp)
        self.moves.remove(last_move)
        self.change_turn()
        self.winner = ''
        self.winner_known = False

    #Makes a random move based on the legal moves 
    def make_random_move(self):
        moves = self.generate_legalmoves()
        self.make_move(moves[rr(len(moves))])
        # Moves made: b2-b3 , d7-d5, c2-c3, a7-a5, g2-g4, 
        #             c7-c6, f2-f4,c8-f5, d1-c2, e7-e6, c3-c4, 
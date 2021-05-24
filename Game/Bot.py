from Game.Board import *
from copy import deepcopy
from random import randrange as rr

INFITY = float('inf')
WINNING_VALUE = INFITY - 20

class Bot(object):

    def __init__(self, depth, side, game):
        self.move_found = None
        self.depth = depth
        self.side = side
        self.game = game

    #Looks for the most optimal move 
    def search_move(self):
        b = deepcopy(self.game)
        value = 0
        assert self.side == b.turn
        self.move_found = None
        if (self.side == 'white'):
            value = self.find_move(b, self.depth, True, 1, - INFITY, INFITY)
        else:
            value = self.find_move(b, self.depth, True, - 1, - INFITY, INFITY)

        return self.move_found


    #Perform alpha-beta pruning on minmax algorithm
    def find_move(self, board, depth, save_move, sense, alpha, beta):
        if (board.winner_known):
            score = self.evaluation(board, board.turn)
            if (board.winner != None):
                score = WINNING_VALUE

            if (board.winner == 'black'):
                score *= -1
            return score

        if depth == 0:
            return self.evaluation(board, board.turn)
        
        current_score = 0
        best_score = 0
        possible_moves = board.generate_legalmoves()
        #maximizer
        if (sense == 1):
            best_score = - INFITY

            for m in possible_moves:
                board.make_move(m)
                current_score = self.find_move(board, depth - 1, False, - 1, alpha, beta)
                board.retract_move()
                if (save_move and current_score > best_score):
                    self.move_found = m
                best_score = max(current_score, best_score)
                alpha =  max(alpha, best_score)
                if(beta <= alpha):
                    break
        #minimizer
        if (sense == -1):
            best_score = INFITY
            for m in possible_moves:
                board.make_move(m)
                current_score = self.find_move(board, depth - 1, False, 1 , alpha, beta)
                board.retract_move()
                if (save_move and current_score < best_score):
                    self.move_found = m
                best_score = min(current_score, best_score)
                beta = min(beta, best_score)
                if (beta <= alpha):
                    break

        return best_score

    def get_move(self):
        assert self.side == self.game.turn
        move = self.search_move()
        return move

    # Provides a score on the current state of the board
    def evaluation(self, b, side):
        num = b.num_pieces(side)
        random_factor = rr(100)
        return b.num_pieces(side) - b.num_pieces(opposite(side)) + random_factor  # To be changed to a better score
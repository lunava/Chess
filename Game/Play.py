from Game.Board import *
from Game.Bot import *


#Runs a game of chess
b = Board()
def announce_winner():
    print('Winner: {}, in {} moves'.format(b.winner, b.moves_made()))
def play():
    b.reset()
    white_bot = Bot(1, 'white', b)
    black_bot = Bot(1, 'black', b)

    playing = True
    while playing:
        if (b.winner_known):
            playing = False
            announce_winner()
        else:
            move = white_bot.get_move() if b.turn == 'white' else black_bot.get_move()
            b.make_move(move)
            print('Move made : {}'.format(move))
            print(b )
        
            


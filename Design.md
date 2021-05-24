
# Board.py
- **Class Attributes**
    - Piece[][] INITIAL_PIECES : Static pieces to set up a standard chess board
    - int _movesMade: number of moves thus far
    - String _turn: either "b" or "w" denoting the player turn
    - String winner : String denoting the winner
    - ArrayList<Move> moves : Collections of Moves made thus far
    - boolean gameOver: Denotes when the game is over
    - Piece[] _pieces: Collection of pieces in the board. Square s is at _pieces[s.index()]
    - Piece[][] _contents : the current contents of the board
    
    - boolean _subsetInitialed: **TODO** for alpha-beta pruning
   
    
- **Functions**:
    - void makeMove(Move move) {makes a MOVE}
    - boolean isLegal(Square from, Square to): returns true if the move FROM to TO is legal. Need to account for the current piece
    - boolean isLegal(Move move): returns true if Move MOVE is true
    - boolean gameOver() : returns true if a winner has been declared
    - String winner: returns the color of the winning player
    - boolean tie(): returns true if the game was a tie
    - void changeTurn(): changes the turn of the player
    - int movesMade(): returns _movesMade
    - int numPieces(String side) : number of pieces from side 
    - List<Move> legalMoves(): returns a list of legal moves that could be done in this current state/turn
    - boolean legalDistance (Square from, Square to, int distance, int dir): returns true if distance corresponds to rules
    - ArrayList<Piece> piecesInDirection (Square Sq, int dir) : returns a list of pieces that are in the direction of DIR of square SQ
    - void PiecesListHelper(ArrayList<Piece> lst, Square sq, int dir): helper function for piecesInDirection()
    - void clear(): resets the board to initial pieces
    - boolean equals(Board board): checks if this == board
    - Piece get(Square sq) : returns the contents of the square
    - void set(Square sq, Piece p, String next): Sets the contents of SQ to P and changes _TURN to NEXT
    - String turn(): returns _turn
    
## Pieces (Knight, Pawn, Queen, King, Bishop,Rook) Parent Representation
Class will be abstracted with a parent class that will share the same basic attributes

class Parent():
    abbrev():
    fullName():
    - static Piece pieceValueOf(String name) : returns the piece given name
    - Piece opposite(Piece): returns the opposite color from piece
func isValidMove():
    Check if the move is valid

Class Child():

**Functions**

    

    
# Square.py
Static class that will not change
__Class Structure__:
static Move mv(String s, boolean capture): class will be static
static Move mv(String move)

# Move.py
**Class Attributes** :
- square _from: the square that we are moving from
- square _to: the square that we are moving to
- boolean capture: returns TRUE if this move is a capture move
- move _captureMove: returns the same move if _capture is TRUE
- static Move[][][] _moves : The set of all possible moves from this move


**Functions**
- Square from(): returns _from
- Square to(): returns _to
- boolean isCapture(): returns _capture
- Move captureMove(): returns _captureMove
- int length(): returns the distance of this move *Will need to account for each different piece*
- private Move(Square from, Square to, boolean Capture): creates a private instance of this class


**It seems that LOA uses the MOVE CLASS to get the Squares FROM and TO and get the pieces based on their INDEX() from _BOARD.**


#**TODO**#
- How to represent Pieces
- How to get Square from Move
- How to get Piece from Square
- Move data structure
- Individual Move rule set for each piece
- Blocked Moves
- How to find the winner
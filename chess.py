#TODO Repetion draw implementation
#TODO Increase robustness of human player getMove
#TODO Crate func to return board state for AI learning or similar

class Board:
    """
    Main class of the chess game, all the game logic and storage are contained within this class.
    """

    def __init__(self, size = 8):
        """
        Init function for class, can take a different boardsize but nothing is implemented for boardsizes != 8.
        Creates the storage containers used in the class.
        """
        self.size = size
        self.unicodeMap = {-1 : "\u265F", -2 : "\u265C", -3 : "\u265E", -4 : "\u265D", -5 : "\u265B", -6 : "\u265A", 1 : "\u2659", 2 : "\u2656", 3 : "\u2658", 4 : "\u2657", 5 : "\u2655", 6 : "\u2654"}
        self.pieces = [[] , dict(), dict()] #-1 will always accses the last element in list
        self.cPlayer = 1
        self.enPassantAvailabe = False
        self.gameOver = False
        self.NOMoves = 0
        self.maxMoves = 200

    def initGame(self):
        """
        Initilizes the game by creating and storing all pieces.
        """
        for color in [-1, 1]:
            for i in range(6):
                self.pieces[color][i] = self.createPieces(color, i)

    def getStatus(self):
        """
        Returns the status of the game.
        """
        return self.gameOver

    def createPieces(self, color, i):
        """
        Helper switch function for the function initGame().
        """
        if i == 0:
            return self.createPawns(color)
        elif i == 1:
            return self.createRooks(color)
        elif i == 2:
            return self.createKnights(color)
        elif i == 3:
            return self.createBishops(color)
        elif i == 4:
            return self.createQueen(color)
        else:
            return self.createKing(color)

    def createPawns(self, color):
        """
        Creates the pawns for input color and returns them.
        """
        if color == 1:
            y = 1
        else:
            y = 6
        pawns = []
        for x in range(8):
            pawns.append(Pawn(color, x, y))
        return pawns
    
    def createRooks(self, color):
        """
        Creates the two rooks of input color and returns them.
        """
        if color == 1:
            y = 0
        else:
            y = 7
        rooks = [Rook(color, 0, y)]
        rooks.append(Rook(color, 7, y))
        return rooks
    
    def createKnights(self, color):
        """
        Creates the two knights of input color and returns them.
        """
        if color == 1:
            y = 0
        else:
            y = 7
        knights = [Knight(color, 1, y)]
        knights.append(Knight(color, 6, y))
        return knights
    
    def createBishops(self, color):
        """
        Creates the two bishops of input color and returns them.
        """
        if color == 1:
            y = 0
        else:
            y = 7
        bishops = [Bishop(color, 2, y)]
        bishops.append(Bishop(color, 5, y))
        return bishops
    
    def createQueen(self, color):
        """
        Creates a queen of input color and returns it.
        """
        if color == 1:
            y = 0
        else:
            y = 7
        return [Queen(color, 3, y)]
    
    def createKing(self, color):
        """
        Creates a king of input color and returns it.
        """
        if color == 1:
            y = 0
        else:
            y = 7
        return [King(color, 4, y)]

    def displayGame(self):
        """
        Displays the game using unicode characters.
        """
        board = [[0 for _ in range(self.size)] for __ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                if i % 2 == j % 2:
                    board[i][j] = "\u25A0"
                else:
                    board[i][j] = "\u25A1"

        for color in [-1, 1]:
            for pIndex, pieces in self.pieces[color].items():
                for piece in pieces:
                    if not piece.getCaptured():
                        board[7- piece.getY()][piece.getX()] = self.unicodeMap[color * (pIndex + 1)]

        for i in range(len(board)):
            print(str(8-i) + "   " + " ".join(board[i]))
        print()
        print("    A B C D E F G H")
        print("    1 2 3 4 5 6 7 8")
    
    def test(self):
        pass
        # print(self.pieces[1][0][0].legalMoves(self))
        # self.pieces[1][0][0].move([1, 5])
        # self.pieces[1][0][0].setFirstMove(False)
        # print(self.pieces[1][0][0].legalMoves(self))

    def getMove(self):
        """
        Gets a move from a human player and executes it.
        """
        if (self.checkLegalMoves() and self.checkCheck(color = self.cPlayer)):
            print("Checkmate, player:", str(self.cPlayer) + ". Lost the game.")
            self.gameOver = True
            return
        
        if self.checkDraw() or self.checkDeadPos():
            print("Draw, game over")
            self.gameOver = True
            return

        i, j = None, None
        while i == None:
            piecePos = input("Input the position of the piece you can to move. (X Y)\n")
            piecePos = piecePos.strip().split(" ")
            try:
                i, j = self.findPiece([int(piecePos[0]) - 1, int(piecePos[1]) - 1], self.cPlayer)
            except IndexError:
                pass

            if i == None:
                print("Please select a valid piece.")

        move = None
        validMoves = self.pieces[self.cPlayer][i][j].legalMoves(self)
        print(validMoves)
        captures = [validMoves[i][2] for i in range(len(validMoves))]
        validMoves = [validMoves[i][:2] for i in range(len(validMoves))]
        if self.pieces[self.cPlayer][i][j].getType() in ["King", "Rook"]:
            castling = self.checkCastling()
            if castling[0]:
                validMoves.append(["0-0-0"])
            if castling[1]:
                validMoves.append(["0-0"])

        if len(validMoves) == 0:
            print("This piece has no legal moves, please select another piece.")
            self.getMove()

        while move == None:
            move = input("Where do you want to move the piece? (X Y)\n")
            move = move.strip().split(" ")
            move = [int(move[i]) - 1 for i in range(2)]
            if not move in validMoves:
                move = None
                print("Please input a valid move.")

        oldX = self.pieces[self.cPlayer][i][j].getX()
        oldY = self.pieces[self.cPlayer][i][j].getY()
       
        if move in ["0-0", "0-0-0"]:
            self.doCastle(move)
        elif captures[validMoves.index(move)]:
            self.doCapture([i, j], move)
        else:
            self.doMove([i, j], move)

        if self.enPassantAvailabe:
            for pawn in self.pieces[-self.cPlayer][0]:
                pawn.setEnPassant(False)

        if self.pieces[self.cPlayer][i][j].getType() == "Pawn":
            if abs(move[1] - oldY) == 2:
                self.pieces[self.cPlayer][i][j].setEnPassant(True)
                self.enPassantAvailabe = True

            promotionLocs = [-1, 7, 0]
            if self.pieces[self.cPlayer][i][j].getY() == promotionLocs[self.pieces[self.cPlayer][i][j].getColor()]:
                self.promotion(self.pieces[self.cPlayer][i][j])

        self.pieces[self.cPlayer][i][j].setFirstMove(False)
        self.cPlayer = -self.cPlayer
        self.NOMoves += 1

    def doMove(self, pieceID = None, move = None, location = None):
        """
        Moves a piece using move and piecedata or location.
        """
        if location != None and pieceID == None:
            pieceID = self.findPiece(location, self.cPlayer)

        if pieceID != None:
            self.pieces[self.cPlayer][pieceID[0]][pieceID[1]].move(move)
        else:
            raise Exception("No piece or location data")

    def doCapture(self, pieceID, move):
        """
        Performs a capture move, useing move and piecedata
        """
        i, j = self.findPiece([move[0], move[1]], -self.cPlayer)
        self.pieces[-self.cPlayer][i][j].setCaptured(True)
        self.pieces[self.cPlayer][pieceID[0]][pieceID[1]].move(move)

    def promotion(self, piece, desiredPiece = None):
        """
        Takes a piece and if the piece is pawn upgrades it to the desired piece.
        Input: piece, the piece being considered
        desiredPiece, if it is None takes a user input for desired piece otherwise uses the given value.
        """
        pieceDict = {"queen" : 4, "bishop" : 3, "knight" : 2, "rook" : 1}
        if piece.getType() == "Pawn":
            while desiredPiece == None:
                desiredPiece = input("What piece to do you want to promote to?\n").lower()
                if desiredPiece not in pieceDict.keys():
                    print("Please enter a valid piece.")
                    desiredPiece = None

            piece.setCaptured(True)
            if pieceDict[desiredPiece] == 4:
                self.pieces[piece.getColor()][pieceDict[desiredPiece]].append(Queen(piece.getColor(), 0, 0))
            elif pieceDict[desiredPiece] == 3:
                self.pieces[piece.getColor()][pieceDict[desiredPiece]].append(Bishop(piece.getColor(), 0, 0))
            elif pieceDict[desiredPiece] == 2:
                self.pieces[piece.getColor()][pieceDict[desiredPiece]].append(Knight(piece.getColor(), 0, 0))
            elif pieceDict[desiredPiece] == 1:
                self.pieces[piece.getColor()][pieceDict[desiredPiece]].append(Rook(piece.getColor(), 0, 0))

            self.pieces[piece.getColor()][pieceDict[desiredPiece]][-1].move([piece.getX(), piece.getY()])

        else:
            raise Exception("Tried to promote piece that is not a pawn.")

    def findPiece(self, location, color):
        """
        Tries to find a piece of input color and on coords input x, y.

        If there is a piece present returns the indices in the game memeory other wise none, none.
        """
        pieces = list(self.pieces[color].values())
        for i in range(len(pieces)):
            for j in range(len(pieces[i])):
                if pieces[i][j].getX() == location[0] and pieces[i][j].getY() == location[1] and not pieces[i][j].getCaptured():
                    return i, j
        return None, None

    def isOccupied(self, location):
        """
        Checks if there is a piece on the input coords x, y.

        Returns true if there is a piece present otherwise false.
        """
        for color in [-1, 1]:
            for pieces in self.pieces[color].values():
                for piece in pieces:
                    if self.checkEnPassant([location[0], location[1]], piece):
                        return True
                    if piece.getX() == location[0] and piece.getY() == location[1] and not piece.getCaptured():
                        return True
        return False
    
    def checkCapture(self, location, color):
        """
        Checks if a move is a capture.
        locations is the coordinates in question.
        color is the color of the current player.

        Returns true if it is a capture, false if it is not a capture
        """
        for pieces in self.pieces[-color].values():
            for piece in pieces:
                if self.checkEnPassant([location[0], location[1]], piece):
                    return True
                if piece.getX() == location[0] and piece.getY() == location[1] and not piece.getCaptured():
                    return True
        return False
    
    def checkCastling(self):
        """
        Checks if a player can castle.
        Returns [bool, bool], where bool1 is if short castle is possible and bool2 for long.
        """
        king = self.pieces[self.cPlayer][5][0]
        if not king.getFirstMove:
            return [False, False]
        
        castlingPossible = [True, True]
        for i in range(2): #Hardcodes since only the first two rooks can castle and dynamicly doing it for len might lead to problems with promoted pieces.
            if self.pieces[self.cPlayer][1][i].getFirstMove():
                for x in range(sorted([self.pieces[self.cPlayer][1][i].getX(), king.getX()])):
                    if self.isOccupied([x, king.getY()]):
                        castlingPossible[i] = False
                        break
            else:
                castlingPossible[i] = False

        castleNot = ["0-0", "0-0-0"]
        oldKx, oldKy = king.getX(), king.getY()
        for i in range(len(castlingPossible)):
            if castlingPossible[i]:
                #Does virtual castle and checks if king can be attacked after castling

                oldRx, oldRy = self.pieces[self.cPlayer][1][i].getX(), self.pieces[self.cPlayer][1][i].getY()
                self.doCastle(castleNot[i])
                if self.checkCheck(color = self.cPlayer):
                    castlingPossible[i] = False

                self.pieces[self.cPlayer][5][0].move([oldKx, oldKy])
                self.pieces[self.cPlayer][1][i].move([oldRx, oldRy])

        return castlingPossible
    
    def doCastle(self, move):
        """
        Performs the castle of type move
        """
        if move == "0-0":
            self.pieces[self.cPlayer][5][0].move(2, self.pieces[self.cPlayer][5][0].getY())
            self.pieces[self.cPlayer][1][0].move(3, self.pieces[self.cPlayer][1][0].getY())

        else:
            self.pieces[self.cPlayer][5][0].move(6, self.pieces[self.cPlayer][5][0].getY())
            self.pieces[self.cPlayer][1][0].move(5, self.pieces[self.cPlayer][1][0].getY())
    
    def checkEnPassant(self, location, piece):
        """
        Checks if the piece a piece can be captured using en passant.
        Input location are the coords of the sqaure being considered.
        Piece is the piece being considered.

        Returns true if is it possible otherwise false.
        """
        if piece.getType() == "Pawn":
            if piece.getEnPassant():
                if location[0] == piece.getX() and location[1] == piece.getY()  - piece.getColor():
                    return True
        return False
    
    def checkCheck(self, king = None, color = None):
        """
        Checks the current board for check.
        Takes input, king and color.
        If a king input is given searches if the king is in check.
        If a color input is given checks the king of that color for check.
        If none are given raises an error.

        Returns true for check and false if it is not check.
        """

        if king == None:
            if color != None:
                king = self.pieces[color][5][0]
            else:
                raise Exception("No args given.")

        """
        When looking for check we can check the legal moves for Queen, knight and pawn from the kings location and if there are any caputering move the king will be in check!
        """
        kX = king.getX()
        kY = king.getY()
        color = king.getColor()
        vQueen = Queen(color, kX, kY)
        vKnight = Knight(color, kX, kY)
        vPawn = Pawn(color, kX, kY)

        legalMoves = vQueen.legalMoves(self)
        legalMoves += vKnight.legalMoves(self)
        legalMoves += vPawn.legalMoves(self)

        for move in legalMoves:
            if move[2]:
                return True

        #Special case for enemy king
        eKing = self.pieces[-color][5][0]
        for x in range(-1,2):
            for y in range(-1,2):
                if eKing.getX() + x == king.getX() and eKing.getY() + y == king.getY():
                    return True
        return False
    
    def checkLegalMoves(self):
        """
        Checks if the current player has any legalmove that doesnt end with king being in check.
        """
        legalMoves = []
        pieces = list(self.pieces[self.cPlayer].values())
        for i in range(len(pieces)):
            for j in range(len(pieces[i])):
                legalMoves = pieces[i][j].legalMoves(self)
                for move in legalMoves:
                    if not self.checkLegal([i, j], move):
                        return False
        return True
    
    def checkLegal(self, pieceID, move):
        """
        Checks if a move is legal for a piece.
        pieceID contains the ID for the piece.
        move is the move to to checked.
        """
        if move[2]:
            if not self.vCapture(pieceID, move[0:2]):
                return False
        else:
            if not self.vMove(pieceID, move[0:2]):
                return False
        return True
    
    def vMove(self, pieceID, move):
        """
        Executes a virtual move, and checks if it results on check for the own king.
        Returns, true for check otherwise false
        """
        oldPos = [self.pieces[self.cPlayer][pieceID[0]][pieceID[1]].getX(), self.pieces[self.cPlayer][pieceID[0]][pieceID[1]].getY()]
        self.pieces[self.cPlayer][pieceID[0]][pieceID[1]].move(move)

        result = self.checkCheck(color = self.pieces[self.cPlayer][pieceID[0]][pieceID[1]].getColor())
        self.pieces[self.cPlayer][pieceID[0]][pieceID[1]].move(oldPos)
        return result

    def vCapture(self, pieceID, move):
        """
        Executes a virtual capture, and checks if it results on check for the own king.
        Returns, true for check otherwise false
        """
        oldPos = [self.pieces[self.cPlayer][pieceID[0]][pieceID[1]].getX(), self.pieces[self.cPlayer][pieceID[0]][pieceID[1]].getY()]
        i, j = self.findPiece([move[0], move[1]], -self.pieces[self.cPlayer][pieceID[0]][pieceID[1]].getColor())

        self.pieces[-self.cPlayer][i][j].setCaptured(True)
        self.pieces[self.cPlayer][pieceID[0]][pieceID[1]].move(move)
        
        result = self.checkCheck(color = self.pieces[self.cPlayer][pieceID[0]][pieceID[1]].color)
        self.pieces[self.cPlayer][pieceID[0]][pieceID[1]].move(oldPos)
        self.pieces[-self.cPlayer][i][j].setCaptured(False)
        return result
    
    def checkDeadPos(self):
        """
        Checks if position is 'dead', by remaining material and if the number of moves is less than the max result.
        Returns true for a dead position oterwise false.
        """
        if self.NOMoves > self.maxMoves:
            return True
        
        piecesToCheck = [[], [], []]
        for color in [-1, 1]:
            for pieces in self.pieces[color].values():
                for piece in pieces:
                    if not piece.getCaptured():
                        piecesToCheck[color].append(piece)
                        if piece.getType() not in ["King", "Knight", "Bishop"]:
                            return False
        
        if len(piecesToCheck[1]) > 2 or len(piecesToCheck[-1]) > 2:
            return False

        if len(piecesToCheck[1]) == 2 and len(piecesToCheck[-1]) == 2:
            if piecesToCheck[1].getType() == "Knight" or piecesToCheck[-1].getType() == "Knight":
                return False
            
            if (piecesToCheck[1].getX() % 2 == piecesToCheck[1].getY() % 2) == (piecesToCheck[-1].getX() % 2 == piecesToCheck[-1].getY() % 2):
                return False
            
        return True
    
    def checkDraw(self):
        """
        Checks if the current player has no legalmoves, if this is the case it will be a draw.
        """
        if not self.checkCheck(color = self.cPlayer):
            if self.checkLegalMoves():
                return True
        return False

class Piece():
    """
    Parent class of all the pieces contains function that are universal for all pieces.
    """
    def __init__(self, color, x, y, ptype):
        self.color = color
        self.x = x
        self.y = y
        self.ptype = ptype
        self.isCaptured = False
        self.firstMove = True

    def move(self, action):
        """
        Moves a pieces to the coords specified in action.
        """
        self.x = action[0]
        self.y = action[1]

    def getColor(self):
        """
        Returns the color of the piece.
        """
        return self.color
    
    def getX(self):
        """
        Returns the x coord for the current piece.
        """
        return self.x
    
    def getY(self):
        """
        Returns the y coord for the current piece.
        """
        return self.y
    
    def getCaptured(self):
        """
        Returns the captured status for the piece
        """
        return self.isCaptured
    
    def setCaptured(self, update):
        """
        Allows setting of the captured status of piece according to the update.
        """
        self.isCaptured = update
    
    def getType(self):
        """
        Returns the type of the current piece.
        """
        return self.ptype
    
    def getFirstMove(self):
        """
        Returns if it is the piece first move.
        """
        return self.firstMove
    
    def setFirstMove(self, update):
        """
        Allows setting the status of first move according to the update.
        """
        self.firstMove = update

class Pawn(Piece):
    def __init__(self, color, x, y):
        self.ptype = "Pawn"
        super().__init__(color, x, y, self.ptype)
        self.enPassantPossible = False

    def legalMoves(self, board):
        """
        Calculates the legal moves for the piece according to the board and returns them.
        """
        moves = []
        for x in range(-1, 2):
            if -1 < self.x + x and self.x + x < 8:
                if x == 0 and not board.isOccupied([self.x + x, self.y + self.color]):
                    moves.append([self.x + x, self.y + self.color, False])
                elif x != 0 and board.checkCapture([self.x + x, self.y + self.color], self.color):
                    moves.append([self.x + x, self.y + self.color, True])

        if self.firstMove:
            moves.append([self.x, self.y + 2*self.color, False])

        return moves

    def getEnPassant(self):
        """
        Returns if the status of en passant possible.
        """
        return self.enPassantPossible
    
    def setEnPassant(self, update):
        """
        Allows setting the status of en passant according to update.
        """
        self.enPassantPossible = update

class Rook(Piece):
    def __init__(self, color, x, y):
        self.ptype = "Rook"
        super().__init__(color, x, y, self.ptype)

    def legalMoves(self, board):
        """
        Calculates the legal moves for the piece according to the board and returns them.
        """
        moves = []
        for x in range(self.x+1, 8):
            if not board.isOccupied([x, self.y]):
                moves.append([x, self.y, False])
            else:
                if board.checkCapture([x, self.y], self.color):
                    moves.append([x, self.y, True])
                break

        for x in range(self.x-1, -1, -1):
            if not board.isOccupied([x, self.y]):
                moves.append([x, self.y, False])
            else:
                if board.checkCapture([x, self.y], self.color):
                    moves.append([x, self.y, True])
                break

        for y in range(self.y+1, 8):
            if not board.isOccupied([self.x, y]):
                moves.append([self.x, y, False])
            else:
                if board.checkCapture([self.x, y], self.color):
                    moves.append([self.x, y, True])
                break

        for y in range(self.y-1, -1, -1):
            if not board.isOccupied([self.x, y]):
                moves.append([self.x, y, False])
            else:
                if board.checkCapture([self.x, y], self.color):
                    moves.append([self.x, y, True])
                break
        return moves

class Bishop(Piece):
    def __init__(self, color, x, y):
        self.ptype = "Bishop"
        super().__init__(color, x, y, self.ptype)

    def legalMoves(self, board):
        """
        Calculates the legal moves for the piece according to the board and returns them.
        """
        moves = []
        for x in range(self.x + 1, 8):
            y = self.y + (x - self.x)
            if y < 8:
                if not board.isOccupied([x, y]):
                    moves.append([x, y, False])
                else:
                    if board.checkCapture([x, y], self.color):
                        moves.append([x, y, True])
                    break
            
            y = self.y - (x - self.x)
            if -1 < y:
                if not board.isOccupied([x, y]):
                    moves.append([x, y, False])
                else:
                    if board.checkCapture([x, y], self.color):
                        moves.append([x, y, True])
                    break

        for x in range(self.x - 1, -1, -1):
            y = self.y - (x - self.x)
            if y < 8:
                if not board.isOccupied([x, y]):
                    moves.append([x, y, False])
                else:
                    if board.checkCapture([x, y], self.color):
                        moves.append([x, y, True])
                    break

            y = self.y + (x - self.x)
            if -1 < y:
                if not board.isOccupied([x, y]):
                    moves.append([x, y, False])
                else:
                    if board.checkCapture([x, y], self.color):
                        moves.append([x, y, True])
                    break
        return moves

class Knight(Piece):
    def __init__(self, color, x, y):
        self.ptype = "Knight"
        super().__init__(color, x, y, self.ptype)

    def legalMoves(self, board):
        """
        Calculates the legal moves for the piece according to the board and returns them.
        """
        moves = []
        for move in [[1, 2], [1, -2], [-1, 2], [-1, -2], [2, 1], [2, -1], [-2, 1], [-2, -1]]:
            if -1 < self.x + move[0] and self.x + move[0] < 8 and -1 < self.y + move[1] and self.y + move[1] < 8:
                if not board.isOccupied([self.x + move[0], self.y + move[1]]):
                    moves.append([self.x + move[0], self.y + move[1], False])
                elif board.checkCapture([self.x + move[0], self.y + move[1]], self.color):
                    moves.append([self.x + move[0], self.y + move[1], True])
        return moves

class King(Piece):
    def __init__(self, color, x, y):
        self.ptype = "King"
        super().__init__(color, x, y, self.ptype)

    def legalMoves(self, board):
        """
        Calculates the legal moves for the piece according to the board and returns them.
        """
        moves = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                if not board.isOccupied([self.x + x, self.y + y]) and not board.checkCheck(self):
                    moves.append([self.x + x, self.y + y, False])
                elif board.checkCapture([self.x + x, self.y + y], self.color) and not board.checkCheck(self):
                    moves.append([self.x + x, self.y + y, True])
        return moves

class Queen(Piece):
    def __init__(self, color, x, y):
        self.ptype = "Queen"
        super().__init__(color, x, y, self.ptype)
        self.rook = Rook(color, x, y)
        self.bishop = Bishop(color, x, y)

    def legalMoves(self, board):
        """
        Calculates the legal moves for the piece according to the board and returns them.
        The queen is a combo between a rook and a bishop so by getting the legal moves for these at the current pos we get the moves for the queen.
        """
        moves = self.rook.legalMoves(board)
        moves += self.bishop.legalMoves(board)
        return moves
    
    def move(self, action):
        """
        Special case move function for the queen that moves its internal rook and bishop aswell.
        """
        self.x = action[0]
        self.y = action[1]
        self.rook.move(action)
        self.bishop.move(action)
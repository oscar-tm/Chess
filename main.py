from chess import *

game = Board()
game.initGame()
game.test()
game.displayGame()
while not game.getStatus:
    game.getMove()
    game.displayGame()
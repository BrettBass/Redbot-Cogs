import sof
import gameState

gs = gameState.GameState()

sof.printGame()

while(not gs.checkQuit()):
    sof.game(gs)
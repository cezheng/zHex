# zHex
# 12/02/2012 version 0.1 Ce Zheng

__version__='0.1'

import os,sys
from functools import partial
sys.path.append(os.path.dirname(__file__)+'/..')
from lib.graphics import *
from gui.HexGUIConf import *

def main():
        global win
        windowSize=600
        win=GraphWin("zHex",windowSize,windowSize)
        agent=HexClickAgent(win)
        menu=HexMenu(win,[["Game",["New Game","PVP First Go","PVP Second Go","PVAI First Go","PVAI Second Go"],["Network","Host","Join"],"Exit"],["Move","Undo","Redo"],["Help","About"]],[[None,[None,partial(agent.resetGame,0),partial(agent.resetGame,1),partial(agent.resetGame,2),partial(agent.resetGame,3)],[None,partial(agent.resetGame,4),partial(agent.resetGame,5)],agent.forceQuit],[None,agent.undo,agent.redo],[None,agent.about]])
        win.master.protocol("WM_DELETE_WINDOW",agent.forceQuit)
        while agent.isRunning():
                agent.newGame()
                if agent.play()!=None:
                        agent.hold()
                time.sleep(.2)

if __name__=="__main__":
        win=None
        main()


from lib.graphics import *
from gui.HexBoard import *
from util.Stack import *

class Player:
        def __init__(self,color,num):
                self.color=color
                self.num=num
        def getColor(self):
                return self.color
        def getNum(self):
                return self.num

class HexGame(object):
        def __init__(self,win,go,size):
                self.running=True
                self.win=win
                self.size=size
                self.players=(Player("blue",1),Player("red",2))
                self.curPlayer=(go+1)%2
                self.board=None
                self.turnText=None
        def end(self):
                self.board.undraw()
                self.turnText.undraw()
                self.board=None
                self.turnText=None
                self.running=False
                self.win.mouseX=self.win.mouseY=[]       #get out of the getMouse() loop
        def isRunning(self):
                return self.running
        def switchPlayer(self):
                self.curPlayer=(self.curPlayer+1)%2
                self.turnText.setText("Player "+str(self.curPlayer+1)+"'s Turn")
        def gameInit(self):
                windowSize=self.win.getWidth()
                self.board=HexBoard(self.win,9,20,Point(50,300))
                self.turnText=Text(Point(windowSize/2,windowSize/10),"Player "+str(self.curPlayer+1)+"'s Turn")
                self.turnText.setSize(20)
                self.turnText.draw(self.win)
        def playerGo(self,co):
                if self.board.placePiece(co,self.players[self.curPlayer]):
                        winner=self.board.winner() 
                        if winner==None:
                                self.switchPlayer()
                        elif winner==self.curPlayer+1:
                                self.turnText.setText("Player "+str(winner)+" wins.") 
                                return winner
                else:
                        return False
                return None
        def play(self,**opt):
                self.gameInit()
                while self.running:
                        self.turnText.setTextColor(self.players[self.curPlayer].getColor())
                        try:
                                p=self.win.getMouse()
                                co=self.board.locate(p)
                        except:
                                self.running=False
                                return None
                        if co!=():
                                if self.playerGo(co)==self.curPlayer+1: 
                                        return self.curPlayer+1
                return None
        def undoClick(self):
                if self.board.removePiece():
                        self.switchPlayer()
        def redoClick(self):
                if self.board.redo():
                        self.switchPlayer()
        def forceQuit(self):
                self.running=False
                self.win.mouseX=self.win.mouseY=[]       #get out of the getMouse() loop
                self.win.close()
                exit(0)

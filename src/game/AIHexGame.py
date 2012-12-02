from HexGame import *

class AIHexGame(HexGame):
        def __init__(self,AI,*args,**kw):
                super(AIHexGame,self).__init__(*args,**kw)
                self.AI=AI
        def AIGo(self):
                co=self.AI.think(self.board)
                if self.board.placePiece(co,self.players[self.curPlayer]):
                        winner=self.board.winner()
                        if winner==None:
                                self.switchPlayer()
                        elif winner==self.curPlayer+1:
                                self.turnText.setText("Player "+str(winner)+" wins.") 
                                return winner
                return None
        def play(self,**opt):
                self.gameInit()
                AIAs=(self.curPlayer+1)%2+1
                self.curPlayer=0
                winner=None
                while self.running:
                        if AIAs==1:
                                winner=self.AIGo()
                                if winner==self.curPlayer+1: 
                                        return winner
                        self.turnText.setTextColor(self.players[self.curPlayer].getColor())
                        while not self.win.isClosed():
                                try:
                                        p=self.win.getMouse()
                                        co=self.board.locate(p)
                                except:
                                        self.running=False
                                        return None
                                if co!=():
                                        winner=self.playerGo(co)
                                        if winner!=False:
                                                break
                        if winner==self.curPlayer+1:
                                        return winner
                        if AIAs==2:
                                winner=self.AIGo()
                                if winner==self.curPlayer+1: 
                                        return winner
                return None
	def undoClick(self):
		self.board.removePiece()
		self.board.removePiece()
	def redoClick(self):
		self.board.redo()
		self.board.redo()


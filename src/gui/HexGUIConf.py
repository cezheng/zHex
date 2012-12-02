import tkMessageBox
from lib.graphics import *
from game.HexGame import *
from game.AIHexGame import *
from game.NetHexGame import *
from ai.HexAI import *

class HexMenu:
        def __init__(self,win,labels,funs):
                self.menu=tk.Menu(win.master)
                for i in range(len(labels)):
                        self.mkSubmenu(self.menu,labels[i],funs[i])
                win.master.config(menu=self.menu)
        def mkSubmenu(self,menu,labels,funs):
                submenu=tk.Menu(menu,tearoff=0)
                for i in range(len(labels)-1):
                        if type(labels[i+1])==list:
                                subsubmenu=self.mkSubmenu(submenu,labels[i+1],funs[i+1])
                        else:
                                if labels[i+1]=="":
                                        submenu.add_separator()
                                else:
                                        submenu.add_command(label=' '+labels[i+1]+' ',command=funs[i+1])
                menu.add_cascade(label=' '+labels[0]+' ',menu=submenu)
                return menu

class HexClickAgent:
        validChoices=set(range(6))
        def __init__(self,win):
                self.game=None
                self.choice=0
                self.running=True
                self.holding=False
                self.win=win
                self.menu=None
        def redo(self):
                try:self.game.redoClick()
                except:pass
        def undo(self):
                try:self.game.undoClick()
                except:pass
        def newGame(self,choice=-1):
                if self.game!=None:
                        return
                if choice==-1:
                        choice=self.choice
                if not choice in HexClickAgent.validChoices:
                        return
                if choice==0:
                        self.game=HexGame(win=self.win,go=1,size=9)
                elif choice==1:
                        self.game=HexGame(win=self.win,go=2,size=9)
                elif choice==2:
                        self.game=AIHexGame(win=self.win,go=1,size=9,AI=HexAI())
                elif choice==3:
                        self.game=AIHexGame(win=self.win,go=2,size=9,AI=HexAI())
                elif choice==4:
                        self.game=HostHexGame(win=self.win,go=1,size=9,port=7878)
                elif choice==5:
                        self.game=JoinHexGame(win=self.win,go=2,size=9,host='127.0.0.1',port=7878)
                self.choice=choice
                self.holding=False
                self.running=True
        def resetGame(self,choice=-1):
                if choice==-1:
                        choice=self.choice
                print "reset"+str(choice)
                if choice in HexClickAgent.validChoices:
                        self.game.end()
                        self.game=None
                        self.newGame(choice)
        def play(self):
                try:
                        return self.game.play()
                except:
                        import traceback
                        traceback.print_exc()
                        return None
        def forceQuit(self):
                #if call quit() or exit() here, the main loop won't end
                self.holding=False
                self.running=False
                self.game.forceQuit()
        def about(self):
                tkMessageBox.showinfo(title="About",message="Ce Zheng\ncezheng.cs@gmail.com")
        def isRunning(self):
                return self.running
        def hold(self):
                self.holding=True
                while self.holding:
                        self.win.getMouse()
        def release(self):
                self.holding=False


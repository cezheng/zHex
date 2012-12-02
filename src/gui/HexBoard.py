import math
from util.Stack import *
from util.Vector import *
from lib.graphics import *

sq3=math.sqrt(3)
halfSq3=math.sqrt(3)/2

class HexMove:
        def __init__(self,player,pos):
                self.player=player
                self.pos=pos
        def getPlayer(self): return self.player
        def getPos(self): return self.pos

class HexBlock:
        Xs=Vector([-1.0,-0.5,0.5,1,0.5,-0.5])
        Ys=Vector([.0,halfSq3,halfSq3,.0,-halfSq3,-halfSq3])
        Vec=[Vector(v) for v in [(0,1),(halfSq3,0.5),(halfSq3,-0.5)]]
        def __init__(self,win,edgeLen,center):
                self.win=win
                self.X,self.Y=center
                self.xs=HexBlock.Xs*edgeLen
                self.ys=HexBlock.Ys*edgeLen
                self.edgeLen=edgeLen
                self.player=None
                points=[]
                for i in range(6):
                        points.append(Point(self.xs[i]+self.X,self.ys[i]+self.Y))
                self.region=Polygon(points)
                self.region.setWidth(2)
                self.region.draw(self.win)
                self.piece=Circle(Point(self.X,self.Y),self.edgeLen/2)
        def undraw(self):
                self.region.undraw()
                self.piece.undraw()
        def clickIn(self,x,y):
                dv=Vector([x-self.X,y-self.Y])
                limit=halfSq3*self.edgeLen
                for v in HexBlock.Vec:
                        if abs(v*dv)>limit:
                                return False
                return True
        def placePiece(self,player):
                if self.player==None:
                        self.piece.setFill(player.getColor())
                        self.piece.draw(self.win)
                        self.player=player.getNum()
                        return True
                else: return False
        def removePiece(self):
                if self.player!=None:
                        self.player=None
                        self.piece.undraw()
                        return True
                else: return False
        def getCenter(self):
                return self.X,self.Y
        def getPlayer(self):
                return self.player

class HexBoard:
        Vec=[Vector(v) for v in [(halfSq3,0.5),(halfSq3,-0.5)]]
        adVec=[Vector(v) for v in [(1,0),(0,1),(-1,0),(0,-1),(-1,1),(1,-1)]]
        def __init__(self,win,size,gridLen,origin):
                self.active=True
                self.mark1,self.mark2=[0]*size,[0]*size
                self.win=win
                self.size=size
                self.gridLen=gridLen
                self.grid=[]
                self.moveStack=Stack(size*size)
                for i in range(size):
                        self.grid.append([])
                self.Xo,self.Yo=origin.getX(),origin.getY()
                pio=self.Xo,self.Yo
                for i in range(size):
                        newCenter=pio
                        for j in range(size):
                                newGrid=HexBlock(win,gridLen,newCenter)
                                self.grid[i].append(newGrid)
                                newCenter=(newCenter[0]+1.5*gridLen,newCenter[1]+halfSq3*gridLen)
                        pio=(pio[0]+1.5*gridLen,pio[1]-halfSq3*gridLen)
                self.drawOuterLines()
        def undraw(self):
                if not self.active:
                        return
                map(lambda item: item.undraw,self.lines)
                map(lambda row: map(lambda item: item.undraw(),row),self.grid)
                self.active=False
        def drawOuterLines(self):
                self.lines=[]
                p1=Point(self.Xo-self.gridLen*2,self.Yo)
                p2=Point(self.Xo+1.5*(self.size-1)*self.gridLen,self.Yo+halfSq3*(self.size+1.0/3)*self.gridLen)
                p3=Point(self.Xo+(3*self.size-1)*self.gridLen,self.Yo)
                p4=Point(self.Xo+1.5*(self.size-1)*self.gridLen,self.Yo-halfSq3*(self.size+1.0/3)*self.gridLen)
                ps=[p1,p2,p3,p4]
                for i in range(4):
                        self.lines.append(Line(ps[i],ps[(i+1)%4]))
                        if i%2:
                                self.lines[i].setOutline("red")
                        else:
                                self.lines[i].setOutline("blue")
                        self.lines[i].setWidth(2)
                        self.lines[i].draw(self.win)
        def locate(self,p):
                x,y=p.getX(),p.getY()
                if self.size==1:
                        if self.grid[0][0].clickIn(x,y):
                                return (0,0)
                        else: 
                                return ()
                elif self.size==2:
                        cord1=0
                        cord2=0
                else:
                        dv=Vector([x-self.Xo,y-self.Yo])
                        prod1=dv*HexBoard.Vec[1]
                        prod2=dv*HexBoard.Vec[0]
                        if halfSq3*dv[1]+0.5*dv[0]>0: param1=-1 #rotate 30 degree counter-clockwise
                        else: param1=1
                        if halfSq3*dv[1]-0.5*dv[0]<0: param2=-1 #rotate 30 degree clockwise
                        else: param2=1
                        cord1=int((prod1+param1*math.sqrt((dv*dv-prod1*prod1)/3))/(sq3*self.gridLen))
                        cord2=int((prod2+param2*math.sqrt((dv*dv-prod2*prod2)/3))/(sq3*self.gridLen))
                if not (0<=cord1<self.size and 0<=cord2<self.size):
                        return ()
                if self.grid[cord1][cord2].clickIn(x,y):
                        return (cord1,cord2)
                elif cord1+1<self.size and self.grid[cord1+1][cord2].clickIn(x,y):
                                return (cord1+1,cord2)
                elif cord2+1<self.size and self.grid[cord1][cord2+1].clickIn(x,y):
                        return (cord1,cord2+1)
                elif cord1+1<self.size and cord2+1<self.size and self.grid[cord1+1][cord2+1].clickIn(x,y):
                        return (cord1+1,cord2+1)
                else: return ()
        def placePiece(self,cord,player):
                success=self.grid[cord[0]][cord[1]].placePiece(player)
                if not success: return False
                n=player.getNum()
                if n==1: self.mark1[cord[0]]+=1
                elif n==2: self.mark2[cord[1]]+=1
                self.moveStack.push(HexMove(player,cord))
                return success
        def removePiece(self):
                cord=self.moveStack.pop()
                if cord!=None:
                        cord=cord.getPos()
                else:
                        return False
                n=self.grid[cord[0]][cord[1]].getPlayer()
                success=self.grid[cord[0]][cord[1]].removePiece()
                if not success: return False
                if n==1: self.mark1[cord[0]]-=1
                elif n==2: self.mark2[cord[1]]=-1
                return success
        def redo(self):
                item=self.moveStack.redo()
                if item!=None:
                        player=item.getPlayer()
                        cord=item.getPos()
                        success=self.grid[cord[0]][cord[1]].placePiece(player)
                        if not success: return False
                        n=player.getNum()
                        if n==1: self.mark1[cord[0]]+=1
                        elif n==2: self.mark2[cord[1]]+=1
                return False
        def winner(self):
                if 0 in self.mark1 and 0 in self.mark2: return None
                if self.scan(1): 
                        return 1
                elif self.scan(2): 
                        return 2
                else:
                        return None
        def inRange(self,pos):
                return 0<=pos[0]<self.size and 0<=pos[1]<self.size
        def getAdjacent(self,iset):
                adjacent=set()
                for item in iset:
                        for v in HexBoard.adVec:
                                candidate=tuple(map(sum,zip(item,v)))
                                if self.inRange(candidate): adjacent.add(candidate)
                return adjacent
        def scan(self,player):
                adjacent=set()
                for j in range(self.size):
                        iset=set()
                        for i in range(self.size):
                                if player==1:
                                        p=self.grid[j][i].getPlayer()
                                        additem=(j,i)
                                elif player==2:
                                        p=self.grid[i][j].getPlayer()
                                        additem=(i,j)
                                if player==p:
                                        iset.add(additem) 
                        if iset.isdisjoint(adjacent) and j>0:
                                return False
                        adjacent=self.getAdjacent(iset)
                return True
        def getGrid(self):
                return self.grid
        def getStack(self):
                return self.moveStack

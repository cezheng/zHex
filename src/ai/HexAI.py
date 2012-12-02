import math,random

class HexAI:
        def think(self,board):
                s,g=board.getStack(),board.getGrid()
                top=s.top()
                if top!=None:
                        pos=top.getPos()
                size=len(g)
                if top!=None and g[size-pos[0]-1][size-pos[1]-1].getPlayer()==None:
                        return (size-pos[0]-1,size-pos[1]-1)
                else:
                        while True:
                                rx,ry=int(random.random()*size/2+size/4),int(random.random()*size/2+size/4)
                                if g[rx][ry].getPlayer()==None:
                                        return (rx,ry)




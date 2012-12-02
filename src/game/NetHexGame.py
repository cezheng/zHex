import socket,random
from HexGame import *
recvUnit=8192

class NetHexGame(HexGame):
        def __init__(self,go,*args,**kw):
                super(NetHexGame,self).__init__(go=go,*args,**kw)
                self.player=(go+1)%2
        def play(self,**opt):
                self.curPlayer=0
                self.gameInit()
                print "connection established"
                i=0
                while self.running:
                        self.turnText.setTextColor(self.players[self.curPlayer].getColor())
                        print "round",i
                        i+=1
                        if self.curPlayer==self.player:
                                print "you turn click the mouse"
                                p=self.win.getMouse()
                                co=self.board.locate(p)
                                if co!=():
                                        if self.go(co)==self.curPlayer+1:
                                                return self.curPlayer+1
                        else:
                                print "opo's turn wait for response"
                                if self.confirmGo()==self.curPlayer+1:
                                        return self.curPlayer+1
        def synGo(self,co):
                while True:
                        self.sock.sendto("syn"+' '+str(co[0])+' '+str(co[1]),self.opo)
                        print "sent"+ "syn"+' '+str(co[0])+' '+str(co[1]) + "to" + str(self.opo)
                        buf=self.sock.recv(recvUnit)
                        if buf=="confirm":
                                print "get confirm for sync"
                                return True
                return False
        def go(self,co):
                if self.board.placePiece(co,self.players[self.player]):
                        if self.synGo(co):
                                winner=self.board.winner()
                                if winner==None:
                                        self.switchPlayer()
                                elif winner==self.curPlayer+1:
                                        self.turnText.setText("Player "+str(winner)+" wins.")
                                return winner
                else:
                        return False
                return None
        def confirmGo(self):
                while True:
                        buf=self.sock.recv(recvUnit)
                        buflist=buf.split()
                        if buflist[0]=="syn":
                                print "get "+buf
                                co=[int(i) for i in buflist[1:]]
                                if self.board.placePiece(co,self.players[(self.player+1)%2]):
                                        print "sent confirm for syn"
                                        self.sock.sendto("confirm",self.opo)
                                        winner=self.board.winner()
                                        if winner==None:
                                                self.switchPlayer()
                                        elif winner==self.curPlayer+1:
                                                self.turnText.setText("Player "+str(winner)+" wins.")
                                        return winner
                                else:
                                        return False
                        else:
                                self.sock.sendto("error",self.opo)
                return None


class HostHexGame(NetHexGame):
        def __init__(self,port,*args,**kw):
                super(HostHexGame,self).__init__(*args,**kw)
                self.port=port
                self.sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
                self.sock.bind(('',port))
                self.state="waiting"
        def gameInit(self):
                super(HostHexGame,self).gameInit()
                self.wait()

        def wait(self):
                while self.state=="waiting":
                        try:
                                msg,adrs=self.sock.recvfrom(recvUnit)
                                print "got msg %s from %s:%d" % (msg,adrs[0],adrs[1])
                                if msg=="join":
                                        print "try respond"
                                        self.sock.sendto("confirm",adrs)
                                        print "done respond"
                                        self.opo=adrs
                                        print "prepare for another confirmation"
                                        while self.state=="waiting":
                                                print "waiting for confirmation"
                                                msg2,adrs2=self.sock.recvfrom(recvUnit)
                                                if msg2=="confirm" and adrs2==adrs:
                                                        self.state="confirming"
                                                        self.sock.sendto("confirmed",adrs)
                                                else:
                                                        self.sock.sendto("retry",adrs)
                                else:
                                        self.sock.sendto("retry",adrs)

                        except:
                                traceback.print_exc()
                        #whoGoseFirst()
                return adrs
        def whoGoesFirst(self):
                first=int(random.random()*2)
                if first:
                        msgsend="first"
                        self.player=1
                else:
                        msgsend="second"
                        self.player=2
                msgsend="confirm "+msgsend
                while self.state=="confirming":
                        self.sock.sendto(msgsend,self.joiner)
                        msgrecv,adrs=self.sock.recvfrom(recvUnit)
                        if msgrecv=="confirm" and adrs==self.joiner:
                                self.state="playing"
                return self.player==1
        
                        
class JoinHexGame(NetHexGame):
        def __init__(self,host,port,*args,**kw):
                super(JoinHexGame,self).__init__(*args,**kw)
                self.state="joining"
                self.opo=(host,port)
        def gameInit(self):
                super(JoinHexGame,self).gameInit()
                self.join(self.opo[0],self.opo[1])
        def join(self,host,port):
                self.sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
                self.sock.bind(('',random.randrange(10000,60000)))
                self.sock.connect(self.opo)
                while self.state=="joining":
                        self.sock.sendall("join")
                        buf=self.sock.recv(recvUnit)
                        if buf=="confirm":
                                while self.state=="joining":
                                        self.sock.sendall("confirm")
                                        self.state="confirming"
                return True
        def whoGoesFirst(self):
                while self.state=="confirming":
                        buf=self.sock.recv(recvUnit)
                        buflist=buf.split()
                        if buflist[0]=="confirm":
                                if buflist[1]=="first" or buflist[1]=="second":
                                        self.sock.sendall("confirm")
                                        self.state="playing"
                                        if buflist[1]=="first":
                                                self.player=1
                                        else:
                                                self.player=2
                return self.player==1





                        


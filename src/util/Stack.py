class Stack:
        def __init__(self,size):
                self.size=size
                self.data=[]
                self.itemSum=0
                self.validSum=0
        def push(self,item):
                if self.itemSum>=self.size: return None
                if len(self.data)<self.size and len(self.data)==self.itemSum:
                        self.data.append(item)
                        self.itemSum+=1
                else:
                        self.data[self.itemSum]=item
                        self.itemSum+=1
                self.validSum=self.itemSum
                return self.data[self.itemSum-1]
        def pop(self):
                if self.itemSum==0: return None
                else:
                        self.itemSum-=1
                        return self.data[self.itemSum]
        def redo(self):
                if self.itemSum<self.validSum:
                        self.itemSum+=1
                        return self.data[self.itemSum-1]
                else: return None
        def top(self):
                if self.itemSum>0:
                        return self.data[self.itemSum-1]
                else:
                        return None


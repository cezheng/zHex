class Vector(list):
	def __init__(self,l):
		super(Vector,self).__init__(l)
	def __add__(self,v2):
		return Vector([self[i]+v2[i] for i in range(len(self))])
	def __mul__(self,v2):
		try:
			return sum([self[i]*v2[i] for i in range(len(self))])
		except:
			return [x*v2 for x in self]



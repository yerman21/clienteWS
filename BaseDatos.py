class BaseDatos:
	data = {}

	def __init__(self):
		self.name = "bd"

	def add(self, idd, info):
		info['status'] = True
		self.data[idd] = info
		return self.data[idd]

	def updateStatus(self, idd):
		self.data[idd]['status'] = False
		return self.data[idd]

	def get(self, idd):
		return self.data[idd]

	def showAll(self):
		return self.data
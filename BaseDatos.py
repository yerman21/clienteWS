class BaseDatos:
	collections = {"qrCollec": {}, "user": {}}
	data = collections

	def __init__(self):
		self.name = "bd"

	def add(self, collec, idd, info):
		info['status'] = True
		self.data.get(collec)[idd] = info
		return self.data.get(collec)[idd]

	def updateStatus(self, collec, idd):
		self.data.get(collec)[idd]['status'] = False
		return self.data.get(collec)[idd]

	def get(self, collec, idd):
		return self.data.get(collec).get(idd, None)

	def showAll(self):
		return self.data
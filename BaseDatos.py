class BaseDatos:
	data = {}

	def __init__(self):
		self.name = "bd"

	def add_update(self, id, info):
		self.data[id] = info
		return self.data[id]

	def get(self, id):
		return self.data[id]
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use the application default credentials
cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db_firestore = firestore.client()

class Auth(object):
	def __init__(self, ip, phone):
		self.ip = ip
		self.phone = phone
		self.auth_band = False

	def createSessionToValidate(self, username):
		user_to_auth = Auth(u''+self.ip, u''+self.phone)
		print("insertando createSessionToValidate {}".format(user_to_auth.to_dict()))
		try:
			db_firestore.collection(u'UserSession').document(u''+username).set(user_to_auth.to_dict())
			return True
		except Exception as e:
			print("Error en createSessionToValidate, motivo: {}".format(e))
			return False

	@staticmethod
	def validateTwoFactorAuth(username):
		print("ejecutando validateAuth username="+username)
		try:
			doc = db_firestore.collection(u'UserSession').document(u''+username).get().to_dict()
			print("resueta {}".format(doc))
			return doc.get("auth_band", None)
		except Exception as e:
			print("Error en validateAuth, motivo: {}".format(e))
			return None

	def to_dict(self):
		return {"ip": self.ip, "phone": self.phone, "auth_band": self.auth_band}

#sessionUsuario:{ user_name:{ip: "", phone: "923832", auth_band: None }, user_name2:{ }}
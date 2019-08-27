import firebase_admin
from firebase_admin import firestore
#from flask_restful import Resource, Api

firebase_admin.get_app()
db_firestore = firestore.client()

#class AuthRest(Resource):
#    def get(self, name):
#        return {"Auth":name}
#    def post(self, name):
#        return {"Auth":name}

class Auth(object):
	def __init__(self, ip, phone):
		self.ip = ip
		self.phone = phone
		self.auth_band = False

	def createSessionToValidate(self, username):
		user_to_auth = Auth(u''+self.ip, u''+str(self.phone))
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
#estructura de la db en firebase
#sessionUsuario:{ user_name:{ip: "", phone: "923832", auth_band: None }, user_name2:{ }}
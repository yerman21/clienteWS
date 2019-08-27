import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
#from flask_restful import Resource, Api

class BaseDatosFirebase(object):
    # Use the application default credentials
    cred = credentials.Certificate("./serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
    db_firestore = firestore.client()

    @staticmethod
    def add(collec, idd, info):
        try:
            db_firestore.collection(u''+collec).document(idd).set(info)
            return db_firestore.collection(u''+collec).document(idd).get().to_dic()
        except Exception as e:
            print("Error en BaseDatosFirebase.add, motivo: {}".format(e))
        return None
    
    @staticmethod
    def get(collec, idd):
        try:
            doc = db_firestore.collection(u''+collec).document(u''+idd).get().to_dic()
            print("resueta {}".format(doc))
            return doc
        except Exception as e:
            print("Error en validateAuth, motivo: {}".format(e))
            return None

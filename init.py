#autor:yerry aguirre
from flask import (
	Flask,
	render_template,
	request,
    redirect,
    url_for,
    json
	)
import datetime
import requests
import io
from random import randint
from BaseDatos import BaseDatos
from authentication.auth import Auth
from flask_restful import Resource, Api

#create the application instance
app = Flask(__name__, template_folder="templates")
api = Api(app)

bd = BaseDatos()
bd.add("user", "junin21", {"phone": "935546214", "nombre": "juanito", "pass": "soltero"})
bd.add("user", "chiripa2", {"phone": "948238432", "nombre": "Chiripandulfo", "pass": "casado"})
bd.add("user", "usuarioLuis", {"phone": "920023499", "nombre": "Luis", "pass": "denunciado"})
bd.add("user", "elDeyvis", {"phone": "904838291", "nombre": "Deyvis", "pass": "planificando"})

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    form = request.form
    user_name = form["user_name"]
    passw = form["pass"]
    ip = request.remote_addr

    if not user_name or not passw: #or not mac:
        return msgRequired("UserName, Password"), 204

    user_of_bd = bd.get('user', user_name)
    if not user_of_bd:
        return "el usuario no existe", 204, 

    if user_of_bd["pass"] != passw:
        return "password incorrecto", 204

    if not Auth(ip, user_of_bd.get("phone")).createSessionToValidate(user_name):
        print("no se pudo crear una createSessionToValidate")
        return "No autorizado", 204
    
    return {"user_name": user_name, "status_create_session": True}, 200
    #sessionUsuario:{ user_name:{ip: "", phone: "923832", auth_band: None }, user_name2:{ }}
    #return render_template("home.html", q=form.to_dict(flat=True))

@app.route("/validateAuth", methods=["POST"])
def validateAuth():
    user_name = request.form["user_name"]
    if not Auth.validateTwoFactorAuth(user_name):
        print("no hay permiso validateTwoFactorAuth")
        return render_template("error.html")
    return render_template("home.html", user_name=user_name)

@app.route("/valiarDescuento", methods=["GET"])
def valid():
    return render_template("lecturaTicket.html")

@app.route("/prueba", methods=["GET"])
def home():
    return render_template("home.html", user_name="missael")

@app.route("/convertToQR", methods=["POST"])
def toQR():
    form = request.form.to_dict(flat=True)
    if not form["producto"] or not form["descuento"]:
        return msgRequired("Producto y Descuento"), 204#, {'Content-Type':'application/json'}

    form["idCodigo"] = "CODI"+str(randint(0, 600))
    form["fecha"] = datetime.datetime.now()
    rptWebService = webservice_toQR(json.dumps(form))
    data = {}

    data["msg"] = rptWebService["msg"]
    data["img64"] = rptWebService["data"]    
    bd.add("qrCollec", form["idCodigo"], form)
    return data, 200, {'Content-Type':'application/json'}

@app.route("/decodeQR", methods=["POST"])
def decodeQR():
    fileCodeQR = request.files["fileCode"]
    if not fileCodeQR:
        return msgRequired("FileCode"), 204#, {'Content-Type':'application/json'}
    #enviando imgCodeQR como bytes[]    
    rptWebService = webservice_decodeQR(fileCodeQR.read())

    data = {}
    data["msg"] = rptWebService["msg"]
    data["info"] = json.loads(rptWebService["data"])

    bd.updateStatus("qrCollec", data["info"]["idCodigo"])
    return data, 200, {'Content-Type':'application/json'}

@app.route("/viewData", methods=['GET'])
def showData():
    return bd.showAll(), 200, {'Content-Type': 'application/json'}

def webservice_toQR(text):
    r = requests.get("http://localhost:8084/AppServidora/webserver/v1/toQR", params = {"value":text})
    #r = {'msg': 'mensaje del server', 'data': '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'}
    #return r
    return r.json()

def webservice_decodeQR(imgCodeQR):
    #si hay tiempo probar el atributo en el post files=[('imgBytes',('test.png', imgCodeQR, 'image/png'))], cambiando en el server de java a File como tipo de parametro
    r = requests.post("http://localhost:8084/AppServidora/webserver/v1/decodeQR", data = imgCodeQR) #json.dumps({"imgBytes":imgCodeQR})
    return r.json()

def msgRequired(parametro):
    return "'"+parametro+"' son(es) requerido(s) por el sistema"

# Si estamos ejecutando en modo independiente, ejecute la aplicación
if __name__ == "__main__":
    app.run(debug=True, port=8000)
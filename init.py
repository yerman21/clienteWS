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
from BaseDatosFirebase import BaseDatosFirebase
from authentication.auth import Auth


#create the application instance
app = Flask(__name__, template_folder="templates")
# api = Api(app)

bd = BaseDatos()
#bd.add("user", "junin21", {"phone": "935546214", "nombre": "juanito", "pass": "soltero"})
#bd.add("user", "chiripa2", {"phone": "948238432", "nombre": "Chiripandulfo", "pass": "casado"})
#bd.add("user", "usuarioLuis", {"phone": "920023499", "nombre": "Luis", "pass": "denunciado"})
#bd.add("user", "elDeyvis", {"phone": "904838291", "nombre": "Deyvis", "pass": "planificando"})

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    form = request.form
    user_name = form["user_name"]
    passw = form["pass"]
    ip = request.remote_addr

    if not user_name or not passw:
        return msgRequired("UserName, Password"), 204

    #user_of_bd = bd.get('user', user_name)
    user_of_bd = BaseDatosFirebase.get('user', user_name)
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
    return r.json()

def webservice_decodeQR(imgCodeQR):
    #si hay tiempo probar el atributo en el post files=[('imgBytes',('test.png', imgCodeQR, 'image/png'))], cambiando en el server de java a File como tipo de parametro
    r = requests.post("http://localhost:8084/AppServidora/webserver/v1/decodeQR", data = imgCodeQR) #json.dumps({"imgBytes":imgCodeQR})
    return r.json()

def msgRequired(parametro):
    return "'"+parametro+"' son(es) requerido(s) por el sistema"

# Si estamos ejecutando en modo independiente, ejecute la aplicación
if __name__ == "__main__":
    app.run(host="172.17.8.22",debug=True, port=8000)

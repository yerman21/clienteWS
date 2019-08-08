#autor:yerry aguirre
from flask import (
	Flask,
	render_template,
	request,
    redirect,
    url_for,
    json
	)
import requests
from BaseDatos import BaseDatos

#create the application instance
app = Flask(__name__, template_folder="templates")
bd = BaseDatos()

@app.route("/")
def home():
    """
   This function just responds to the browser ULR
    localhost:5000/

    :return:        the rendered template 'home.html
    """
    return render_template("home.html")

@app.route("/convertToQR", methods=["POST"])
def toQR():
    texto = request.form["texto"]
    data = {}

    if not texto:
        data["msg"] = 'El "texto" es requerido'
        return 'mal muy mal', 204#, {'Content-Type':'application/json'}

    rptWebService = webservice_toQR(texto)
    data["msg"] = rptWebService["msg"]
    data["img64"] = rptWebService["data"]
    #data["url"] = "/perfil"

    #baseDatos["0"] = {img64: vl_img64, cod: "id123"}

    return data, 200, {'Content-Type':'application/json'}
    #return "<img src='data:image/jpg;base64,"+texto+"'>"

@app.route("/perfil", methods=["POST", "GET"])
def showPerfil():
    return render_template("perfil.html", result=request.form.get("result"))

def webservice_toQR(text):
    r = requests.get("http://localhost:8585/AppServidora/webserver/v1/toQR", params = {"value":text})
    return r.json()
    #return "convertido a QR"+text

def msgRequired(parametro):
    return "'"+parametro+"' es requerido por el sistema"

# Si estamos ejecutando en modo independiente, ejecute la aplicación
if __name__ == "__main__":
    app.run(debug=True, port=8000)
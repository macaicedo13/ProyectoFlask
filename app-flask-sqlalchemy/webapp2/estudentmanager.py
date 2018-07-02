import os

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

# enlace a base de datos vía sqlalchemy
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "estudentDB.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

# modelado
class Estudent(db.Model):
    """
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(80), unique=True, nullable=False)
    apellido = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return "<Nombre: {}>".format(self.nombre)

# vistas
# @app.route("/")
@app.route("/", methods=["GET", "POST"])
def home():
    # return "My flask app"
    if request.form:
        print(request.form)
        estudent = Estudent(nombre=request.form.get("nombre"),apellido=request.form.get("apellido"))
        db.session.add(estudent)
        db.session.commit()
        return redirect("/")
        
    estudents = Estudent.query.all()
    return render_template("home.html", estudents = estudents)
    # return render_template("home.html")
    
@app.route("/update", methods=["POST"])
def update():
    newnombre = request.form.get("newnombre")
    newapellido = request.form.get("newapellido")
    idestudent = request.form.get("idestudent")
    estudent = Estudent.query.get(idestudent)
    estudent.nombre = newnombre
    estudent.apellido = newapellido
    db.session.commit()
    return redirect("/")  

@app.route("/delete", methods=["POST"])
def delete():
    idestudent = request.form.get("idestudent")
    estudent = Estudent.query.get(idestudent)
    db.session.delete(estudent)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)




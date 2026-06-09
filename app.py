from datetime import date
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

from database import db, User, Paciente, create_user, get_user_by_username, get_user_by_id

app = Flask(__name__)
app.secret_key = "clinicvet-secret-key-2026"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///citas.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Extensiones
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
migrate = Migrate(app, db)

db.init_app(app)


@app.context_processor
def inject_globals():
    """Variables disponibles en todas las plantillas."""
    return {"today": date.today().isoformat()}


# --------------------------------------------------------------------
# AUTH - Flask-Login
# --------------------------------------------------------------------
@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(int(user_id))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            flash("Usuario y contraseña son obligatorios.", "danger")
            return render_template("register.html", username=username)

        if get_user_by_username(username):
            flash("El nombre de usuario ya existe.", "danger")
            return render_template("register.html", username=username)

        pw_hash = bcrypt.generate_password_hash(password).decode("utf-8")
        create_user(username, pw_hash)
        flash("Registro completado. Ya puedes iniciar sesión.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = get_user_by_username(username)
        if not user or not bcrypt.check_password_hash(user.password_hash, password):
            flash("Usuario o contraseña incorrectos.", "danger")
            return render_template("login.html", username=username)

        login_user(user)
        flash(f"Bienvenido, {user.username}.", "success")
        next_page = request.args.get("next") or url_for("agenda")
        return redirect(next_page)

    return render_template("login.html")


@app.route("/logout")
def logout():
    logout_user()
    flash("Sesión cerrada.", "success")
    return redirect(url_for("agenda"))


# --------------------------------------------------------------------
# AGENDA — listado principal
# --------------------------------------------------------------------
@app.route("/")
def agenda():
    citas = Paciente.query.order_by(Paciente.fecha.asc(), Paciente.id.asc()).all()
    total = len(citas)
    hoy = sum(1 for c in citas if c.fecha == date.today().isoformat())
    especies = len({c.especie for c in citas if c.especie})
    return render_template(
        "agenda.html",
        citas=citas,
        total=total,
        hoy=hoy,
        especies=especies,
    )


# --------------------------------------------------------------------
# AGENDAR — nueva cita
# --------------------------------------------------------------------
@app.route("/agendar", methods=["GET", "POST"])
@login_required
def agendar():
    if request.method == "POST":
        mascota = request.form.get("mascota", "").strip()
        propietario = request.form.get("propietario", "").strip()
        especie = request.form.get("especie", "").strip()
        fecha = request.form.get("fecha", "").strip()

        if not mascota or not propietario or not fecha:
            flash("Los campos Mascota, Propietario y Fecha son obligatorios.", "danger")
            return render_template("agendar.html",
                                   mascota=mascota, propietario=propietario,
                                   especie=especie, fecha=fecha)

        cita = Paciente(mascota=mascota, propietario=propietario, especie=especie, fecha=fecha)
        db.session.add(cita)
        db.session.commit()
        flash(f"Cita de {mascota} agendada con exito.", "success")
        return redirect(url_for("agenda"))

    return render_template("agendar.html")


# --------------------------------------------------------------------
# MODIFICAR — editar cita
# --------------------------------------------------------------------
@app.route("/modificar/<int:id>", methods=["GET", "POST"])
@login_required
def modificar(id):
    cita = Paciente.query.get_or_404(id)

    if request.method == "POST":
        mascota = request.form.get("mascota", "").strip()
        propietario = request.form.get("propietario", "").strip()
        especie = request.form.get("especie", "").strip()
        fecha = request.form.get("fecha", "").strip()

        if not mascota or not propietario or not fecha:
            flash("Los campos Mascota, Propietario y Fecha son obligatorios.", "danger")
            return redirect(url_for("modificar", id=id))

        cita.mascota = mascota
        cita.propietario = propietario
        cita.especie = especie
        cita.fecha = fecha
        db.session.commit()
        flash("Cita modificada correctamente.", "success")
        return redirect(url_for("agenda"))

    return render_template("modificar.html", cita=cita)


# --------------------------------------------------------------------
# CANCELAR — eliminar cita
# --------------------------------------------------------------------
@app.route("/cancelar/<int:id>", methods=["POST"])
@login_required
def cancelar(id):
    cita = Paciente.query.get_or_404(id)
    db.session.delete(cita)
    db.session.commit()
    flash(f"Cita de {cita.mascota} cancelada.", "warning")
    return redirect(url_for("agenda"))


if __name__ == "__main__":
    app.run(debug=True)

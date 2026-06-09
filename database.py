from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)


class Paciente(db.Model):
    __tablename__ = "pacientes"

    id = db.Column(db.Integer, primary_key=True)
    mascota = db.Column(db.String(120), nullable=False)
    propietario = db.Column(db.String(120), nullable=False)
    especie = db.Column(db.String(80), nullable=True)
    fecha = db.Column(db.String(20), nullable=False)


def create_user(username: str, password_hash: str) -> int:
    user = User(username=username, password_hash=password_hash)
    db.session.add(user)
    db.session.commit()
    return user.id


def get_user_by_username(username: str):
    return User.query.filter_by(username=username).first()


def get_user_by_id(user_id: int):
    return User.query.get(user_id)

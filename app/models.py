from flask_login import UserMixin
from .extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


# =========================
# TABLA USUARIO
# =========================
class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), unique=True, nullable=False)

    password = db.Column(db.String(250), nullable=False)

    name = db.Column(db.String(150), nullable=False)  

    role = db.Column(db.String(50), default="user")

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

# =========================
# TABLA CLIENTE
# =========================
class Cliente(db.Model):

    _tablename_ = "cliente"

    id_cliente = db.Column(db.Integer, primary_key=True)

    nombre = db.Column(db.String(100))

    telefono = db.Column(db.String(20))


    def _repr_(self):
        return self.nombre
    
# TABLA VENTA
# =========================
class Venta(db.Model):
    __tablename__ = "venta"

    id_venta = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    id_cliente = db.Column(db.Integer, db.ForeignKey("cliente.id_cliente"))
    id = db.Column(db.Integer, db.ForeignKey("user.id"))  # <-- apunta a User.id
    total = db.Column(db.Numeric(10,2))


    # Relaciones para acceder a nombre directamente
    cliente = db.relationship("Cliente", backref="ventas")
    user = db.relationship("User", backref="ventas")  # <-- relación con User

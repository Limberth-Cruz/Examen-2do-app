from flask_login import current_user
from flask import redirect, url_for, request, flash
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose

from .extensions import admin_panel, db
from .models import User

# =========================
# CRUD protegido para admin
# =========================
class SecurityModelView(ModelView):
    column_exclude_list = ["password","ventas"]


    




    def inaccessible_callback(self, name, **kwargs):
        flash("No tienes permisos para acceder a esta sección", "warning")
        return redirect(url_for("auth.login"))
    


# por defecto rol aqui
class RoleModelView(ModelView):

    allowed_roles = ["admin", "vendedor", "cajero"]  

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role in self.allowed_roles
    








    
# =========================
# Registrar todas las vistas en admin
# =========================
def configuracion_admin():
    # CRUD normales
    # Solo admin ve usuarios
    admin_panel.add_view(SecurityModelView(User, db.session))
    

from flask_login import current_user
from flask import redirect, url_for, request, flash
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose

from .extensions import admin_panel, db
from .models import User,Cliente
from .models import User, Proveedor, Cliente
from .models import User,Proveedor

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
class ClienteAdmin(RoleModelView):


    allowed_roles = ["admin", "vendedor", "cajero"]  

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role in self.allowed_roles
    


class ClienteAdmin(RoleModelView):

    column_exclude_list = ["ventas"]
    form_excluded_columns = ["ventas"]


class VenderView(BaseView):
    @expose('/', methods=['GET', 'POST'])
    def index(self):
        clientes = Cliente.query.all()
        usuarios = User.query.all()  

        if request.method == 'POST':
            # Productos seleccionados
            carrito_ids = request.form.getlist('producto')
            id_cliente = request.form.get('cliente')
            id = request.form.get('user')  

            # Tomar cantidades según los productos seleccionados
            cantidades = []
            for pid in carrito_ids:
                cantidad = int(request.form.get(f'cantidad_{pid}', 0))
                cantidades.append(cantidad)

            # Validar que haya al menos un producto con cantidad > 0
            if not carrito_ids or not any(c > 0 for c in cantidades):
                flash('Seleccione productos y cantidades', 'danger')
                return redirect(url_for('.index'))

            

            db.session.commit()

           

        # GET: mostrar formulario
        return self.render(
            'venta.html',
            clientes=clientes,
            usuarios=usuarios  # <-- pasar usuarios
        )
    
# =========================
# Registrar todas las vistas en admin
# =========================
def configuracion_admin():
    # CRUD normales
    # Solo admin ve usuarios
    admin_panel.add_view(SecurityModelView(User, db.session))
    admin_panel.add_view(SecurityModelView(Proveedor, db.session))

    
    admin_panel.add_view(ClienteAdmin(Cliente, db.session))
    # Vista personalizada de ventas también visible para estos roles
    admin_panel.add_view(VenderView(name='Vender', endpoint='vender'))



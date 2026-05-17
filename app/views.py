import os
from werkzeug.utils import secure_filename
from flask_wtf.file import FileField
from flask import request, current_app, jsonify, redirect, url_for
from markupsafe import Markup

from .extensions import appbuilder, db
from flask_appbuilder import BaseView, ModelView, expose
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.security.decorators import has_access

from .models import Categoria, Producto, Venta, Detalleventa, Cliente


# =====================================================
# CATEGORIA
# =====================================================
class CategoriaModelView(ModelView):
    datamodel = SQLAInterface(Categoria)

    label_columns = {
        "nombre": "Nombre",
        "descripcion": "Descripcion",
        "imagen": "Imagen",
        "estado": "Estado",
        "creado_en": "Creado en",
        "actualizado_en": "Actualizado en"
    }

    list_columns = [
        "nombre",
        "descripcion",
        "imagen",
        "estado",
        "creado_en"
    ]

    add_columns = [
        "nombre",
        "descripcion",
        "imagen",
        "estado"
    ]

    edit_columns = [
        "nombre",
        "descripcion",
        "imagen",
        "estado"
    ]

    add_form_extra_fields = {
        "imagen": FileField("Imagen")
    }

    edit_form_extra_fields = {
        "imagen": FileField("Imagen")
    }

    def guardar_imagen(self, item):

        archivo = request.files.get("imagen")

        if archivo and archivo.filename != "":

            nombre_archivo = secure_filename(archivo.filename)

            carpeta_upload = os.path.join(
                current_app.root_path,
                "static",
                "uploads"
            )

            if not os.path.exists(carpeta_upload):
                os.makedirs(carpeta_upload)

            ruta = os.path.join(
                carpeta_upload,
                nombre_archivo
            )

            archivo.save(ruta)

            item.imagen = f"uploads/{nombre_archivo}"

    def pre_add(self, item):
        self.guardar_imagen(item)

    def pre_update(self, item):
        self.guardar_imagen(item)

    def vista_imagen(self, obj):

        if obj.imagen:
            return Markup(
                f'<img src="/static/{obj.imagen}" width="100">'
            )

        return "Sin imagen"


# =====================================================
# PRODUCTO
# =====================================================
class ProductoModelView(ModelView):
    datamodel = SQLAInterface(Producto)

    label_columns = {
        "nombre": "Nombre",
        "descripcion": "Descripcion",
        "precio": "Precio",
        "categorias": "Categoria",
        "imagen": "Imagen",
        "estado": "Estado",
        "creado_en": "Creado en",
        "actualizado_en": "Actualizado en"
    }

    list_columns = [
        "nombre",
        "descripcion",
        "precio",
        "categorias",
        "imagen",
        "estado"
    ]

    add_columns = [
        "nombre",
        "descripcion",
        "precio",
        "categorias",
        "imagen",
        "estado"
    ]

    edit_columns = [
        "nombre",
        "descripcion",
        "precio",
        "categorias",
        "imagen",
        "estado"
    ]

    add_form_extra_fields = {
        "imagen": FileField("Imagen")
    }

    edit_form_extra_fields = {
        "imagen": FileField("Imagen")
    }

    def guardar_imagen(self, item):

        archivo = request.files.get("imagen")

        if archivo and archivo.filename != "":

            nombre_archivo = secure_filename(
                archivo.filename
            )

            carpeta_upload = os.path.join(
                current_app.root_path,
                "static",
                "uploads"
            )

            if not os.path.exists(carpeta_upload):
                os.makedirs(carpeta_upload)

            ruta = os.path.join(
                carpeta_upload,
                nombre_archivo
            )

            archivo.save(ruta)

            item.imagen = f"uploads/{nombre_archivo}"

    def pre_add(self, item):
        self.guardar_imagen(item)

    def pre_update(self, item):
        self.guardar_imagen(item)

    def vista_imagen(self, obj):

        if obj.imagen:
            return Markup(
                f'<img src="/static/{obj.imagen}" width="100">'
            )

        return "Sin imagen"


# =====================================================
# DETALLE VENTA
# =====================================================
class DetalleventaModelView(ModelView):
    datamodel = SQLAInterface(Detalleventa)

    label_columns = {
        "venta": "Venta",
        "producto": "Producto",
        "cantidad": "Cantidad",
        "precio_unitario": "Precio Unitario",
        "subtotal": "Subtotal"
    }

    list_columns = [
        "venta",
        "producto",
        "cantidad",
        "precio_unitario",
        "subtotal"
    ]

    add_columns = ["venta", "producto", "cantidad"]
    edit_columns = ["venta", "producto", "cantidad"]

    def pre_add(self, item):
        item.precio_unitario = item.producto.precio
        item.subtotal = item.cantidad * item.precio_unitario

    def pre_update(self, item):
        item.precio_unitario = item.producto.precio
        item.subtotal = item.cantidad * item.precio_unitario

    def post_add(self, item):
        self._recalcular_total(item.venta)

    def post_update(self, item):
        self._recalcular_total(item.venta)

    def post_delete(self, item):
        self._recalcular_total(item.venta)

    def _recalcular_total(self, venta):
        venta.total = sum(d.subtotal for d in venta.detalles)
        db.session.commit()


# =====================================================
# VENTA
# =====================================================
class VentaModelView(ModelView):
    datamodel = SQLAInterface(Venta)

    base_permissions = ["can_list", "can_show", "can_edit", "can_delete"]

    label_columns = {
        "cliente": "Cliente",
        "fecha": "Fecha",
        "total": "Total"
    }

    list_columns = ["id", "cliente", "fecha", "total"]
    edit_columns = ["cliente"]
    show_columns = ["id", "cliente", "fecha", "total"]

    related_views = [DetalleventaModelView]
    show_template = "appbuilder/general/model/show_cascade.html"


# =====================================================
# CLIENTE
# =====================================================
class ClienteModelView(ModelView):
    datamodel = SQLAInterface(Cliente)

    label_columns = {
        "nombre": "Nombre",
        "apellido": "Apellido",
        "telefono": "Teléfono"
    }

    list_columns = ["nombre", "apellido", "telefono"]
    add_columns = ["nombre", "apellido", "telefono"]
    edit_columns = ["nombre", "apellido", "telefono"]


# =====================================================
# NUEVA VENTA (Punto de Venta de una sola pantalla)
# =====================================================
class VentaNuevaView(BaseView):

    route_base = "/venta"

    @expose("/nueva/")
    @has_access
    def nueva(self):
        clientes = db.session.query(Cliente).order_by(Cliente.nombre).all()
        productos = (
            db.session.query(Producto)
            .filter(Producto.precio.isnot(None))
            .order_by(Producto.nombre)
            .all()
        )
        return self.render_template(
            "venta_nueva.html",
            clientes=clientes,
            productos=productos
        )

    @expose("/guardar/", methods=["POST"])
    @has_access
    def guardar(self):
        data = request.get_json(silent=True) or {}
        cliente_id = data.get("cliente_id")
        detalles = data.get("detalles", [])

        if not cliente_id or not detalles:
            return jsonify({"error": "Falta cliente o productos"}), 400

        venta = Venta(cliente_id=int(cliente_id), total=0)
        db.session.add(venta)
        db.session.flush()

        total = 0
        for d in detalles:
            producto = db.session.get(Producto, int(d["producto_id"]))
            cantidad = int(d["cantidad"])
            precio = float(producto.precio)
            subtotal = cantidad * precio
            db.session.add(Detalleventa(
                venta_id=venta.id,
                producto_id=producto.id,
                cantidad=cantidad,
                precio_unitario=precio,
                subtotal=subtotal
            ))
            total += subtotal

        venta.total = total
        db.session.commit()

        return jsonify({"ok": True, "venta_id": venta.id})


# =====================================================
# REPORTES
# =====================================================
class ReporteView(BaseView):

    route_base = "/reportes"

    @expose("/")
    def index(self):

        total_ventas = db.session.query(
            Venta
        ).count()

        total_ingresos = db.session.query(
            db.func.sum(Venta.total)
        ).scalar() or 0

        venta_por_producto = db.session.query(
            Producto.nombre,
            db.func.sum(Detalleventa.cantidad)
        ).join(
            Detalleventa.producto
        ).group_by(
            Producto.nombre
        ).all()

        return self.render_template(
            "reportes.html",
            t_ventas=total_ventas,
            t_ingresos=total_ingresos,
            venta_por_producto=venta_por_producto
        )


# =====================================================
# REGISTRO DE VISTAS
# =====================================================

appbuilder.add_view(
    ClienteModelView,
    "Clientes",
    icon="fa-users",
    category="Configuraciones",
    category_icon="fa-cog"
)

appbuilder.add_view(
    CategoriaModelView,
    "Categorias",
    icon="fa-tags",
    category="Configuraciones",
    category_icon="fa-cog"
)

appbuilder.add_view(
    ProductoModelView,
    "Productos",
    icon="fa-cube",
    category="Configuraciones",
    category_icon="fa-cog"
)

appbuilder.add_view_no_menu(VentaNuevaView())

appbuilder.add_link(
    "Nueva Venta",
    href="/venta/nueva/",
    icon="fa-cash-register",
    category="Ventas",
    category_icon="fa-shopping-cart"
)

appbuilder.add_view(
    VentaModelView,
    "Ventas",
    icon="fa-cart-plus",
    category="Ventas",
    category_icon="fa-shopping-cart"
)

appbuilder.add_view_no_menu(DetalleventaModelView)

# =====================================================
# REPORTES
# =====================================================

appbuilder.add_view_no_menu(
    ReporteView()
)

appbuilder.add_link(
    "Reportes",
    href="/reportes/",
    icon="fa-chart-bar",
    category="Reportes",
    category_icon="fa-shopping-cart"
)
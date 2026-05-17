import os
from werkzeug.utils import secure_filename
from flask_wtf.file import FileField
from flask import request, current_app
from markupsafe import Markup

from .extensions import appbuilder, db
from flask_appbuilder import BaseView, ModelView, expose
from flask_appbuilder.models.sqla.interface import SQLAInterface

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
# VENTA
# =====================================================
class VentaModelView(ModelView):
    datamodel = SQLAInterface(Venta)

    label_columns = {
        "cliente": "Cliente",
        "producto": "Producto",
        "cantidad": "Cantidad",
        "precio_unitario": "Precio Unitario",
        "total": "Total",
        "fecha": "Fecha"
    }

    description_columns = {
        "cliente": Markup(
            '¿No encuentras al cliente? '
            '<a href="/clientemodelview/add" target="_blank" '
            'class="btn btn-success btn-sm">'
            '<i class="fa fa-plus"></i> Agregar nuevo cliente</a>'
        )
    }

    list_columns = [
        "cliente",
        "producto",
        "cantidad",
        "precio_unitario",
        "total",
        "fecha"
    ]

    add_columns = [
        "cliente",
        "producto",
        "cantidad",
        "precio_unitario",
        "total"
    ]

    edit_columns = [
        "cliente",
        "producto",
        "cantidad",
        "precio_unitario",
        "total"
    ]


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

    add_columns = [
        "venta",
        "producto",
        "cantidad",
        "precio_unitario",
        "subtotal"
    ]

    edit_columns = [
        "venta",
        "producto",
        "cantidad",
        "precio_unitario",
        "subtotal"
    ]


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
            db.func.sum(Venta.cantidad)
        ).join(
            Venta.producto
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
    CategoriaModelView,
    "Categorias",
    icon="fa-info",
    category="Configuraciones",
    category_icon="fa-info"
)

appbuilder.add_view(
    ProductoModelView,
    "Productos",
    icon="fa-info",
    category="Configuraciones",
    category_icon="fa-info"
)

appbuilder.add_view(
    ClienteModelView,
    "Clientes",
    icon="fa-user",
    category="Configuraciones",
    category_icon="fa-info"
)

appbuilder.add_view(
    VentaModelView,
    "Ventas",
    icon="fa-cart-plus",
    category="Ventas",
    category_icon="fa-shopping-cart"
)

appbuilder.add_view(
    DetalleventaModelView,
    "Detalleventas",
    icon="fa-cart-plus",
    category="Detalleventas",
    category_icon="fa-shopping-cart"
)

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
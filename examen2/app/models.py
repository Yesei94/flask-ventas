import datetime
from flask_appbuilder import Model
from sqlalchemy import Boolean, Column, DateTime, Integer, Numeric, String, ForeignKey, Text
from sqlalchemy.orm import relationship

class Categoria(Model):
    __tablename__="categoria"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    imagen = Column(String(255), nullable=True)
    estado = Column(Boolean, nullable=True)

    # Fecha de creación
    creado_en = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    # Fecha de actualización
    actualizado_en = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False
    )

    productos = relationship(
        "Producto",
        back_populates="categorias"
    )

    def __repr__(self):
        return self.nombre


class Producto(Model):
    __tablename__="producto"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    precio = Column(Numeric(10, 2), nullable=True)

    categoria_id = Column(
        Integer,
        ForeignKey("categoria.id"),
        nullable=False
    )

    imagen = Column(String(255), nullable=True)
    estado = Column(Boolean, nullable=True)

    # Fecha de creación
    creado_en = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    # Fecha de actualización
    actualizado_en = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False
    )

    categorias = relationship(
        "Categoria",
        back_populates="productos"
    )

    # RELACION CON DETALLEVENTA
    detalleventas = relationship(
        "Detalleventa",
        back_populates="producto"
    )

    def __repr__(self):
        return self.nombre


class Cliente(Model):
    __tablename__="cliente"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    telefono = Column(String(20), nullable=True)

    # RELACION CON VENTA
    ventas = relationship(
        "Venta",
        back_populates="cliente"
    )

    def __repr__(self):
        return f"{self.nombre} {self.apellido}"


class Venta(Model):
    __tablename__="venta"

    id = Column(Integer, primary_key=True)

    cliente_id = Column(
        Integer,
        ForeignKey("cliente.id"),
        nullable=False
    )

    fecha = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        nullable=False
    )

    total = Column(
        Numeric(10, 2),
        default=0,
        nullable=False
    )

    # RELACION CON CLIENTE
    cliente = relationship(
        "Cliente",
        back_populates="ventas"
    )

    # RELACION CON DETALLEVENTA
    detalles = relationship(
        "Detalleventa",
        back_populates="venta",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Venta #{self.id}"


class Detalleventa(Model):
    __tablename__="detalleventa"

    id = Column(Integer, primary_key=True)

    venta_id = Column(
        Integer,
        ForeignKey("venta.id"),
        nullable=False
    )

    producto_id = Column(
        Integer,
        ForeignKey("producto.id"),
        nullable=False
    )

    cantidad = Column(Integer, nullable=False)

    precio_unitario = Column(
        Numeric(10, 2),
        nullable=False
    )

    subtotal = Column(
        Numeric(10, 2),
        nullable=False
    )

    # RELACION CON VENTA
    venta = relationship(
        "Venta",
        back_populates="detalles"
    )

    # RELACION CON PRODUCTO
    producto = relationship(
        "Producto",
        back_populates="detalleventas"
    )
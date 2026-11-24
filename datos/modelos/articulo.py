import datetime
from peewee import AutoField, CharField, TextField, DateField, IntegerField, ForeignKeyField, CompositeKey
from datos.modelos.base import BaseModel
from datos.modelos.usuario import Autor


class Categoria(BaseModel):
    id_categoria = AutoField()
    nombre = CharField(max_length=100, unique=True)
    habilitado = IntegerField(default=1)

    class Meta:
        table_name = 'categorias'


class Etiqueta(BaseModel):
    id_etiqueta = AutoField()
    nombre = CharField(max_length=50, unique=True)
    habilitado = IntegerField(default=1)

    class Meta:
        table_name = 'etiquetas'


class EstadoArticulo(BaseModel):
    id_estado = AutoField()
    estado = CharField(max_length=30, unique=True)

    class Meta:
        table_name = 'estados_articulo'


class Articulo(BaseModel):
    id_articulo = AutoField()
    titulo = CharField(max_length=150)
    contenido = TextField()
    fecha_publicacion = DateField(default=datetime.date.today)
    autor = ForeignKeyField(Autor, column_name='id_autor', backref='articulos')
    categoria = ForeignKeyField(Categoria, column_name='id_categoria', backref='articulos')
    estado = ForeignKeyField(EstadoArticulo, column_name='id_estado', backref='articulos')
    habilitado = IntegerField(default=1)

    class Meta:
        table_name = 'articulos'


class ArticuloEtiqueta(BaseModel):
    articulo = ForeignKeyField(Articulo, column_name='id_articulo', backref='articulos_etiquetas')
    etiqueta = ForeignKeyField(Etiqueta, column_name='id_etiqueta', backref='articulos_etiquetas')

    class Meta:
        table_name = 'articulos_etiquetas'
        primary_key = CompositeKey('articulo', 'etiqueta')

import datetime
from peewee import AutoField, CharField, DecimalField, IntegerField, DateField, TextField, ForeignKeyField
from datos.modelos.base import BaseModel
from datos.modelos.usuario import Lector
from datos.modelos.articulo import Articulo

ESTADO_ACTIVA = 'ACTIVA'
ESTADO_VENCIDA = 'VENCIDA'
ESTADO_CANCELADA = 'CANCELADA'


class Plan(BaseModel):
    id_plan = AutoField()
    nombre = CharField(max_length=50)
    precio = DecimalField(max_digits=10, decimal_places=2)
    duracion_dias = IntegerField()
    habilitado = IntegerField(default=1)

    class Meta:
        table_name = 'planes'


class Suscripcion(BaseModel):
    id_suscripcion = AutoField()
    lector = ForeignKeyField(Lector, column_name='id_lector', backref='suscripciones')
    plan = ForeignKeyField(Plan, column_name='id_plan', backref='suscripciones')
    fecha_inicio = DateField(default=datetime.date.today)
    fecha_fin = DateField()
    estado = CharField(max_length=20, default=ESTADO_ACTIVA)

    class Meta:
        table_name = 'suscripciones'


class Comentario(BaseModel):
    id_comentario = AutoField()
    lector = ForeignKeyField(Lector, column_name='id_lector', backref='comentarios')
    articulo = ForeignKeyField(Articulo, column_name='id_articulo', backref='comentarios')
    fecha = DateField(default=datetime.date.today)
    contenido = TextField()
    habilitado = IntegerField(default=1)

    class Meta:
        table_name = 'comentarios'

    def resumen(self):
        texto = self.contenido if len(self.contenido) <= 60 else self.contenido[:57] + '...'
        return f'Comentó: "{texto}"'


class Like(BaseModel):
    id_like = AutoField()
    lector = ForeignKeyField(Lector, column_name='id_lector', backref='likes')
    articulo = ForeignKeyField(Articulo, column_name='id_articulo', backref='likes')
    fecha = DateField(default=datetime.date.today)

    class Meta:
        table_name = 'likes'

    def resumen(self):
        return 'Le dio like al artículo'

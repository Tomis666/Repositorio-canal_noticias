from peewee import AutoField, CharField, TextField, IntegerField, ForeignKeyField
from datos.modelos.base import BaseModel


class Rol(BaseModel):
    id_rol = AutoField()
    nombre = CharField(max_length=50, unique=True)
    permisos = CharField(max_length=255)
    habilitado = IntegerField(default=1)

    class Meta:
        table_name = 'roles'


class Usuario(BaseModel):
    id_usuario = AutoField()
    nombre = CharField(max_length=100)
    correo = CharField(max_length=100, unique=True)
    contrasena = CharField(max_length=255)
    rol = ForeignKeyField(Rol, column_name='id_rol', backref='usuarios')
    habilitado = IntegerField(default=1)

    class Meta:
        table_name = 'usuarios'

    def descripcion(self):
        return f'Usuario {self.nombre} <{self.correo}> ({self.rol.nombre})'


class Autor(BaseModel):
    id_autor = AutoField()
    usuario = ForeignKeyField(Usuario, column_name='id_usuario', unique=True, backref='autor')
    biografia = TextField(null=True)
    habilitado = IntegerField(default=1)

    class Meta:
        table_name = 'autores'

    def descripcion(self):
        return f'Autor {self.usuario.nombre} <{self.usuario.correo}>'


class Lector(BaseModel):
    id_lector = AutoField()
    usuario = ForeignKeyField(Usuario, column_name='id_usuario', unique=True, backref='lector')
    habilitado = IntegerField(default=1)

    class Meta:
        table_name = 'lectores'

    def descripcion(self):
        return f'Lector {self.usuario.nombre} <{self.usuario.correo}>'

from datos.modelos.usuario import Rol, Usuario, Autor, Lector
from datos.modelos.articulo import Articulo
from datos.modelos.suscripcion import Suscripcion, ESTADO_ACTIVA


# --- ROLES ---
def listado_roles():
    return Rol.select().where(Rol.habilitado == 1).order_by(Rol.nombre)


def obtener_rol(id_rol):
    return Rol.get_or_none((Rol.id_rol == id_rol) & (Rol.habilitado == 1))


def obtener_rol_nombre(nombre):
    return Rol.get_or_none(Rol.nombre == nombre)


def guardar_rol(rol: Rol):
    rol.save()
    return rol


def contar_usuarios_rol(id_rol):
    return Usuario.select().where((Usuario.rol == id_rol) & (Usuario.habilitado == 1)).count()


# --- USUARIOS ---
def _consulta_usuario():
    return Usuario.select(Usuario, Rol).join(Rol, on=(Usuario.rol == Rol.id_rol))


def listado_usuarios():
    return _consulta_usuario().where(Usuario.habilitado == 1).order_by(Usuario.nombre)


def obtener_usuario(id_usuario):
    return _consulta_usuario().where((Usuario.id_usuario == id_usuario) & (Usuario.habilitado == 1)).first()


def obtener_usuario_correo(correo):
    return _consulta_usuario().where(Usuario.correo == correo).first()


def guardar_usuario(usuario: Usuario):
    usuario.save()
    return usuario


# --- AUTORES ---
def _consulta_autor():
    return Autor.select(Autor, Usuario).join(Usuario, on=(Autor.usuario == Usuario.id_usuario))


def listado_autores():
    return _consulta_autor().where((Autor.habilitado == 1) & (Usuario.habilitado == 1)).order_by(Usuario.nombre)


def obtener_autor(id_autor):
    return _consulta_autor().where((Autor.id_autor == id_autor) & (Autor.habilitado == 1)).first()


def obtener_autor_de_usuario(id_usuario):
    return _consulta_autor().where(Autor.usuario == id_usuario).first()


def guardar_autor(autor: Autor):
    autor.save()
    return autor


def contar_articulos_autor(id_autor):
    return Articulo.select().where((Articulo.autor == id_autor) & (Articulo.habilitado == 1)).count()


# --- LECTORES ---
def _consulta_lector():
    return Lector.select(Lector, Usuario).join(Usuario, on=(Lector.usuario == Usuario.id_usuario))


def listado_lectores():
    return _consulta_lector().where((Lector.habilitado == 1) & (Usuario.habilitado == 1)).order_by(Usuario.nombre)


def obtener_lector(id_lector):
    return _consulta_lector().where((Lector.id_lector == id_lector) & (Lector.habilitado == 1)).first()


def obtener_lector_de_usuario(id_usuario):
    return _consulta_lector().where(Lector.usuario == id_usuario).first()


def guardar_lector(lector: Lector):
    lector.save()
    return lector


def contar_suscripciones_activas_lector(id_lector):
    return Suscripcion.select().where((Suscripcion.lector == id_lector) & (Suscripcion.estado == ESTADO_ACTIVA)).count()
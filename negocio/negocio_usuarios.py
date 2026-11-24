from datos.modelos.usuario import Rol, Usuario, Autor, Lector
from datos.repositorios.repo_usuario import (
    listado_roles, obtener_rol, obtener_rol_nombre, guardar_rol, contar_usuarios_rol,
    listado_usuarios, obtener_usuario, obtener_usuario_correo, guardar_usuario,
    listado_autores, obtener_autor, obtener_autor_de_usuario, guardar_autor, contar_articulos_autor,
    listado_lectores, obtener_lector, obtener_lector_de_usuario, guardar_lector, contar_suscripciones_activas_lector
)
from auxiliares.validaciones import hashear_contrasena, verificar_contrasena, validar_contrasena


def _exigir_contrasena_segura(contrasena):
    _, errores = validar_contrasena(contrasena)
    if errores:
        raise ValueError('La contraseña no es segura: ' + ' '.join(errores))


def lista_roles():
    return list(listado_roles())


def buscar_rol(id_rol):
    return obtener_rol(id_rol)


def registrar_rol(nombre, permisos):
    nombre, permisos = nombre.strip(), permisos.strip()
    if len(nombre) < 3:
        raise ValueError('El nombre del rol debe tener al menos 3 caracteres.')
    if permisos == '':
        raise ValueError('Debe indicar los permisos del rol.')
    existente = obtener_rol_nombre(nombre)
    if existente is not None:
        if existente.habilitado == 1:
            raise ValueError(f'Ya existe el rol "{nombre}".')
        existente.habilitado = 1
        existente.permisos = permisos
        return guardar_rol(existente)
    rol = Rol(nombre=nombre, permisos=permisos)
    return guardar_rol(rol)


def editar_rol(rol: Rol, nombre, permisos):
    nombre, permisos = nombre.strip(), permisos.strip()
    if len(nombre) < 3:
        raise ValueError('El nombre del rol debe tener al menos 3 caracteres.')
    otro = obtener_rol_nombre(nombre)
    if otro is not None and otro.id_rol != rol.id_rol:
        raise ValueError(f'Ya existe otro rol llamado "{nombre}".')
    rol.nombre = nombre
    rol.permisos = permisos
    return guardar_rol(rol)


def deshabilitar_rol(rol: Rol):
    if contar_usuarios_rol(rol.id_rol) > 0:
        raise ValueError('No se puede eliminar: hay usuarios con este rol.')
    rol.habilitado = 0
    guardar_rol(rol)



def _validar_usuario(nombre, correo, id_rol):
    nombre = nombre.strip()
    correo = correo.strip().lower()
    if len(nombre) < 3:
        raise ValueError('El nombre debe tener al menos 3 caracteres.')
    if '@' not in correo or '.' not in correo.split('@')[-1]:
        raise ValueError('El correo no tiene un formato válido.')
    if obtener_rol(id_rol) is None:
        raise ValueError('El rol indicado no existe.')
    return nombre, correo


def lista_usuarios():
    return list(listado_usuarios())


def buscar_usuario(id_usuario):
    return obtener_usuario(id_usuario)


def registrar_usuario(nombre, correo, contrasena, id_rol):
    nombre, correo = _validar_usuario(nombre, correo, id_rol)
    _exigir_contrasena_segura(contrasena)
    existente = obtener_usuario_correo(correo)
    if existente is not None and existente.habilitado == 1:
        raise ValueError(f'Ya existe un usuario con el correo {correo}.')
    usuario = existente if existente is not None else Usuario()
    usuario.nombre = nombre
    usuario.correo = correo
    usuario.contrasena = hashear_contrasena(contrasena)
    usuario.rol = id_rol
    usuario.habilitado = 1
    return guardar_usuario(usuario)


def editar_usuario(usuario: Usuario, nombre, correo, id_rol, contrasena_nueva=None):
    nombre, correo = _validar_usuario(nombre, correo, id_rol)
    otro = obtener_usuario_correo(correo)
    if otro is not None and otro.id_usuario != usuario.id_usuario:
        raise ValueError(f'El correo {correo} ya está en uso.')
    usuario.nombre = nombre
    usuario.correo = correo
    usuario.rol = id_rol
    if contrasena_nueva:
        _exigir_contrasena_segura(contrasena_nueva)
        usuario.contrasena = hashear_contrasena(contrasena_nueva)
    return guardar_usuario(usuario)


def deshabilitar_usuario(usuario: Usuario):
    autor = obtener_autor_de_usuario(usuario.id_usuario)
    if autor is not None and autor.habilitado == 1:
        raise ValueError('No se puede eliminar: el usuario es Autor activo.')
    lector = obtener_lector_de_usuario(usuario.id_usuario)
    if lector is not None and lector.habilitado == 1:
        raise ValueError('No se puede eliminar: el usuario es Lector activo.')
    usuario.habilitado = 0
    guardar_usuario(usuario)


def iniciar_sesion(correo, contrasena):
    usuario = obtener_usuario_correo(correo.strip().lower())
    if usuario is None or usuario.habilitado != 1 or not verificar_contrasena(contrasena, usuario.contrasena):
        raise ValueError('Correo o contraseña incorrectos.')
    return usuario



def lista_autores():
    return list(listado_autores())


def buscar_autor(id_autor):
    return obtener_autor(id_autor)


def usuarios_sin_perfil_autor():
    disponibles = []
    for usuario in lista_usuarios():
        perfil = obtener_autor_de_usuario(usuario.id_usuario)
        if perfil is None or perfil.habilitado == 0:
            disponibles.append(usuario)
    return disponibles


def registrar_autor(id_usuario, biografia):
    if obtener_usuario(id_usuario) is None:
        raise ValueError('El usuario indicado no existe.')
    existente = obtener_autor_de_usuario(id_usuario)
    if existente is not None and existente.habilitado == 1:
        raise ValueError('Ese usuario ya es autor.')
    autor = existente if existente is not None else Autor()
    autor.usuario = id_usuario
    autor.biografia = biografia.strip()
    autor.habilitado = 1
    return guardar_autor(autor)


def editar_autor(autor: Autor, biografia):
    autor.biografia = biografia.strip()
    return guardar_autor(autor)


def deshabilitar_autor(autor: Autor):
    if contar_articulos_autor(autor.id_autor) > 0:
        raise ValueError('No se puede eliminar: el autor tiene artículos publicados.')
    autor.habilitado = 0
    guardar_autor(autor)



def lista_lectores():
    return list(listado_lectores())


def buscar_lector(id_lector):
    return obtener_lector(id_lector)


def usuarios_sin_perfil_lector():
    disponibles = []
    for usuario in lista_usuarios():
        perfil = obtener_lector_de_usuario(usuario.id_usuario)
        if perfil is None or perfil.habilitado == 0:
            disponibles.append(usuario)
    return disponibles


def registrar_lector(id_usuario):
    if obtener_usuario(id_usuario) is None:
        raise ValueError('El usuario indicado no existe.')
    existente = obtener_lector_de_usuario(id_usuario)
    if existente is not None and existente.habilitado == 1:
        raise ValueError('Ese usuario ya está registrado como lector.')
    lector = existente if existente is not None else Lector()
    lector.usuario = id_usuario
    lector.habilitado = 1
    return guardar_lector(lector)


def deshabilitar_lector(lector: Lector):
    if contar_suscripciones_activas_lector(lector.id_lector) > 0:
        raise ValueError('No se puede eliminar: el lector tiene una suscripción activa.')
    lector.habilitado = 0
    guardar_lector(lector)



def directorio_personas():
    personas = []
    personas.extend(listado_usuarios())
    personas.extend(listado_autores())
    personas.extend(listado_lectores())
    return personas

import datetime
from datos.modelos.suscripcion import Plan, ESTADO_ACTIVA, ESTADO_CANCELADA
from datos.repositorios.repo_suscripcion import (
    listado_planes, obtener_plan, guardar_plan, contar_suscripciones_activas_plan,
    listado_suscripciones, obtener_suscripcion, suscripcion_activa_de, crear_suscripcion,
    guardar_suscripcion, marcar_vencidas,
    comentarios_de_articulo, obtener_comentario, crear_comentario, guardar_comentario,
    likes_de_articulo, obtener_like, crear_like, eliminar_like
)
from datos.repositorios.repo_usuario import obtener_lector
from datos.repositorios.repo_articulo import obtener_articulo



def lista_planes():
    return list(listado_planes())


def buscar_plan(id_plan):
    return obtener_plan(id_plan)


def registrar_plan(nombre, precio, duracion_dias):
    nombre = nombre.strip()
    if len(nombre) < 3:
        raise ValueError('El nombre del plan debe tener al menos 3 caracteres.')
    if precio < 0 or duracion_dias < 1:
        raise ValueError('Precio o duración inválidos.')
    return guardar_plan(Plan(nombre=nombre, precio=precio, duracion_dias=duracion_dias))


def editar_plan(plan: Plan, nombre, precio, duracion_dias):
    nombre = nombre.strip()
    if len(nombre) < 3:
        raise ValueError('El nombre del plan debe tener al menos 3 caracteres.')
    plan.nombre = nombre
    plan.precio = precio
    plan.duracion_dias = duracion_dias
    return guardar_plan(plan)


def deshabilitar_plan(plan: Plan):
    if contar_suscripciones_activas_plan(plan.id_plan) > 0:
        raise ValueError('No se puede eliminar: hay suscripciones activas con este plan.')
    plan.habilitado = 0
    guardar_plan(plan)



def lista_suscripciones():
    marcar_vencidas(datetime.date.today())
    return list(listado_suscripciones())


def suscribir_lector(id_lector, id_plan):
    if obtener_lector(id_lector) is None:
        raise ValueError('El lector indicado no existe.')
    plan = obtener_plan(id_plan)
    if plan is None:
        raise ValueError('El plan indicado no existe.')
    hoy = datetime.date.today()
    marcar_vencidas(hoy)
    if suscripcion_activa_de(id_lector) is not None:
        raise ValueError('El lector ya tiene una suscripción activa.')
    fin = hoy + datetime.timedelta(days=plan.duracion_dias)
    return crear_suscripcion(id_lector, id_plan, hoy, fin)


def suscripciones_activas():
    return [s for s in lista_suscripciones() if s.estado == ESTADO_ACTIVA]


def cancelar_suscripcion(id_suscripcion):
    suscripcion = obtener_suscripcion(id_suscripcion)
    if suscripcion is None:
        raise ValueError('No existe una suscripción con ese id.')
    if suscripcion.estado != ESTADO_ACTIVA:
        raise ValueError(f'Solo se pueden cancelar suscripciones activas (esta está {suscripcion.estado}).')
    suscripcion.estado = ESTADO_CANCELADA
    return guardar_suscripcion(suscripcion)



def comentarios_del_articulo(id_articulo):
    return list(comentarios_de_articulo(id_articulo))


def registrar_comentario(id_lector, id_articulo, contenido):
    contenido = contenido.strip()
    if len(contenido) < 3:
        raise ValueError('El comentario debe tener al menos 3 caracteres.')
    if obtener_lector(id_lector) is None:
        raise ValueError('El lector indicado no existe.')
    if obtener_articulo(id_articulo) is None:
        raise ValueError('El artículo indicado no existe.')
    return crear_comentario(id_lector, id_articulo, contenido)


def deshabilitar_comentario(id_comentario):
    comentario = obtener_comentario(id_comentario)
    if comentario is None:
        raise ValueError('No existe un comentario con ese id.')
    comentario.habilitado = 0
    guardar_comentario(comentario)


def dar_like(id_lector, id_articulo):
    if obtener_lector(id_lector) is None:
        raise ValueError('El lector indicado no existe.')
    if obtener_articulo(id_articulo) is None:
        raise ValueError('El artículo indicado no existe.')
    if obtener_like(id_lector, id_articulo) is not None:
        raise ValueError('Ese lector ya le dio like a este artículo.')
    return crear_like(id_lector, id_articulo)


def quitar_like(id_lector, id_articulo):
    like = obtener_like(id_lector, id_articulo)
    if like is None:
        raise ValueError('Ese lector no le había dado like a este artículo.')
    eliminar_like(like)


def interacciones_de_articulo(id_articulo):
    interacciones = list(comentarios_de_articulo(id_articulo)) + list(likes_de_articulo(id_articulo))
    return sorted(interacciones, key=lambda i: i.fecha)

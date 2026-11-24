from datos.modelos.suscripcion import Plan, Suscripcion, Comentario, Like, ESTADO_ACTIVA, ESTADO_VENCIDA
from datos.modelos.usuario import Lector, Usuario



def listado_planes():
    return Plan.select().where(Plan.habilitado == 1).order_by(Plan.precio)


def obtener_plan(id_plan):
    return Plan.get_or_none((Plan.id_plan == id_plan) & (Plan.habilitado == 1))


def guardar_plan(plan: Plan):
    plan.save()
    return plan


def contar_suscripciones_activas_plan(id_plan):
    return Suscripcion.select().where((Suscripcion.plan == id_plan) & (Suscripcion.estado == ESTADO_ACTIVA)).count()



def listado_suscripciones():
    return (Suscripcion
            .select(Suscripcion, Lector, Usuario, Plan)
            .join(Lector, on=(Suscripcion.lector == Lector.id_lector))
            .join(Usuario, on=(Lector.usuario == Usuario.id_usuario))
            .switch(Suscripcion)
            .join(Plan, on=(Suscripcion.plan == Plan.id_plan))
            .order_by(Suscripcion.fecha_fin.desc()))


def obtener_suscripcion(id_suscripcion):
    return Suscripcion.get_or_none(Suscripcion.id_suscripcion == id_suscripcion)


def suscripcion_activa_de(id_lector):
    return Suscripcion.select().where((Suscripcion.lector == id_lector) & (Suscripcion.estado == ESTADO_ACTIVA)).first()


def crear_suscripcion(id_lector, id_plan, fecha_inicio, fecha_fin):
    return Suscripcion.create(lector=id_lector, plan=id_plan, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, estado=ESTADO_ACTIVA)


def guardar_suscripcion(suscripcion: Suscripcion):
    suscripcion.save()
    return suscripcion


def marcar_vencidas(hoy):
    Suscripcion.update(estado=ESTADO_VENCIDA).where((Suscripcion.estado == ESTADO_ACTIVA) & (Suscripcion.fecha_fin < hoy)).execute()



def comentarios_de_articulo(id_articulo):
    return (Comentario
            .select(Comentario, Lector, Usuario)
            .join(Lector, on=(Comentario.lector == Lector.id_lector))
            .join(Usuario, on=(Lector.usuario == Usuario.id_usuario))
            .where((Comentario.articulo == id_articulo) & (Comentario.habilitado == 1))
            .order_by(Comentario.fecha, Comentario.id_comentario))


def obtener_comentario(id_comentario):
    return Comentario.get_or_none((Comentario.id_comentario == id_comentario) & (Comentario.habilitado == 1))


def crear_comentario(id_lector, id_articulo, contenido):
    return Comentario.create(lector=id_lector, articulo=id_articulo, contenido=contenido)


def guardar_comentario(comentario: Comentario):
    comentario.save()
    return comentario


def contar_comentarios(id_articulo):
    return Comentario.select().where((Comentario.articulo == id_articulo) & (Comentario.habilitado == 1)).count()


def likes_de_articulo(id_articulo):
    return (Like
            .select(Like, Lector, Usuario)
            .join(Lector, on=(Like.lector == Lector.id_lector))
            .join(Usuario, on=(Lector.usuario == Usuario.id_usuario))
            .where(Like.articulo == id_articulo)
            .order_by(Like.fecha, Like.id_like))


def obtener_like(id_lector, id_articulo):
    return Like.select().where((Like.lector == id_lector) & (Like.articulo == id_articulo)).first()


def crear_like(id_lector, id_articulo):
    return Like.create(lector=id_lector, articulo=id_articulo)


def eliminar_like(like: Like):
    like.delete_instance()


def contar_likes(id_articulo):
    return Like.select().where(Like.articulo == id_articulo).count()

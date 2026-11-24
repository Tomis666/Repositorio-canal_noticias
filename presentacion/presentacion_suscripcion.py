from auxiliares.validaciones import pedir_texto, pedir_entero, pedir_decimal, elegir_registro, confirmar, manejar_errores, mostrar_tabla
from negocio.negocio_suscripciones import (
    lista_planes, buscar_plan, registrar_plan, editar_plan, deshabilitar_plan,
    lista_suscripciones, suscripciones_activas, suscribir_lector, cancelar_suscripcion,
    comentarios_del_articulo, registrar_comentario, deshabilitar_comentario,
    dar_like, quitar_like, interacciones_de_articulo
)
from negocio.negocio_usuarios import lista_lectores
from negocio.negocio_articulos import lista_articulos



@manejar_errores
def mostrar_planes():
    filas = [[p.id_plan, p.nombre, f'${p.precio:,.0f}', p.duracion_dias] for p in lista_planes()]
    mostrar_tabla('PLANES', ['Id', 'Nombre', 'Precio', 'Duración (días)'], filas, izquierda=['Nombre'])


@manejar_errores
def agregar_plan():
    nombre = pedir_texto('Ingrese el nombre del plan: ', minimo=3)
    precio = pedir_decimal('Ingrese el precio: ')
    duracion = pedir_entero('Ingrese la duración en días: ', minimo=1)
    plan = registrar_plan(nombre, precio, duracion)
    print(f'Plan guardado con éxito. Id: {plan.id_plan}\n')


@manejar_errores
def modificar_plan():
    mostrar_planes()
    plan = buscar_plan(pedir_entero('Ingrese el id del plan: ', minimo=1))
    if plan is None:
        raise ValueError('No existe un plan con ese id.')
    nombre = pedir_texto(f'Nombre [{plan.nombre}] (ENTER para conservar): ', minimo=3, conservar=plan.nombre)
    precio = pedir_decimal(f'Precio [{plan.precio}] (ENTER para conservar): ', conservar=plan.precio)
    duracion = pedir_entero(f'Duración [{plan.duracion_dias}] (ENTER para conservar): ', minimo=1, conservar=plan.duracion_dias)
    editar_plan(plan, nombre, precio, duracion)
    print('Plan actualizado con éxito.\n')


@manejar_errores
def eliminar_plan():
    mostrar_planes()
    plan = buscar_plan(pedir_entero('Ingrese el id del plan: ', minimo=1))
    if plan is None:
        raise ValueError('No existe un plan con ese id.')
    if confirmar(f'¿Eliminar el plan "{plan.nombre}"?'):
        deshabilitar_plan(plan)
        print('Plan eliminado con éxito.\n')



@manejar_errores
def mostrar_suscripciones():
    filas = [[s.id_suscripcion, s.lector.usuario.nombre, s.plan.nombre, s.fecha_inicio, s.fecha_fin, s.estado]
             for s in lista_suscripciones()]
    mostrar_tabla('SUSCRIPCIONES', ['Id', 'Lector', 'Plan', 'Inicio', 'Fin', 'Estado'], filas, izquierda=['Lector', 'Plan'])


@manejar_errores
def agregar_suscripcion():
    id_lector = elegir_registro('Lectores', lista_lectores(), lambda l: f'{l.usuario.nombre} <{l.usuario.correo}>',
                                mensaje='Id del lector: ', campo_id='id_lector')
    id_plan = elegir_registro('Planes', lista_planes(), lambda p: f'{p.nombre} - ${p.precio:,.0f} por {p.duracion_dias} días',
                              mensaje='Id del plan: ', campo_id='id_plan')
    susc = suscribir_lector(id_lector, id_plan)
    print(f'Suscripción creada con éxito. Id: {susc.id_suscripcion} (vence el {susc.fecha_fin})\n')


@manejar_errores
def anular_suscripcion():
    id_susc = elegir_registro('Suscripciones activas', suscripciones_activas(),
                              lambda s: f'{s.lector.usuario.nombre} - {s.plan.nombre} (vence {s.fecha_fin})',
                              mensaje='Id de la suscripción: ', campo_id='id_suscripcion')
    if confirmar('¿Cancelar esta suscripción?'):
        cancelar_suscripcion(id_susc)
        print('Suscripción cancelada con éxito.\n')



@manejar_errores
def mostrar_interacciones():
    id_art = elegir_registro('Artículos', lista_articulos(), lambda a: a.titulo, mensaje='Id del artículo: ', campo_id='id_articulo')
    interacciones = interacciones_de_articulo(id_art)
    print(f'\n=== INTERACCIONES DEL ARTÍCULO {id_art} ===')
    if not interacciones:
        print('(sin comentarios ni likes)\n')
        return
    for i in interacciones:
        print(f'{i.fecha} | {i.lector.usuario.nombre}: {i.resumen()}')
    print()


@manejar_errores
def agregar_comentario():
    id_art = elegir_registro('Artículos', lista_articulos(), lambda a: a.titulo, mensaje='Id del artículo: ', campo_id='id_articulo')
    id_lec = elegir_registro('Lectores', lista_lectores(), lambda l: f'{l.usuario.nombre} <{l.usuario.correo}>',
                             mensaje='Id del lector: ', campo_id='id_lector')
    com = registrar_comentario(id_lec, id_art, pedir_texto('Escriba el comentario: ', minimo=3))
    print(f'Comentario guardado con éxito. Id: {com.id_comentario}\n')


@manejar_errores
def eliminar_comentario():
    id_art = elegir_registro('Artículos', lista_articulos(), lambda a: a.titulo, mensaje='Id del artículo: ', campo_id='id_articulo')
    id_com = elegir_registro('Comentarios', comentarios_del_articulo(id_art),
                             lambda c: f'{c.lector.usuario.nombre}: {c.resumen()}',
                             mensaje='Id del comentario: ', campo_id='id_comentario')
    deshabilitar_comentario(id_com)
    print('Comentario eliminado con éxito.\n')


@manejar_errores
def agregar_like():
    id_art = elegir_registro('Artículos', lista_articulos(), lambda a: a.titulo, mensaje='Id del artículo: ', campo_id='id_articulo')
    id_lec = elegir_registro('Lectores', lista_lectores(), lambda l: f'{l.usuario.nombre} <{l.usuario.correo}>',
                             mensaje='Id del lector: ', campo_id='id_lector')
    dar_like(id_lec, id_art)
    print('Like registrado con éxito.\n')


@manejar_errores
def eliminar_like():
    id_art = elegir_registro('Artículos', lista_articulos(), lambda a: a.titulo, mensaje='Id del artículo: ', campo_id='id_articulo')
    id_lec = elegir_registro('Lectores', lista_lectores(), lambda l: f'{l.usuario.nombre} <{l.usuario.correo}>',
                             mensaje='Id del lector: ', campo_id='id_lector')
    quitar_like(id_lec, id_art)
    print('Like eliminado con éxito.\n')

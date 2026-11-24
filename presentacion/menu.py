from collections.abc import Callable
from auxiliares.info_app import nombre_app, version_app, opcion_invalida, opcion_volver
from auxiliares.opciones_menu import (
    menu_superior, menu_articulos, menu_autores, menu_usuarios, menu_roles, menu_lectores,
    menu_planes, menu_suscripciones, menu_categorias, menu_etiquetas, menu_interacciones
)
from presentacion.presentacion_articulo import (
    mostrar_articulos, ver_articulo, buscar_articulos, agregar_articulo, modificar_articulo, eliminar_articulo,
    mostrar_categorias, agregar_categoria, modificar_categoria, eliminar_categoria,
    mostrar_etiquetas, agregar_etiqueta, modificar_etiqueta, eliminar_etiqueta
)
from presentacion.presentacion_usuario import (
    mostrar_usuarios, agregar_usuario, modificar_usuario, eliminar_usuario,
    mostrar_roles, agregar_rol, modificar_rol, eliminar_rol,
    mostrar_autores, agregar_autor, modificar_autor, eliminar_autor,
    mostrar_lectores, agregar_lector, eliminar_lector, mostrar_directorio
)
from presentacion.presentacion_suscripcion import (
    mostrar_planes, agregar_plan, modificar_plan, eliminar_plan,
    mostrar_suscripciones, agregar_suscripcion, anular_suscripcion,
    mostrar_interacciones, agregar_comentario, eliminar_comentario, agregar_like, eliminar_like
)
from auxiliares.opciones_menu import (
    menu_superior, menu_articulos, menu_autores, menu_usuarios, menu_roles, menu_lectores,
    menu_planes, menu_suscripciones, menu_categorias, menu_etiquetas, menu_interacciones,
    menu_grupo_contenido, menu_grupo_personas, menu_grupo_suscripciones
)

def _ejecutar_menu(opciones: dict[str, str], acciones: dict[str, Callable[[], None]], mensaje_salida: str = opcion_volver) -> None:
    while True:
        for clave, valor in opciones.items():
            print(f'[{clave}] - {valor}')
        opcion = input('Ingrese su opción: ').strip()
        if opcion not in opciones:
            print(opcion_invalida)
        elif opcion == '0':
            print(mensaje_salida)
            return
        elif opcion in acciones:
            acciones[opcion]()
        else:
            print('Esta opción aún no está implementada.\n')


def _submenu(opciones, acciones):
    def abrir():
        _ejecutar_menu(opciones, acciones)
    return abrir


def menu_principal(usuario) -> None:
    print(f'\n{nombre_app} v{version_app}')
    print('=' * (len(nombre_app) + len(version_app) + 2))
    print(f'Sesión iniciada: {usuario.nombre} <{usuario.correo}> (rol: {usuario.rol.nombre})\n')

    _ejecutar_menu
    articulos = _submenu(menu_articulos, {
        '1': mostrar_articulos, '2': ver_articulo, '3': buscar_articulos,
        '4': agregar_articulo, '5': modificar_articulo, '6': eliminar_articulo})
    categorias = _submenu(menu_categorias, {
        '1': mostrar_categorias, '2': agregar_categoria, '3': modificar_categoria, '4': eliminar_categoria})
    etiquetas = _submenu(menu_etiquetas, {
        '1': mostrar_etiquetas, '2': agregar_etiqueta, '3': modificar_etiqueta, '4': eliminar_etiqueta})
    usuarios = _submenu(menu_usuarios, {
        '1': mostrar_usuarios, '2': agregar_usuario, '3': modificar_usuario, '4': eliminar_usuario})
    roles = _submenu(menu_roles, {
        '1': mostrar_roles, '2': agregar_rol, '3': modificar_rol, '4': eliminar_rol})
    autores = _submenu(menu_autores, {
        '1': mostrar_autores, '2': agregar_autor, '3': modificar_autor, '4': eliminar_autor})
    lectores = _submenu(menu_lectores, {
        '1': mostrar_lectores, '2': agregar_lector, '3': eliminar_lector})
    planes = _submenu(menu_planes, {
        '1': mostrar_planes, '2': agregar_plan, '3': modificar_plan, '4': eliminar_plan})
    suscripciones = _submenu(menu_suscripciones, {
        '1': mostrar_suscripciones, '2': agregar_suscripcion, '3': anular_suscripcion})
    interacciones = _submenu(menu_interacciones, {
        '1': mostrar_interacciones, '2': agregar_comentario, '3': eliminar_comentario,
        '4': agregar_like, '5': eliminar_like})
    
    contenido = _submenu(menu_grupo_contenido, {'1': articulos, '2': categorias, '3': etiquetas})
    personas = _submenu(menu_grupo_personas, {
        '1': usuarios, '2': roles, '3': autores, '4': lectores, '5': mostrar_directorio})
    suscripciones_y_planes = _submenu(menu_grupo_suscripciones, {'1': planes, '2': suscripciones})


    _ejecutar_menu(
        menu_superior,
        {'1': contenido, '2': personas, '3': suscripciones_y_planes, '4': interacciones},
        'Saliendo...\n',
    )
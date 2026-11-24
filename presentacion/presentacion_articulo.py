import datetime
from auxiliares.validaciones import (
    pedir_texto, pedir_entero, pedir_fecha, elegir_registro, elegir_varios, confirmar, manejar_errores, mostrar_tabla
)
from negocio.negocio_articulos import (
    lista_articulos, buscar_por_titulo, buscar_articulo, detalle_articulo, lista_estados,
    etiquetas_del_articulo, registrar_articulo, editar_articulo, deshabilitar_articulo,
    lista_categorias, buscar_categoria, registrar_categoria, editar_categoria, deshabilitar_categoria,
    lista_etiquetas, buscar_etiqueta, registrar_etiqueta, editar_etiqueta, deshabilitar_etiqueta
)
from negocio.negocio_usuarios import lista_autores

_COLUMNAS = ['Id', 'Titular', 'Categoría', 'Autor', 'Estado', 'Fecha']


def _filas(articulos):
    return [[a.id_articulo, a.titulo, a.categoria.nombre, a.autor.usuario.nombre, a.estado.estado, a.fecha_publicacion]
            for a in articulos]


#articulos
@manejar_errores
def mostrar_articulos():
    mostrar_tabla('ARTÍCULOS', _COLUMNAS, _filas(lista_articulos()), izquierda=['Titular'])


@manejar_errores
def ver_articulo():
    detalle = detalle_articulo(pedir_entero('Ingrese el id del artículo: ', minimo=1))
    articulo = detalle['articulo']
    etiquetas = ', '.join(e.nombre for e in detalle['etiquetas']) or '(sin etiquetas)'
    print(f'\n{articulo.titulo}\n' + '-' * len(articulo.titulo))
    print(f'Autor: {articulo.autor.usuario.nombre} | Categoría: {articulo.categoria.nombre} | Estado: {articulo.estado.estado} | Fecha: {articulo.fecha_publicacion}')
    print(f'Etiquetas: {etiquetas} | Likes: {detalle["likes"]} | Comentarios: {detalle["comentarios"]}\n{articulo.contenido}\n')


@manejar_errores
def buscar_articulos():
    texto = pedir_texto('Ingrese parte del título a buscar: ')
    mostrar_tabla(f'RESULTADOS PARA "{texto}"', _COLUMNAS, _filas(buscar_por_titulo(texto)), izquierda=['Titular'])


@manejar_errores
def agregar_articulo():
    titulo = pedir_texto('Ingrese el titular (mínimo 5 caracteres): ', minimo=5)
    contenido = pedir_texto('Ingrese el contenido: ')
    id_autor = elegir_registro('Autores', lista_autores(), lambda a: a.usuario.nombre, mensaje='Id del autor: ', campo_id='id_autor')
    id_categoria = elegir_registro('Categorías', lista_categorias(), lambda c: c.nombre, mensaje='Id de la categoría: ', campo_id='id_categoria')
    id_estado = elegir_registro('Estados', lista_estados(), lambda e: e.estado, mensaje='Id del estado: ', campo_id='id_estado')
    ids_etiquetas = elegir_varios('Etiquetas', lista_etiquetas(), lambda e: e.nombre, campo_id='id_etiqueta')
    fecha = pedir_fecha('Fecha de publicación [dd/mm/aaaa] (ENTER = hoy): ', conservar=datetime.date.today())
    articulo = registrar_articulo(titulo, contenido, id_autor, id_categoria, id_estado, ids_etiquetas, fecha)
    print(f'Artículo guardado con éxito. Id: {articulo.id_articulo}\n')


@manejar_errores
def modificar_articulo():
    mostrar_articulos()
    articulo = buscar_articulo(pedir_entero('Ingrese el id del artículo: ', minimo=1))
    if articulo is None:
        raise ValueError('No existe un artículo con ese id.')
    titulo = pedir_texto(f'Titular [{articulo.titulo}] (ENTER para conservar): ', minimo=5, conservar=articulo.titulo)
    contenido = pedir_texto('Contenido (ENTER para conservar): ', conservar=articulo.contenido)
    id_categoria = elegir_registro('Categorías', lista_categorias(), lambda c: c.nombre, conservar=articulo.categoria_id,
                                   mensaje=f'Id de la categoría [{articulo.categoria.nombre}]: ', campo_id='id_categoria')
    id_estado = elegir_registro('Estados', lista_estados(), lambda e: e.estado, conservar=articulo.estado_id,
                                mensaje=f'Id del estado [{articulo.estado.estado}]: ', campo_id='id_estado')
    actuales = [e.id_etiqueta for e in etiquetas_del_articulo(articulo.id_articulo)]
    ids_etiquetas = elegir_varios('Etiquetas', lista_etiquetas(), lambda e: e.nombre, conservar=actuales, campo_id='id_etiqueta')
    fecha = pedir_fecha(f'Fecha de publicación [{articulo.fecha_publicacion:%d/%m/%Y}] (ENTER para conservar): ',
                        conservar=articulo.fecha_publicacion)
    editar_articulo(articulo, titulo, contenido, id_categoria, id_estado, ids_etiquetas, fecha)
    print('Artículo actualizado con éxito.\n')


@manejar_errores
def eliminar_articulo():
    mostrar_articulos()
    articulo = buscar_articulo(pedir_entero('Ingrese el id del artículo: ', minimo=1))
    if articulo is None:
        raise ValueError('No existe un artículo con ese id.')
    if confirmar(f'¿Eliminar el artículo "{articulo.titulo}"?'):
        deshabilitar_articulo(articulo)
        print('Artículo eliminado con éxito.\n')


# Categorias
@manejar_errores
def mostrar_categorias():
    mostrar_tabla('CATEGORÍAS', ['Id', 'Nombre'], [[c.id_categoria, c.nombre] for c in lista_categorias()])


@manejar_errores
def agregar_categoria():
    cat = registrar_categoria(pedir_texto('Ingrese el nombre de la categoría: ', minimo=3))
    print(f'Categoría guardada con éxito. Id: {cat.id_categoria}\n')


@manejar_errores
def modificar_categoria():
    mostrar_categorias()
    cat = buscar_categoria(pedir_entero('Ingrese el id de la categoría: ', minimo=1))
    if cat is None:
        raise ValueError('No existe una categoría con ese id.')
    editar_categoria(cat, pedir_texto(f'Nombre [{cat.nombre}] (ENTER para conservar): ', minimo=3, conservar=cat.nombre))
    print('Categoría actualizada con éxito.\n')


@manejar_errores
def eliminar_categoria():
    mostrar_categorias()
    cat = buscar_categoria(pedir_entero('Ingrese el id de la categoría: ', minimo=1))
    if cat is None:
        raise ValueError('No existe una categoría con ese id.')
    if confirmar(f'¿Eliminar la categoría "{cat.nombre}"?'):
        deshabilitar_categoria(cat)
        print('Categoría eliminada con éxito.\n')


@manejar_errores
def mostrar_etiquetas():
    mostrar_tabla('ETIQUETAS', ['Id', 'Nombre'], [[e.id_etiqueta, e.nombre] for e in lista_etiquetas()])


@manejar_errores
def agregar_etiqueta():
    eti = registrar_etiqueta(pedir_texto('Ingrese el nombre de la etiqueta: ', minimo=2))
    print(f'Etiqueta guardada con éxito. Id: {eti.id_etiqueta}\n')


@manejar_errores
def modificar_etiqueta():
    mostrar_etiquetas()
    eti = buscar_etiqueta(pedir_entero('Ingrese el id de la etiqueta: ', minimo=1))
    if eti is None:
        raise ValueError('No existe una etiqueta con ese id.')
    editar_etiqueta(eti, pedir_texto(f'Nombre [{eti.nombre}] (ENTER para conservar): ', minimo=2, conservar=eti.nombre))
    print('Etiqueta actualizada con éxito.\n')


@manejar_errores
def eliminar_etiqueta():
    mostrar_etiquetas()
    eti = buscar_etiqueta(pedir_entero('Ingrese el id de la etiqueta: ', minimo=1))
    if eti is None:
        raise ValueError('No existe una etiqueta con ese id.')
    if confirmar(f'¿Eliminar la etiqueta "{eti.nombre}"?'):
        deshabilitar_etiqueta(eti)
        print('Etiqueta eliminada con éxito.\n')

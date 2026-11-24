from datos.modelos.articulo import Categoria, Etiqueta, Articulo
from datos.repositorios.repo_articulo import (
    listado_categorias, obtener_categoria, obtener_categoria_nombre, guardar_categoria, contar_articulos_categoria,
    listado_etiquetas, obtener_etiqueta, obtener_etiqueta_nombre, guardar_etiqueta, contar_articulos_etiqueta,
    listado_articulos, buscar_articulos, obtener_articulo, listado_estados, obtener_estado,
    etiquetas_de_articulo, crear_articulo, guardar_articulo
)
from datos.repositorios.repo_usuario import obtener_autor
from datos.repositorios.repo_suscripcion import contar_comentarios, contar_likes



def lista_categorias():
    return list(listado_categorias())


def buscar_categoria(id_categoria):
    return obtener_categoria(id_categoria)


def registrar_categoria(nombre):
    nombre = nombre.strip()
    if len(nombre) < 3:
        raise ValueError('El nombre de la categoría debe tener al menos 3 caracteres.')
    existente = obtener_categoria_nombre(nombre)
    if existente is not None:
        if existente.habilitado == 1:
            raise ValueError(f'Ya existe la categoría "{nombre}".')
        existente.habilitado = 1
        return guardar_categoria(existente)
    return guardar_categoria(Categoria(nombre=nombre))


def editar_categoria(categoria: Categoria, nombre):
    nombre = nombre.strip()
    if len(nombre) < 3:
        raise ValueError('El nombre de la categoría debe tener al menos 3 caracteres.')
    otra = obtener_categoria_nombre(nombre)
    if otra is not None and otra.id_categoria != categoria.id_categoria:
        raise ValueError(f'Ya existe otra categoría llamada "{nombre}".')
    categoria.nombre = nombre
    return guardar_categoria(categoria)


def deshabilitar_categoria(categoria: Categoria):
    if contar_articulos_categoria(categoria.id_categoria) > 0:
        raise ValueError('No se puede eliminar: la categoría tiene artículos asociados.')
    categoria.habilitado = 0
    guardar_categoria(categoria)



def lista_etiquetas():
    return list(listado_etiquetas())


def buscar_etiqueta(id_etiqueta):
    return obtener_etiqueta(id_etiqueta)


def registrar_etiqueta(nombre):
    nombre = nombre.strip()
    if len(nombre) < 2:
        raise ValueError('El nombre de la etiqueta debe tener al menos 2 caracteres.')
    existente = obtener_etiqueta_nombre(nombre)
    if existente is not None:
        if existente.habilitado == 1:
            raise ValueError(f'Ya existe la etiqueta "{nombre}".')
        existente.habilitado = 1
        return guardar_etiqueta(existente)
    return guardar_etiqueta(Etiqueta(nombre=nombre))


def editar_etiqueta(etiqueta: Etiqueta, nombre):
    nombre = nombre.strip()
    if len(nombre) < 2:
        raise ValueError('El nombre de la etiqueta debe tener al menos 2 caracteres.')
    otra = obtener_etiqueta_nombre(nombre)
    if otra is not None and otra.id_etiqueta != etiqueta.id_etiqueta:
        raise ValueError(f'Ya existe otra etiqueta llamada "{nombre}".')
    etiqueta.nombre = nombre
    return guardar_etiqueta(etiqueta)


def deshabilitar_etiqueta(etiqueta: Etiqueta):
    if contar_articulos_etiqueta(etiqueta.id_etiqueta) > 0:
        raise ValueError('No se puede eliminar: la etiqueta está usada en artículos.')
    etiqueta.habilitado = 0
    guardar_etiqueta(etiqueta)



def lista_articulos():
    return list(listado_articulos())


def buscar_por_titulo(texto):
    texto = texto.strip()
    if texto == '':
        raise ValueError('Debe ingresar un texto para buscar.')
    return list(buscar_articulos(texto))


def buscar_articulo(id_articulo):
    return obtener_articulo(id_articulo)


def lista_estados():
    return list(listado_estados())


def etiquetas_del_articulo(id_articulo):
    return list(etiquetas_de_articulo(id_articulo))


def detalle_articulo(id_articulo):
    articulo = obtener_articulo(id_articulo)
    if articulo is None:
        raise ValueError('No existe un artículo con ese id.')
    return {
        'articulo': articulo,
        'etiquetas': etiquetas_del_articulo(articulo.id_articulo),
        'likes': contar_likes(articulo.id_articulo),
        'comentarios': contar_comentarios(articulo.id_articulo),
    }


def _validar_articulo(titulo, contenido, id_categoria, id_estado, ids_etiquetas):
    titulo, contenido = titulo.strip(), contenido.strip()
    if len(titulo) < 5:
        raise ValueError('El titular debe tener al menos 5 caracteres.')
    if contenido == '':
        raise ValueError('El cuerpo de la noticia no puede estar vacío.')
    if obtener_categoria(id_categoria) is None:
        raise ValueError('La categoría indicada no existe.')
    if obtener_estado(id_estado) is None:
        raise ValueError('El estado indicado no existe.')
    for id_etiqueta in ids_etiquetas:
        if obtener_etiqueta(id_etiqueta) is None:
            raise ValueError(f'La etiqueta con id {id_etiqueta} no existe.')
    return titulo, contenido


def registrar_articulo(titulo, contenido, id_autor, id_categoria, id_estado, ids_etiquetas, fecha_publicacion=None):
    titulo, contenido = _validar_articulo(titulo, contenido, id_categoria, id_estado, ids_etiquetas)
    if obtener_autor(id_autor) is None:
        raise ValueError('El autor indicado no existe.')
    return crear_articulo(titulo, contenido, id_autor, id_categoria, id_estado, ids_etiquetas, fecha_publicacion)


def editar_articulo(articulo: Articulo, titulo, contenido, id_categoria, id_estado, ids_etiquetas, fecha_publicacion=None):
    titulo, contenido = _validar_articulo(titulo, contenido, id_categoria, id_estado, ids_etiquetas)
    if fecha_publicacion is not None:
        articulo.fecha_publicacion = fecha_publicacion
    articulo.titulo = titulo
    articulo.contenido = contenido
    articulo.categoria = id_categoria
    articulo.estado = id_estado
    return guardar_articulo(articulo, ids_etiquetas)


def deshabilitar_articulo(articulo: Articulo):
    articulo.habilitado = 0
    guardar_articulo(articulo)

from datos.modelos.base import database
from datos.modelos.articulo import Categoria, Etiqueta, EstadoArticulo, Articulo, ArticuloEtiqueta
from datos.modelos.usuario import Autor, Usuario

def listado_categorias():
    return Categoria.select().where(Categoria.habilitado == 1).order_by(Categoria.nombre)


def obtener_categoria(id_categoria):
    return Categoria.get_or_none((Categoria.id_categoria == id_categoria) & (Categoria.habilitado == 1))


def obtener_categoria_nombre(nombre):
    return Categoria.get_or_none(Categoria.nombre == nombre)


def guardar_categoria(categoria: Categoria):
    categoria.save()
    return categoria


def contar_articulos_categoria(id_categoria):
    return Articulo.select().where((Articulo.categoria == id_categoria) & (Articulo.habilitado == 1)).count()

#etiquetas
def listado_etiquetas():
    return Etiqueta.select().where(Etiqueta.habilitado == 1).order_by(Etiqueta.nombre)


def obtener_etiqueta(id_etiqueta):
    return Etiqueta.get_or_none((Etiqueta.id_etiqueta == id_etiqueta) & (Etiqueta.habilitado == 1))


def obtener_etiqueta_nombre(nombre):
    return Etiqueta.get_or_none(Etiqueta.nombre == nombre)


def guardar_etiqueta(etiqueta: Etiqueta):
    etiqueta.save()
    return etiqueta


def contar_articulos_etiqueta(id_etiqueta):
    return (ArticuloEtiqueta.select()
            .join(Articulo, on=(ArticuloEtiqueta.articulo == Articulo.id_articulo))
            .where((ArticuloEtiqueta.etiqueta == id_etiqueta) & (Articulo.habilitado == 1))
            .count())


# Articulos y estados
def _consulta_articulo():
    return (Articulo
            .select(Articulo, Autor, Usuario, Categoria, EstadoArticulo)
            .join(Categoria, on=(Articulo.categoria == Categoria.id_categoria))
            .switch(Articulo)
            .join(EstadoArticulo, on=(Articulo.estado == EstadoArticulo.id_estado))
            .switch(Articulo)
            .join(Autor, on=(Articulo.autor == Autor.id_autor))
            .join(Usuario, on=(Autor.usuario == Usuario.id_usuario)))


def listado_articulos():
    return _consulta_articulo().where(Articulo.habilitado == 1).order_by(Articulo.fecha_publicacion.desc(), Articulo.id_articulo.desc())


def buscar_articulos(texto):
    return _consulta_articulo().where((Articulo.habilitado == 1) & (Articulo.titulo.contains(texto))).order_by(Articulo.fecha_publicacion.desc())


def obtener_articulo(id_articulo):
    return _consulta_articulo().where((Articulo.id_articulo == id_articulo) & (Articulo.habilitado == 1)).first()


def listado_estados():
    return EstadoArticulo.select().order_by(EstadoArticulo.id_estado)


def obtener_estado(id_estado):
    return EstadoArticulo.get_or_none(EstadoArticulo.id_estado == id_estado)


def etiquetas_de_articulo(id_articulo):
    return (Etiqueta.select()
            .join(ArticuloEtiqueta, on=(ArticuloEtiqueta.etiqueta == Etiqueta.id_etiqueta))
            .where(ArticuloEtiqueta.articulo == id_articulo)
            .order_by(Etiqueta.nombre))


def _asignar_etiquetas(id_articulo, ids_etiquetas):
    ArticuloEtiqueta.delete().where(ArticuloEtiqueta.articulo == id_articulo).execute()
    filas = [{'articulo': id_articulo, 'etiqueta': id_etiqueta} for id_etiqueta in ids_etiquetas]
    if filas:
        ArticuloEtiqueta.insert_many(filas).execute()


def crear_articulo(titulo, contenido, id_autor, id_categoria, id_estado, ids_etiquetas, fecha_publicacion=None):
    datos = {}
    if fecha_publicacion is not None:
        datos['fecha_publicacion'] = fecha_publicacion
    with database.atomic():
        articulo = Articulo.create(titulo=titulo, contenido=contenido, autor=id_autor,
                                   categoria=id_categoria, estado=id_estado, **datos)
        _asignar_etiquetas(articulo.id_articulo, ids_etiquetas)
    return articulo


def guardar_articulo(articulo: Articulo, ids_etiquetas=None):
    with database.atomic():
        articulo.save()
        if ids_etiquetas is not None:
            _asignar_etiquetas(articulo.id_articulo, ids_etiquetas)
    return articulo

import getpass
from auxiliares.validaciones import (
    pedir_texto, pedir_entero, pedir_contrasena_nueva, elegir_registro, confirmar, manejar_errores, mostrar_tabla
)
from negocio.negocio_usuarios import (
    lista_roles, buscar_rol, registrar_rol, editar_rol, deshabilitar_rol,
    lista_usuarios, buscar_usuario, registrar_usuario, editar_usuario, deshabilitar_usuario, iniciar_sesion,
    lista_autores, buscar_autor, usuarios_sin_perfil_autor, registrar_autor, editar_autor, deshabilitar_autor,
    lista_lectores, buscar_lector, usuarios_sin_perfil_lector, registrar_lector, deshabilitar_lector,
    directorio_personas
)


def pedir_login(intentos=3):
    for restantes in range(intentos - 1, -1, -1):
        correo = input('Correo: ').strip()
        contrasena = input('Contraseña: ')
        try:
            return iniciar_sesion(correo, contrasena)
        except ValueError as error:
            print(f'{error} Intentos restantes: {restantes}\n')
    return None



@manejar_errores
def mostrar_roles():
    filas = [[r.id_rol, r.nombre, r.permisos] for r in lista_roles()]
    mostrar_tabla('ROLES', ['Id', 'Nombre', 'Permisos'], filas)


@manejar_errores
def agregar_rol():
    nombre = pedir_texto('Ingrese el nombre del rol: ', minimo=3)
    permisos = pedir_texto('Ingrese los permisos (ej: ALL, EDICION, LECTURA): ')
    rol = registrar_rol(nombre, permisos)
    print(f'Rol guardado con éxito. Id: {rol.id_rol}\n')


@manejar_errores
def modificar_rol():
    mostrar_roles()
    rol = buscar_rol(pedir_entero('Ingrese el id del rol: ', minimo=1))
    if rol is None:
        raise ValueError('No existe un rol con ese id.')
    nombre = pedir_texto(f'Nombre [{rol.nombre}] (ENTER para conservar): ', minimo=3, conservar=rol.nombre)
    permisos = pedir_texto(f'Permisos [{rol.permisos}] (ENTER para conservar): ', conservar=rol.permisos)
    editar_rol(rol, nombre, permisos)
    print('Rol actualizado con éxito.\n')


@manejar_errores
def eliminar_rol():
    mostrar_roles()
    rol = buscar_rol(pedir_entero('Ingrese el id del rol: ', minimo=1))
    if rol is None:
        raise ValueError('No existe un rol con ese id.')
    if confirmar(f'¿Eliminar el rol "{rol.nombre}"?'):
        deshabilitar_rol(rol)
        print('Rol eliminado con éxito.\n')



@manejar_errores
def mostrar_usuarios():
    filas = [[u.id_usuario, u.nombre, u.correo, u.rol.nombre] for u in lista_usuarios()]
    mostrar_tabla('USUARIOS', ['Id', 'Nombre', 'Correo', 'Rol'], filas, izquierda=['Nombre', 'Correo'])


@manejar_errores
def agregar_usuario():
    nombre = pedir_texto('Ingrese el nombre: ', minimo=3)
    correo = pedir_texto('Ingrese el correo: ')
    contrasena = pedir_contrasena_nueva('Ingrese la contraseña: ')
    id_rol = elegir_registro('Roles', lista_roles(), lambda r: r.nombre, campo_id='id_rol')
    usuario = registrar_usuario(nombre, correo, contrasena, id_rol)
    print(f'Usuario guardado con éxito. Id: {usuario.id_usuario}\n')


@manejar_errores
def modificar_usuario():
    mostrar_usuarios()
    usuario = buscar_usuario(pedir_entero('Ingrese el id del usuario: ', minimo=1))
    if usuario is None:
        raise ValueError('No existe un usuario con ese id.')
    nombre = pedir_texto(f'Nombre [{usuario.nombre}] (ENTER para conservar): ', minimo=3, conservar=usuario.nombre)
    correo = pedir_texto(f'Correo [{usuario.correo}] (ENTER para conservar): ', conservar=usuario.correo)
    id_rol = elegir_registro('Roles', lista_roles(), lambda r: r.nombre, conservar=usuario.id_rol,
                             mensaje=f'Id del rol [{usuario.rol.nombre}] (ENTER para conservar): ', campo_id='id_rol')
    nueva = pedir_contrasena_nueva('Nueva contraseña (ENTER para conservar la actual): ', conservar=True)
    editar_usuario(usuario, nombre, correo, id_rol, nueva or None)
    print('Usuario actualizado con éxito.\n')


@manejar_errores
def eliminar_usuario():
    mostrar_usuarios()
    usuario = buscar_usuario(pedir_entero('Ingrese el id del usuario: ', minimo=1))
    if usuario is None:
        raise ValueError('No existe un usuario con ese id.')
    if confirmar(f'¿Eliminar al usuario "{usuario.nombre}"?'):
        deshabilitar_usuario(usuario)
        print('Usuario eliminado con éxito.\n')



@manejar_errores
def mostrar_autores():
    filas = []
    for a in lista_autores():
        bio = a.biografia or ''
        resumen = bio if len(bio) <= 50 else bio[:47] + '...'
        filas.append([a.id_autor, a.usuario.nombre, a.usuario.correo, resumen])
    mostrar_tabla('AUTORES', ['Id', 'Nombre', 'Correo', 'Biografía'], filas, izquierda=['Nombre', 'Correo', 'Biografía'])


@manejar_errores
def agregar_autor():
    id_usuario = elegir_registro('Usuarios disponibles', usuarios_sin_perfil_autor(),
                                 lambda u: f'{u.nombre} <{u.correo}>', mensaje='Id del usuario: ', campo_id='id_usuario')
    biografia = pedir_texto('Ingrese la biografía (opcional): ', obligatorio=False)
    autor = registrar_autor(id_usuario, biografia)
    print(f'Autor guardado con éxito. Id: {autor.id_autor}\n')


@manejar_errores
def modificar_autor():
    mostrar_autores()
    autor = buscar_autor(pedir_entero('Ingrese el id del autor: ', minimo=1))
    if autor is None:
        raise ValueError('No existe un autor con ese id.')
    biografia = pedir_texto('Nueva biografía (ENTER para conservar): ', conservar=autor.biografia or '', obligatorio=False)
    editar_autor(autor, biografia)
    print('Autor actualizado con éxito.\n')


@manejar_errores
def eliminar_autor():
    mostrar_autores()
    autor = buscar_autor(pedir_entero('Ingrese el id del autor: ', minimo=1))
    if autor is None:
        raise ValueError('No existe un autor con ese id.')
    if confirmar(f'¿Eliminar al autor "{autor.usuario.nombre}"?'):
        deshabilitar_autor(autor)
        print('Autor eliminado con éxito.\n')



@manejar_errores
def mostrar_lectores():
    filas = [[l.id_lector, l.usuario.nombre, l.usuario.correo] for l in lista_lectores()]
    mostrar_tabla('LECTORES', ['Id', 'Nombre', 'Correo'], filas, izquierda=['Nombre', 'Correo'])


@manejar_errores
def agregar_lector():
    id_usuario = elegir_registro('Usuarios disponibles', usuarios_sin_perfil_lector(),
                                 lambda u: f'{u.nombre} <{u.correo}>', mensaje='Id del usuario: ', campo_id='id_usuario')
    lector = registrar_lector(id_usuario)
    print(f'Lector habilitado con éxito. Id: {lector.id_lector}\n')


@manejar_errores
def eliminar_lector():
    mostrar_lectores()
    lector = buscar_lector(pedir_entero('Ingrese el id del lector: ', minimo=1))
    if lector is None:
        raise ValueError('No existe un lector con ese id.')
    if confirmar(f'¿Eliminar al lector "{lector.usuario.nombre}"?'):
        deshabilitar_lector(lector)
        print('Lector eliminado con éxito.\n')



@manejar_errores
def mostrar_directorio():
    personas = directorio_personas()
    print('\n=== DIRECTORIO DE PERSONAS (POLIMORFISMO) ===')
    if not personas:
        print('(sin registros)\n')
        return
    for p in personas:
        print(f' - {p.descripcion()}')
    print()

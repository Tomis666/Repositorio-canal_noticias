import functools
import getpass
import hashlib
import hmac
import os
import re
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from prettytable import PrettyTable
from auxiliares.info_app import mensaje_error

_ITERACIONES = 100_000

def hashear_contrasena(contrasena: str) -> str:
    sal = os.urandom(16)
    hash_bytes = hashlib.pbkdf2_hmac('sha256', contrasena.encode('utf-8'), sal, _ITERACIONES)
    return f'{sal.hex()}${hash_bytes.hex()}'


def verificar_contrasena(contrasena: str, guardada: str) -> bool:
    try:
        sal_hex, hash_hex = guardada.split('$')
        sal = bytes.fromhex(sal_hex)
    except ValueError:
        return False
    hash_bytes = hashlib.pbkdf2_hmac('sha256', contrasena.encode('utf-8'), sal, _ITERACIONES)
    return hmac.compare_digest(hash_bytes.hex(), hash_hex)


def validar_contrasena(contrasena: str):
    """Devuelve (contrasena, errores). Si hay errores, la contraseña vuelve como ''."""
    errores = []
    if len(contrasena) < 8 or len(contrasena) > 15:
        errores.append('Debe tener entre 8 y 15 caracteres.')
    if not any(c.isupper() for c in contrasena):
        errores.append('Debe contener al menos una letra mayúscula.')
    if not any(c.islower() for c in contrasena):
        errores.append('Debe contener al menos una letra minúscula.')
    if not any(c.isdigit() for c in contrasena):
        errores.append('Debe contener al menos un número.')
    if not any(c in '!@#$%&/' for c in contrasena):
        errores.append('Debe contener al menos un símbolo de este grupo: ! @ # $ % & /')
    if errores:
        contrasena = ''
    return contrasena, errores


def validar_fecha(texto: str):
    """Valida una fecha dd/mm/aaaa (años 1900-2099). Devuelve (date, mensaje) o ('', mensaje)."""
    patron = r'^(0[1-9]|[12]\d|3[01])/(0[1-9]|1[0-2])/(19\d\d|20\d\d)$'
    if re.match(patron, texto):
        try:
            return datetime.strptime(texto, '%d/%m/%Y').date(), 'Fecha válida.'
        except ValueError:
            pass 
    return '', 'Fecha inválida. Use el formato dd/mm/aaaa con una fecha real (ej.: 23/11/2026).'


def pedir_contrasena_nueva(mensaje='Contraseña: ', conservar=False):
    """Pide una contraseña oculta y repite hasta que cumpla la política.
    Con conservar=True, ENTER devuelve '' (= no cambiarla)."""
    print('La contraseña debe tener 8-15 caracteres, mayúscula, minúscula, número y un símbolo de: ! @ # $ % & /')
    while True:
        valor = getpass.getpass(mensaje)
        if valor == '' and conservar:
            return ''
        valor, errores = validar_contrasena(valor)
        if not errores:
            return valor
        print('Contraseña inválida:')
        for error in errores:
            print(f'  - {error}')


def pedir_fecha(mensaje, conservar=None):
    """Pide una fecha dd/mm/aaaa y repite hasta que sea válida. ENTER devuelve `conservar` si se indicó."""
    while True:
        valor = input(mensaje).strip()
        if valor == '' and conservar is not None:
            return conservar
        fecha, texto = validar_fecha(valor)
        if fecha != '':
            return fecha
        print(texto)


def manejar_errores(funcion):
    @functools.wraps(funcion)
    def envoltura(*args, **kwargs):
        try:
            return funcion(*args, **kwargs)
        except (EOFError, KeyboardInterrupt):
            raise
        except ValueError as error:
            print(f'\nNo se pudo completar la operación: {error}\n')
        except Exception as error:
            print(f'\n{mensaje_error}{error}\n')
    return envoltura



def mostrar_tabla(titulo, columnas, filas, izquierda=()):
    print(f'\n=== {titulo} ===')
    if not filas:
        print('(sin registros)\n')
        return
    tabla = PrettyTable()
    tabla.field_names = columnas
    for columna in izquierda:
        tabla.align[columna] = 'l'
    for fila in filas:
        tabla.add_row(fila)
    print(tabla)
    print()



def pedir_texto(mensaje, minimo=1, conservar=None, obligatorio=True):
    while True:
        valor = input(mensaje).strip()
        if valor == '':
            if conservar is not None:
                return conservar
            if not obligatorio:
                return ''
        elif len(valor) >= minimo:
            return valor
        print(f'Debe ingresar un texto de al menos {minimo} carácter(es).')


def pedir_entero(mensaje, minimo=None, conservar=None):
    while True:
        valor = input(mensaje).strip()
        if valor == '' and conservar is not None:
            return conservar
        try:
            numero = int(valor)
        except ValueError:
            print('Debe ingresar un número entero.')
            continue
        if minimo is not None and numero < minimo:
            print(f'El número debe ser mayor o igual a {minimo}.')
            continue
        return numero


def pedir_decimal(mensaje, minimo=0, conservar=None):
    while True:
        valor = input(mensaje).strip().replace(',', '.')
        if valor == '' and conservar is not None:
            return conservar
        try:
            numero = Decimal(valor)
        except InvalidOperation:
            print('Debe ingresar un número (por ejemplo 4990 o 4990.50).')
            continue
        if numero < minimo:
            print(f'El número debe ser mayor o igual a {minimo}.')
            continue
        return numero


def pedir_id(mensaje, ids_validos, conservar=None):
    while True:
        numero = pedir_entero(mensaje, conservar=conservar)
        if numero in ids_validos:
            return numero
        print('Ese id no está en la lista. Intente nuevamente.')


def confirmar(mensaje):
    return input(f'{mensaje} (s/n): ').strip().lower() in ('s', 'si', 'sí')


def elegir_registro(titulo, registros, describir, conservar=None, mensaje='Ingrese el id: ', campo_id='id'):
    if not registros:
        raise ValueError(f'No hay registros en "{titulo}". Agregue uno primero.')
    print(f'\n{titulo}:')
    for registro in registros:
        id_reg = getattr(registro, campo_id)
        print(f'  [{id_reg}] {describir(registro)}')
    ids = {getattr(registro, campo_id) for registro in registros}
    return pedir_id(mensaje, ids, conservar)


def elegir_varios(titulo, registros, describir, conservar=None, campo_id='id'):
    if not registros:
        return list(conservar or [])
    print(f'\n{titulo}:')
    for registro in registros:
        id_reg = getattr(registro, campo_id)
        print(f'  [{id_reg}] {describir(registro)}')
    ids = {getattr(registro, campo_id) for registro in registros}
    while True:
        texto = input('Ids separados por coma (0 = ninguno, ENTER = conservar/ninguno): ').strip()
        if texto == '':
            return list(conservar or [])
        if texto == '0':
            return []
        try:
            elegidos = [int(parte) for parte in texto.split(',') if parte.strip() != '']
        except ValueError:
            print('Use solo números separados por coma. Ejemplo: 1,3')
            continue
        if all(numero in ids for numero in elegidos):
            return sorted(set(elegidos))
        print('Alguno de los ids no está en la lista. Intente nuevamente.')

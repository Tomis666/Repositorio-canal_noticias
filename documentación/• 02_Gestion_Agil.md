#Organisación del trabajo

#Roles del Equipo
(Ajusta los nombres segun corresponda)
 Product Owner ([Tu Nombre]): Definió qué funciones eran más urgentes para el canal de noticias y revisó que todo funcionara al final.
 Scrum Master ([Tu Nombre]): Organizo los tiempos de entrega y resolvió los problemas que iban saliendo en el camino.
 Desarrolladores ([Nombres]): Crearon la base de datos, programaron las funciones en Python y probaron el sistema.

(Product Backlog)
1. [Alta] Armar la base de datos y conectar Python con SQL.
2. [Alta] Crear el registro e inicio de sesión con contraseñas encriptadas.
3. [Alta] Programar las opciones para crear, ver, editar y borrar noticias.
4. [Media] Programar la gestión de suscripciones de los usuarios.
5. [Media] Agregar filtros para que el prograna no falle si el usuario escribe mal un dato.

Planificación por Etapas (Sprints)
Semana 1 (Sprint 1) - Base de datos y estructura: se crearon las tablas en SQL, se configuró la conexión (`conexion_db.py`) y se armaron las clases principales (`Usuario`, `Articulo`, `Suscripcion`).
Semana 2 (Sprint 2) - Funciones y seguridad:se programaron las operaciones para guardar/leer datos, se implementó el encriptado de claves (`generar_hash.py`) y las validaciones.
Semana 3 (Sprint 3) - Menús y ajustes finales:sse armaron loos menús de consola (`presentacion/`), se corrigieron los datos de prueba (`Insert_datos_corregido.sql`) y se armó esta documentación.
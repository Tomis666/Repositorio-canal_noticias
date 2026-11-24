# 1 Problemática del Cliente
El cliente requiere una plataforma centralizada para gestionar la publicación de artículos informativos, administrar el registro y autenticación segura de usuarios y controlar el estado de sus suscripciones, garantizando la integridad y confidencialidad de los datos almacenados.





# 2 Requerimientos Funcionales


| **RF-01**  Gestión de Usuarios (CRUD) | El sistema permite registrar, consultar, actualizar y eliminar usuarios con validación de datos. | Alta | Permite identificar y administrar a los lectores y editores del canal. |
| **RF-02** | Autenticación Segura | El sistema valida credenciales de inicio de sesión comparando contraseñas encriptadas. | Alta | Impide el acceso no autorizado a las funciones del sistema. |
| **RF-03** | Gestión de Artículos (CRUD) | El sistema permite crear, leer, editar y eliminar artículos noticiosos. | Alta | Resuelve la necesidad principal de publicar y mantener contenido informativo. |
| **RF-04** | Gestión de Suscripciones (CRUD) | El sistema permite asociar, modificar y cancelar suscripciones de los usuarios al canal. | Media | Controla el acceso y estado de membresía de los lectores. |
| **RF-05** | Menú Interactivo | El sistema ofrece una interfaz de consola estructurada por módulos para navegar entre opciones. | Media | Facilita la operación del sistema por parte del usuario final. |





# 3 Requerimientos No Funcionales

| **RNF-01** | Seguridad | Las contraseñas deben almacenarse mediante algoritmos de hash irreversibles (`generar_hash.py`), nunca en texto plano. | Alta |
| **RNF-02** | Seguridad | Las credenciales de conexión a la base de datos deben gestionarse mediante variables de entorno (`.env`). | Alta |
| **RNF-03** | Arquitectura | El código debe estructurarse en arquitectura por capas (`presentacion`, `negocio`, `datos`, `auxiliares`) bajo el paradigma POO. | Alta |
| **RNF-04** | Persistencia | Los datos deben almacenarse de forma relacional mediante scripts SQL estructurados (`DDL` y `DML`). | Alta |
| **RNF-05** | Validación | Toda entrada de datos por consola debe ser validada (`validaciones.py`) antes de procesarse en la capa de negocio. | Media |

#Revisión de Seguridad y Uso de IA

#Cómo usamos y corregimos la IA
Usamos la IA para situciones que nos resultarón desafiantes o que no podiamos comprender del todo. Fuimos consultando por cada detalle y el porque de lo que se hizo.

#Revisión de Seguridad del Sistema
Con apoyo de la IA revisamos qué riesgos podía tener nuestro código y aplicamos tres mejoras clave:
No subir contraseñas al repositorio:** Usamos un archivo `.env` (con su plantilla `.env.example`) y lo bloqueamos en `.gitignore` para que nadie vea los datos de conexión a la base de datos.
Claves encriptadas:Usamos `generar_hash.py` para convertir las contraseñas en un código ilegible antes de guardarlas en SQL.
Filtro de entradas: Validamos los datos antes de procesarlos para evitar errores o inyecciones de código malicio.
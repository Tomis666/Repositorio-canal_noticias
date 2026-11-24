Trabajillo De POO

Para main.py: Correo_admin@canal.cl/Contraseña_Laila12..


Renato Espinoza
                Ignacio Contreras

Instalar las librerías necesarias

   ```bash
   pip install -r requirements.txt
   ```

Configurar la conexión a la base de datos:

Copia el archivo `.env.example`, cámbiale el nombre a `.env` y pon ahí tu usuario y contraseña de base de datos.

Cargar la base de datos:
   Ejecuta los archivos de la carpeta `datos/sql/` en este orden:
   1. `2026.11.07_20.00_DDL_CanalNoticias.sql`
   2. `2026.11.07_20.05_CREATE_USER.sql`
   3. `Insert_datos_corregido.sql`

   ```bash
   python main.py
   ```
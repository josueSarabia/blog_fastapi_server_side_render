# proyecto_final

Blog es un server side rendered website  que tiene una sección de usuarios (la función de búsqueda, buscar por título las publicaciones y fecha), repostear, autenticación, publicaciones que pueden recibir comentarios.

# prerequisitos
 tener instalado
- Python 3.10
- PostgreSQL

# ambiente virtual (opcional)
en la carpeta src, instalar y activar el ambiente virtual de su preferencia.
para este proyecto se uso: virtualenv
nombre del ambiente virtual: venv

# Dependencias
En la terminal de su preferencia ir a la carpeta /src
ejecutar el siguiente comando
- pip install -r requirements.txt
  
# Creacion de la base de datos
Crear una base de datos llamada blogs.
ve al archivo src/.env y agrega la contraseña de su usuario de PostgreSQL
Nota:
- el proyecto usa nombre de usuario, puerto y host  por defecto. SI usas uno distinto
por favor actualizar el archivo .env

En la linea de comandos ejecuta 
- alembic revision --autogenerate -m "just a comment"
- alembic upgrade head

Nota:
- Si alembic muestra el error que no encuentra una revision. eliminar el contenido de src/alembic/version/ y todas las filas de la tabla alembic_version en postgreSQL

# Corre el proyecto
dentro de la carpeta src/ ejecuta
- uvicorn main:app --reload

Ya puedes probar el proyecto 
- localhost:8000/	
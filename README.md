# INTRODUCCION
Resolvi el challenge con Django y Django Rest Framework, lenguaje Python

# INSTRUCCIONES DE INSTALACION
Primero, clonemos el repositorio de GitHub:
```
git clone git@github.com:MiguelSequeiros/transactions.git
```
Con docker compose, levantemos el entorno de desarrollo:
```
docker-compose build --no-cache
```
Note usted que la primera vez que lo corra, probablemente tenga que tener permisos de super administrador o sudo
```
sudo docker-compose build --no-cache
```
No debería de arrojar mayor problema.


# CORRIENDO LA APLICACION
Instalado el entorno de desarrollo, podemos correr la aplicación.
Primero levantamos los servicios:
```
docker-compose up -d
```
Luego corremos las migraciones necesarias
```
docker-compose run web python manage.py migrate
```
Y listo, no se agregó una capa de autenticación para reducir complejidad a la aplicación
De cualquier forma, podemos crear un super usuario para que pueda probar el admin de django en
localhost:8000/admin/
```
docker-compose run web python manage.py createsuperuser
```

# EXPLORANDO LA API
Para explorar la API podemos usar la interfaz que entrega django rest framework por defecto
las rutas se encuentran expuestas en 

/api/companies/
/api/abstract/

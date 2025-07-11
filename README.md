# MKQueue

***

**Sistema de Automatizacion para actualizacion de calculos y sincronizacion en los routers Mikrotik con compatibilidad con base de contratos en sistema Wispro**

## Dependencias

***

- Python 3.13.5
- flet 0.28.3
- flet-desktop 0.28.3
- psycopg2
- python-dotenv

***

## Requerimientos

***

1. Base de Datos PostgreSQL 17
2. Listado de contratos estilo Sistema de gestion Wispro en formato .csv y .xlsx

## Confiuracion de Variables de entorno

### Variables.json

***

Se requiere crear un archivo JSON con el nombre especifico "Variables.json" el cual debera de llevar los datos de la siguiente forma:

```json
{
    "ROUTERS": [
        {
        "nombre": Nombre del Equipo (coincidencia con el archivo de Wispro),
        "ip": Dirrecion Ip del router,
        "usuario": Esuario del router,
        "contraseña": Clave del Router,
        "puerto": Puerto de ssh
        },
        ***Mas Registros...***
    ]
    "PARENT": [
        {
        "nombre": Nombre de Pariente,
        "padre": Nombre de Pariente superior o Null si es la WAN,
        "download": Nombre de Cola para descarga en router,
        "upload": Nombre de Cola para subida en router,
        "router": Nombre del router al cual sincronizar
        },
        ***Mas Registros...***
    ]
    "PLANES": [
        {
        "nombre": Nombre de Cola,
        "router": Nombre del router al cual sincronizar,
        "parent": Nombre de Pariente superior,
        "velocidad": Velocidad de plan,
        "download": Nombre de Cola para descarga en router,
        "upload": "Nombre de Cola para subida en router"
        },
        ***Mas Registros...***
    ]
}
```

***

### .env

se requiere crear un archivo .env donde se alojaran los datos para la conexion con la base de datos. el codigo sera el siguiente:

```env
DB_HOST= Dirrecion de la Base de Datos o localhost
DB_PORT= Puerto de la base de datos o por defecto 5432
DB_NAME= Nombre de la base de datos por defecto (postgres)
DB_USER= Usuario con permisos de edicion y creacion de base de datos
DB_PASSWORD= Contraseña del usuario
```
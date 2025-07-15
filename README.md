# MKQueue

***

**Sistema de Automatización para actualización de cálculos y sincronización en los routers Mikrotik con compatibilidad con base de contratos en sistema Wispro**

## Descripción

MKQueue es una aplicación de escritorio desarrollada en Python con Flet que permite gestionar y sincronizar configuraciones de colas de tráfico en routers Mikrotik. El sistema incluye un completo módulo de autenticación y gestión de usuarios, así como herramientas para administrar routers, árboles de colas y planes de servicio.

## Características Principales

### 🔐 Sistema de Autenticación
- **Login seguro** con verificación de credenciales en base de datos PostgreSQL
- **Gestión de usuarios** completa con CRUD (Crear, Leer, Actualizar, Eliminar)
- **Datos de usuario activo** que se mantienen durante toda la sesión
- **Protección de rutas** automática en todas las páginas principales
- **Configuración automática** de campos con datos del usuario logueado

### 🖥️ Interfaz de Usuario
- **Interfaz moderna** desarrollada con Flet
- **Navegación intuitiva** con barra lateral
- **Diseño responsivo** optimizado para escritorio
- **Temas personalizables** con estilos consistentes

### 🗄️ Gestión de Datos
- **Base de datos PostgreSQL** para almacenamiento persistente
- **Configuración JSON** para routers, padres y planes
- **Sincronización automática** de datos iniciales
- **Gestión de múltiples routers** Mikrotik

## Módulos del Sistema

### 📊 Dashboard
- Vista general del sistema
- Estadísticas de colas activas
- Información de routers conectados
- Gráficos de tráfico WAN

### 🌳 Queue Tree Management
- Gestión de árboles de colas
- Configuración de padres e hijos
- Asignación de velocidades
- Sincronización con routers

### 🛰️ Router Management
- Administración de routers Mikrotik
- Configuración de conexiones SSH
- Gestión de credenciales
- Monitoreo de estado

### ⚙️ Settings
- **Datos del usuario activo** (automáticamente rellenados)
- **Gestión de usuarios** del sistema
- **Configuración de la aplicación**
- **Administración de permisos**

## Estructura del Proyecto

```
MKQueue/
├── main.py                 # Punto de entrada de la aplicación
├── Database/              # Módulo de base de datos
│   ├── init_db.py         # Inicialización y creación de tablas
│   └── querys.py          # Funciones de consulta
├── Pages/                 # Páginas principales
│   ├── Login.py           # Página de autenticación
│   ├── dashboard.py       # Dashboard principal
│   ├── QueueTree.py       # Gestión de árboles de colas
│   ├── Router.py          # Gestión de routers
│   ├── Settings.py        # Configuración y usuarios
│   └── Sub_Pages/         # Páginas secundarias
│       ├── Add_New_User.py
│       ├── Add_Router.py
│       └── Add_Queue_tree.py
├── Objects/               # Funciones y componentes
│   ├── Global_Function.py # Funciones globales y autenticación
│   ├── Navigation_Bar.py  # Barra de navegación
│   ├── Settings_Function.py
│   ├── Router_Function.py
│   └── Queue_Tree_Function.py
├── Styles/                # Estilos y temas
│   └── styles.py
├── Recursos/              # Recursos estáticos
│   ├── Fuentes/
│   └── Iconos/
└── Variables.json         # Configuración del sistema
```

## Dependencias

- **Python 3.13.5** o superior
- **flet 0.28.3** - Framework de UI
- **flet-desktop 0.28.3** - Soporte para escritorio
- **psycopg2** - Conector PostgreSQL
- **python-dotenv** - Gestión de variables de entorno

## Requerimientos del Sistema

1. **Base de Datos PostgreSQL 17** o superior
2. **Python 3.13.5** o superior
3. **Acceso SSH** a routers Mikrotik
4. **Archivo de configuración** Variables.json

## Instalación y Configuración

### 1. Clonar el Repositorio
```bash
git clone <url-del-repositorio>
cd MKQueue
```

### 2. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar Variables de Entorno

Crear un archivo `.env` en la raíz del proyecto:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
```

### 4. Configurar Variables.json

Crear el archivo `Variables.json` con la siguiente estructura:

```json
{
  "ROUTERS": [
    {
      "nombre": "Nombre del Router",
      "ip": "192.168.1.1",
      "usuario": "admin",
      "contraseña": "password",
      "puerto": "22"
    }
  ],
  "PARENT": [
    {
      "nombre": "WAN",
      "padre": null,
      "download": "DOWNLOAD_SERVICIOS",
      "upload": "UPLOAD_SERVICIOS",
      "router": "Nombre del Router"
    }
  ],
  "PLANES": [
    {
      "nombre": "Plan Básico 10 Mbps",
      "router": "Nombre del Router",
      "parent": "WAN",
      "velocidad": 10,
      "download": "DownPlanBasico10Mbps",
      "upload": "UpPlanBasico10Mbps"
    }
  ],
  "ADMIN": [
    {
      "username": "admin",
      "email": "admin@empresa.com",
      "name": "Administrador",
      "last_name": "Sistema",
      "password": "password123",
      "Confirmation": "password123"
    }
  ]
}
```

### 5. Inicializar Base de Datos
```bash
python Database/init_db.py
```

### 6. Ejecutar la Aplicación
```bash
python main.py
```

## Sistema de Autenticación

### Flujo de Login

1. **Ingreso de Credenciales**: El usuario ingresa su nombre de usuario y contraseña
2. **Verificación en Base de Datos**: Se valida contra la tabla `users` de PostgreSQL
3. **Almacenamiento de Datos**: Si la autenticación es exitosa, se guardan los datos del usuario en la sesión
4. **Redirección**: Se redirige al dashboard principal

### Datos del Usuario Activo

Los siguientes datos se almacenan automáticamente después del login exitoso:
- `username`: Nombre de usuario
- `email`: Correo electrónico
- `name`: Nombre completo
- `last_name`: Apellido

### Protección de Rutas

Todas las páginas principales del sistema verifican automáticamente la autenticación:
- **Dashboard**: Página principal del sistema
- **Queue Tree**: Gestión de árboles de colas
- **Router**: Administración de routers
- **Settings**: Configuración del sistema y gestión de usuarios

Si un usuario no autenticado intenta acceder a cualquiera de estas páginas, será redirigido automáticamente al login.

### Página de Configuración

La página de Settings muestra automáticamente los datos del usuario activo en los campos correspondientes:
- Los campos se rellenan con la información del usuario logueado
- Los campos están deshabilitados para evitar edición accidental
- Se muestra la lista completa de usuarios del sistema para administración

### Funciones de Autenticación

- `Authentication(page, username, password)`: Valida credenciales y guarda datos del usuario
- `get_active_user_data(page)`: Obtiene los datos del usuario activo
- `require_auth(page)`: Verifica autenticación y redirige al login si es necesario

## Estructura de Base de Datos

### Tabla `users`
```sql
CREATE TABLE users (
    username VARCHAR(255) PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255),
    password VARCHAR(255) NOT NULL,
    confirm_password VARCHAR(255) NOT NULL
);
```

### Tabla `router`
```sql
CREATE TABLE router (
    router_name VARCHAR(255) PRIMARY KEY,
    router_ip CIDR NOT NULL,
    router_user VARCHAR(255) NOT NULL,
    router_password VARCHAR(255) NOT NULL,
    router_port VARCHAR(255) NOT NULL
);
```

### Tabla `parent`
```sql
CREATE TABLE parent (
    id SERIAL PRIMARY KEY,
    parent_name VARCHAR(255) NOT NULL,
    parent VARCHAR(255),
    download_queue VARCHAR(255) NOT NULL,
    upload_queue VARCHAR(255) NOT NULL,
    router VARCHAR(255) NOT NULL
);
```

### Tabla `queue_tree`
```sql
CREATE TABLE queue_tree (
    id SERIAL PRIMARY KEY,
    queuetree_name VARCHAR(255) NOT NULL,
    queuetree_router VARCHAR(255) NOT NULL,
    queuetree_parent VARCHAR(255),
    speed INT NOT NULL,
    download_queue VARCHAR(255) NOT NULL,
    upload_queue VARCHAR(255) NOT NULL
);
```

## Uso del Sistema

### 1. Iniciar Sesión
- Ejecutar la aplicación con `python main.py`
- Ingresar credenciales de usuario
- El sistema validará las credenciales y redirigirá al dashboard

### 2. Navegación
- Usar la barra lateral para navegar entre módulos
- Cada página verifica automáticamente la autenticación
- Los datos del usuario activo se mantienen durante toda la sesión

### 3. Gestión de Usuarios
- Acceder a Settings para ver datos del usuario activo
- Administrar usuarios del sistema (agregar, editar, eliminar)
- Los campos del usuario activo se rellenan automáticamente

### 4. Gestión de Routers
- Configurar routers Mikrotik con credenciales SSH
- Monitorear estado de conexión
- Administrar múltiples routers

### 5. Gestión de Queue Trees
- Crear y configurar árboles de colas
- Asignar velocidades y padres
- Sincronizar configuraciones con routers


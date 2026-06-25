# device_systems API v3.0

API REST para gestión de usuarios con FastAPI + SQLAlchemy + SQLite.

## Estructura del proyecto

```
device_systems/
│── app/
│   │── main.py
│   │── database/
│   │   └── connection.py        # Engine, SessionLocal, Base, get_db
│   │── models/
│   │   └── user_model.py        # Modelo SQLAlchemy User
│   │── schemas/
│   │   └── user_schema.py       # Schemas Pydantic: Create, Update, Patch, Response
│   │── routes/
│   │   └── user_routes.py       # Endpoints GET, POST, PUT, PATCH, DELETE
│   │── services/
│   │   └── user_service.py      # Lógica CRUD con SQLAlchemy
│   └── dependencies/
│       └── database_dependency.py
│── requirements.txt
└── README.md
```

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
uvicorn app.main:app --reload
```

## Documentación

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints disponibles

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | /users | Listar todos los usuarios (filtros: role, is_active, order_by) |
| GET | /users/{id} | Consultar usuario por ID |
| POST | /users | Crear nuevo usuario |
| PUT | /users/{id} | Actualizar usuario completo |
| PATCH | /users/{id} | Actualizar usuario parcialmente |
| DELETE | /users/{id} | Eliminar usuario |

## Query Parameters (GET /users)

- `role`: Filtrar por rol (`admin`, `user`, `support`)
- `is_active`: Filtrar por estado (`true` / `false`)
- `order_by`: Ordenar por `name` o `created_at`

## Roles válidos

- `admin`
- `user`
- `support`

## Códigos de respuesta

| Situación | Código |
|-----------|--------|
| Usuario creado | 201 Created |
| Consulta exitosa | 200 OK |
| Actualización exitosa | 200 OK |
| Eliminación exitosa | 200 OK |
| Usuario no encontrado | 404 Not Found |
| Email duplicado | 400 Bad Request |
| Rol no permitido | 422 Unprocessable Entity |
| Datos inválidos | 422 Unprocessable Entity |

## Base de datos

SQLite local: `device_systems.db` (creado automáticamente al iniciar).

## Ejemplo de uso

### Crear usuario
```json
POST /users
{
  "name": "Ana García",
  "email": "ana@example.com",
  "role": "admin",
  "is_active": true
}
```

### Filtrar usuarios activos con rol admin
```
GET /users?role=admin&is_active=true
```

### Actualización parcial
```json
PATCH /users/1
{
  "is_active": false
}
```

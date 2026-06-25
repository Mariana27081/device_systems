# device_systems API v3.0

API REST para gestión de usuarios con FastAPI + SQLAlchemy + SQLite.

## Estructura del proyecto

![estructura](/device_systems/images/Estructure.png)

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
uvicorn app.main:app --reload
```


## captura del swagger iu
![swagger](/device_systems/images/swagger.png)

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

## tablas generadas
![tablas](/device_systems/images/db-.png)

## Ejemplo de uso

* get 

![get](/device_systems/images/get.png)

* get id

![getid](/device_systems/images/get_id.png)

* post

![post](/device_systems/images/post.png)

* put 

![put](/device_systems/images/put.png)

* patch 

![patch](/device_systems/images/patch.png)

* delete 

![delete](/device_systems/images/del.png)

* erore controlado

![errors](/device_systems/images/errors.png)

## diferencias entre sqlalchemy vs schema pydantic

SQLAlchemy interactúa con el motor de base de datos para guardar la información, mientras que Pydantic interactúa con el cliente HTTP para validar y limpiar los datos que entran y salen de la aplicación.

## reflexion final
El desarrollo e incremento modular de la plataforma device_systems representa un salto crítico en mi formación como desarrollador backend, pasando de un CRUD básico y plano de una sola entidad a un ecosistema de software interconectado, robusto y blindado bajo estándares profesionales de la industria.

## Link del video


https://youtu.be/QRuVcfRnnP0

# Auth API - FastAPI

API de autenticación profesional construida con **FastAPI**, usando **PostgreSQL**, **JWT**, arquitectura por capas y control de acceso por roles(RBAC)
---

## 📌 Características

* Registro de usuarios
* Login con autenticación JWT(Bearer Token)
* Hash seguro de contraseñas (bcrypt)
* Rutas protegidas con autenticación
* Contorl de acceso por roles (admin/user)
* Obtencion del usuario actual desde token
* Arquitectura por capas (clean architecture)
* Configuración por variables de entorno (.env)F



---

## Tecnologías

* Python 3.10+
* FastAPI
* SQLAlchemy
* PostgreSQL
* JWT (python-jose)
* Passlib (bcrypt)
* python-dotenv

---

## 📁 Estructura del proyecto

```
app/
│
├── api/
│   └── v1/
│       └── routes/
│           └── auth.py
|           └── user.py
│
├── core/
│   ├── config.py
│   └── security.py
|   └── dependencies.py
│
├── db/
│   └── session.py
│
├── models/
│   └── user.py
│
├── schemas/
│   └── user.py
│
├── repositories/
│   └── user_repository.py
│
├── services/
│   └── auth_service.py
│
└── main.py
```

---

## Configuración del entorno

### 1. Clonar repositorio

```
git clone https://github.com/TU_USER/auth-api-fastapi.git
cd auth-api-fastapi
```

---

### 2. Crear entorno virtual

```
python -m venv venv
```

Activar:

```
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

---

### 3. Instalar dependencias

```
pip install -r requirements.txt
```

---

### 4. Configurar variables de entorno

Crear archivo `.env`:

```
DATABASE_URL=postgresql://user:password@localhost/db_name
SECRET_KEY=supersecret
ALGORITHM=HS256
```

---

## ▶️ Ejecutar servidor

```
uvicorn app.main:app --reload
```

Abrir en navegador:

👉 http://127.0.0.1:8000/docs

---
Autenticación

La API usa JWT (Bearer Token).

Flujo:
Login → obtiene token
Enviar token en headers
Acceder a rutas protegidas

Header:

Authorization: Bearer <your_token>


Endpoints
🔑 Auth
Registro
POST /auth/register
Login
POST /auth/login


Usuarios
Obtener usuario actual
GET /users/me

👉 Requiere token

---

Admin
Endpoint solo admin
GET /users/admin

👉 Requiere rol "admin"

### Seguridad

Passwords encriptadas con bcrypt
Tokens JWT firmados
Middleware de autenticación
Control de acceso por roles (RBAC)
Variables sensibles en .env


## 🧪 Testing manual

Puedes usar:

* Swagger UI (`/docs`)
* Postman


---

## Flujo de trabajo (Git)

* `main` → producción
* `feature/*` → nuevas funcionalidades
* `refactor/*` → mejoras de código

Ejemplo:

```
feature/auth
feature/env-config
refactor/add-comments
```

### Próximas mejoras
Expiración de tokens
Refresh tokens
Permisos granulares
Docker
Deploy (Render / Railway)
Migraciones con Alembic---


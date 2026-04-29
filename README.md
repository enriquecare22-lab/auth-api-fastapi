# 🚀 Auth API - FastAPI

API de autenticación profesional construida con **FastAPI**, usando **PostgreSQL**, **JWT**, arquitectura por capas y control de acceso por roles (**RBAC**).

---

## 📌 Características

* Registro de usuarios
* Login con autenticación JWT (**Bearer Token**)
* Hash seguro de contraseñas (**bcrypt**)
* Rutas protegidas con autenticación
* Control de acceso por roles (**admin / user**)
* Obtención del usuario actual desde el token
* Arquitectura por capas (Clean Architecture)
* Configuración mediante variables de entorno (`.env`)

---

## 🛠️ Tecnologías

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
│           ├── auth.py
│           └── user.py
│
├── core/
│   ├── config.py
│   ├── security.py
│   └── dependencies.py
│
├── db/
│   └── session.py
│
├── models/
│   └── user.py
│   └── token_blacklist.py
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

## ⚙️ Configuración del entorno

### 1. Clonar repositorio

```bash
git clone https://github.com/TU_USER/auth-api-fastapi.git
cd auth-api-fastapi
```

---

### 2. Crear entorno virtual

```bash
python -m venv venv
```

Activar:

```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

---

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

### 4. Configurar variables de entorno

Crear archivo `.env`:

```env
DATABASE_URL=postgresql://user:password@localhost/db_name
SECRET_KEY=supersecret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ACCESS_TOKen_EXPIRE_DAYS=7
```

---

## ▶️ Ejecutar servidor

```bash
uvicorn app.main:app --reload
```

Abrir en navegador:

👉 http://127.0.0.1:8000/docs

---
## Logout (Blacklist)

La API implementa una blacklist básica de tokens:

Al hacer logout → el token se guarda en DB
Tokens en blacklist → no pueden acceder


## 🔐 Autenticación

La API utiliza **JWT con esquema Bearer Token**.

### Flujo:

1. Login → obtiene token
2. Enviar token en headers
3. Acceder a rutas protegidas

### Header requerido

```http
Authorization: Bearer <your_token>
```

---

## 🌐 Endpoints

### 🔑 Auth

**Registro**

```http
POST /auth/register
```

**Login**

```http
POST /auth/login
```

Body:

```json
{
  "email": "user@email.com",
  "password": "123456"
}
```

---

### 👤 Usuarios

**Obtener usuario actual**

```http
GET /users/me
```

👉 Requiere autenticación

---

### 👑 Admin

**Endpoint solo admin**

```http
GET /users/admin
```

👉 Requiere rol `"admin"`

---

## 🛡️ Seguridad

* Contraseñas encriptadas con bcrypt
* Tokens JWT firmados
* Expiración configurable
* Middleware de autenticación
* Control de acceso por roles (RBAC)
* Blacklist de tokens
* Variables sensibles protegidas en `.env`

---

## 🧪 Testing

Puedes probar la API con:

* Swagger UI (`/docs`)
* Postman

---

## 🌿 Flujo de trabajo (Git)

* `main` → producción
* `feature/*` → nuevas funcionalidades
* `refactor/*` → mejoras

Ejemplo:

```bash
feature/auth
feature/env-config
feature/roles-rbac
refactor/code-cleanup
```

---

## 🚀 Próximas mejoras

* Expiración de tokens
* Refresh tokens
* Permisos granulares
* Docker
* Deploy (Render / Railway)
* Migraciones con Alembic

---

